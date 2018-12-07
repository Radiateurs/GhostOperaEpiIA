import board
import node
import character

# Create Board
world = board.Board()

myNode = node.Node()
myNode.dump()
print(myNode.computeScoreInspector())
print(myNode.computeScoreGhost(character.Color.WHITE))
myNode.moveCharacter(character.Color.PINK, 4)
myNode.dump()

# Get link at room 0
print(world.getLinkForRoom(0))

# Lock room 0 - 1
world.lockPath(0, 1)

# Get new link at room 0
print(world.getLinkForRoom(0))
