from dataclasses import dataclass


@dataclass
class Anchoriser:
    obj: object

    def anchorise(self):
        return self.obj
