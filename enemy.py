import pygame

class Enemy():

    pygame.mixer.init()
    pygame.init()

    #sounds
    hitSound = pygame.mixer.Sound('Sound/attack.wav')
    hitSound.set_volume(0.7)
    shieldHit = pygame.mixer.Sound('Sound/shieldhit.wav')
    shieldHit.set_volume(0.3)

    #images
    pygame.display.set_mode((1280, 720))

    green = pygame.image.load('Characters/aliensmall.png').convert_alpha()
    blue = pygame.image.load('Characters/alienbig1.png').convert_alpha()
    grey = pygame.image.load('Characters/alienjump.png').convert_alpha()

    images = [green, blue, grey]
    

    def __init__(self, x, index, data):
        self.steps = [2, 3, 3, 3]
        self.size = data[0]    #blue = 205
        self.rectSize = data[1]  #blue = 3.6
        self.imageScale = 1
        self.offset = data[2]  #blue = [35, 40]
        self.flip = False
        self.switch = 5
        self.animationList = self.load_images(Enemy.images[index], self.steps)
        self.action = 0 #0:idle, 1:move, 2:hurt, 3:dead
        self.frameIndex = 0
        self.image = self.animationList[self.action][self.frameIndex]
        self.updateTime = pygame.time.get_ticks()
        self.rect = pygame.Rect(x, 600, 40 * self.rectSize, 40 * self.rectSize)
        self.velY = 0
        self.moving = True
        self.jump = False
        self.r = data[4]
        self.jumpUpdate = pygame.time.get_ticks()
        self.hitUpdate = pygame.time.get_ticks()
        self.defendUpdate = pygame.time.get_ticks()
        self.hit = False
        self.hitCd = 0
        self.attackCd = 0
        self.health = data[3][0]
        self.startHealth = data[3][0]
        self.blueH = data[3][1]
        self.alive = True
        self.show = False

        #sound bools
        self.soundPlay = False
        self.shieldPlay = False
        
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

    def move(self, sWidth, sHeight, win, player):
        vel = 5
        grav = 1
        dx = 0  
        dy = 0

        if self.alive:

                #player protect
                if player.protect == True and player.defending == True and player.shieldHealth >= 0 and player.defendRect.colliderect(self.rect) == True:
                    self.moving = False
                    self.hit = True
                    if self.flip == True:
                        if self.rect.right + 40 > sWidth:
                            self.rect.x = sWidth - self.rect.width
                        else: self.rect.x += 40
                    else: 
                        if self.rect.left - 40 < 0:
                            self.rect.x = 0
                        else: self.rect.x -= 40

                #player bubble
                if self.rect.colliderect(player.bubbleRect) == True and player.bubble == True:

                    #running
                    if player.run == True:
                        if (player.bubbleRect.x + player.bubbleRect.right) - 1 < (self.rect.left + self.rect.x):
                            if self.rect.right + 15 > sWidth:
                                self.rect.x = sWidth - self.rect.width
                            else: self.rect.x += 15
                        elif (player.bubbleRect.x + player.bubbleRect.left) + 1 > (self.rect.right + self.rect.x):
                            if self.rect.left - 15 < 0:
                                self.rect.x = 0
                            else: self.rect.x -= 15
                        self.velY = -30

                    #walking
                    elif player.walk == True:
                        if (player.bubbleRect.x + player.bubbleRect.right) - 1 < (self.rect.left + self.rect.x):
                            if self.rect.right + 10 > sWidth:
                                self.rect.x = sWidth - self.rect.width
                            else: self.rect.x += 10
                        elif (player.bubbleRect.x + player.bubbleRect.left) + 1 > (self.rect.right + self.rect.x):
                            if self.rect.left - 10 < 0:
                                self.rect.x = 0
                            else: self.rect.x -= 10
                        self.velY = -20
     
                    #stand still
                    else:
                        if (player.bubbleRect.x + player.bubbleRect.right) - 1 < (self.rect.left + self.rect.x):
                            if self.rect.right + 5 > sWidth:
                                self.rect.x = sWidth - self.rect.width
                            else: self.rect.x += 5
                        elif (player.bubbleRect.x + player.bubbleRect.left) + 1 > (self.rect.right + self.rect.x):
                            if self.rect.left - 5 < 0:
                                self.rect.x = 0
                            else: self.rect.x -= 5
                        self.velY = -15

                #hit
                if self.hit == True:
                    self.shieldPlay = False
                    self.soundPlay = False
                        
                    self.moving = False
                    self.hitCd = 30
                    self.hit = False
                elif self.hit == False:
                    if self.hitCd == 0:
                        self.moving = True
                

                if self.hitCd > 0:
                    self.hitCd -= 1
                

                #movement
                if self.moving == True:
                    if self.flip == True:
                        self.switch = -vel
                        if(dx == self.rect.left):
                             self.flip = False
                    if self.flip == False:
                        self.switch = vel
                        if(dx == sWidth - self.rect.right):
                            self.flip = True
                dx = self.switch
              

                #jump
                if (self.jump == False and self.r == 1) and pygame.time.get_ticks() - self.jumpUpdate > 1000:
                    self.velY = -20
                    self.jump = True
                    self.frameIndex = 2
                    self.jumpUpdate = pygame.time.get_ticks()

                

        #detects if player hitbox collides with enemy and applies hit cooldown
        if player.rect.colliderect(self.rect) and player.hitCd == 0 and player.meteorCd == 0 and self.health > 0 and player.protect == False and self.hitCd == 0:
            if player.bubble == False:
                if (player.rect.x + player.rect.left) + 1 > (self.rect.right + self.rect.x):
                    player.rightHit = True
                if (player.rect.x + player.rect.right) - 1 < (self.rect.left + self.rect.x):
                    player.leftHit = True
                if player.health > 10:
                    player.hit = True
                player.health -= 10
                player.hitCd = 120
          
        #player defend
        if player.defending == True and player.shieldHealth > 0:
            if player.flip == True:
                player.defendRect = pygame.Rect(player.rect.centerx - player.rect.width // 2 - 3, player.rect.y-1, 5, player.rect.height)
                #pygame.draw.rect(win, (0, 255, 0), player.defendRect)
            else:
                player.defendRect = pygame.Rect(player.rect.centerx + player.rect.width // 2, player.rect.y-1, 5, player.rect.height)
                #pygame.draw.rect(win, (0, 255, 0), player.defendRect)

            if player.defendRect.colliderect(self.rect) and self.health > 0  and (pygame.time.get_ticks() - self.defendUpdate > 500):
                if player.bubble == False:
                    if self.shieldPlay == False:
                        Enemy.shieldHit.play(0, 500)
                        self.shieldPlay = True
                    player.protect = True
                    player.shieldHealth -= 10
                    self.defendUpdate = pygame.time.get_ticks()

        #player attacks
        if player.attacking == True:
            if player.attackType == 1:
                #pygame.draw.rect(win, (0, 255, 0), player.attackRect)
                if player.attackRect.colliderect(self.rect) and (pygame.time.get_ticks() - self.hitUpdate > len(player.animationList[player.action]) * 100):
                    if self.soundPlay == False:
                        Enemy.hitSound.play(0, 300)
                        self.soundPlay = True
                    self.hit = True
                    if player.count == 2:
                        self.health -= player.attackDamage
                    self.health -= player.attackDamage
                    self.hitUpdate = pygame.time.get_ticks()

            if player.attackType == 2:
                #pygame.draw.rect(win, (0, 255, 0), player.attackRect2)
                if player.attackRect2.colliderect(self.rect) and (pygame.time.get_ticks() - self.hitUpdate > len(player.animationList[player.action]) * 75):
                    if self.soundPlay == False:
                        Enemy.hitSound.play(0, 300)
                        self.soundPlay = True
                    self.hit = True
                    self.health -= player.attackDamage * 2
                    self.hitUpdate = pygame.time.get_ticks()

            
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

        #update enemy position
        if self.moving == True:
            self.rect.x += dx
            self.rect.y += dy
        else: 
            self.rect.x += 0
            self.rect.y += 0

        if self.health <= 0:
            self.alive = False

        #check action
        if self.health <= 0:
            self.alive = False
            self.health = 0
            self.update_action(3)
            animationCd = 100
        elif self.moving == False:
            self.update_action(2)
            animationCd = 25
        elif self.moving == True:
            self.update_action(1)
            animationCd = 100



        self.image = self.animationList[self.action][self.frameIndex]
        #check if enough time has passed since last update
        if pygame.time.get_ticks() - self.updateTime > animationCd:
            self.frameIndex += 1
            self.updateTime = pygame.time.get_ticks()

         #check if the animation finished
        if self.frameIndex >= len(self.animationList[self.action]):
            if self.alive == False:
                self.frameIndex = len(self.animationList[self.action]) - 1
            else: self.frameIndex = 0

            #check if some action is the current animation
            if self.action == 2 and self.moving == False:
                self.frameIndex = 2
                if player.protect == True:
                    player.protect = False
            if self.action == 1 and self.jump == True:
                self.frameIndex = 2


        #displays enemy
        img = pygame.transform.flip(self.image, self.flip, False)
        #pygame.draw.rect(win, (0,0,0), self.rect)
        if self.imageScale == 1:
            win.blit(img, (self.rect.x - self.offset[0], self.rect.y - 65 + self.offset[1]))
        elif self.imageScale > 1:
            win.blit(img, (self.rect.x - (self.offset[0] * self.imageScale), (self.rect.y - 65) + self.offset[1] - (self.size * (self.imageScale - 1))))

        
        if self.alive == True and self.health < self.startHealth and self.health > 0:
            if self.flip == False:
                self.draw_enemy_health(win, self.health, self.rect.x + self.blueH, self.rect.top - 10)
            elif self.flip == True:
                self.draw_enemy_health(win, self.health, self.rect.x -3 + self.blueH, self.rect.top - 10)



    def update_action(self, newAction):
        #check if new action is different then prev
        if newAction != self.action:
            self.action = newAction
            #update animation settings
            self.frameIndex = 0
            self.updateTime = pygame.time.get_ticks()

            
    def draw_enemy_health(self, win, health, x, y):
        pygame.draw.rect(win, (255, 255, 255), (x-2, y-2, 50, 9))
        pygame.draw.rect(win, (255, 0, 0), (x, y, 46, 5))
        ratio = health/self.startHealth
        pygame.draw.rect(win, (255, 255, 0), (x, y, (46 * ratio), 5))



