import node
import board
import character

class Tree:

    def __init__(self):
        self.root = node.Node()
        self._actual = self.root
        self._board = board.Board()

# Useless unless you stock everything before.
# Must be used after parsing the info.txt file.
# The states ghost_character (opt.), STARS, world_info and character_pos must have been parsed before initiate.
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

    def get_turn(self):
        return self._actual.playLevel

    def go_to_child(self, child):
        self._actual = child

    def go_to_adverse_move(self, character_moved: character.Character):
        for child in self._actual.child:
            if child.characters[character_moved.color.value].position == character_moved.position:
                self._actual = child
                break

    def go_to_best_child(self):
        best_child: node.Node = None
        for child in self._actual.child:
            if best_child is None or child.heuristic > best_child.heuristic:
                best_child = child
