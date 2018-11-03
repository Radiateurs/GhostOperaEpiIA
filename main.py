import board

# Create Board
world = board.Board()

# Get link at room 0
print(world.getLinkForRoom(0))

# Lock room 0 - 1
world.lockPath(0, 1)

# Get new link at room 0
print(world.getLinkForRoom(0))
