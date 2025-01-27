import pygame
from ability import Bubble

class Player():
    def __init__(self, x, y, image, steps):
        self.size = 128
        self.imageScale = 1
        self.offset = [11, 2]
        self.flip = False
        self.animationList = self.load_images(image, steps)
        self.action = 0#0:idle, 1:walk, 2:run, 3:jump, 4:attack
        self.frameIndex = 0
        self.image = self.animationList[self.action][self.frameIndex]
        self.updateTime = pygame.time.get_ticks()
        self.rect = pygame.Rect(x, y, 45, 65)
        self.velY = 0
        self.walk = False
        self.run = False
        self.jump = False
        self.attacking = False
        self.defending = False
        self.protect = False
        self.kDown = False
        self.jDown = False
        self.hit = False
        self.rightHit = False
        self.leftHit = False
        self.hitAmount = 0
        self.hitCd = 0
        self.meteorCd = 0
        self.attackCd = 0
        self.count = 0
        self.dashCount = 1
        self.comboTimer = 0
        self.health = 100
        self.shieldHealth = 30
        self.attackDamage = 10
        #cur health amts
        self.curHealth = 100
        self.curShield = 30
        self.alive = True
        self.revive = False
        self.deadover = False

        #abilities
        self.bubble = False
        self.bubbleRect = Bubble.img.get_rect()

        #coin amount
        self.coins = 0

        #sounds
        self.jumpSound = pygame.mixer.Sound('Sound/jump.wav')
        self.jumpSound.set_volume(0.75)
        self.hitSound = pygame.mixer.Sound('Sound/hit.wav')
        self.hitPlay = False
        self.dashSound = pygame.mixer.Sound('Sound/attack2.wav')
        self.dashSound.set_volume(0.05)
        self.dashPlay = False
        self.swordSound = pygame.mixer.Sound('Sound/attack1.mp3')
        self.swordSound.set_volume(0.15)
        self.swordPlay = False
        self.walkSound = pygame.mixer.Sound('Sound/walk.wav')
        self.walkSound.set_volume(0.35)
        self.walkPlay = False
        self.runSound = pygame.mixer.Sound('Sound/run.wav')
        self.runSound.set_volume(0.35)
        self.runPlay = False

        self.shop = False

        self.shopwalkSound = pygame.mixer.Sound('Sound/shopwalk.wav')
        self.shopwalkSound.set_volume(0.15)
        self.shopwalkPlay = False
        self.shoprunSound = pygame.mixer.Sound('Sound/shoprun.wav')
        self.shoprunSound.set_volume(0.15)
        self.shoprunPlay = False
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

    #moves player
    def move(self, sWidth, sHeight):
        vel = 5
        grav = 1
        dx = 0 
        dy = 0
        self.walk = False
        self.run = False

        keys = pygame.key.get_pressed()
        if self.alive:

            if self.hitCd > 0:
                self.hitCd -= 1
            if self.meteorCd > 0:
                self.meteorCd -= 1

            if self.attacking == False and self.hit == False and self.defending == False:
                #movement
                if(keys[pygame.K_a]):
                    self.flip = True
                    self.walk = True
                    if(keys[pygame.K_LSHIFT]):
                        self.walk = False
                        self.run = True
                        vel = 10
                    dx = -vel
                if(keys[pygame.K_d]):
                    self.flip = False
                    self.walk = True
                    if(keys[pygame.K_LSHIFT]):
                        self.walk = False
                        self.run = True
                        vel = 10
                    dx = vel
                #jump
                if(keys[pygame.K_SPACE] and self.jump == False):
                    self.velY = -20
                    self.jump = True
                    self.jumpSound.play(0, 500)
                #attack
                if(self.jDown == True):
                    self.attackType = 1
                    self.attack()
                    if self.swordPlay == False:
                        self.swordSound.play(0)
                        self.swordPlay = True
            if(self.kDown == True and self.hit == False and self.defending == False):
                self.attackType = 2
                self.attack()
                if self.dashPlay == False:
                    self.dashSound.play(0)
                    self.dashPlay = True

                #defending
            if(keys[pygame.K_l] and self.attacking == False):
                if self.hit == False:
                    self.defending = True

        #movement sounds
        if self.shop == False:
            if dx == 5 or dx == -5:
                if self.walkPlay == False:
                    self.walkSound.play(-1)
                    self.walkPlay = True

            if dx == 10 or dx == -10:
                if self.runPlay == False:
                    self.runSound.play(-1)
                    self.runPlay = True

        else:
            if dx == 5 or dx == -5:
                if self.shopwalkPlay == False:
                    self.shopwalkSound.play(-1)
                    self.shopwalkPlay = True

            if dx == 10 or dx == -10:
                if self.shoprunPlay == False:
                    self.shoprunSound.play(-1)
                    self.shoprunPlay = True

        if self.walkPlay == True and self.walk == False or self.jump == True:
            self.walkSound.stop()
            self.walkPlay = False

        if self.runPlay == True and self.run == False or self.jump == True:
            self.runSound.stop()
            self.runPlay = False

        if self.shopwalkPlay == True and self.walk == False or self.jump == True:
            self.shopwalkSound.stop()
            self.shopwalkPlay = False

        if self.shoprunPlay == True and self.run == False or self.jump == True:
            self.shoprunSound.stop()
            self.shoprunPlay = False
            
        #apply grav
        self.velY += grav
        dy += self.velY

        #player stays on screen
        if self.rect.left + dx < 0:
            dx = self.rect.left
        if self.rect.right + dx > sWidth:
            dx = sWidth - self.rect.right
        if self.rect.bottom + dy > sHeight - 160:
            self.velY = 0
            dy = sHeight - 160 - self.rect.bottom
            self.jump = False
       
        #apply attack cooldown
        if self.attackCd > 0:
            self.attackCd -= 1
            
        #apply attack combo timer
        if self.comboTimer > 0:
            self.comboTimer -= 1

        #update player position
        self.rect.x += dx


        if self.action == 6 and self.attackType == 2:#attacking with k
            if self.flip == True:
                self.rect.x -= 15
                if self.rect.left - 15 < 0:
                    self.rect.left -= self.rect.left
            else: 
                self.rect.x += 15
                if self.rect.right - 15 < 0:
                    self.rect.right += sWidth - self.rect.right

        self.rect.y += dy

        #bubble rect pos
        self.bubbleRect.x = self.rect.x - 45
        self.bubbleRect.y = self.rect.y - 30

    # method for handling animations
    def update(self, sWidth = None):

        #check action
        if self.alive == False and self.revive == True and self.deadover == True:
            self.update_action(11)
            animationCd = 100

        if self.health <= 0 and (self.deadover == False or self.revive == False):
            self.alive = False
            self.health = 0
            self.update_action(10)
            animationCd = 100

        elif self.defending == True and self.hit == False:
            self.update_action(8)
            animationCd = 200
        elif self.attacking == True and self.attackType == 1:
            if self.count == 0:
                self.update_action(4)
                animationCd = 50
            elif self.count == 1:
                self.update_action(5)
                animationCd = 75
            elif self.count == 2:
                self.update_action(6)
                animationCd = 50
        elif self.attacking == True and self.attackType == 2:
            self.update_action(6)
            animationCd = 75
        elif self.hit == True and self.alive == True:
            if self.hitPlay == False:
                self.hitSound.play(0, 300)
                self.hitPlay = True
            self.update_action(9)

            if self.rightHit == True:
                if self.rect.right + 5 > sWidth:
                    self.rect.x = sWidth - self.rect.width
                else: self.rect.x += 5
            elif self.leftHit == True: 
                if self.rect.left - 5 < 0:
                    self.rect.x = 0
                else: self.rect.x -= 5

            animationCd = 100
        elif self.jump == True:
            self.update_action(3)
            animationCd = 150
        elif self.walk == True:
            self.update_action(1)
            animationCd = 100
        elif self.run == True:
            self.update_action(2)
            animationCd = 75
        elif self.alive == True:
            self.update_action(0)
            animationCd = 200



        self.image = self.animationList[self.action][self.frameIndex]
        #check if enough time has passed since last update
        if pygame.time.get_ticks() - self.updateTime > animationCd:
            self.frameIndex += 1
            self.updateTime = pygame.time.get_ticks()

        #lunge mechanic when attacking with j and k
        
        elif self.action == 6:#attacking with j
            if self.flip == True:
                self.rect.x -= 5
            else: self.rect.x += 5

        #combo attack not hold down
        if self.frameIndex == 0:
            self.jDown = False

        #check if the animation finished
        if self.frameIndex >= len(self.animationList[self.action]):
            if self.alive == False:
                self.frameIndex = len(self.animationList[self.action]) - 1
            else: self.frameIndex = 0
            #check if some action is the current animation
            if self.action == 11:
                self.health = self.curHealth
                self.alive = True
                self.deadover = False
                self.revive = False
            if self.action == 10:
                self.deadover = True
            if self.action == 9:
                self.hit = False
                self.rightHit = False
                self.leftHit = False
                self.attacking = False
                self.hitPlay = False
            if (self.action == 4 or self.action == 5 or self.action == 6) and self.attackType == 1:
                self.attacking = False
                #check if last attack animation has ended
                if self.count == 2 and self.attackType == 1:
                    self.count = 0
                    self.attackCd = 50
                self.count += 1
                self.comboTimer = 25
            if self.action == 6 and self.attackType == 2:
                self.attacking = False
                self.hitAmount = 0
                self.kDown = False
                self.dashPlay = False
                if self.dashCount == 2:
                    self.attackCd = 50
                    self.dashCount = 0
                else: self.attackCd = 5
                self.dashCount += 1
                
            
    
    def attack(self):
        if self.attackCd == 0:
            self.swordPlay = False
            if self.comboTimer == 0 and self.attackType == 1:
                self.count = 0
            self.attacking = True
        
            if self.attackType == 1:
                self.attackRect = pygame.Rect(self.rect.centerx - (self.rect.width * 1.7 * self.flip), self.rect.y, 1.7 * self.rect.width, self.rect.height)
            
            if self.attackType == 2:
                self.attackRect2 = pygame.Rect(self.rect.centerx - (self.rect.width * 1.7 * self.flip), self.rect.y, 1.7 * self.rect.width, self.rect.height)


    
        

    def update_action(self, newAction):
        #check if new action is different then prev
        if newAction != self.action:
            self.action = newAction
            #update animation settings
            self.frameIndex = 0
            self.updateTime = pygame.time.get_ticks()

    #displays player    
    def draw(self, win):
        img = pygame.transform.flip(self.image, self.flip, False)
        #pygame.draw.rect(win, (0,0,0), self.rect)
        if self.flip:
            #left facing
            if self.imageScale == 1:
                win.blit(img, (self.rect.x - self.offset[0] - 60, self.rect.y - 65 + self.offset[1]))
            elif self.imageScale > 1:
                win.blit(img, (self.rect.x - (self.offset[0] * self.imageScale) - (60 * self.imageScale), (self.rect.y - 65) + self.offset[1] - (self.size * (self.imageScale - 1))))
        else:
            #right facing
            if self.imageScale == 1:
                win.blit(img, (self.rect.x - self.offset[0], self.rect.y - 65 + self.offset[1]))
            elif self.imageScale > 1:
                win.blit(img, (self.rect.x - (self.offset[0] * self.imageScale), (self.rect.y - 65) + self.offset[1] - (self.size * (self.imageScale - 1))))


        if self.bubble == True:
            #pygame.draw.rect(win, (0,0,0), self.bubbleRect)
            win.blit(Bubble.img, (self.rect.x -45, self.rect.y - 30))




