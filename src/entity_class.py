# Carlos Armendariz
# andrew id: carmenda

import pygame
import math
from planet_class import Planet
"""
contains all moving objects and defines their movement
"""
# based on Lukas Peraza's game object class for asteroids
class GameObject(pygame.sprite.Sprite):

    def __init__(self, x, y, speed, image):
        pygame.sprite.Sprite.__init__(self)
        self.hitPoints = 6
        self.scrollX, self.scrollY = 0, 0
        self.x, self.y = x, y

        self.velocity = [0, 0]
        self.angle = 0
        self.speed = speed
        self.originalSpeed = self.speed
        self.speedLimit = speed * 2
        self.originalSpeedLimit = self.speedLimit

        self.image = image
        self.originalImage = self.image.copy()

        self.width, self.height = self.image.get_size()
        self.radius = max(self.width, self.height)

        self.rect = pygame.Rect(self.x - self.radius / 2, self.y - self.radius / 2,
                                self.radius, self.radius)
        self.updateRect()

    def applyResitance(self):
        xResistance = 0.15 * self.originalSpeed
        yResistance = 0.15 * self.originalSpeed

        if self.velocity[0] > 0:

            self.velocity[0] -= xResistance
        elif self.velocity[0] < 0:
            self.velocity[0] += xResistance

        if self.velocity[1] > 0:
            self.velocity[1] -= yResistance
        elif self.velocity[1] < 0:
            self.velocity[1] += yResistance

    def applySpeedLimit(self):
        if self.velocity[0] > self.speedLimit:
            self.velocity[0] = self.speedLimit
        elif self.velocity[0] < -self.speedLimit:
            self.velocity[0] = -self.speedLimit

        if self.velocity[1] > self.speedLimit:
            self.velocity[1] = self.speedLimit
        elif self.velocity[1] < -self.speedLimit:
            self.velocity[1] = -self.speedLimit

    def move(self):
        vx, vy = self.velocity
        self.scrollX += vx
        self.scrollY += vy

    def update(self):
        self.move()
        self.updateRect()

    def updateRect(self):
        self.rect = self.image.get_rect()
        self.width, self.height = self.image.get_size()
        self.radius = max(self.width, self.height)
        self.rect.center = (self.x, self.y)

