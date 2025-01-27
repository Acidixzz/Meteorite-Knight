import pygame
import random
from player import Player
from coin import Coin
from enemy import Enemy
from meteorite import Meteor
from menu import MainMenu, Pause
from button import Button
from ability import Heart, Shield, Attack, Bubble, SelfRevive


class Game():
    def __init__(self):

        pygame.init()

        self.sWidth = 1280
        self.sHeight = 720

        #create game self.window
        self.win = pygame.display.set_mode((self.sWidth, self.sHeight), pygame.FULLSCREEN) #pygame.FULLSCREEN as second arguement
        pygame.display.set_caption('Meteorite Knight')

        #set framerate
        self.clock = pygame.time.Clock()
        self.FPS = 60

        #Asset creation-----------------------------------------------------------------------------|

        #load bg image
        self.bg = pygame.image.load('BackGround/forest.jpg').convert_alpha()
        self.shopBg = pygame.image.load('BackGround/shopinterior1.png').convert_alpha()
        self.shopEntrance = [pygame.image.load('assets/newshop.png').convert_alpha().subsurface(0, 0, 200, 200), pygame.image.load('assets/newshop.png').convert_alpha().subsurface(200, 0, 200, 200)]

        #game over setup
        self.retry = Button(440, 330, pygame.image.load('Background/buttons/retry.png').convert_alpha())
        self.retryB = False
        self.menuExit = Button(440, 430, pygame.image.load('Background/buttons/menuexit.png').convert_alpha())
        self.menuExitB = False
        self.fadein = 60
        self.black = pygame.image.load('Background/black.png').convert_alpha()
        self.alpha = 0

        #pause menu setup
        self.p = Pause()
        self.pause = pygame.image.load('Background/pause.png').convert_alpha()

        #shop setup
        self.shop = False
        self.resetpos = False
        self.Heart = Heart(1)
        self.Shield = Shield(2)
        self.Attack = Attack(3)
        self.Bubble = Bubble(4)
        self.SelfRevive = SelfRevive(5)

        #Knight
        self.knightImage = pygame.image.load('Characters/Knight1.png').convert_alpha()
        self.knightSteps = [4, 8, 7, 6, 5, 4, 4, 6, 5, 2, 6, 6]
        self.Knight = Player(0, 560, self.knightImage, self.knightSteps)

        #wave sounds
        self.letterSound = pygame.mixer.Sound('Sound/wave.wav')
        self.letterSound.set_volume(0.3)
        self.letterPlay = False
        self.waveMove = pygame.mixer.Sound('Sound/wavemove.wav')
        self.waveMove.set_volume(0.3)
        self.waveMovePlay = False

        #setup
        self.m = MainMenu(self.win)
        self.x1 = 490
        self.y1 = 310
        self.initialSpawn = True
        self.showMeteorDelay = 0
        self.showMeteorDelayBlue = 0
        self.showMeteorDelayGrey = 0
        self.moveCd = 0
        self.wave = 0
        self.waveInProgress = False
        self.intermission = False
        self.waveCount = -1
        self.update = 100
        self.update2 = 100
        self.update3 = 100
        self.update4 = 100
        self.update5 = 100
        self.update6 = 100
        self.starting = False
        self.run = True
        self.cd = 0
        self.end = False
        self.started = False
        self.exited = False
        #music
        self.musicChannel = pygame.mixer.Channel(0)
        self.menuMusic = pygame.mixer.Sound('Sound/menu.wav')
        self.menuMusic.set_volume(0.1)
        self.startSound = pygame.mixer.Sound('Sound/start.wav')
        self.gameMusic = pygame.mixer.Sound('Sound/game.wav')
        self.gameMusic.set_volume(0.10)
        self.shopMusic = pygame.mixer.Sound('Sound/shop.wav')
        self.shopMusic.set_volume(0.10)
        self.overMusic = pygame.mixer.Sound('Sound/gameover.wav')
        self.overMusic.set_volume(0.15)
        self.overPlay = False
        self.openDoor = pygame.mixer.Sound('Sound/opendoor.wav')
        self.openDoor.set_volume(0.15)
        self.openPlay = False
        self.closeDoor = pygame.mixer.Sound('Sound/closedoor.wav')
        self.closeDoor.set_volume(0.15)
        self.closePlay = False
        #counter variable for sounds in the different loops (game states)
        self.c = 0

    #reset game
    def game_reset(self):
        self.Knight = Player(0, 560, self.knightImage, self.knightSteps)
        self.overPlay = False
        self.wave = 0
        self.alpha = 0
        self.fadein = 60
        self.menuExitB = False
        self.retryB = False
        self.initialSpawn = True
        self.waveInProgress = False
        self.bubble = False
        self.Heart = Heart(1)
        self.Shield = Shield(2)
        self.Attack = Attack(3)
        self.Bubble = Bubble(4)
        self.SelfRevive = SelfRevive(5)


    #resize image to display window and displays it
    def draw_bg(self):
        scaledBg = pygame.transform.scale(self.bg, (self.sWidth, self.sHeight))
        self.win.blit(scaledBg, (0,0))

    def draw_shop_bg(self):
        self.win.blit(self.shopBg, (0, 0))

    def draw_powers(self):
        self.Heart.draw(self.win, self.Knight)
        if self.Heart.display_coin:
            self.Heart.draw_coin_amount(self.win, self.Heart.requirement, (55 + 170 + (self.Heart.i - 1) * 170), self.Heart.y + 35)

        self.Shield.draw(self.win, self.Knight)
        if self.Shield.display_coin:
            self.Shield.draw_coin_amount(self.win, self.Shield.requirement, (53 + 170 + (self.Shield.i - 1) * 170), self.Shield.y + 15)

        self.Attack.draw(self.win, self.Knight)
        if self.Attack.display_coin:
            self.Attack.draw_coin_amount(self.win, self.Attack.requirement, (55 + 170 + (self.Attack.i - 1) * 170), self.Attack.y + 40)

        self.Bubble.draw(self.win, self.Knight)
        if self.Bubble.display_coin:
            self.Bubble.draw_coin_amount(self.win, self.Bubble.requirement, (52 + 170 + (self.Bubble.i - 1) * 170), self.Bubble.y + 30)

        self.SelfRevive.draw(self.win, self.Knight)
        if self.SelfRevive.display_coin:
            self.SelfRevive.draw_coin_amount(self.win, self.SelfRevive.requirement, (50 + 170 + (self.SelfRevive.i - 1) * 170), self.SelfRevive.y + 30)

    def reset_powers(self):
        if self.Heart.upgradeCount < 5:
            self.Heart.pickedUp = False

        if self.Shield.upgradeCount < 5:
            self.Shield.pickedUp = False

        if self.Attack.upgradeCount < 5:
            self.Attack.pickedUp = False

        if self.Bubble.inInventory == False:
            self.Bubble.pickedUp = False

        if self.Knight.revive == False:
            self.SelfRevive.pickedUp = False
        #next powerups below

    def draw_lights(self):
        self.Heart.draw_light(self.win)
        self.Shield.draw_light(self.win)
        self.Attack.draw_light(self.win)
        self.Bubble.draw_light(self.win)
        self.SelfRevive.draw_light(self.win)

    #draw health bar
    def draw_health(self, x, y):
        pygame.draw.rect(self.win, (255, 255, 255), (x-2, y-2, 404 + ((self.Knight.curHealth % 100) * 4), 34))
        pygame.draw.rect(self.win, (255, 0, 0), (x, y, 400 + ((self.Knight.curHealth % 100) * 4), 30))
        ratio = self.Knight.health/self.Knight.curHealth
        pygame.draw.rect(self.win, (255, 255, 0), (x, y, ((400 + ((self.Knight.curHealth % 100) * 4)) * ratio), 30))

    def draw_sHealth(self, x, y):
        pygame.draw.rect(self.win, (255, 255, 255), (x-2, y-2, 304 + ((self.Knight.curShield - 30) * 3), 24))
        pygame.draw.rect(self.win, (0, 0, 0), (x, y, 300 + ((self.Knight.curShield - 30) * 3), 20))
        ratio = self.Knight.shieldHealth/self.Knight.curShield
        pygame.draw.rect(self.win, (0, 0, 255), (x, y, ((300 + ((self.Knight.curShield - 30) * 3)) * ratio), 20))

    def draw_cd(self, attackCd, x, y):
        pygame.draw.rect(self.win, (255, 255, 255), (x-2, y-2, 204, 24))
        pygame.draw.rect(self.win, (0, 0, 0), (x, y, 200, 20))
        ratio = attackCd/50
        pygame.draw.rect(self.win, (0, 255, 0), (x, y, (200 * ratio), 20))

    def draw_coin_amount(self, coins, x, y):
        font = pygame.font.Font('fonts/Stackedpixel.ttf', 30)
        if coins < 10:
            amount = font.render('0' + str(coins), True, (255, 255, 255))
            amountO = font.render('0' + str(coins), True, (0, 0, 0))
        else: 
            amount = font.render(str(coins), True, (255, 255, 255))
            amountO = font.render(str(coins), True, (0, 0, 0))

        self.win.blit(Coin.img.subsurface(0, 32, 32, 32), (x, y - 3))
        self.win.blit(amountO, (x + 32, y + 5))
        self.win.blit(amount, (x + 30, y + 3))
        
        

    def spawn_enemies(self, wave):
        '''
        instance = ['alien', 'meteor']
        instance2 = ['alien', 'meteor']

        grey = [instance, instance2]
        blue = [instance, instance2]
        green = [instance, instance2]
        enemyList = [green, blue, grey]'''

        if self.wave > 50:
            multiplier = 5

        elif self.wave > 40:
            multiplier = 4

        elif self.wave > 30:
            multiplier = 3
 
        elif self.wave > 20:
            multiplier = 2

        elif self.wave > 10:
            multiplier = 1

        else:
            multiplier = 0

        greenIndex = 0
        greenData = [50, 1, [5, 63], [30 + (multiplier * 30), 0], 0]
        blueIndex = 1
        blueData = [205, 3.5, [30, 34], [60 + (multiplier * 30), 50], 0]
        greyIndex = 2
        greyData = [50, 1, [5, 63], [20 + (multiplier * 10), 0], 1]

        if wave % 10 == 0: #CHANNNNGGEE THiIISIIIIs   if wave%10 == 0:
            greenAmount = 0
        else: greenAmount = 2 + wave * 2
    
        if wave % 5 == 0 and wave % 10 != 0:
            blueAmount = wave // 5
        else: blueAmount = 0

        if wave % 10 == 0:
            greyAmount = (wave // 10) * 6
        elif wave > 10:
            greyAmount = (wave // 10)
        else: greyAmount = 0

        spawnList = []
        for Type in range(3):
            greenList = []
            blueList = []
            greyList = []
            if Type == 0:
                for _ in range(greenAmount):
                    flip = random.randrange(2)
                    tempList = []
                    tempMeteor = Meteor(1)
                    tempEnemy = Enemy(tempMeteor.rect.x, greenIndex, greenData)
                    hasCoin = random.randrange(2)
                    if hasCoin == 1:
                        tempCoin = Coin(tempEnemy.rect.x)
                    if flip == 1:
                        tempEnemy.flip = True
                    tempList.append(tempMeteor)
                    tempList.append(tempEnemy)
                    if hasCoin == 1:
                        tempList.append(tempCoin)
                    greenList.append(tempList)
                spawnList.append(greenList)
            
            elif Type == 1:
                for _ in range(blueAmount):
                    flip = random.randrange(2)
                    tempList = []
                    tempMeteor = Meteor(3)
                    tempEnemy = Enemy(tempMeteor.rect.x, blueIndex, blueData)
                    tempCoin = Coin(tempEnemy.rect.x)
                    tempCoin2 = Coin(tempEnemy.rect.x)
                    tempCoin3 = Coin(tempEnemy.rect.x)
                    if flip == 1:
                        tempEnemy.flip = True
                    tempList.append(tempMeteor)
                    tempList.append(tempEnemy)
                    tempList.append(tempCoin)
                    tempList.append(tempCoin2)
                    tempList.append(tempCoin3)
                    blueList.append(tempList)
                spawnList.append(blueList)
            
            else:
                for _ in range(greyAmount):
                    flip = random.randrange(2)
                    tempList = []
                    tempMeteor = Meteor(1)
                    tempEnemy = Enemy(tempMeteor.rect.x, greyIndex, greyData)
                    if flip == 1:
                        tempEnemy.flip = True
                    tempList.append(tempMeteor)
                    tempList.append(tempEnemy)
                    greyList.append(tempList)
                spawnList.append(greyList)
            
        return spawnList

    def show_enemy(self, enemyList):

        if not enemyList[0] and not enemyList[1] and not enemyList[2]:
            self.waveInProgress = False
            self.InitialSpawn = True
            if self.wave % 5 == 0:
                self.intermission = True

        #Green------------------------------------------------------------------------------------|
        for i in enemyList[0]:
            if i[1].alive == True:
                if i[0].action == 1 and i[0].frameIndex == 3:
                    i[1].show = True
                if i[1].show == True:
                    i[1].move(self.sWidth, self.sHeight + 65, self.win, self.Knight)
                    if len(i) == 3:
                        if i[2].pickedUp == False:
                            i[2].move(self.sWidth, self.sHeight + 65, self.win, self.Knight)

            else:
                if self.update <= 0:
                    enemyList[0].remove(i)
                    self.update = 100
                else: 
                    i[1].move(self.sWidth, self.sHeight + 65, self.win, self.Knight)
                    self.update -= 1

        #Blue-------------------------------------------------------------------------------------|
        for i in enemyList[1]:
            if i[1].alive == True:
                if i[0].action == 1 and i[0].frameIndex == 3:
                    i[1].show = True
                if i[1].show == True:
                    i[1].move(self.sWidth, self.sHeight + 65, self.win, self.Knight)
                    if i[2].pickedUp == False:
                        i[2].move(self.sWidth, self.sHeight + 65, self.win, self.Knight)
                    if i[3].pickedUp == False:
                        i[3].move(self.sWidth, self.sHeight + 65, self.win, self.Knight)
                    if i[4].pickedUp == False:
                        i[4].move(self.sWidth, self.sHeight + 65, self.win, self.Knight)
            else:
                if self.update <= 0:
                    enemyList[1].remove(i)
                    self.update = 100
                else: 
                    i[1].move(self.sWidth, self.sHeight + 65, self.win, self.Knight)
                    self.update -= 1

        #Grey--------------------------------------------------------------------------------------|
        for i in enemyList[2]:
            if i[1].alive == True:
                if i[0].action == 1 and i[0].frameIndex == 3:
                    i[1].show = True
                if i[1].show == True:
                    i[1].move(self.sWidth, self.sHeight + 65, self.win, self.Knight)
            else:
                if self.update <= 0:
                    enemyList[2].remove(i)
                    self.update = 100
                else: 
                    i[1].move(self.sWidth, self.sHeight + 65, self.win, self.Knight)
                    self.update -= 1

    def show_meteor(self, enemyList):
        if self.initialSpawn == True:
            self.showMeteorDelayBlue = 0
            self.showMeteorDelayGrey = 0
            self.initialSpawn = False


        #Green--------------------------------------------------------------------------------------|
        for i in enemyList[0]:
            if i[0].display == True:
                if i[0].move(self.sHeight, self.win, self.Knight, self.showMeteorDelay == 0) == True:
                    self.showMeteorDelay = random.randint(120, 180)
                    break
        if self.showMeteorDelay > 0:
            self.showMeteorDelay -= 1

        #Blue--------------------------------------------------------------------------------------|
        for i in enemyList[1]:
            if i[0].display == True:
                if i[0].move(self.sHeight, self.win, self.Knight, self.showMeteorDelayBlue == 0) == True:
                    self.showMeteorDelayBlue = random.randint(600, 900)
                    break
        if self.showMeteorDelayBlue > 0:
            self.showMeteorDelayBlue -= 1

        #Grey--------------------------------------------------------------------------------------|
        for i in enemyList[2]:
            if i[0].display == True:
                if i[0].move(self.sHeight, self.win, self.Knight, self.showMeteorDelayGrey == 0) == True:
                    self.showMeteorDelayGrey = random.randint(120, 180)
                    break
        if self.showMeteorDelayGrey > 0:
            self.showMeteorDelayGrey -= 1


    def draw_wave(self, wave, x, y):

        string = 'Wave '

        if pygame.time.get_ticks() - self.updateTime > 3000 and self.waveInProgress == True:
            string = string.replace('W', ' ')
        if pygame.time.get_ticks() - self.updateTime > 3500 and self.waveInProgress == True:
            string = string.replace('a', ' ')
        if pygame.time.get_ticks() - self.updateTime > 4000 and self.waveInProgress == True:
            string = string.replace('v', ' ')
        if pygame.time.get_ticks() - self.updateTime > 4500 and self.waveInProgress == True:
            string = string.replace('e', ' ')

        font = pygame.font.Font('fonts/Stackedpixel.ttf', 100)
        waveOut = font.render(string + str(wave), True, (0, 0, 0))
        waveNum2 = font.render(string + str(wave), True, (255, 128, 0))
        waveNum = font.render(string + str(wave), True, (255, 178, 102))
        if wave < 10:
            x -= 0
        elif wave < 100:
            x -= 20
        elif wave < 1000:
            x -= 40
        elif wave >= 1000:
            x -= 60
    
        self.win.blit(waveOut, (x - 5, y))
        self.win.blit(waveOut, (x + 10, y))
        self.win.blit(waveOut, (x + 5, y))
        self.win.blit(waveOut, (x, y - 5)) 
        self.win.blit(waveOut, (x + 5, y - 5)) 
        self.win.blit(waveOut, (x, y + 5)) 
        self.win.blit(waveOut, (x - 5, y + 5)) 
        self.win.blit(waveOut, (x + 10, y + 2))
        self.win.blit(waveOut, (x + 10, y + 7)) 
        self.win.blit(waveOut, (x + 10, y + 10)) 
        self.win.blit(waveOut, (x - 1, y + 10)) 
    
        self.win.blit(waveNum2, (x + 6, y + 5))
        self.win.blit(waveNum, (x, y))

    def draw_end(self):
        wave = self.wave - 1
        string = ('You survived ' + str(wave) + ' Rounds!')
        x = 135
        y = 150

        font = pygame.font.Font('fonts/Stackedpixel.ttf', 100)
        waveOut = font.render(string, True, (0, 0, 0))
        waveNum2 = font.render(string, True, (255, 128, 0))
        waveNum = font.render(string, True, (255, 178, 102))

        self.black.set_alpha(self.alpha)
        self.win.blit(self.black, (0, 0))

        if self.overPlay == False:
            self.overMusic.play(-1)
            self.overPlay = True

        if self.fadein == 0:
            self.win.blit(waveOut, (x - 5, y))
            self.win.blit(waveOut, (x + 10, y))
            self.win.blit(waveOut, (x + 5, y))
            self.win.blit(waveOut, (x, y - 5)) 
            self.win.blit(waveOut, (x + 5, y - 5)) 
            self.win.blit(waveOut, (x, y + 5)) 
            self.win.blit(waveOut, (x - 5, y + 5)) 
            self.win.blit(waveOut, (x + 10, y + 2))
            self.win.blit(waveOut, (x + 10, y + 7)) 
            self.win.blit(waveOut, (x + 10, y + 10)) 
            self.win.blit(waveOut, (x - 1, y + 10)) 
    
            self.win.blit(waveNum2, (x + 6, y + 5))
            self.win.blit(waveNum, (x, y))

            if self.retry.draw(self.win):
                self.retryB = True
                self.overMusic.stop()
            if not self.retry.buttonChannel.get_busy() and self.retryB:
                self.game_reset()
                self.c = 2

            if self.menuExit.draw(self.win):
                self.menuExitB = True
                self.overMusic.stop()
            if not self.menuExit.buttonChannel.get_busy() and self.menuExitB:
                self.started = False
                self.m.menu = True
                self.m.i = 0
                self.end = False
                self.c = 0
                self.game_reset()

        #black img opacity
        if self.fadein <= 0:
            self.alpha = 255
            self.fadein = 0
        elif self.fadein <= 10:
            self.alpha = 213
            self.fadein -= 0.25
        elif self.fadein <= 20:
            self.alpha = 170
            self.fadein -= 0.25
        elif self.fadein <= 30:
            self.alpha = 128
            self.fadein -= 0.25
        elif self.fadein <= 40:
            self.alpha = 85
            self.fadein -= 0.25
        elif self.fadein <= 50:
            self.alpha = 43
            self.fadein -= 0.25
        elif self.fadein <= 60:
            self.alpha = 0
            self.fadein -= 0.25

    def check_menu(self):
        #main menu
        while self.m.menu:
            if self.c == 0:
                self.musicChannel.play(self.menuMusic, -1)
                self.c += 1
            self.m.state_menu()
            start = self.m.start.draw(self.m.win)
            if start:
                self.started = True
                self.musicChannel.stop()
            if self.started and not self.m.start.buttonChannel.get_busy():
                self.m.menu = False
                self.starting = True
            #self.m.tutorial.draw(self.m.win)
            self.exit = self.m.exit.draw(self.m.win)
            if self.exit:
                self.exited = True
            if self.exited and not self.m.exit.buttonChannel.get_busy():
                self.m.menu = False
                self.run = False
            for _ in pygame.event.get():
               pass

            pygame.display.update()

    def start_cutscene(self):
        while self.starting:
            if self.c == 1:
                self.startSound.play(0, 2000)
                self.c += 1
            if self.cd <= 0:
                if self.m.i == 5 and self.end == True:
                    self.starting = False
                elif self.m.i == 5:
                    self.cd = 2000
                    self.end = True
                self.win.blit(self.m.startList[self.m.i], (-160, 0))
                if self.m.i < 5:
                    self.m.i +=1
                    self.cd = 150
            else: self.cd -= 1

            pygame.display.update()

    def shopfront(self):
        self.doorRect = pygame.Rect(1230, 525, 50, 100)
        self.exitRect = pygame.Rect(0, 525, 50, 100)
        #pygame.draw.rect(self.win, (0, 255, 0), self.doorRect)
        #pygame.draw.rect(self.win, (0, 255, 0), self.exitRect)
        if self.Knight.rect.colliderect(self.doorRect):
            self.closePlay = False
            self.win.blit(self.shopEntrance[1], (1080, 425))
            if self.openPlay == False:
                self.openDoor.play(0, 500)
                self.openPlay = True
        else:
            self.openPlay = False
            self.win.blit(self.shopEntrance[0], (1080, 425))
            if self.closePlay == False:
                self.closeDoor.play(0, 500)
                self.closePlay = True


    def game_loop(self):

        while self.run:
            #set fps
            self.clock.tick(self.FPS)

            self.check_menu() 
            self.menuMusic.stop()
            self.start_cutscene()
            #pause menu
            if self.p.paused:
                self.pause.set_alpha(127)
                self.win.blit(self.pause, (0, 0))
                self.p.pause_loop(self.win)
                
            else:
                self.musicChannel.unpause()


            if self.c == 2 and self.shop == False:
                self.musicChannel.fadeout(500)
                self.musicChannel.play(self.gameMusic, -1)
                self.c += 1
            if self.c == 3 and self.shop == True:
                self.musicChannel.fadeout(750)
                self.musicChannel.play(self.shopMusic, -1, fade_ms = 750)
                self.c -= 1

            if self.shop == True:
                self.draw_shop_bg() 
            else:
                self.draw_bg()
                if self.intermission == True:
                    self.shopfront()
                    if self.wave % 5 == 0:
                        self.Knight.health = self.Knight.curHealth
                        self.Knight.shieldHealth = self.Knight.curShield
                        self.reset_powers()


            if self.waveInProgress == False and self.intermission == False:
                self.x1 = 490
                self.y1 = 310
                self.waveInProgress = True
                self.wave += 1
                enemyList = self.spawn_enemies(self.wave)
                self.waveCount = 90
                self.waveMovePlay = False
                self.updateTime = pygame.time.get_ticks()

            if self.waveInProgress == True and pygame.time.get_ticks() - self.updateTime > 6000 and self.Knight.alive:
                #alien
                self.show_enemy(enemyList)

            #sets knight position to left side of the screen
            if self.resetpos == True:
                if self.intermission == False:
                    self.Knight.rect.x = 1280
                    self.resetpos = False
                else:
                    self.Knight.rect.x = 0
                    self.resetpos = False

            #move player, change animations, and show player
            if self.shop == True:
                #draw shop interior
                self.draw_powers()


                self.Knight.move(1020, self.sHeight + 65)
                self.Knight.update(self.sWidth)
                self.Knight.draw(self.win)

                #draw lights so they are over player
                self.draw_lights()
            else:

                if self.Knight.alive == False and self.Knight.revive == False and self.Knight.deadover == True:
                    self.draw_end()

                self.Knight.move(self.sWidth, self.sHeight + 65)
                self.Knight.update(self.sWidth)
                self.Knight.draw(self.win)


            if self.Knight.alive == False and self.Knight.revive == False:
                self.gameMusic.fadeout(100)

            if self.waveInProgress == True and pygame.time.get_ticks() - self.updateTime > 6000 and self.Knight.alive:
                #meteor
                self.show_meteor(enemyList)
    
            if self.Knight.alive:
                self.draw_health(20, 20)
                self.draw_sHealth(20, 60)
                self.draw_cd(self.Knight.attackCd, 20, 90)
                self.draw_coin_amount(self.Knight.coins, 13, 116)
    
            #wave draw-----------------------------------------------------------------------------------------------------------------------|
            if self.waveInProgress == True and self.Knight.alive == True:
                self.draw_wave(self.wave, self.x1, self.y1)
                if pygame.time.get_ticks() - self.updateTime > 3000:
                    if self.letterPlay == False:
                        self.letterSound.play(0, 500)
                        self.letterPlay = True
                    if self.waveCount == 90:
                        self.letterPlay = False
                    if self.waveCount == 60:
                        self.letterPlay = False
                    elif self.waveCount == 30:
                        self.letterPlay = False
                    elif self.waveCount == 0:
                        self.letterPlay = False
                    self.waveCount -= 1
                    if self.waveCount < 0:
                        self.waveCount = -1


            if pygame.time.get_ticks() - self.updateTime <= 5000 and pygame.time.get_ticks() - self.updateTime > 4750 and self.waveInProgress == True:
                self.moveCd = 50
                if self.waveMovePlay == False:
                    self.waveMove.play(0, 1500)
                    self.waveMovePlay = True

            if self.moveCd > 0:
                self.moveCd -= 1
                if self.wave < 10:
                    self.x1 += 8.75
                elif self.wave < 100:
                    self.x1 += 8.5
                elif self.wave < 1000:
                    self.x1 += 8.0
                self.y1 -= 4.55


            #event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and self.moveCd <= 0 and pygame.time.get_ticks() - self.updateTime > 5000:
                        self.p.paused = True
                        self.musicChannel.pause()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_k:
                        if self.Knight.attackCd == 0:
                            self.Knight.kDown = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_j:
                        if self.Knight.attackCd == 0:
                            self.Knight.jDown = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_l:
                        self.Knight.defending = False
                        self.Knight.protect = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        if self.intermission == True and self.Knight.rect.colliderect(self.doorRect):
                            self.shop = True
                            self.Knight.shop = True
                            self.resetpos = True
                        if self.intermission == True and self.shop == True and self.Knight.rect.colliderect(self.exitRect):
                            self.shop = False
                            self.Knight.shop = False
                            self.resetpos = True
                            self.intermission = False

                        #power up / upgrades
                        if self.shop == True and self.Knight.rect.colliderect(self.Heart.powerRect) and self.Heart.pickedUp == False:
                            if self.Knight.coins >= self.Heart.requirement:
                                self.Heart.pickedUp = True
                                self.Heart.ability(self.Knight)

                        if self.shop == True and self.Knight.rect.colliderect(self.Shield.powerRect) and self.Shield.pickedUp == False:
                            if self.Knight.coins >= self.Shield.requirement:
                                self.Shield.pickedUp = True
                                self.Shield.ability(self.Knight)

                        if self.shop == True and self.Knight.rect.colliderect(self.Attack.powerRect) and self.Attack.pickedUp == False:
                            if self.Knight.coins >= self.Attack.requirement:
                                self.Attack.pickedUp = True
                                self.Attack.ability(self.Knight)

                        if self.shop == True and self.Knight.rect.colliderect(self.Bubble.powerRect) and self.Bubble.pickedUp == False:
                            if self.Knight.coins >= self.Bubble.requirement:
                                self.Bubble.pickedUp = True
                                self.Bubble.ability(self.Knight)

                        if self.shop == True and self.Knight.rect.colliderect(self.SelfRevive.powerRect) and self.SelfRevive.pickedUp == False:
                            if self.Knight.coins >= self.SelfRevive.requirement:
                                self.SelfRevive.pickedUp = True
                                self.SelfRevive.ability(self.Knight)

                    #power up use
                    if event.key == pygame.K_f:
                        if self.waveInProgress == True and self.Bubble.inInventory == True:
                            self.Knight.bubble = True
                            self.Bubble.update = pygame.time.get_ticks()

                    if pygame.time.get_ticks() - self.Bubble.update > 20000 and self.Knight.bubble == True:
                        self.Knight.bubble = False
                        self.Bubble.inInventory = False

                    #power up selection swap
                    #if event.key == pygame.K_c:
                    #    self.switch()

            pygame.display.update()

        pygame.quit()