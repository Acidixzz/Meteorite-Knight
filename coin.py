import pygame
import random

class Coin():
    pygame.init()
    pygame.mixer.init()

    #image
    pygame.display.set_mode((1280, 720))
    img = pygame.image.load('assets/coinbig.png').convert_alpha()

    #sounds
    pickUpSound = pygame.mixer.Sound('Sound/coin.wav')
    pickUpSound.set_volume(0.3)

    def __init__(self, x):
        self.coinAdd = False

        self.size = 32
        self.animationList = self.load_images(Coin.img, [8, 1])
        self.action = 0
        self.frameIndex = 0

        self.rect = self.animationList[self.action][0].get_rect()
        self.rect.bottomleft = (x, 600)
        self.moving = True
        self.vel = random.randint(2,5)
        self.i = random.randrange(2)
        self.jump = False
        self.jumpCount = 0
        self.velY = 0

        self.updateTime = pygame.time.get_ticks()
        self.pickUp = False
        #bool to detect if the pickup animation is over
        self.pickedUp = False

        #sound bool
        self.pickUpPlay = False

    def load_images(self, image, steps):
        #put each frame in list inside of a masterlist
        animationList = []
        for y, animation in enumerate(steps):
            tempList = []
            for x in range(animation):
                tempImg = image.subsurface(x * self.size, y * self.size, self.size, self.size)
                tempList.append(tempImg)
            animationList.append(tempList)
        return animationList

    def move(self, sWidth, sHeight, win, player):
        grav = 1
        dx = 0  
        dy = 0

        #coin pickup
        if player.rect.colliderect(self.rect):
            self.pickUp = True

        if self.pickUp:
            self.update_action(1)
            if self.pickUpPlay == False:
                Coin.pickUpSound.play(0, 500)
                self.pickUpPlay = True
            self.moving = False
            self.jumpCount = -1
            self.rect.x = player.rect.centerx - self.size//2
            if self.rect.y > player.rect.top - 40:
                self.rect.y -= 10
            else:
                self.pickedUp = True

            #adds 1 to the player's coin amount
            if self.coinAdd == False:
                player.coins += 1
                self.coinAdd = True

        #coin move
        if self.moving == True and self.vel > 0:
            if self.i == 0:
                dx = -self.vel
            elif self.i == 1:
                dx = self.vel
            self.vel -= 0.075

        #jump
        if self.jump == False and self.jumpCount >= 0:
            if self.jumpCount == 0:
                self.velY = -10
                self.jump = True
                self.jumpCount += 1
            elif self.jumpCount == 1:
                self.velY = -8
                self.jump = True
                self.jumpCount += 1
            elif self.jumpCount == 2:
                self.velY = -5
                self.jump = True
                self.jumpCount += 1
            elif self.jumpCount == 3:
                self.velY = -3
                self.jump = True
                self.jumpCount = -1

        if not self.pickUp:
            #apply grav
            self.velY += grav
            dy += self.velY

        #coin stays on screen
        if self.rect.left + dx < 0:
            dx = self.rect.left
        if self.rect.right + dx > sWidth:
            dx = sWidth - self.rect.right
        if self.rect.bottom + dy > sHeight - 160:
            self.velY = 0
            dy = sHeight - 160 - self.rect.bottom
            self.jump = False

        #update coin position
        self.rect.x += dx
        self.rect.y += dy

        animationCd = 150
        self.image = self.animationList[self.action][self.frameIndex]
        #check if enough time has passed since last update
        if pygame.time.get_ticks() - self.updateTime > animationCd:
            self.frameIndex += 1
            self.updateTime = pygame.time.get_ticks()
        #check if the animation finished
        if self.frameIndex >= len(self.animationList[self.action]):
            self.frameIndex = 0
            #check if some action is current animation


        #displays coin
        #pygame.draw.rect(win, (0,0,0), self.rect)
        if self.pickedUp == False:
            win.blit(self.image, (self.rect.x, self.rect.y))

    def update_action(self, newAction):
        #check if new action is different then prev
        if newAction != self.action:
            self.action = newAction
            #update animation settings
            self.frameIndex = 0
            self.updateTime = pygame.time.get_ticks()