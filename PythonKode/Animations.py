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
        self.currentTick = 1



        if self.name == "ETB":
            self.maxTick = FPS*1.5
            circleMoveAmmountMax=0.2
            self.circleInfo = []
            if self.customVariable:
                self.color = pygame.color.Color(YOUR_COLOR)
            else:
                self.color = pygame.color.Color(OPPONENT_COLOR)
            for i in range (24):
                self.circleInfo.append(((random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)),(random.uniform(-circleMoveAmmountMax, circleMoveAmmountMax), random.uniform(-circleMoveAmmountMax, circleMoveAmmountMax))))

        elif self.name == "endGamePopUp":
            self.maxTick = FPS*8
            if self.customVariable == "youWin":
                self.image=pygame.image.load(pathToGameDataFile("Visuals\DevArt", "WinImage", ".png")).convert_alpha()
            elif self.customVariable == "opponentWin":
                self.image=pygame.image.load(pathToGameDataFile("Visuals\DevArt", "LoseImage", ".png")).convert_alpha()
            elif self.customVariable == "draw":
                self.image=pygame.image.load(pathToGameDataFile("Visuals\DevArt", "DrawImage", ".png")).convert_alpha()
            width, height=self.image.get_size()
            self.relation = width/height
            self.scaledImage = 0

        elif self.name == "heartCloud":
            self.maxTick = int(FPS*2)

    def drawMe(self, surface: pygame.surface, grid):
        match self.name:
            case "ETB": self.ETB(surface, grid)
            case "heartCloud": self.heartCloud(surface, grid)
            case "endGamePopUp": self.endGamePopUp(surface, grid)

        self.currentTick += 1

    def ETB(self, surface: pygame.surface, grid):
        
        circleRadius = grid.getRealLen(self.size)*0.125
        self.color.a = self.linearFadeOf()
            
        intermediateSurface= pygame.surface.Surface(surface.get_size(), pygame.SRCALPHA)
        for circle in self.circleInfo:
            pygame.draw.circle(intermediateSurface, self.color, (   (grid.getReal(self.gridCenter)[0] + (circle[0][0] + (circle[1][0] * self.currentTick / self.maxTick) )*grid.getRealLen(self.size)*0.5),     
                                                                       (grid.getReal(self.gridCenter)[1] + (circle[0][1] + (circle[1][1] * self.currentTick / self.maxTick) )*grid.getRealLen(self.size)*0.5)), 
                                                                    circleRadius)
        surface.blit(intermediateSurface, (0,0))

    def heartCloud(self, surface: pygame.surface, grid):
        if self.customVariable == "fadeToOpponent":
            pass
        elif self.customVariable == "fadeToYou":
            pass
    
    def endGamePopUp(self, surface: pygame.surface, grid):
        if self.scaledImage:
            surface.blit(self.scaledImage, grid.getReal((self.gridCenter[0]-(self.size*self.relation*0.5), self.gridCenter[1]-(self.size*0.5))))
        else:
            self.scaledImage = pygame.transform.scale(self.image, grid.getRealLen((self.size*self.relation, self.size)))
        

    def linearFadeOf(self):
        return int((self.maxTick/self.currentTick)*(255/self.maxTick))
    
    def ETBalfa(self):
        if self.currentTick >= self.maxTick/10*8:
            return (1/self.currentTick)*255
        else: return ((1/self.currentTick)*255)*1/abs(self.currentTick-self.maxTick)
    
    def isOver(self):
        if self.currentTick > self.maxTick:    
            return True
        else: 
            return False



    