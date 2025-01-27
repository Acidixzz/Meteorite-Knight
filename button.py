import pygame

class Button():

    pygame.mixer.init()

    #sounds
    selectSound = pygame.mixer.Sound('Sound/select.wav')
    hoverSound = pygame.mixer.Sound('Sound/menuSound.wav')

    def __init__(self, x, y, image):
        self.image = image
        self.off = image.subsurface(400, 0, 400, 50)
        self.rect = self.off.get_rect()
        self.rect.topleft = (x, y)
        self.on = image.subsurface(0, 0, 400, 50)
        self.state = [self.off, self.on]
        self.clicked = False
        self.hover = False
        self.select = False

        #sounds
        self.buttonChannel = pygame.mixer.Channel(1)
        Button.hoverSound.set_volume(0.5)
        #Button.hoverSound.set_volume(0.5)
        #Button.selectSound.set_volume(0.5)

    def draw(self, win):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos) == True:
           win.blit(self.state[1], (self.rect.x, self.rect.y))
           if self.hover == False:
               Button.hoverSound.play(0, 100)
               self.hover = True
           if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
               self.clicked = True
               if self.select == False:
                   self.buttonChannel.play(Button.selectSound, 0, 500)
                   self.select = True
               action = True

           if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
                self.select = False

        else: 
            win.blit(self.state[0], (self.rect.x, self.rect.y))
            self.hover = False
        return action



