from helper import World
import IAs

# ghost

def lancer():
    world = World(jid=1)
    world.init_file()
    ia = IAs.noPowerIA(jid=1)
    while world.is_end() is False:
        ia.play()
    print("DONE")
