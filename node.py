from enum import Enum
import character
import board


class PlayLevelId(Enum):
    ghost1 = 0
    inspector1 = 1
    inspector2 = 2
    ghost2 = 3
    inspector3 = 4
    ghost3 = 5
    ghost4 = 6
    inspector4 = 7


class PlayLevel:

    @staticmethod
    def getNextMove(level: PlayLevelId):
        if level == PlayLevelId.inspector4:
            return PlayLevelId.ghost1
        next = [ PlayLevelId.ghost1,
                 PlayLevelId.inspector1,
                 PlayLevelId.inspector2,
                 PlayLevelId.ghost2,
                 PlayLevelId.inspector3,
                 PlayLevelId.ghost3,
                 PlayLevelId.ghost4,
                 PlayLevelId.inspector4 ]
        for n in range(len(next)):
            if next[n] == level:
                return next[n + 1]

    @staticmethod
    def isGhostTurn(level):
        if level == PlayLevelId.ghost1 or level == PlayLevelId.ghost2 or \
                level == PlayLevelId.ghost3 or level == PlayLevelId.ghost4:
            return True
        return False

    @staticmethod
    def isInspectorTurn(level):
        if level == PlayLevelId.inspector1 or level == PlayLevelId.inspector2 or \
                level == PlayLevelId.inspector3 or level == PlayLevelId.inspector4:
            return True
        return False


class Node:

    def __init__(self):
        self.playLevel = None
        self.ghostColor = character.Color.NONE
        self.parent = None
        self.child = []
        self.characters = [character.Character(character.Color.RED, 0),
                           character.Character(character.Color.PINK, 0),
                           character.Character(character.Color.GREY, 0),
                           character.Character(character.Color.BLUE, 0),
                           character.Character(character.Color.PURPLE, 0),
                           character.Character(character.Color.BROWN, 0),
                           character.Character(character.Color.BLACK, 0),
                           character.Character(character.Color.WHITE, 0)]
        self.lock = [0, 1]
        self.lightOff = 0
        self.board = board.Board()
        self.heuristic = None

# Try to move a character to a new position.
# Returns true on success.
# (Character should be a color).
    def moveCharacter(self, to_move, new_position):
        global path
        global path_pink

        if new_position < 0 or new_position > 9 or\
                (self.characters[to_move.value].position == self.lock[0] and new_position == self.lock[1]) or\
                (self.characters[to_move.value].position == self.lock[1] and new_position == self.lock[0]):
            return False
        if to_move == character.Color.PINK:
            if new_position in board.path_pink[self.characters[to_move.value].position]:
                self.characters[to_move.value].position = new_position
                return True
            else:
                return False
        else:
            if new_position in board.path[self.characters[to_move.value].position]:
                self.characters[to_move.value].position = new_position
                return True
            else:
                return False

# Outputs the node in its current state
    def dump(self):
        print("Characters : ")
        for character in self.characters:
            character.dump()
        print("Lights are off in room : "+str(self.lightOff))
        print("Lock : " + str(self.lock))
        print("Playing for : ")
        if PlayLevel.isGhostTurn(self.playLevel):
            print("Ghost\n")
        else:
            if PlayLevel.isInspectorTurn(self.playLevel):
                print("Inspector\n")
            else:
                print("Unknown")

# HIGHER SCORE is better (goes from -4 to 9)
# Returns -1000 if the ghost loose the game
    def computeScoreGhost(self, ghost_color):
        ghost = self.characters[ghost_color.value]
        seen = 0
        unseen = 0
        ghostSeen = False
        if self.lightOff != ghost.position and self.nbPeopleInRoom(ghost.position) > 1:
            ghostSeen = True
        for character in self.characters:
            if character.suspect:
                if character.position == self.lightOff:
                    unseen += 1
                elif self.nbPeopleInRoom(character.position) > 1:
                    seen += 1
                else:
                    unseen += 1
        if (ghostSeen and seen == 1) or (not ghostSeen and unseen == 1):
            return -1000
        if ghostSeen:
            return seen - unseen
        return unseen - seen + 1

# LOWER SCORE is better (goes from 0 to 8)
    def computeScoreInspector(self):
        seen = 0
        unseen = 0
        for character in self.characters:
            if character.suspect:
                if character.position == self.lightOff:
                    unseen += 1
                elif self.nbPeopleInRoom(character.position) > 1:
                    seen += 1
                else:
                    unseen += 1
        return abs(seen - unseen)

    def nbPeopleInRoom(self, pos):
        nbPeople = 0
        for character in self.characters:
            if character.position == pos:
                nbPeople += 1
        return nbPeople

    def generate_direct_child(self, depth=0, max_depth=2):
        for char in character.Color:
            if char == character.Color.NONE:
                continue
            rooms = self.board.getLinkForRoom(self.characters[char.value].position)
            for room in rooms:
                tmp = Node()
                tmp.parent = self
                for i in range(len(self.characters)):
                    tmp.characters[i] = character.Character(self.characters[i].color, self.characters[i].position)
                    tmp.characters[i].suspect = self.characters[i].suspect
                tmp.lightOff = self.lightOff
                tmp.lock = self.lock
                tmp.setPosition(char, room)
                tmp.playLevel = PlayLevel.getNextMove(self.playLevel)
                tmp.ghostColor = self.ghostColor
                if self.ghostColor is not character.Color.NONE:
                    tmp.heuristic = tmp.computeScoreGhost(tmp.ghostColor)
                else:
                    tmp.heuristic = tmp.computeScoreInspector()
                print("Generating character " + character.characters_string[char.value] + " for room " + str(room) +
                      " with a depth of " + str(depth) + " for turn " + str(self.playLevel) + " with heuristic of "
                      + str(tmp.heuristic))
                if depth < max_depth:
                    tmp.generate_direct_child(depth=depth+1)
                self.child.append(tmp)

# For test purposes. Please use moveCharacter.
    def setPosition(self, to_move, new_position):
        self.characters[to_move.value].position = new_position

# Set the character list to a given one
    def set_character(self, characters):
        self.characters = characters

# Set the light
    def set_light_off(self, light):
        self.lightOff = light

# Set the lock
    def set_lock(self, lock):
        self.lock = lock
        self.board.lockPath(self.lock[0], self.lock[1])

# Get the light
    def get_light_off(self):
        return self.lightOff

# Get the lock
    def get_lock(self):
        return self.lock

# Set the parent
    def set_parent(self, parent):
        self.parent = parent

# Get the parent
    def get_parent(self):
        return self.parent

# Add a children
    def add_children(self, child):
        self.child.append(child)

# Get the characters
    def get_characters(self):
        return self.characters
