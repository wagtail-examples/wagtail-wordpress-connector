import json
from dataclasses import dataclass, field

from bs4 import BeautifulSoup as bs


@dataclass
class StreamFieldable:
    """
    Produes a Stremfidl value for goven html content
    """

    content: str
    streamdata: json = field(init=False)

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

            if not tag.text:
                continue

            # If streamdata is empty add the first tag
            if not streamdata:
                streamdata.append(self.build_paragaraph_block(tag))
                continue

            # If the last item in streamdata is a paragraph and this item is a paragraph
            # then append the text to the last streamdata item value

            if streamdata[-1]["type"] == "paragraph" and tag.name == "p":
                streamdata[-1]["value"] += f"{tag}"
                continue

            # anything not a paragraph will start a new block
            streamdata.append(self.build_paragaraph_block(tag))

        return json.dumps(streamdata)

    def build_paragaraph_block(self, tag):
        block = {
            "type": "paragraph",
            "value": f"{tag}",
        }
        return block
