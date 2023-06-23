from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            raise BaseException("Unknown item")


