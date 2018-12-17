from random import randrange

import info_parser
import node
from helper import World, Question
from tree import Tree
import character
import IAs

# ghost

def lancer():
    world = World(jid=1)
    world.init_file()
    ia = IAs.noPowerIA(jid=1)
    while world.is_end() is False:
        ia.play()
    print("DONE")
