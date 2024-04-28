from Constants import *
import pygame
from Database import pathToGameDataFile
import random
class Animation:
    def __init__(self, name: str, customVariable, size: int | float, gridCenter : tuple | list) -> None:
        self.size = int(size)
        self.name = name
        self.customVariable = customVariable
        self.gridCenter = gridCenter
        if self.name == "ETB":
            self.maxTick = FPS*1

        elif self.name == "endGamePopUp":
            self.maxTick = FPS*8
        elif self.name == "heartCloud":
            self.maxTick = int(FPS*1.5)
        self.currentTick = 1

    def drawStep(self, surface: pygame.surface, grid):
        match self.name:
            case "ETB": self.ETB(surface, grid)
            case "heartCloud": self.heartCloud(surface, grid)
            case "endGamePopUp": self.endGamePopUp(surface, grid)

        self.currentTick += 1

    def ETB(self, surface: pygame.surface, grid):
        circleMoveAmmountMax=0.2
        circleRadius = grid.getRealLen(self.size)*0.125
        colorThisTick = (0,0,255, self.linearFadeOf()) 
        if self.currentTick == 1:
            for i in range (16):
                self.customVariable.append((random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)),(random.uniform(-circleMoveAmmountMax, circleMoveAmmountMax), random.uniform(-circleMoveAmmountMax, circleMoveAmmountMax)))
        for circleInfo in self.customVariable:
            pygame.draw.circle(surface, colorThisTick, (   (grid.getReal(self.gridCenter)[0] + (circleInfo[0][0] + (circleInfo[1][0] * self.currentTick / self.maxTick) )*self.size*0.5),     
                                                           (grid.getReal(self.gridCenter)[1] + (circleInfo[0][1] + (circleInfo[1][1] * self.currentTick / self.maxTick) )*self.size*0.5)), 
                                                           circleRadius)

    

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

        scaledImage = pygame.transform.scale(image, grid.getRealLen((self.size, self.size*relation)))
        surface.blit(scaledImage, grid.getReal((self.gridCenter[0]-(self.size*0.5), self.gridCenter[1]-(self.size*relation*0.5))))

    def linearFadeOf(self):
        return int((self.currentTick/self.maxTick)*255)
    
    def ETBalfa(self):
        if self.currentTick >= self.maxTick/10*8:
            return (1/self.currentTick)*255
        else: return ((1/self.currentTick)*255)*1/abs(self.currentTick-self.maxTick)
    
    def isOver(self):
        if self.currentTick > self.maxTick:    
            return True
        else: 
            return False



    