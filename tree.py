import node
import board
import character

class Tree:

    def __init__(self):
        self.root = node.Node()
        self._actual = self.root
        self._board = board.Board()

    def initiate_root(self, characters, lock, light):
        self.root.set_character(characters)
        self.root.set_lock(lock)
        self.root.set_light_off(light)
        self.root.playLevel = node.PlayLevelId.ghost1

    def parent(self):
        if self._actual is not self.root:
            self._actual = self._actual.parent

    def generate(self):
        self._actual.generate_direct_child(depth=0, max_depth=3)

    def get_childs(self):
        return self._actual.child

    def go_to_child(self, child):
        self._actual = child
