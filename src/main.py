# Carlos Armendariz
# andrew id: carmenda
# 15-112 Fall 2018 Section K
# Term Project

import module_manager
module_manager.review()
import pygame
import pygame.gfxdraw
import planet_class, entity_class, hud, assets
import random, copy
pygame.font.init()
pygame.mixer.init()
'''
This is the main file that the game is run from.

project built around pygame framework created by Lukas Peraza

ship images based on sprites from https://kenney.nl/
player image from https://dribbble.com/shots/845764--GIF-Meet-Minimus-the-last-astronaut

sounds from https://www.pmsfx.com/pmsfxsamplerfree and
https://www.dl-sounds.com/
 '''
class PygameGame(object):
    def init(self):
        self.bgColor = (30, 30, 30)

        '''
        fade animation from PygameNerd on:
        https://stackoverflow.com/questions/12255558/how-to-use-pygame-set-alpha-on-a-picture
        '''
        self.alphaSurface = pygame.Surface((self.width, self.height))
        self.alphaSurface.fill(self.bgColor)
        self.alphaSurface.set_alpha(0)
        self.alph = 250

        self.audioContainer = assets.Audio()
        self.audioContainer.introMusic.play(-1)
        self.imageContainer = assets.Image(self.width, self.height)

        self.gameState = "startScreen"
        self.gameClock = 0
        self.playerSpeed = 4
        self.enemySpeed = 2
        self.scrollX = 0
        self.scrollY = 0

        self.planetCount = 7
        self.planetMap = []
        self.solarSystemSize = self.planetCount * 500
        self.solarSystemCenter = random.choice(
            [[-self.solarSystemSize / 2, -self.solarSystemSize / 2],
             [self.solarSystemSize / 2, self.solarSystemSize / 2],
             [self.solarSystemSize / 2, -self.solarSystemSize / 2],
             [-self.solarSystemSize / 2, self.solarSystemSize / 2]])
        self.generatePlanetLocations()
        self.generateSolarSystem(self.solarSystemSize)


        self.playerGroup = pygame.sprite.Group(
            entity_class.Player(self.width / 2, self.height / 2, self.playerSpeed,
                                self.imageContainer.playerImage,
                                self.imageContainer.dynamicShipImage,
                                self.imageContainer.staticShipImage))
        self.levelNum = 1
        self.loadHUD()
        self.enemyGroup = pygame.sprite.Group()
        self.generateEnemyPattern()
        self.enemyCount = self.planetCount
        self.bulletGroup = pygame.sprite.Group()
        self.endDelay = 150
        self.sandBoxImageList = self.getSandBoxImageList()
        self.hightlightSelectionCol = 1
        self.sandBoxPlacedList = []

        self.planetsRequired = (len(self.planetGroup) - 1) // 2

    # creates images that are correct size for display in sandbox mode
    def getSandBoxImageList(self):
        imageList = []
        for num in range(len(self.imageContainer.planetImageDict)):
            currImage = pygame.transform.scale(self.imageContainer.planetImageDict[num], (100, 100))
            imageList.append(currImage)

        sunImage = pygame.transform.scale(self.imageContainer.sunImage, (100, 100))
        imageList.append(sunImage)
        enemyImage = pygame.transform.scale(self.imageContainer.enemyImage, (100, 100))
        imageList.append(enemyImage)
        return imageList

    #loads placed objects into the game from sandbox mode
    def generateSandBoxLevel(self):
        self.planetGroup.empty()
        self.enemyGroup.empty()
        self.bulletGroup.empty()
        self.playerGroup = pygame.sprite.Group(
            entity_class.Player(self.width / 2, self.height / 2,
                                self.playerSpeed,
                                self.imageContainer.playerImage,
                                self.imageContainer.dynamicShipImage,
                                self.imageContainer.staticShipImage))

        self.gameState = "gamePlay"
        self.solarSystemSize = len(self.sandBoxPlacedList)
        scale = 11

        for planet in self.sandBoxPlacedList:

            xDistFromCenter = self.width / 2 - planet[0]
            yDistFromCenter = self.height / 3 - planet[1]
            planetX = -(xDistFromCenter) * scale
            planetY = -(yDistFromCenter) * scale
            planetR = 1000

            if planet[2] == 6:
                planetImage = self.imageContainer.sunImage
                self.generatePlanet(planetX, planetY, planetR, planetImage)

            elif planet[2] == 7:
                self.generateEnemy(planetX, planetY)

            else:
                planetImage = self.imageContainer.planetImageDict[planet[2] - 1]
                self.generatePlanet(planetX, planetY, planetR, planetImage)

    #this function allows the game to be restarted without reloading images
    def reset(self):
        self.enemyGroup.empty()
        self.bulletGroup.empty()
        self.planetGroup.empty()
        self.playerGroup.empty()
        self.playerGroup = pygame.sprite.Group(
            entity_class.Player(self.width / 2, self.height / 2,
                                self.playerSpeed,
                                self.imageContainer.playerImage,
                                self.imageContainer.dynamicShipImage,
                                self.imageContainer.staticShipImage))
        self.gameClock = 0
        self.scrollX = 0
        self.scrollY = 0

        self.planetMap = []
        self.solarSystemSize = self.planetCount * 1000
        self.solarSystemCenter = random.choice(
            [[-self.solarSystemSize / 2, -self.solarSystemSize / 2],
             [self.solarSystemSize / 2, self.solarSystemSize / 2],
             [self.solarSystemSize / 2, -self.solarSystemSize / 2],
             [-self.solarSystemSize / 2, self.solarSystemSize / 2]])
        self.generatePlanetLocations()
        self.generateSolarSystem(self.solarSystemSize)
        self.planetsRequiredTracker = (len(self.planetGroup) - 1) // 2
        self.planetsRequired = self.planetsRequiredTracker
        self.loadHUD()
        self.endDelay = 200
        self.generateEnemyPattern()
        self.hightlightSelectionCol = 1
        self.sandBoxPlacedList = []

        self.alph = 250

