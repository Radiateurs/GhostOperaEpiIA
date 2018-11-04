from random import randrange
from helper import World
import info_parser

def lancer():
    world = World(jid=1)
    old_question = None
    old_line = None
    parser = info_parser.ParseInfo(jid=1)
    while world.is_end() is False:
        question = world.pull_question(file=world.file_question)
        if question != old_question:
            print(question)
            reponse = str(randrange(6))
            world.push_response(text=reponse)
            print(reponse)
            old_question = question
            parser.read_file()
            while parser.has_next_line():
                print("State : ")
                print(parser.get_line_state())
                parser.read_next()
            print("State : ")
            print(parser.get_line_state())
