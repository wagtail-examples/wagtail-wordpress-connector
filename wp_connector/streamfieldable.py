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
            item = tag

            if not item.text:
                continue

            # If streamdata is empty add the first tag
            if not streamdata:
                streamdata.append({"type": "paragraph", "value": f"{item}"})
                continue

            # If the last item in streamdata is a paragraph and this item is a paragraph
            # then append the text to the last streamdata item value

            if streamdata[-1]["type"] == "paragraph" and item.name == "p":
                streamdata[-1]["value"] += f"{item}"
                continue

            # otherise add the item as a new streamdata item
            streamdata.append({"type": "paragraph", "value": f"{item}"})

        return json.dumps(streamdata)