class Player(GameObject):
    def __init__(self, x, y, speed, playerImage, staticShipImage, dynamicShipImage):
        super().__init__(x, y, speed, playerImage)

        self.dynamicShipImage = dynamicShipImage
        self.originalDynamicShipImage = self.dynamicShipImage.copy()

        self.staticShipImage = staticShipImage
        self.originalStaticShipImage = self.staticShipImage.copy()

        self.isShip = True
        self.mouseAngle = self.angle
        self.isOnPlanet = False
        self.jumpX, self.jumpY = 0, 0
        self.score = 0
        self.hasWon = False
        self.facing = "right"

    def update(self, isKeyPressed, bulletGroup):
        if self.isShip:
            self.applyResitance()

            self.angle = self.mouseAngle
            self.image = pygame.transform.rotate(self.originalStaticShipImage,
                                                 -abs(self.angle))
            if isKeyPressed(304):
                self.speedLimit = self.originalSpeedLimit * 4
                self.speed = self.originalSpeed * 4
            else:
                self.speed = self.originalSpeed
                self.speedLimit = self.originalSpeedLimit * 2

            if isKeyPressed(119):
                self.image = pygame.transform.rotate(self.originalDynamicShipImage,
                                                     -abs(self.angle))

                self.velocity[0] = -math.sin(math.radians(self.mouseAngle)) * self.speedLimit
                self.velocity[1] = math.cos(math.radians(self.mouseAngle)) * self.speedLimit

            elif isKeyPressed(115):
                self.velocity[0] = math.sin(math.radians(self.mouseAngle)) * self.speedLimit / 4
                self.velocity[1] = -math.cos(math.radians(self.mouseAngle)) * self.speedLimit / 4

            if isKeyPressed(97):
                self.velocity[0] = math.sin(
                    math.radians(self.mouseAngle + 90)) * self.speedLimit / 4
                self.velocity[1] = -math.cos(
                    math.radians(self.mouseAngle + 90)) * self.speedLimit / 4

            elif isKeyPressed(100):
                self.velocity[0] = math.sin(
                    math.radians(self.mouseAngle - 90)) * self.speedLimit / 4
                self.velocity[1] = -math.cos(
                    math.radians(self.mouseAngle - 90)) * self.speedLimit / 4

        elif not self.isShip:
            if self.facing == "right":
                self.image = pygame.transform.rotate(self.originalImage,
                                                     -abs(self.angle))
            elif self.facing == "left":
                self.image = pygame.transform.flip(self.originalImage, True, False)
                self.image = pygame.transform.rotate(self.image,
                                                     -abs(self.angle))

            self.speedLimit = self.originalSpeedLimit * 1.5
            self.speed = self.originalSpeed * 1.5

            if not self.hasWon and self.isOnPlanet:
                self.applyResitance()
                if isKeyPressed(97):
                    self.facing = "left"
                    self.velocity[0] = (math.sin(math.radians(self.angle + 85)) * self.speed) + self.jumpX
                    self.velocity[1] = (math.cos(
                        math.radians(self.angle - 95)) * self.speed) + self.jumpY

                elif isKeyPressed(100):
                    self.facing = "right"
                    self.velocity[0] = (math.sin(math.radians(self.angle - 85)) * self.speed) + self.jumpX
                    self.velocity[1] = (math.cos(
                        math.radians(self.angle + 95)) * self.speed) + self.jumpY

        self.applySpeedLimit()
        super(Player, self).update()

    def destroyPlanet(self, planet):
        sizeChange = 0.1
        planet.scale -= sizeChange

    def getMouseAngle(self, x, y):
        yDif = self.y - y
        xDif = x - self.x

        if xDif != 0:
            self.mouseAngle = math.atan(yDif / xDif)
        else:
            self.mouseAngle = 90

        if xDif > 0:
            self.mouseAngle = abs(math.degrees(self.mouseAngle) - 90)
        else:
            self.mouseAngle = abs(math.degrees(self.mouseAngle) - 270)

        if self.mouseAngle > 360:
            if yDif > 0:
                self.mouseAngle = 0
            else:
                self.mouseAngle = 180

    def shoot(self, bulletGroup, bulletRadius = 5):
        bulletX = self.x - self.scrollX
        bulletY = self.y - self.scrollY
        bulletSpeed = 20
        bulletAngle = self.mouseAngle + 90

        newBullet = Bullet(bulletX, bulletY,
                           bulletAngle, bulletRadius, bulletSpeed)

        newBullet.source = "player"
        bulletGroup.add(newBullet)

