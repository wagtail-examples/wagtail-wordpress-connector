import json
from dataclasses import dataclass, field

from bs4 import BeautifulSoup as bs
from django.utils.module_loading import import_string

# from home.blocks import StreamBlocks, HeadingBlock, ParagraphBlock


def build_paragraph_block(tag):
    block = {
        "type": "paragraph",
        "value": f"{tag}",
    }
    return block


def build_heading_block(tag):
    block_dict = {
        "type": "heading",
        "value": {"text": tag.text, "level": tag.name},
    }
    return block_dict


def build_blockquote_block(tag):
    cite = tag.attrs.get("cite")
    block = {
        "type": "blockquote",
        "value": {
            "quote": tag.text,
            "attribution": cite,
        },
    }
    return block


@dataclass
class StreamFieldable:
    """
    Produes a Stremfidl value for goven html content
    """

    content: str
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
    }

    def __post_init__(self):
        self.streamdata = self.get_streamdata()

    def get_streamdata(self):
        """
        Create stream data from html content
        """
        soup = bs(self.content, "html.parser")

        streamdata = []

        for tag in soup.find_all(recursive=False):
            # item = tag
            module = __name__
            method = self.tags_to_blocks.get(tag.name, "build_paragraph_block")
            block_builder = import_string(f"{module}.{method}")
            print(block_builder)

            if not tag.text:
                continue

            # If streamdata is empty add the first tag
            if not streamdata:
                # block_name = import_string(f"{module}.{method}")
                streamdata.append(block_builder(tag))
                continue

            # If the last item in streamdata is a paragraph and this item is a paragraph
            # then append the text to the last streamdata item value

            if streamdata[-1]["type"] == "paragraph" and tag.name == "p":
                streamdata[-1]["value"] += f"{tag}"
                continue

            # anything not a paragraph will start a new block
            # streamdata.append(self.build_paragraph_block(tag))
            streamdata.append(block_builder(tag))

        return json.dumps(streamdata)
