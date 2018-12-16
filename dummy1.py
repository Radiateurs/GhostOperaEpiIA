from random import randrange
from helper import World
import info_parser
import node
from tree import Tree

def lancer():
    world = World(jid=1)
    old_question = None
    my_tree = Tree()
    my_tree.root.playLevel = node.PlayLevelId.ghost1
    parser = info_parser.ParseInfo(jid=1)
    parser.computeLine(my_tree)
    my_tree.generate()
    while world.is_end() is False:
        question = world.pull_question(file=world.file_question)
        parser.computeLine(my_tree)
        if question != old_question:
            parser.computeLine(my_tree)
            print(question)
            reponse = str(randrange(6))
            world.push_response(text=reponse)
            print(reponse)
            old_question = question
