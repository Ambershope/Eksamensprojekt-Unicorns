from Constants import *
import pygame
from Database import pathToGameDataFile
class Animation:
    def __init__(self, name: str, customVariable, size: int | float, gridCenter : tuple | list) -> None:
        self.size = int(size)
        self.name = name
        self.customVariable = customVariable
        
        if self.name == "ETB":
            self.maxTick = FPS*1

        elif self.name == "endGamePopUp":
            self.maxTick = FPS*8
        elif self.name == "heartCloud":
            self.maxTick = int(FPS*1.5)
        self.currentTick = 0

    def drawStep(self, surface: pygame.surface, grid):
        match self.name:
            case "ETB": self.ETB(surface, grid)
            case "heartCloud": self.heartCloud(surface, grid)
            case "endGamePopUp": self.endGamePopUp(surface, grid)

    def ETB(self, surface: pygame.surface, grid):
        pass

    def heartCloud(self, surface: pygame.surface, grid):
        if self.customVariable == "fadeToOpponent":
            pass
        elif self.customVariable == "fadeToYou":
            pass
    
    def endGamePopUp(self, surface: pygame.surface, grid):
        if self.customVariable == "youWin":
            image=pygame.image.load(pathToGameDataFile("Visuals\DevArt", "WinImage", ".png")).convert_alpha()
        elif self.customVariable == "opponentWin":
            image=pygame.image.load(pathToGameDataFile("Visuals\DevArt", "LoseImage", ".png")).convert_alpha()
        elif self.customVariable == "draw":
            image=pygame.image.load(pathToGameDataFile("Visuals\DevArt", "DrawImage", ".png")).convert_alpha()
        height, width=image.get_size()
        relation = width/height
        
        scaledImage = pygame.transform.scale(image, grid.getRealLen((self.size, self.size*relation))))


    def linearFadeOf(self):
        return int((self.maxTick/self.currentTick)*255)

    