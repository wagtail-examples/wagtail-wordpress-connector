import json
from dataclasses import dataclass, field

from bs4 import BeautifulSoup as bs
from django.utils.module_loading import import_string


@dataclass
class StreamFieldable:
    """
    StreamFieldable class to create stream data from html content.

    Args:
        content (str):
                The html content
        obj (object):
                The object (optional, but useful for debugging)

    Attributes:
        streamdata (json):
                The stream data
        tags_to_blocks (dict):
                The mapping between html tags and block builders
    """

    content: str
    obj: object = None
    streamdata: json = field(init=False)
    tags_to_blocks = {
        "p": "build_paragraph_block",
        "h1": "build_heading_block",
        "h2": "build_heading_block",
        "h3": "build_heading_block",
        "h4": "build_heading_block",
        "h5": "build_heading_block",
        "h6": "build_heading_block",
        "blockquote": "build_blockquote_block",
        "dl": "build_definition_list_block",
    }

    def __post_init__(self):
        self.streamdata = self.get_streamdata()

    def get_streamdata(self):
        """
        Get the stream data from the html content.

        Returns:
            json: The stream data
        """
        soup = bs(self.content, "html.parser")

        streamdata = []

        for tag in soup.find_all(recursive=False):
            # prepare the block builder for this tag
            module = __name__
            method = self.tags_to_blocks.get(tag.name, "build_paragraph_block")
            block_builder = import_string(f"{module}.{method}")

            # Skip empty tags
            if not tag.text:
                continue

            # Always add the first block to streamdata
            if not streamdata:
                streamdata.append(block_builder(tag, self.obj))
                continue

            # If the last item in streamdata is a paragraph and this item is a paragraph
            # then append the text to the last streamdata item value
            if streamdata[-1]["type"] == "paragraph" and tag.name == "p":
                streamdata[-1]["value"] += f"{tag}"
                continue

            # Always add the block to streamdata if it's not one of the above cases
            # consider adding more cases here
            streamdata.append(block_builder(tag, self.obj))

        return json.dumps(streamdata)


def build_paragraph_block(tag, *args, **kwargs):
    block = {
        "type": "paragraph",
        "value": f"{tag}",
    }
    return block


def build_heading_block(tag, *args, **kwargs):
    block_dict = {
        "type": "heading",
        "value": {"text": tag.text, "level": tag.name},
    }
    return block_dict


def build_blockquote_block(tag, *args, **kwargs):
    cite = tag.attrs.get("cite")
    block = {
        "type": "blockquote",
        "value": {
            "quote": tag.text,
            "attribution": cite,
        },
    }
    return block


def build_definition_list_block(tag, *args, **kwargs):
    list_items = []

    for item in tag.find_all("dt"):
        # Try/Except to handle cases where the tag is empty and ouput to the console
        # so the developer can see what is missing
        # But still continue to the next item and not break the loop
        try:
            term = item.text
        except AttributeError:
            term = ""
            print(f"Empty term in definition list: {tag} {item} {args} {kwargs}")

        try:
            definition = item.find_next("dd").text
        except AttributeError:
            definition = ""
            print(f"Empty definition in definition list: {tag} {item} {args} {kwargs}")

        list_items.append({"term": term, "definition": definition})

    block = {
        "type": "definition_list",
        "value": {
            "list": list_items,
        },
    }
    return block