# creates all objects needed for the heads up display
    def loadHUD(self):
        self.healthBar = pygame.sprite.Group(hud.HealthBar(self.imageContainer.healthBarDict, 0, 0))

        mmSize = self.width / 6
        margin = 15

        self.miniMap = pygame.sprite.Group(
            hud.MiniMap(self.width - mmSize - margin, 0 + margin,
                        mmSize, self.planetGroup, self.playerGroup,
                        self.solarSystemSize, self.solarSystemCenter, self.width, self.height))

        self.fontSize = 30
        self.playerScore = pygame.font.SysFont("cambria", self.fontSize)
        for player in self.playerGroup:
            self.playerScoreSurface = self.playerScore.render(
                str(player.score), False, (255, 255, 255))

        self.level = pygame.font.SysFont("cambria", self.fontSize)
        self.levelCount = self.level.render(
            "Level: " + str(self.levelNum), False, (255, 255, 255))

    # checks where the mouse is when pressed on start screen
    def checkStartScreenPresses(self, x, y):
        if (self.width > x > self.width * 0.7) and \
                (self.height * 0.67 < y < self.height * 0.77):
            self.gameState = "gamePlay"

            pygame.mixer.fadeout(1000)
            self.audioContainer.dramaticSound.play(0)
            pygame.mixer_music.play(-1)

        if self.width > x > self.width * 0.74 and \
                self.height * 0.78 < y < self.height * 0.78 + self.height - self.height * 0.93:
            self.gameState = "sandBox"

        if self.width > x > self.width * 0.95 and \
                self.height * 0.9 < y < self.height:
            self.gameState = "helpScreen"

        if self.width * 0.75 < x < self.width * 0.75 + self.width - self.width * 0.82 and \
                self.height * 0.9 < y < self.height * 0.9 + self.height - self.height * 0.92:
            self.playing = False

    # checks where the mouse is when pressed on sandbox screen
    def checkSandBoxScreenPresses(self, x, y):
        if self.height - self.height * 0.2 < y < self.height - self.height * 0.2 + 100:
            for num in range(1, 8):
                if self.spacing * num < x < self.spacing * num + 100:
                    self.hightlightSelectionCol = num

        elif 0 < y < self.width * 0.045:

            if 0 < x < self.width * 0.1:
                if len(self.sandBoxPlacedList) > 0:
                    self.sandBoxPlacedList.pop()

            elif self.width > x > self.width - self.width * 0.3:
                self.gameState = "startScreen"
                self.sandBoxPlacedList = []

            elif self.width * 0.15 < x < self.width * 0.27:
                self.sandBoxPlacedList = []

        elif self.height * 0.1 < y < self.height - self.height * 0.34:
            self.sandBoxPlacedList.append((x, y, self.hightlightSelectionCol))

    def mousePressed(self, x, y):
        if self.gameState == "startScreen":
            self.checkStartScreenPresses(x, y)

        elif self.gameState == "sandBox":
            self.checkSandBoxScreenPresses(x, y)

        elif self.gameState == "helpScreen":
            if self.width * 0.78 < x < self.width and \
                self.height * 0.95 < y < self.height:
                self.gameState = "startScreen"

        elif self.gameState == "gamePlay":
            for player in self.playerGroup:
                player.shoot(self.bulletGroup)
                self.audioContainer.laserSound.play()

        elif self.gameState == "paused":
            if self.width * 0.29 < x < self.width * 0.29 + self.width * 0.42 and \
                self.height * 0.68 < y < self.height * 0.68 + self.height * 0.1:
                self.reset()
                self.levelNum = 1
                self.gameState = "startScreen"
                pygame.mixer.stop()
                self.audioContainer.introMusic.play(-1)

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):

        for player in self.playerGroup:
            player.getMouseAngle(x, y)

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        if self.gameState == "gamePlay":
            if keyCode == 114 and len(self.sandBoxPlacedList) == 0:
                self.reset()
                self.gameState = "gamePlay"

            elif keyCode == 114 and len(self.sandBoxPlacedList) > 0:
                self.generateSandBoxLevel()
                pygame.mixer_music.play(-1)

            if keyCode == 122:
                self.generateEnemy(self.width/2 - self.scrollX,
                                   self.height/2 - self.scrollY)
            if keyCode == 32:
                for player in self.playerGroup:
                    player.isShip = not player.isShip
            elif keyCode == 113 and len(self.planetGroup) <= 1:
                for player in self.playerGroup:
                    if player.isShip:
                        player.shoot(self.bulletGroup, 60)
                        self.audioContainer.bulletSound.play()

            if keyCode == 27:
                self.gameState = "paused"
                pygame.mixer_music.pause()


        elif self.gameState == "paused":
            if keyCode == 27:
                self.gameState = "gamePlay"
                pygame.mixer_music.unpause()


        elif self.gameState == "gameOver":
            if keyCode == 114 and len(self.sandBoxPlacedList) == 0:
                pygame.mixer.stop()
                self.reset()
                self.gameState = "gamePlay"
                pygame.mixer_music.play(-1)
            elif keyCode == 114 and len(self.sandBoxPlacedList) > 0:
                self.generateSandBoxLevel()
                pygame.mixer_music.play(-1)

            elif keyCode == 13:
                self.reset()
                self.levelNum = 1
                self.gameState = "startScreen"
                pygame.mixer.stop()
                self.audioContainer.introMusic.play(-1)

        elif self.gameState == "sandBox":
            if keyCode == 13:
                self.generateSandBoxLevel()
                pygame.mixer.stop()
                pygame.mixer_music.play(-1)

    def keyReleased(self, keyCode, modifier):
        pass

    def sideScroll(self):
        for player in self.playerGroup:
            self.scrollX = player.scrollX
            self.scrollY = player.scrollY

    #runs functions that allow planets to interact with the player and enemies
    def applyUniversalGravity(self):
        for planet in self.planetGroup:
            for player in self.playerGroup:
                planet.attractPlayer(player)
            for enemy in self.enemyGroup:
                planet.attractEntity(enemy)