class Enemy(GameObject):
    def __init__(self, x, y,speed, staticImage, dynamicImage):
        super().__init__(x, y, speed, staticImage)
        self.dynamicImage =dynamicImage
        self.originalDynamicImage = self.dynamicImage.copy()
        self.attackRadius = 400
        self.rect = self.originalImage.get_rect()
        self.originalX, self.originalY = x, y
        self.movedX, self.movedY = 0, 0
        self.angle = 0
        self.speedLimit = self.speed / 2
        self.originalSpeedLimit = self.speedLimit
        self.rect.center = (x, y)
        self.attackDelay = 50
        self.originalAttackDelay = self.attackDelay
        # self.isHostile = False

    def update(self, target):
        if self.velocity == [0, 0]:
            self.image = pygame.transform.rotate(self.originalImage,
                                             -abs(self.angle))

        else: self.image = pygame.transform.rotate(self.dynamicImage,
                                             -abs(self.angle))
        self.scrollX = target.scrollX
        self.scrollY = target.scrollY
        self.x = self.originalX + self.scrollX + self.movedX
        self.y = self.originalY + self.scrollY + self.movedY
        self.updateRect()

    def updateRect(self):
        self.rect = self.image.get_rect()
        self.radius = max(self.image.get_size()) // 2
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def getDistance(self, target):
        distance = ((self.x - target.x) ** 2 +
                    (self.y  - target.y) ** 2) ** 0.5
        return distance

    def look(self, target):
        self.xDistance = target.x - self.x
        self.yDistance  = target.y - self.y

        if self.xDistance < 0:
            self.angle = -int(math.degrees(
                math.atan(self.yDistance / self.xDistance))) - 270
        elif self.xDistance > 0:
            self.angle = int(math.degrees(
                math.atan(self.yDistance / self.xDistance))) + 90

        self.angle = abs(self.angle)

    def chase(self, target):
        self.distanceFromPlayer = self.getDistance(target)
        self.look(target)

        if self.distanceFromPlayer > self.attackRadius:
            self.velocity[0] += math.sin(math.radians((self.angle))) * self.speed * 2
            self.velocity[1] += math.cos(math.radians((self.angle))) * self.speed * 2

        elif self.distanceFromPlayer < self.attackRadius / 2:
            self.velocity[0] -= math.sin(
                math.radians((self.angle))) * self.speed

            self.velocity[1] -= math.cos(
                math.radians((self.angle))) * self.speed

        self.applySpeedLimit()
        self.movedX += self.velocity[0] * self.speed
        self.movedY -= self.velocity[1] * self.speed

    def shoot(self, bulletGroup):
        bulletX = self.x - self.scrollX
        bulletY = self.y - self.scrollY
        bulletRadius = 5
        bulletSpeed = 20
        bulletAngle = self.angle + 90

        newBullet = Bullet(bulletX, bulletY,
                            bulletAngle, bulletRadius, bulletSpeed)

        bulletGroup.add(newBullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, radius, speed):
        pygame.sprite.Sprite.__init__(self)
        self.lifeSpan = 3000
        self.source = "enemy"
        self.collided = False
        self.x, self.y = x, y
        self.angle = angle
        self.radius = radius
        self.speed = speed

        self.velocity = [0, 0]
        self.velocity[0] = math.cos(math.radians(self.angle)) * self.speed
        self.velocity[1] = math.sin(math.radians(self.angle)) * self.speed
        self.scrollX, self.scrollY = 0, 0
        self.rect = pygame.Rect(self.x, self.y, self.radius, self.radius)

    def move(self):
        self.x -= self.velocity[0]
        self.y -= self.velocity[1]

    def update(self, scrollX, scrollY):
        self.scrollX, self.scrollY = scrollX, scrollY
        self.updateRect()
        self.move()

    def updateRect(self):
        self.rect.center = self.x - self.radius / 2 + self.scrollX, self.y - self.radius / 2 + self.scrollY

    def checkCollisions(self, targetGroup, planetsRequired, player, generateEnemy = ""):
        self.lifeSpan -= 1
        if self.lifeSpan <= 0:
            self.kill()
        for target in targetGroup:
            if self.rect.colliderect(target.rect):

                if isinstance(target, Player) and self.source == "enemy":
                    self.kill()
                    target.hitPoints -= 0

                elif isinstance(target, Planet):
                    xDistanceFromPlanet = target.rect.center[0] - self.rect.center[0]
                    yDistanceFromPlanet = target.rect.center[1] - self.rect.center[1]
                    distance = (xDistanceFromPlanet ** 2 + yDistanceFromPlanet ** 2) ** 0.5
                    distanceFromEntintity = distance - self.radius - target.radius
                    if distanceFromEntintity < 0:
                        self.kill()
                        if self.source == "player":
                            if player != "":
                                if not player.isShip and not target.isSun and not target.isBlackHole:

                                    target.scale -= 0.05
                                    planetIsKill = target.sizeToScale()

                                    if planetIsKill:
                                        player.score += 1
                                        if generateEnemy != "":
                                            generateEnemy(target.x, target.y)

                                elif player.isShip and target.isSun and \
                                        len(targetGroup) == 1 and self.radius > 5:
                                    target.isBlackHole = True
                                    target.isSun = False

                elif isinstance(target, Enemy) and self.source == "player":
                    self.kill()
                    target.kill()
                    if player.hitPoints < 6:
                        player.hitPoints += 1
