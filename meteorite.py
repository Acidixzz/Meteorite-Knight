import pygame
import random

class Meteor():

    pygame.mixer.init()

    #sounds
    explode = pygame.mixer.Sound('Sound/explosion.wav')
    explode.set_volume(0.5)
    fall = pygame.mixer.Sound('Sound/fall.wav')
    fall.set_volume(0.1)

    #image
    img = pygame.image.load('meteor/meteor1.png').convert_alpha()
 
    def __init__(self, scale):
        self.steps = [8, 7]
        self.size = 100
        self.imageScale = scale
        self.offset = [22, 10]
        self.animationList = self.load_images(Meteor.img, self.steps)
        self.action = 0 #0:meteor 1:explosion
        self.frameIndex = 0
        self.image = self.animationList[self.action][self.frameIndex]
        self.updateTime = pygame.time.get_ticks()
        self.rect = pygame.Rect(random.randint(0, 123) * 10, -45, 50 * self.imageScale, 45 * self.imageScale)
        self.moving = True
        self.display = True
        #sound bools
        self.explodePlay = False
        self.fallPlay = False
     


    def load_images(self, image, steps):
        #put each frame in list inside of a masterlist
        animationList = []
        for y, animation in enumerate(steps):
            tempList = []
            for x in range(animation):
                tempImg = image.subsurface(x * self.size, y * self.size, self.size, self.size)
                tempList.append(pygame.transform.scale(tempImg, (self.size * self.imageScale, self.size * self.imageScale)))
            animationList.append(tempList)
        return animationList

    def move(self, sHeight, win, player, allowSpawn):
        firstDrawn = self.rect.y == -45
        if (firstDrawn and allowSpawn) or not firstDrawn:

            dy = 0
            grav = 5

            #apply grav
            dy += grav

            #meteor crashes
            if self.rect.bottom + dy == 630:
                if self.explodePlay == False:
                    Meteor.explode.play(0, 1000)
                    self.explodePlay = True
                self.moving = False

            #update meteor position
            if self.moving == True: 
                if self.fallPlay == False:
                    Meteor.fall.play(0, 2000)
                    self.fallPlay = True
                self.rect.y += dy

            #detects if player hitbox collides with enemy and applies hit cooldown
            if self.rect.colliderect(player.rect) and player.meteorCd == 0 and player.hitCd == 0 and player.protect == False:
                if (player.rect.x + player.rect.left) + 1 > (self.rect.right + self.rect.x):
                    player.rightHit = True
                if (player.rect.x + player.rect.right) - 1 < (self.rect.left + self.rect.x):
                    player.leftHit = True
                player.hit = True
                player.health -= 10
                player.meteorCd = 120

            #check action
            if self.moving == True:
                self.update_action(0)
                animationCd = 100
            else:
                self.update_action(1)
                animationCd = 110


            self.image = self.animationList[self.action][self.frameIndex]
            #check if enough time has passed since last update
            if pygame.time.get_ticks() - self.updateTime > animationCd:
                self.frameIndex += 1
                self.updateTime = pygame.time.get_ticks()

             #check if the animation finished
            if self.frameIndex >= len(self.animationList[self.action]):
                self.frameIndex = 0

                #check if some action is the current animation
                if self.action == 1:
                    self.display = False

            img = self.image
            #pygame.draw.rect(win, (0,0,0), self.rect)
            if self.imageScale == 1:
                win.blit(img, (self.rect.x - self.offset[0], self.rect.y - 65 + self.offset[1]))
            elif self.imageScale > 1:
                win.blit(img, (self.rect.x - (self.offset[0] * self.imageScale), (self.rect.y + (-65 + self.offset[1]) * self.imageScale)))
      
        return firstDrawn and allowSpawn

    def update_action(self, newAction):
        #check if new action is different then prev
        if newAction != self.action:
            self.action = newAction
            #update animation settings
            self.frameIndex = 0
            self.updateTime = pygame.time.get_ticks()
    


