import character
import board

class Node:

    def __init__(self):
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
        print("Lock : "+ str(self.lock)+"\n")

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

    def generate_direct_child(self):
        for char in character.Color:
            if char == character.Color.NONE:
                continue
            rooms = self.board.getLinkForRoom(self.characters[char.value].position)
            for room in rooms:
                print("Generating character " + character.characters_string[char.value] + " for room " + str(room))
                tmp = Node()
                tmp.parent = self
                for i in range(len(self.characters)):
                    tmp.characters[i] = character.Character(self.characters[i].color, self.characters[i].position)
                    tmp.characters[i].suspect = self.characters[i].suspect
                tmp.lightOff = self.lightOff
                tmp.lock = self.lock
                tmp.setPosition(char, room)
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

# Set the light
    def set_lock(self, lock):
        self.lock = lock
        self.board.lockPath(self.lock[0], self.lock[1])

    def get_light_off(self):
        return self.lightOff

    def get_lock(self):
        return self.lock

    def set_parent(self, parent):
        self.parent = parent

    def get_parent(self):
        return self.parent

    def add_children(self, child):
        self.child.append(child)

    def get_characters(self):
        return self.characters
