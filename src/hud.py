# Carlos Armendariz
# andrew id: carmenda
import pygame
import random
pygame.font.init()

"""
contains healthbar and minimap info
"""

class HealthBar(pygame.sprite.Sprite):
    def __init__(self, imageDict, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.imageDict = imageDict
        self.hitPoints = 6

        self.currentImage = imageDict[self.hitPoints]
        self.image = imageDict[self.hitPoints]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self, target):
        self.hitPoints = target.hitPoints
        if 0 <= self.hitPoints <= 6 and self.imageDict[self.hitPoints] != self.currentImage:
            self.currentImage = self.image
            self.image = self.imageDict[self.hitPoints]

class MiniMap(pygame.sprite.Sprite):
    def __init__(self, x, y, size, planetGroup, playerGroup, solarSystemSize, solarSystemCenter, winWidth, winHeight):
        pygame.sprite.Sprite.__init__(self)
        self.solarSystemSize = solarSystemSize
        self.size = size
        self.scale = self.size / self.solarSystemSize
        self.center = solarSystemCenter
        self.winWidth = winWidth
        self.winHeight = winHeight
        self.rect = pygame.Rect(x, y, size, size)
        self.image = pygame.Surface((size, size))
        self.color = (255, 0, 255)
        self.image.set_colorkey(self.color)
        self.image = self.image.convert()
        self.planetGroup = planetGroup

        self.update(playerGroup)
    # draws each planet in the list at its location on the minimap
    def update(self, playerGroup):
        self.image.fill(self.color)
        self.image = self.image.convert()

        yModifier, xModifier = 1, 1
        if self.center[0] < 1: xModifier = -1
        if self.center[1] < 0: yModifier = -1

        for planet in self.planetGroup:
            planetX = int((planet.x + planet.scrollX + (self.center[0]) * xModifier - self.winWidth / 2)
                          * self.scale)
            planetY = int((planet.y + planet.scrollY + (self.center[1]) * yModifier - self.winHeight / 2)
                          * self.scale)
            planetRadius = int(planet.radius * self.scale)

            if planetX - planetRadius > self.size:
                planetX = int(self.size)
                planetRadius = 20
                if not planet.isSun and not planet.isBlackHole:
                    planetRadius = 10

            elif planetX + planetRadius < 0:
                planetX = 0
                planetRadius = 20
                if not planet.isSun and not planet.isBlackHole:
                    planetRadius = 10

            if planetY - planetRadius > self.size:
                planetY = int(self.size)
                planetRadius = 20
                if not planet.isSun and not planet.isBlackHole:
                    planetRadius = 10

            elif planetY + planetRadius < 0:
                planetY = 0
                planetRadius = 20
                if not planet.isSun and not planet.isBlackHole:
                    planetRadius = 10

            if planet.isSun:
                planetColor = (255, 255, 0)

            elif planet.isBlackHole:
                r = random.randint(30, 200)
                g = random.randint(30, 200)
                b = random.randint(30, 200)
                planetColor = (r, g, b)
                planetRadius = 20

            else:
                planetColor = (0, 85, 255)

            pygame.draw.circle(self.image, planetColor,
                               (planetX, planetY), planetRadius)

        playerRadius = 3
        pygame.draw.circle(self.image, (255, 0, 0),
                           (int(self.size / 2), int(self.size / 2)),
                           playerRadius)

        pygame.draw.rect(self.image, (255, 255, 255), (0, 0, self.size, self.size), 1)

