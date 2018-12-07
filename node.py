import character
import board

class Node:

#TODO !!!!!!
#For now the constructor always puts the characters in room 0
#The constructor should place the characters in their proper room

#TODO !!!!!!
#For now the constructor always puts the lock between 1 and 0
#The constructor should place the lock in the proper room

#TODO !!!!!!
#For now the constructor always puts the lightOff in room 0
#The constructor should place the lightOff in the proper room

    def __init__(self):
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

# Try to move a character to a new position.
# Returns true on success.
# (Character should be a color).
    def moveCharacter(self, to_move, new_position):
        global path
        global path_pink
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
        print("Lock : "+str(self.lock)+"\n")

# Returns a score for the current Node.
# Lower is good for gohst, higher is good for inspector
    def computeScoreGohst(self, ghost):
        print("ghost")

    def computeScoreInspector(self):
        print("inspector")

