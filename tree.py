import node
import board
import character

class Tree:

    def __init__(self):
        self.root = node.Node()
        self._actual = self.root
        self.root.playLevel = node.PlayLevelId.ghost1

# Useless unless you stock everything before.
# Must be used after parsing the info.txt file.
# The states ghost_character (opt.), STARS, world_info and character_pos must have been parsed before initiate.
    def initiate_root(self, characters, lock, light):
        self.root.set_character(characters)
        self.root.set_lock(lock)
        self.root.depth = 0
        self.root.set_light_off(light)
        self.root.playLevel = node.PlayLevelId.ghost

    def parent(self):
        if self._actual is not self.root:
            self._actual = self._actual.parent

    def generate(self):
        print("generating")
        self._actual.generate_direct_child(depth=0, max_depth=0)
        print("done generating")

# generate child other childs
    def generate_deeper(self):
        if self._actual.child is None or len(self._actual.child) == 0:
            self.generate()
        else:
            for child in self._actual.child:
                child.generate_direct_child(depth=0, max_depth=0)

    def get_actual(self):
        return self._actual

    def get_actual_pos(self):
        return self._actual.characters[self._actual.playedCharacter.value].position

    def get_childs(self):
        return self._actual.child

    def get_turn(self):
        return self._actual.playLevel

    def go_to_child(self, child):
        self._actual = child

    def go_to_adverse_move(self, character_moved: character.Character):
        print("Moving to adverse move")
        print(character.characters_string[character_moved.color.value] + str(character_moved.position))
        for child in self._actual.child:
            print ("in")
            if child.characters[character_moved.color.value].position == character_moved.position:
                self._actual = child
                child.dump()
                break

    def go_to_best_child(self, allowed_colors):
        print("Getting the best child")
        best_child: node.Node = None
        for child in self._actual.child:
            if child.playedCharacter in allowed_colors:
                if best_child is None or child.heuristic > best_child.heuristic:
                    best_child = child
        self._actual = best_child
        print("choosed pos : " + str(allowed_colors.index(self._actual.playedCharacter)))
        return allowed_colors.index(self._actual.playedCharacter)

    def get_generated_depth(self):
        tmp = self._actual
        depth = 0
        while len(tmp.child) > 0:
            depth += 1
            tmp = tmp.child[0]
        return depth

    def print(self, layer: node.Node = None):
        if layer is None:
            layer = self._actual
        layer.dump()
        for child in layer.child:
            self.print(child)

    def update_suspect_world(self, characters):
        print("updating")
        self.update_node(self._actual, characters, self._actual.lock, self._actual.lightOff)

    def update_world_info(self, lock, light):
        print("updating wi")
        self.update_node(self._actual, self._actual.characters, lock, light)

    def update_node(self, target_node: node.Node, characters, lock, light):
        if target_node is None:
            return
        for char in characters:
            target_node.characters[char.color.value].suspect = char.suspect
            target_node.lock = lock
            target_node.lighOff = light
            if target_node.ghostColor is not character.Color.NONE:
                target_node.heuristic = target_node.computeScoreGhost(target_node.ghostColor)
            else:
                target_node.heuristic = target_node.computeScoreInspector()
            target_node.heuristic = target_node.computeScoreInspector()
        for child in target_node.child:
            self.update_node(child, characters, lock, light)
