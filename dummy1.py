from random import randrange
<<<<<<< HEAD
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
=======

def lancer():
    fini = False
    old_question = ""
    while not fini:
        qf = open('./1/questions.txt','r')
        question = qf.read()
        qf.close()
        if question != old_question :
            rf = open('./1/reponses.txt','w')
            rf.write(str(randrange(6)))
            rf.close()
            old_question = question
        infof = open('./1/infos.txt','r')
        lines = infof.readlines()
        infof.close()
        if len(lines) > 0:
            fini = "Score final" in lines[-1]
>>>>>>> 50aa00f563116bb6665732340db8bf28e03304c8
