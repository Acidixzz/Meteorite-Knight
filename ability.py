import pygame
from powerup import PowerUp

class Heart(PowerUp):

    def __init__(self, i):
        super().__init__(i)

        self.upgradeCount = 0
        self.requirement = 15

    def ability(self, player):
        if self.upgradeCount < 5:
            player.curHealth += 10
            player.health = player.curHealth
            player.coins -= self.requirement
            self.requirement += 5
            self.upgradeCount += 1
        if self.upgradeCount == 5:
            self.maxed = True


class Shield(PowerUp):

    def __init__(self, i):
        super().__init__(i)

        self.upgradeCount = 0
        self.requirement = 5

    def ability(self, player):
        if self.upgradeCount < 5:
            player.curShield += 10
            player.shieldHealth = player.curShield
            player.coins -= self.requirement
            self.requirement += 5
            self.upgradeCount += 1
        if self.upgradeCount == 5:
            self.maxed = True

class Attack(PowerUp):

    def __init__(self, i):
        super().__init__(i)

        self.upgradeCount = 0
        self.requirement = 10

    def ability(self, player):

        if self.upgradeCount < 5:
            player.attackDamage += 10
            player.coins -= self.requirement
            self.requirement += 10
            self.upgradeCount += 1
        if self.upgradeCount == 5:
            self.maxed = True

class Bubble(PowerUp):

    pygame.init()
    pygame.display.set_mode((1280, 720))

    img = pygame.image.load('assets/bigbubble.png').convert_alpha()

    def __init__(self, i):
        super().__init__(i)

        self.inInventory = False
        self.requirement = 30
        
        self.update = 0

    def ability(self, player):
        player.coins -= self.requirement
        self.inInventory = True

class SelfRevive(PowerUp):

    pygame.init()
    pygame.display.set_mode((1280, 720))

    img = pygame.image.load('assets/bigbubble.png').convert_alpha()

    def __init__(self, i):
        super().__init__(i)

        self.requirement = 50

    def ability(self, player):
        player.coins -= self.requirement
        player.revive = True
