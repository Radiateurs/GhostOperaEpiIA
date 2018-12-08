from random import randrange
from helper import World
import info_parser
import node
from tree import Tree


def computeLine(parser, tree):
    parser.read_file()
    while parser.has_next_line():
        print("State : ")
        print(parser.get_line_state())
        if parser.get_line_state() is info_parser.State.world_info:
            tree.root.lightOff = parser.get_light()
            tree.root.lock = parser.get_lock()
            tree.root.dump()
        if parser.get_line_state() is info_parser.State.character_pos:
            tree.root.characters = parser.get_characters()
            tree.root.dump()
        parser.read_next()
    print("State : ")
    print(parser.get_line_state())
    if parser.get_line_state() is info_parser.State.world_info:
        tree.root.lightOff = parser.get_light()
        tree.root.lock = parser.get_lock()
        tree.root.dump()
    if parser.get_line_state() is info_parser.State.character_pos:
        tree.root.characters = parser.get_characters()
        tree.root.dump()
    return tree


def lancer():
    world = World(jid=1)
    old_question = None
    my_tree = Tree()
    parser = info_parser.ParseInfo(jid=1)
    computeLine(parser, my_tree)
    my_tree.generate()
    print("Root:")
    my_tree.root.dump()
    for i in range(len(my_tree.get_childs())):
        print("Node n:" + str(i))
        my_tree.root.child[i].dump()
    while world.is_end() is False:
        question = world.pull_question(file=world.file_question)
        if question != old_question:
            print(question)
            reponse = str(randrange(6))
            world.push_response(text=reponse)
            print(reponse)
            old_question = question
