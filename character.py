from enum import Enum

characters_string = ["rouge", "rose", "gris", "bleu", "violet", "marron", "noir", "blanc"]


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


class Character:
    def __init__(self, _color, _position):
        self.color = _color
        self.position = _position
        self.suspect = True

    def __init__(self, _color, _position, _suspect):
        self.color = _color
        self.position = _position
        self.suspect = _suspect

    def dump(self):
        print("  "+str(self.color)+", position: "+str(self.position)+", suspect: "+str(self.suspect))

    def get_character_color_to_string(self):
        return characters_string[self.color]
