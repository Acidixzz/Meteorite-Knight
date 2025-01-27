import pygame
from button import Button

class MainMenu():

    def __init__(self, win):
        self.menu = True
        self.win = win
        bg = pygame.image.load('Background/castle.jpg').convert_alpha()
        self.bg = pygame.transform.scale(bg, (1600, 840))
        self.startList = self.load_start()
        self.i = 0
        self.cd = 250
        self.start = Button(440, 330, pygame.image.load('Background/buttons/start.png'))
        #self.tutorial = Button(440, 430, pygame.image.load('Background/buttons/tutorial.png'))
        self.exit = Button(440, 430, pygame.image.load('Background/buttons/exit.png'))
        self.updateTime = pygame.time.get_ticks()

    def load_start(self):
        img = []
        for i in range(0,6):
            bg = pygame.image.load(f'Background/castlestart{i}.jpg').convert_alpha()
            bg = pygame.transform.scale(bg, (1600, 840))
            img.append(bg)
        return img

    def state_menu(self):
        self.win.blit(self.bg, (-160, 0))


class Pause():

    def __init__(self):
        self.paused = False
        self.black = pygame.image.load('Background/black.png').convert_alpha()
        self.alpha = 0


    def draw(self, win):

        word = "Paused"

        font = pygame.font.Font('fonts/Stackedpixel.ttf', 100)
        outline = font.render(word, True, (0, 0, 0))
        string2 = font.render(word, True, (200, 200, 200))
        string = font.render(word, True, (255, 255, 255))

        x = 490
        y = 340

        win.blit(outline, (x - 5, y))
        win.blit(outline, (x + 10, y))
        win.blit(outline, (x + 5, y))
        win.blit(outline, (x, y - 5)) 
        win.blit(outline, (x + 5, y - 5)) 
        win.blit(outline, (x, y + 5)) 
        win.blit(outline, (x - 5, y + 5)) 
        win.blit(outline, (x + 10, y + 2))
        win.blit(outline, (x + 10, y + 7)) 
        win.blit(outline, (x + 10, y + 10)) 
        win.blit(outline, (x - 1, y + 10)) 
    
        win.blit(string2, (x + 6, y + 5))
        win.blit(string, (x, y))


    def pause_loop(self, win):
        while self.paused:

            self.draw(win)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = False

            pygame.display.update()

