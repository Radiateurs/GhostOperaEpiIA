import board
import node
import character

# Create Board
world = board.Board()

newNode = node.Node()
newNode.dump()
newNode.moveCharacter(character.Color.WHITE, 1)
newNode.moveCharacter(character.Color.RED, 5)
newNode.dump()

#red = character.Character(character.Color.RED, 0);
#red.dump()

# Get link at room 0
print(world.getLinkForRoom(0))

# Lock room 0 - 1
world.lockPath(0, 1)

# Get new link at room 0
print(world.getLinkForRoom(0))
