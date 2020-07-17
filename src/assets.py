# Carlos Armendariz
# andrew id: carmenda

import pygame
pygame.mixer.init()
"""
This file contains an object that loads and
stores all the images and sounds required for
the game when an instance is created.
"""

class Image(object):
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.imageDirectory = "../images/"
        self.loadEntityImages()
        self.loadHudImages()
        self.loadPlanetImages()
        self.loadScreens()
        self.loadBackGround()

    def loadEntityImages(self):

        astronautHeight = 50
        self.astronautImage = pygame.image.load(
            self.imageDirectory + "player_image.png").convert_alpha()
        self.astronautImage = pygame.transform.scale(self.astronautImage, (int(astronautHeight * 0.8), astronautHeight))

        self.dynamicShipImage = pygame.image.load(
            self.imageDirectory + "player_ship.png").convert_alpha()
        self.dynamicShipImage = pygame.transform.scale(self.dynamicShipImage,
                                                       (astronautHeight * 2, astronautHeight * 2))
        self.staticShipImage = pygame.image.load(
            self.imageDirectory + "player_dynamic_ship.png").convert_alpha()
        self.staticShipImage = pygame.transform.scale(self.staticShipImage,
                                                      (astronautHeight * 2, astronautHeight * 2))
        self.playerImage = self.astronautImage

        self.enemyImage = pygame.image.load(
            self.imageDirectory + "enemy/enemy_static.png").convert_alpha()
        self.dynamicEnemyImage = pygame.image.load(
            self.imageDirectory + "enemy/enemy_moving.png").convert_alpha()

        self.enemyImage = pygame.transform.scale(self.enemyImage, (astronautHeight * 2, astronautHeight * 2))
        self.dynamicEnemyImage = pygame.transform.scale(self.dynamicEnemyImage, (astronautHeight * 2, astronautHeight * 2))

    def loadPlanetImages(self):
        self.planetImageDict = dict()

        self.sunImage = pygame.image.load(self.imageDirectory + "planets/sun.png").convert_alpha()
        self.blackHoleImage = pygame.image.load(self.imageDirectory + "planets/black_hole.png").convert_alpha()

        planetList = ["planets/earth.png",
                      "planets/green_planet.png",
                      "planets/purple_planet.png",
                      "planets/blue_planet.png",
                      "planets/red_planet.png"]

        for imageIndex in range(len(planetList)):
            newImage = pygame.image.load(self.imageDirectory + planetList[imageIndex]).convert_alpha()
            self.planetImageDict[imageIndex] = newImage

    def loadHudImages(self):
        healthBarList = [
            "health_bar/health-empty.png",
            "health_bar/health-5.png",
            "health_bar/health-4.png",
            "health_bar/health-3.png",
            "health_bar/health-2.png",
            "health_bar/health-1.png",
            "health_bar/health_full.png"]

        self.healthBarDict = dict()

        for imageIndex in range(len(healthBarList)):
            newImage = pygame.image.load(
                self.imageDirectory + healthBarList[imageIndex]).convert_alpha()
            newImage = pygame.transform.scale(newImage, (400, 80))
            self.healthBarDict[imageIndex] = newImage

        self.highlightSelection = pygame.image.load(
            self.imageDirectory + "highlight_selection.png")

    def loadScreens(self):
        self.startScreen = pygame.image.load(
            self.imageDirectory + "screens/start_screen.png").convert_alpha()
        self.startScreen = pygame.transform.scale(self.startScreen,
                                                  (self.width, self.height))

        self.deathScreen = pygame.image.load(
            self.imageDirectory + "screens/death_screen.png").convert_alpha()
        self.deathScreen = pygame.transform.scale(self.deathScreen,
                                                  (self.width, self.height))

        self.pauseScreen = pygame.image.load(
            self.imageDirectory + "screens/pause_screen.png").convert_alpha()
        self.pauseScreen = pygame.transform.scale(self.pauseScreen,
                                                  (self.width, self.height))

        self.helpScreen =pygame.image.load(
            self.imageDirectory + "screens/help_screen.png").convert_alpha()
        self.helpScreen = pygame.transform.scale(self.helpScreen,
                                                  (self.width, self.height))

        self.sandBoxScreen = pygame.image.load(
            self.imageDirectory + "screens/sand_box_screen.png").convert_alpha()
        self.sandBoxScreen = pygame.transform.scale(self.sandBoxScreen,
                                                 (self.width, self.height))

    def loadBackGround(self):
        self.backgroundTile = pygame.image.load(
          self.imageDirectory + "screens/universe_background.png").convert_alpha()

        self.tileSize = (int(self.width / 3), int(self.height))
        self.backgroundTile = pygame.transform.scale(self.backgroundTile,
                                                 self.tileSize)

        self.backgroundTileRect = self.backgroundTile.get_rect()

        self.tileList = []
        for row in range(3):
            for col in range(4):
                currX = (col * self.tileSize[0] - self.tileSize[0])
                currY = (row * self.tileSize[1] - self.tileSize[1])
                self.tileList.append([currX, currY])

class Audio(object):

    def __init__(self):
        self.audioDirectory = "../audio/"


        self.dramaticSound = pygame.mixer.Sound(self.audioDirectory + "black_hole_forming.wav")
        self.bulletSound = pygame.mixer.Sound(self.audioDirectory + "large_laser.wav")
        self.laserSound = pygame.mixer.Sound(self.audioDirectory + "laser_sound.wav")
        self.playerLaserSound = pygame.mixer.Sound(self.audioDirectory + "laser_sound.wav")
        self.introMusic = pygame.mixer.Sound(self.audioDirectory + "intro_screen.wav")
        self.crashSound = pygame.mixer.Sound(self.audioDirectory + "crash_sound.wav")
        pygame.mixer.music.load(self.audioDirectory + "/Motivated.wav")
