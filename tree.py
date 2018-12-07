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

    def parent(self):
        if self._actual is not self.root:
            self._actual = self._actual.parent

    def generate_direct_child(self):
        for char in character.Color:
            if char == character.Color.NONE:
                continue
            rooms = self._board.getLinkForRoom(self._actual.characters[char.value].position)
            for room in rooms:
                if room == self._actual.characters[char.value].position:
                    continue
                tmp = node.Node()
                tmp.parent = self._actual
                tmp.characters = self._actual.characters
                tmp.lightOff = self._actual.lightOff
                tmp.lock = self._actual.lock
                tmp.setPosition(char, room)
                self._actual.child.append(tmp)

    def get_childs(self):
        return self._actual.child

    def go_to_child(self, child):
        self._actual = child
