from game import Game

g = Game()

def dev(g):
    g.wave = 4
    g.c = 2
    g.shop = True
    g.m.menu = False #main menu
    g.starting = False #start cutscene

#dev(g)
g.game_loop()