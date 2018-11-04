from random import randrange

from helper import World, Question

colors = ['rose', 'rouge','gris','bleu', 'violet','marron', 'noir','blanc']

# inspecteur

def choose_tile(tiles_name_list):
    return randrange(len(tiles_name_list))

def choose_activate_power():
    i = randrange(1)
    if (i == 0):
        return False
    else:
        return True

def choose_dest_case(case_id_list):
    return randrange(len(case_id_list))

def choose_purple_power_target():
    return colors[randrange(8)]

def choose_grey_power_target():
    return randrange(len(8))

def choose_blue_power_case_target():
    return randrange(len(10))

def choose_blue_power_door_target(door_id_list):
    return randrange(len(door_id_list))

def choose_white_power_target(case_id_list):
    return randrange(len(case_id_list))


def switch(q: Question):
    if q.type == Question.Type.tuile_dispo:
        return choose_tile(q.args)
    elif q.type == Question.Type.position_dispo:
        return choose_dest_case(q.args)
    elif q.type == Question.Type.activer_pouvoir:
        return choose_activate_power()
    elif q.type == Question.Type.pouvoir.gris:
        return choose_grey_power_target()
    elif q.type == Question.Type.pouvoir.violet:
        return choose_purple_power_target()
    elif q.type == Question.Type.pouvoir.blanc:
        return choose_white_power_target(q.args)
    elif q.type == Question.Type.pouvoir.bleu.un:
        return choose_blue_power_case_target()
    elif q.type == Question.Type.pouvoir.bleu.deux:
        return choose_blue_power_door_target(q.args)
    else: # unknown
        pass

def lancer():
    world = World(0)
    fini = False
    old_question = ""
    while not fini:
        qf = open('./0/questions.txt','r')
        question = qf.read()
        qf.close()
        if question != old_question and question:
            q = world.parse_question(question)
            answer = switch(q)
            rf = open('./0/reponses.txt','w')
            rf.write(str(answer))
            rf.close()
            old_question = question
        infof = open('./0/infos.txt','r')
        lines = infof.readlines()
        infof.close()
        if len(lines) > 0:
            fini = "Score final" in lines[-1]
    print("partie finie")
