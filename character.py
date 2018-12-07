from enum import Enum

class Character:
    def __init__(self, _color, _position):
        self.color = _color
        self.position = _position
        self.cleared = False

    def dump(self):
        print("  "+str(self.color)+", position: "+str(self.position)+", cleared: "+str(self.cleared))

class Color(Enum):
    RED = 0
    PINK = 1
    GREY = 2
    BLUE = 3
    PURPLE = 4
    BROWN = 5
    BLACK = 6
    WHITE = 7
    NONE = 8