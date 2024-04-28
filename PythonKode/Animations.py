from Constants import *
import pygame
from Database import pathToGameDataFile
import random
import math
class Animation:
    def __init__(self, name: str, customVariable, size: int | float, gridCenter : tuple | list) -> None:
        self.size = int(size)
        self.name = name
        self.customVariable = customVariable
        self.gridCenter = gridCenter
        self.currentTick = 1



        if self.name == "ETB":
            self.maxTick = FPS*3
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
            self.maxTick = int(FPS*4)

            self.startHeart = pygame.image.load(pathToGameDataFile("Visuals\DevArt", "Heart", ".png")).convert_alpha() #it ryhmes lol
            self.inbetweenHeart = pygame.image.load(pathToGameDataFile("Visuals\DevArt", "Heart_purpel", ".png")).convert_alpha()
            self.endHeart =  pygame.image.load(pathToGameDataFile("Visuals\DevArt", "Heart_red", ".png")).convert_alpha()
            if self.customVariable == "fadeToYou":
                self.startHeart, self.endHeart = self.endHeart, self.startHeart

            self.heartInfo=[]
            for i in range (32):
                offset=(random.uniform(0.0, 1.0), random.uniform(0.0, 1.0))
                direction = (1/(0.5-offset[0])*0.2, 1/(0.5-offset[1])*0.2)
                self.heartInfo.append((offset, direction)) 
                                        

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
        modifier, type = self.heartSizeAndType()
        if type == 0:
            heart = self.startHeart
        elif type == 1:
            heart = self.inbetweenHeart
        elif type == 2:
            heart = self.endHeart
        else:
            return False
        
        heartScaled=pygame.transform.scale(heart, grid.getRealLen((self.size*modifier, self.size*modifier)))
        for heartInf in self.heartInfo:
            
            cordsLeftCorner=(grid.getRealLen(heartInf[0][0]*self.size) - heartScaled.get_width()*0.5  + (grid.getReal(self.gridCenter)[0]-grid.getRealLen(self.size*0.5)) + grid.getRealLen(heartInf[1][0]*self.currentTick/self.maxTick),
                             grid.getRealLen(heartInf[0][1]*self.size) - heartScaled.get_height()*0.5 + (grid.getReal(self.gridCenter)[1]-grid.getRealLen(self.size*0.5)) + grid.getRealLen(heartInf[1][1]*self.currentTick/self.maxTick))
            surface.blit(heartScaled, cordsLeftCorner)
            surface.blit(heartScaled, cordsLeftCorner)
            surface.blit(heartScaled, cordsLeftCorner)

    
    def endGamePopUp(self, surface: pygame.surface, grid):
        if self.scaledImage:
            surface.blit(self.scaledImage, grid.getReal((self.gridCenter[0]-(self.size*self.relation*0.5), self.gridCenter[1]-(self.size*0.5))))
        else:
            self.scaledImage = pygame.transform.scale(self.image, grid.getRealLen((self.size*self.relation, self.size)))
        

    def linearFadeOf(self):
        return int(self.currentTick*(255/self.maxTick))
    
    def heartSizeAndType(self):
        type = self.currentTick//(self.maxTick/3)
        sizeMin, sizeMax = 0.2, 0.3
        if type >=2:
            sizeMin = 0
        size = (sizeMax-sizeMin)*1/(self.currentTick%(self.maxTick/3)+1) + sizeMin 
        return (size, type) 
    
    def isOver(self):
        if self.currentTick > self.maxTick:    
            return True
        else: 
            return False



    