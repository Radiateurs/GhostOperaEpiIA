from helper import World
import IAs

# inspector

def lancer():
    world = World(jid=0)
    world.init_file()
    ia = IAs.noPowerIA(jid=0)
    while world.is_end() is False:
        ia.play()
    print("DONE")
