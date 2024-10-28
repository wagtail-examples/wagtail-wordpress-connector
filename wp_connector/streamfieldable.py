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
            # For now just make each/any top level tag a paragraph block
            # Later consecutive paragraph blocks can be merged
            if not tag.text:
                continue
            streamdata.append({"type": "paragraph", "value": f"{tag}"})

        return json.dumps(streamdata)
