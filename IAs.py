from helper import World, Question
from random import randrange
import info_parser
from tree import Tree
import character

class noPowerIA:
    def __init__(self, jid):
        self.old_question = None
        self.world = World(jid)
        self.jid = jid
        self.tree = Tree()
        self.parser = info_parser.ParseInfo(jid)
        self.init = False
        self.question_history = []

    def play(self):
        self.tree = self.compute_info_line()
        if self.parser.is_init() and not self.init:
            self.tree.generate()
            self.init = True
        question = self.world.pull_question(file=self.world.file_question)
        if question != self.old_question and question != "":
            self.answer_question(question)
            self.old_question = question
        if self.init and self.tree.get_generated_depth() < 1:
            self.tree.generate_deeper()

    def handle_info_state(self):
        if self.parser.get_line_state() is info_parser.State.world_info:
            if self.parser.is_init() is True:
                self.tree.update_world_info(self.parser.get_light(), self.parser.get_lock())
            self.tree.root.lightOff = self.parser.get_light()
            self.tree.root.lock = self.parser.get_lock()
        if self.parser.get_line_state() is info_parser.State.character_pos:
            if self.parser.is_init() is True:
                self.tree.update_suspect_world(self.parser.get_characters())
            else:
                self.tree.root.characters = self.parser.get_characters()
        if self.parser.get_line_state() is info_parser.State.ghost_character:
            self.tree.root.ghostColor = self.parser.get_ghost_color()
        if self.parser.get_line_state() is info_parser.State.new_placement:
            self.tree.go_to_adverse_move(self.parser.get_last_played_character())

    def compute_info_line(self):
        self.parser.read_file()
        while self.parser.has_next_line():
            self.handle_info_state()
            self.parser.read_next()
        self.handle_info_state()
        return self.tree

    def answer_question(self, question):
        print(question)
        q = self.world.parse_question(question)
        available = []
        response= ''
        if q.type is Question.Type.tuile_dispo:
            for arg in q.args:
               available.append(character.Character.convert_from_tile_color(arg))
            response = str(self.tree.go_to_best_child(available))
            self.tree.get_actual().dump()
        elif q.type is Question.Type.position_dispo:
            for arg in q.args:
                available.append(int(arg))
            response = str(available.index(self.tree.get_actual_pos()))
        else:
            response = str(randrange(6))
        # Add in front the old question type
        self.question_history = [q.type] + self.question_history
        print("RESPONSE IS : " + response)
        path = './{jid}/reponses.txt'.format(jid=self.jid)
        rf = open(path, 'w+')
        rf.write(response)
        rf.close()
        self.tree.generate_deeper()