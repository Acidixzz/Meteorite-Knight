from random import randrange
from coin import Coin
import pygame

class PowerUp():

    pygame.init()
    pygame.mixer.init()

    #images
    pygame.display.set_mode((1280, 720))

    lights = pygame.image.load('assets/newlights.png').convert_alpha()
    altars = pygame.image.load('assets/newaltars.png').convert_alpha()
    powers = pygame.image.load('assets/newpowerups.png').convert_alpha()
    highlights = pygame.image.load('assets/newhighlights.png').convert_alpha()
    #Sounds
    
    def __init__(self, i):
        #images
        self.lights = self.load_images(PowerUp.lights, 170, 574, 6)
        self.altars = self.load_images(PowerUp.altars, 80, 80, 6)
        self.powers = self.load_images(PowerUp.powers, 170, 170, 5)
        self.highlights = self.load_images(PowerUp.highlights, 170, 170, 5)

        #checks if player is hovering over
        self.display_coin = False

        #moving powers up and down
        self.y = 465
        self.grav = randrange(-20, -9)/100

        self.pickedUp = False
        self.maxed = False

        self.i = i
        self.power = self.powers[i-1]
        self.highlight = self.highlights[i-1]
        self.altar = self.altars[i]
        self.light = self.lights[i]
        self.powerRect = pygame.Rect(215 + ((i - 1) * 170), self.y + 60, 80, 100)

    def load_images(self, image, length, height, steps):
        #put each frame in list inside of a masterlist
        tempList = []
        for x in range(steps):
            tempImg = image.subsurface(x * length, 0, length, height)
            tempList.append(tempImg)
        return tempList

    def draw(self, win, player):
        #up and down for power
        if self.y > 465:
            self.y = 465
            self.grav = randrange(-20, -9)/100

        if self.y < 455:
            self.y = 455
            self.grav = randrange(10, 21)/100

        self.y += self.grav


        #pygame.draw.rect(win, (0,255,0), powerRect)
        if self.pickedUp == False:
            win.blit(self.altar, (215 + ((self.i - 1) * 170), 542))
            if player.rect.colliderect(self.powerRect):
                win.blit(self.highlight, (170 + ((self.i - 1) * 170), self.y))
                self.display_coin = True
            else:
                win.blit(self.power, (170 + ((self.i - 1) * 170), self.y))
                self.display_coin = False
        else:
            win.blit(self.altars[0], (215 + ((self.i - 1) * 170), 542))
            self.display_coin = False


    def draw_coin_amount(self, win, coins, x, y):
        font = pygame.font.Font('fonts/Stackedpixel.ttf', 30)
        if coins < 10:
            amount = font.render('0' + str(coins), True, (255, 255, 255))
            amountO = font.render('0' + str(coins), True, (0, 0, 0))
        else: 
            amount = font.render(str(coins), True, (255, 255, 255))
            amountO = font.render(str(coins), True, (0, 0, 0))

        win.blit(Coin.img.subsurface(0, 32, 32, 32), (x, y - 3))
        win.blit(amountO, (x + 32, y + 5))
        win.blit(amount, (x + 30, y + 3))


    def draw_light(self, win):
        if self.maxed == False:
            win.blit(self.light, (170 + ((self.i - 1) * 170), 85))
        else:
            win.blit(self.lights[0], (170 + ((self.i - 1) * 170), 85))

