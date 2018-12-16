import re
import character
from enum import Enum
from tree import Tree
import node

class State(Enum):
    unknown = 0             # Unknown line
    stars = 1               # *****************
    world_info = 2          # Tour: 1, Score: 4/22
    character_pos = 3       # bleu-3-suspect rouge-6-clean [...]
    question = 4            # QUESTION : [...]
    answer_given = 5        # REPONSE DONNEE : [...]
    answer_understood = 6   # REPONSE INTERPRETEE : [...]
    character_played = 7    # [le fantome / l'inspecteur] a joue [bleu/rouge/etc...]
    power_played = 8        # Pouvoir de [couleur] active
    ghost_state = 9         # pas de cri / le fantome a frappe
    new_placement = 10      # NOUVEAU PLACEMENT : couleur-pos-suspect/clean
    inspector_turn = 11     # Le tour de l'inspecteur
    ghost_turn = 12         # Le tour de le fantome
    ghost_character = 13    # !!! le fantôme est : [couleur]

# Class to parse the ./{jid}/info.txt file
# HOW TO USE IT :
#
# create a variable of type ParseInfo and give it the id of the player:
# ID PLAYER : 0 = ghost 1 = inspector
# ``` parse = ParseInfo(0) ```
#
# To get the first line from the past read lines use the get_line method :
# ``` line = parse.get_line() ```
#
# To fill the buffer use the read_file method:
# ``` parse.read_file() ```
#
# To change the cursor position (current line) use the read_next method:
# ```   parse.read_file()
#       if parse.has_next_line():
#           parse.read_read_next() ```
#
# To get the state of the current line use get_line_state method :
# ```   parse.read_file()
#       state = parse.get_line_state() ```
#
class ParseInfo():

    file_info = 'infos.txt'
    _stack = None
    _line = None
    _state: State = State.unknown
    _stat_history = []
    _characters = []
    _light = None
    _lock = []
    _ghostColor = character.Color.NONE
    _last_played_character = None

    def __init__(self, jid: int):
        self._jid = jid
        self._lock = [None, None]
        self._characters = [character.Character(character.Color.RED, 0),
                           character.Character(character.Color.PINK, 0),
                           character.Character(character.Color.GREY, 0),
                           character.Character(character.Color.BLUE, 0),
                           character.Character(character.Color.PURPLE, 0),
                           character.Character(character.Color.BROWN, 0),
                           character.Character(character.Color.BLACK, 0),
                           character.Character(character.Color.WHITE, 0)]

    def computeLine(self, tree):
        self.read_file()
        if tree == None:
            tree = Tree()
        while self.has_next_line():
            #        print("State : ")
            #       print(parser.get_line_state())
            if self.get_line_state() is State.world_info:
                tree.root.lightOff = self.get_light()
                tree.root.lock = self.get_lock()
            #            tree.root.dump()
            if self.get_line_state() is State.character_pos:
                tree.root.characters = self.get_characters()
            #            tree.root.dump()
            self.read_next()
        #    print("State : ")
        #    print(parser.get_line_state())
        if self.get_line_state() is State.world_info:
            tree.root.lightOff = self.get_light()
            tree.root.lock = self.get_lock()
        #        tree.root.dump()
        if self.get_line_state() is State.character_pos:
            tree.root.characters = self.get_characters()
        #        tree.root.dump()
        if self.get_line_state() is State.ghost_character:
            tree.root.ghostColor = self.get_ghost_color()
        if self.get_line_state() is State.new_placement and \
                node.PlayLevel.isAdverseMove(self._jid, tree.get_turn()):
            tree.go_to_adverse_move(self.get_last_played_character())
        return tree

    def read_file(self):
        path = './{jid}/{file}'.format(jid=self._jid, file=self.file_info)
        with open(path, 'r') as f:
            self._stack = f.read()
            if self._stack is not None:
                if (self._stack.splitlines() is not None) and (len(self._stack.splitlines()) > 0):
                    self._line = self._stack.splitlines()[0]
                else:
                    self._line = self._stack
                self.init_state()

    def get_line(self):
        return self._line

