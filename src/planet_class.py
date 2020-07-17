# Carlos Armendariz
# andrew id: carmenda

import pygame
import math
"""
contains planet class
"""

class Planet(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, image, blackHoleImage):
        pygame.sprite.Sprite.__init__(self)

        self.isSun = False
        self.isBlackHole = False
        self.x, self.y = x, y
        self.originalX, self.originalY = x, y
        self.velocity = [0, 0]
        self.scrollX, self.scrollY = 0, 0
        self.distance = 0
        self.distanceFromTarget = 0

        self.image = image
        self.image = pygame.transform.scale(self.image, (radius*2, radius*2))
        self.originalImage = self.image
        self.blackHoleImage = pygame.transform.scale(blackHoleImage, (radius // 2, radius // 2))
        self.originalBlackHoleImage = self.blackHoleImage.copy()
        self.rect = self.image.get_rect()

        self.radius = radius
        self.originalRadius = radius
        self.rect.center = (self.x, self.y)

        self.scale = 1
        self.gravity = 0.3
        self.originalGravity = self.gravity
        self.updateRect()

    def update(self, target):
        if self.isBlackHole:
            self.image = self.originalBlackHoleImage
            self.gravity = self.originalGravity * 1000
            if self.scale == 1:
                self.scale = 0.25
                self.sizeToScale()

        self.scrollX = target.scrollX
        self.scrollY = target.scrollY
        self.x = self.originalX + self.scrollX
        self.y = self.originalY + self.scrollY
        self.updateRect()

    def updateRect(self):
        if self.isBlackHole:
            self.areaOfEffect = self.radius ** 2
        else:
            self.areaOfEffect = self.radius * 2.5
        width, height = self.radius * 2, self.radius * 2
        self.rect = pygame.Rect((self.x - width , self.y - height), (width, height))
        self.rect.center = (self.x + self.scrollX, self.y + self.scrollY)

    #resize planet based on its scale (default is 1)
    def sizeToScale(self):
        self.radius = self.originalRadius * self.scale
        self.image = pygame.transform.scale(self.originalImage, (
                int(self.originalRadius * 2 * self.scale),
                int(self.originalRadius * 2 * self.scale)))
        self.updateRect()

        if not self.isSun or not self.isBlackHole:
            if self.radius < 100:
                self.kill()
                return True

        return False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def getDistance(self, target):
        distance = ((self.x + self.scrollX - target.x) ** 2 +
                    (self.y + self.scrollY - target.y) ** 2) ** 0.5

        return distance

    # moves entity location based on its distance from the planet
    def attractEntity(self, target):
        xDistance = self.rect.center[0] - target.rect.center[0]
        yDistance = self.rect.center[1] - target.rect.center[1]

        distance = (xDistance**2 + yDistance**2) ** 0.5
        distanceFromEntintity = distance - self.radius - target.radius


        if int(distance) < self.areaOfEffect:

            if xDistance < 0:
                angleFromPlanet = int(math.degrees(
                    math.atan(yDistance / xDistance))) + 90

            elif xDistance > 0:
                angleFromPlanet = int(math.degrees(
                    math.atan(yDistance / xDistance))) + 270

            else:
                if yDistance > 0:
                    angleFromPlanet = 90

                else:
                    angleFromPlanet = -90

            if distanceFromEntintity > 0:

                target.velocity[1] -= math.cos(math.radians(angleFromPlanet)) * self.gravity
                target.velocity[0] += math.sin(math.radians(angleFromPlanet)) * self.gravity

            elif distanceFromEntintity < 0:

                target.velocity = [0, 0]


                if xDistance > 0:

                    if yDistance < 0:
                        target.movedY += math.sin(
                            math.radians((angleFromPlanet))) * distanceFromEntintity

                    else:
                        target.movedY -= math.sin(
                            math.radians(
                                (angleFromPlanet))) * distanceFromEntintity

                else:
                    if yDistance < 0:
                        target.movedY -= math.sin(
                            math.radians((angleFromPlanet))) * distanceFromEntintity


                    else:
                        target.movedY += math.sin(
                            math.radians((angleFromPlanet))) * distanceFromEntintity

    #attracts player to the planet
    def attractPlayer(self, target):
        self.distance = self.getDistance(target)
        self.distanceFromTarget = self.distance - target.radius / 2 - self.radius
        planetCenter = (self.x + self.scrollX, self.y + self.scrollY)
        xDistance = target.x - planetCenter[0]
        yDistance = target.y - planetCenter[1]


        if self.distance < self.areaOfEffect:
            # setting angle of player so it rotates around center of planet
            if xDistance > 0:
                target.angle = int(math.degrees(
                    math.atan(yDistance / xDistance))) + 90

            elif xDistance < 0:
                target.angle = int(math.degrees(
                    math.atan(yDistance / xDistance))) + 270

            if self.distanceFromTarget > 0 or self.isBlackHole:

                if self.isBlackHole and self.distance < target.radius:
                    target.hasWon = True
                    target.isShip = False
                else:
                    target.hasWon = False
                target.velocity[1] -= math.cos(math.radians(target.angle)) * self.gravity
                target.velocity[0] += math.sin( math.radians(target.angle)) * self.gravity

            elif self.distanceFromTarget < 0  and not self.isBlackHole:
                if self.isSun:
                    target.hitPoints -= 1

                target.scrollY -= math.cos(
                    math.radians(target.angle)) * self.distanceFromTarget

                target.scrollX += math.sin(
                    math.radians(target.angle)) * self.distanceFromTarget