# helper function for generateSolarSystem(); adds planet with given values to planetGroup
    def generatePlanet(self, x, y, radius, image = ""):
        blackHoleImage = self.imageContainer.blackHoleImage
        if image == "":
            imageIndex = random.randint(0, len(self.imageContainer.planetImageDict) - 1)
            planetImage = self.imageContainer.planetImageDict[imageIndex]
            newPlanet = planet_class.Planet(x, y, radius, planetImage, blackHoleImage)
        else:
            planetImage = image
            if planetImage == self.imageContainer.sunImage:
                radius = 1500
            else:
                radius = random.randint (500, 700)
            newPlanet = planet_class.Planet(x, y, radius, planetImage, blackHoleImage)

            if planetImage == self.imageContainer.sunImage:
                newPlanet.isSun = True

        self.planetGroup.add(newPlanet)

#this ugly boi makes sure that the given cell on the grid has no other 1s near it
    def adjacentCellHasOne(self, grid, row, col):
        if row - 1 >= 0:
            if grid[row - 1][col] == 1:
                return True
            elif grid[row - 1][col] == 1 :
                return True

            elif grid[row - 1][col - 1] == 1 :
                return True

            if col + 1 <= len(grid[row]) - 1:
                if grid[row - 1][col + 1] == 1:
                    return True

        if row - 1 <= len(grid):
            if grid[row + 1][col] == 1:
                return True
            if col - 1 >= 0:
                if grid[row + 1][col - 1] == 1 :
                    return True

            if col + 1 <= len(grid[row]) - 1:
                if grid[row + 1][col + 1] == 1:
                    return True
        return False

    #creates random solar system grid by randomly placing one planet in each row
    def generatePlanetLocations(self):
        assert(self.planetCount >= 6)

        gridCenter = self.planetCount // 2
        centerEmptyZone = set()

        for rowMargin in range(-1, 2):
            for colMargin in range(-1,2):
                centerEmptyZone.add((gridCenter - rowMargin, gridCenter - colMargin))
                centerEmptyZone.add((gridCenter + rowMargin, gridCenter + colMargin))
                centerEmptyZone.add((gridCenter + rowMargin, gridCenter - colMargin))

        grid = []
        planetList = []
        for row in range(self.planetCount + 1):
            grid.append([0] * (self.planetCount))

        for rows in range(len(grid) - 1):
            planetCol = random.randint(0, self.planetCount - 1)
            while (rows, planetCol) in centerEmptyZone or self.adjacentCellHasOne(grid, rows, planetCol):

                planetCol = random.randint(0, self.planetCount - 1)

            for i in range(self.planetCount):
                if i == planetCol:
                    grid[rows][planetCol] = 1
                    planetList.append((rows, i))

                elif rows == i == gridCenter:
                    grid[rows][i] = "c"
                    planetList.append((rows, i))
        return planetList

    # creates planets based on info in grid
    def generateSolarSystem(self, size):
        centerX, centerY = copy.copy(self.solarSystemCenter)
        self.planetGroup = pygame.sprite.Group()
        self.planetList = self.generatePlanetLocations()
        cellSize = size / ((self.planetCount / 2) + 1)
        for planet in self.planetList:

            x, y = planet
            xOffsetFromCenter = -(self.planetCount // 2 - x) * 2
            yOffsetFromCenter = -(self.planetCount // 2 - y) * 2
            newPlanetR = random.randint(500, int(cellSize))

            xMin = (xOffsetFromCenter* cellSize) + centerX
            yMin = (yOffsetFromCenter* cellSize) + centerY

            if xMin < 0:
                xMax = xMin
                xMin = xMax - cellSize

            else: xMax = xMin + cellSize

            if yMin < 0:
                yMax = yMin
                yMin = yMax - cellSize

            else: yMax = yMin + cellSize

            newPlanetX = xMax - ((xMax - xMin) / 2)
            newPlanetY = yMax - ((yMax - yMin) / 2)

            if planet == (self.planetCount // 2, self.planetCount // 2):
                self.generatePlanet(newPlanetX, newPlanetY, newPlanetR, self.imageContainer.sunImage)
            else:
                self.planetMap.append((newPlanetX, newPlanetX))
                self.generatePlanet(newPlanetX, newPlanetY, newPlanetR)

    #places an enemy at given x,y coordinate
    def generateEnemy(self, x, y):
        image = self.imageContainer.enemyImage
        dynamicImage = self.imageContainer.dynamicEnemyImage

        speed = self.enemySpeed

        newEnemy = entity_class.Enemy(x, y, speed, image, dynamicImage)
        self.enemyGroup.add(newEnemy)

    # places enemies at start of level
    def generateEnemyPattern(self):
        for planet in self.planetGroup:
            self.generateEnemy(planet.rect.center[0], planet.rect.center[1])

    # checks if the player is touching a planet
    def checkPlayerGrounded(self, player):
        found = False
        for planet in self.planetGroup:
                if 0 > planet.distanceFromTarget < planet.areaOfEffect:
                    found = True
        player.isOnPlanet = found

    # runs all functions that are based on two or more objects
    def runInteractions(self):
        for player in self.playerGroup:
            self.checkPlayerGrounded(player)
            self.planetGroup.update(player)

            for bullet in self.bulletGroup:
                bullet.update(player.scrollX, player.scrollY)


            checkedEnemies = set()
            for enemy in self.enemyGroup:
                enemy.chase(player)
                enemy.update(player)
                checkedEnemies.add(enemy)
                for otherEnemy in self.enemyGroup:
                    if otherEnemy not in checkedEnemies:
                        if enemy.rect.colliderect(otherEnemy):
                            enemy.velocity[0] -= 1
                            otherEnemy.velocity[0] += 1
                            enemy.velocity[1] -= 1
                            otherEnemy.velocity[1] += 1

                if enemy.distanceFromPlayer < self.width:
                    enemy.attackDelay -= 1
                    if enemy.attackDelay <= 0:
                        enemy.shoot(self.bulletGroup)
                        self.audioContainer.laserSound.play()
                        enemy.attackDelay = enemy.originalAttackDelay

            self.healthBar.update(player)
            player.update(self.isKeyPressed, self.bulletGroup)
            if player.hitPoints <= 0:
                self.gameState = "gameOver"
                pygame.mixer_music.stop()
                self.audioContainer.crashSound.play()
                player.kill()


            self.healthBar.update(player)

        for bullet in self.bulletGroup:
            if len(self.enemyGroup) == 0 and bullet.source == "enemy":
                bullet.kill()

            for player in self.playerGroup:
                bullet.checkCollisions(self.planetGroup, self.planetsRequired, player, self.generateEnemy)
                bullet.checkCollisions(self.enemyGroup, self.planetsRequired, player)
                bullet.checkCollisions(self.playerGroup, self.planetsRequired, player)

        self.applyUniversalGravity()
        self.sideScroll()

    def timerFired(self, dt):
        if self.gameState == "gamePlay":
            self.gameClock += 1
            self.runInteractions()
            self.miniMap.update(self.playerGroup)

            for player in self.playerGroup:
                color = (255, 255, 255)

                if len(self.planetGroup) <= 1:
                    r = random.randint(30, 200)
                    g = random.randint(30, 200)
                    b = random.randint(30, 200)
                    color = (r, g, b)
                    text = "Weapon Ready"
                else:
                    text = "Planets Left: %d" % (len(self.planetGroup) - 1)

                self.playerScoreSurface = self.playerScore.render(text, False, color)

                if player.hasWon:
                    if self.endDelay <= 0 and len(self.sandBoxPlacedList) == 0:
                        self.levelNum += 1
                        self.planetCount += 2
                        if self.enemySpeed < 10:
                            self.enemySpeed += 1
                        self.reset()

                    elif self.endDelay <= 0 and len(self.sandBoxPlacedList) > 0:
                        self.generateSandBoxLevel()
                        self.endDelay = 150
                        self.audioContainer.dramaticSound.play(0)


                    elif self.endDelay == 150:
                        self.audioContainer.dramaticSound.play(0)

                    self.endDelay -= 1

            if len(self.sandBoxPlacedList) == 0:
                levelText ="Level: %d" % self.levelNum
            elif len(self.sandBoxPlacedList) > 0:
                levelText = "Level: Custom"
            self.levelCount = self.level.render(levelText, False, (255, 255, 255))

            ###### from PygameNerd
            self.alph -= 2
            self.alphaSurface.set_alpha(self.alph)
            ######
    #draws everything in the sandbox screen
    def renderSandboxScreen(self, screen):
        self.spacing = 165
        currentX = 160
        for image in self.sandBoxImageList:
            planetImage = pygame.transform.scale(image, (100, 100))
            pygame.Surface.blit(screen, planetImage,(currentX, self.height - self.height * 0.2))
            currentX += self.spacing

        pygame.Surface.blit(screen, self.imageContainer.highlightSelection,
                            (self.hightlightSelectionCol * self.spacing - 17, self.height - self.height * 0.22))

        for placedImage in self.sandBoxPlacedList:
            pygame.Surface.blit(screen, self.sandBoxImageList[placedImage[2] - 1],
                                (placedImage[0] - 50, placedImage[1] - 50))

    # creates and moves tiles for scrolling background
    def tileBackground(self, screen):
        for tile in self.imageContainer.tileList:
            curRect = pygame.Rect((tile[0] + self.scrollX / 2, tile[1] + self.scrollY / 2),
                                   self.imageContainer.backgroundTileRect.size)

            distanceFromLeft = curRect.right
            distanceFromRight = curRect.left
            distanceFromTop = curRect.bottom
            distanceFromBottom = curRect.top

            if distanceFromLeft < 0:
                tile[0] += int(self.imageContainer.tileSize[0] * 4)

            elif distanceFromRight > self.width:
                tile[0] -= int(self.imageContainer.tileSize[0] * 4)

            if distanceFromTop < 0:
                tile[1] += int(self.imageContainer.tileSize[1] * 3)

            elif distanceFromBottom > self.height:
                tile[1] -= int(self.imageContainer.tileSize[1] * 3)

            else:
                pygame.Surface.blit(screen, self.imageContainer.backgroundTile,
                                    (curRect.topleft))

    def redrawAll(self, screen):

        if self.gameState == "startScreen":
            pygame.Surface.blit(screen, self.imageContainer.startScreen, (0, 0))

        elif self.gameState == "helpScreen":
            pygame.Surface.blit(screen, self.imageContainer.helpScreen, (0, 0))

        elif self.gameState == "gamePlay" or self.gameState == "gameOver" or self.gameState == "paused":
            self.tileBackground(screen)

            for bullet in self.bulletGroup:
                if bullet.source == "enemy":
                    color = (255, 0, 0)

                elif bullet.radius != 5:
                    r = random.randint(30, 200)
                    g = random.randint(30, 200)
                    b = random.randint(30, 200)
                    color = (r, g, b)
                else:
                    color = (0, 255, 255)
                pygame.draw.circle(screen, color, bullet.rect.center, bullet.radius)

            for enemy in self.enemyGroup:
                if enemy.rect.left < self.width and enemy.rect.right > 0 \
                and enemy.rect.top < self.height and enemy.rect.bottom > 0:
                    enemy.draw(screen)

            for planet in self.planetGroup:
                if planet.distanceFromTarget < self.width:
                    planet.draw(screen)

            self.playerGroup.draw(screen)

            self.healthBar.draw(screen)
            self.miniMap.draw(screen)

            pygame.Surface.blit(screen, self.playerScoreSurface, (self.width // 2 - self.fontSize, 0))
            pygame.Surface.blit(screen, self.levelCount, (0 + self.fontSize, self.height - self.fontSize * 2))

            if self.gameState == "gameOver":
                pygame.Surface.blit(screen, self.imageContainer.deathScreen,
                                    (0, 0))
            elif self.gameState == "paused":
                pygame.Surface.blit(screen, self.imageContainer.pauseScreen, (0, 0))

            if self.alph > 0:
                screen.blit(self.alphaSurface, (0, 0))

        elif self.gameState == "sandBox":
            self.tileBackground(screen)
            pygame.Surface.blit(screen, self.imageContainer.sandBoxScreen, (0, 0))
            self.renderSandboxScreen(screen)


    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''

        return self._keys.get(key, False)

    def __init__(self, width=600, height=400, fps=50, title="112 Pygame Game"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)
        pygame.init()

    def run(self):

        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        self.screen = screen
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        ####
        loadingScreen = pygame.image.load(
            "../images/screens/loading_screen.png").convert_alpha()
        loadingScreen = pygame.transform.scale(loadingScreen,
                                               (self.width, self.height))
        pygame.Surface.blit(self.screen, loadingScreen, (0, 0))
        pygame.display.flip()
        ####

        # call game-specific initialization
        self.init()

        self.playing = True
        while self.playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    self.playing = False
            screen.fill(self.bgColor)
            self.redrawAll(screen)

            pygame.display.flip()
        pygame.quit()

def main():
    game = PygameGame(1400, 700, 60, "Event Horizon")
    # window ratio must be 2:1
    game.run()

if __name__ == '__main__':
    main()