# return True if there's more to read
    def has_next_line(self):
        return True if self._stack is not None and self._stack.splitlines() is not None and\
                       len(self._stack.splitlines()) > 0 else False

    def read_next(self):
        if self._stack is None:
            return self.read_file()
        lines = self._stack.splitlines()
        if lines is not None and len(lines) > 1:
            lines.pop(0)
            self._line = lines[0]
            self._stack = ''
            for index in range(len(lines)):
                self._stack += lines[index]
                if index < len(lines):
                    self._stack += '\n'
            self.init_state()
        else:
            return self.read_file()

    def init_state(self):
        self._state = State.unknown
        if self._line == None:
            return
        tokens = [r'[*]+', r'Tour:.', r'^([a-z]+-[0-9]-(suspect|clean)(  |)){8}',
                  r'QUESTION :.', r'REPONSE DONNEE.', r'REPONSE INTERPRETEE.',
                  r'l(e fantome|\'inspecteur) joue', r'Pouvoir de [a-z]+ activé',
                  r'(le fantome frappe|pas de cri)', r'NOUVEAU PLACEMENT : [a-z]+-[0-9]-(suspect|clean)',
                  r'^  Tour de l\'inspecteur', r'  Tour de le fantome', r'[!]{3}.', r'!!! Le fantôme est : *']
        for token in range(len(tokens)):
            if re.search(tokens[token], self._line):
                self._state = State(token + 1)
                break
        if self._state is State.character_pos:
            self.init_characters()
        if self._state is State.world_info:
            self.init_world_info()
        if self._state is State.ghost_character:
            self.parseGhostColor()
        if self._state is State.new_placement:
            self.parseNewPosition()
        print("LINE : " + self._line + "$$$")
        print("STATE : " + str(self._state) + "$$$")

    def init_characters(self):
        if self._line == None:
            return
        # Create a list of {gris-2-suspect} from the line
        raw_characters = self._line.split("  ")
        for raw in range(len(raw_characters)):
            # Separate each object in the given strings to create a list of [{color}, {pos}, {state}]
            raw_states = raw_characters[raw].split("-")
            # Get the index by looking in the characters_string list.
            char_index = character.characters_string.index(raw_states[0])
            # Get the character room number
            char_room = int(raw_states[1])
            # set is_char_suspect to False if "suspect" is not contained in the given string or True if it is.
            is_char_suspect = "suspect" in raw_states[2]
            self._characters[char_index].position = char_room
            self._characters[char_index].suspect = is_char_suspect

    def parseNewPosition(self):
        if ":" not in self._line:
            return
        char_place = self._line[(self._line.find(':') + 1):]
        raw_states = char_place.split("-")
        # Get the index by looking in the characters_string list.
        char_index = character.characters_string.index(raw_states[0])
        # Get the character room number
        char_room = int(raw_states[1])
        # set is_char_suspect to False if "suspect" is not contained in the given string or True if it is.
        is_char_suspect = "suspect" in raw_states[2]
        self._last_played_character = character.Character(character.Color(char_index), char_room, is_char_suspect)

    def init_world_info(self):
        if self._line == None or "Ombre:" not in self._line or "Bloque:" not in self._line:
            return
        self._light = int(self._line[self._line.find("Ombre:") + 6:self._line.find("Ombre:") + 7])
        self._lock[0] = int(self._line[self._line.find("Bloque:") + 8:self._line.find("Bloque:") + 9])
        self._lock[1] = int(self._line[self._line.find("Bloque:") + 11:self._line.find("Bloque:") + 12])

    def parseGhostColor(self):
        for color in range(len(character.characters_string)):
            if character.characters_string[color] in self._line:
                self._ghostColor = character.Color(color)
                break

    def get_line_state(self):
        return self._state

    def get_light(self):
        return self._light

    def get_lock(self):
        return self._lock

    def get_characters(self):
        return self._characters

    def get_ghost_color(self):
        return self._ghostColor

    def get_last_played_character(self):
        return self._last_played_character