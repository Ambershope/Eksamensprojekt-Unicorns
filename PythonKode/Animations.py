from Constants import *
import pygame
class Animation:
    def __init__(self, name: str, customVariable, size: int | float, center : tuple | list) -> None:
        self.size = int(size)
        self.name = name
        self.customVariable = customVariable
        
        if self.name == "ETB":
            self.maxTick = FPS*1

        elif self.name == "endGamePopUp":
            self.maxTick = FPS*8

        self.currentTick = 0

    def drawStep(self, surface: pygame.surface):
        match self.name:
            case "ETB": self.ETB(surface)
            case "heartCloud": self.heartCloud(surface)
            case "endGamePopUp": self.endGamePopUp(surface)

    def ETB(self, surface: pygame.surface):
        pass

    def heartCloud(self, surface: pygame.surface):
        if self.customVariable == "fadeToOpponent":
            pass
        elif self.customVariable == "fadeToYou":
            pass
    
    def endGamePopUp(self, surface: pygame.surface):
        if self.customVariable == "youWin":
            pass
        elif self.customVariable == "opponentWin":
            pass
        elif self.customVariable == "draw":
            pass

    def linearFadeOf(self):
        return int((self.maxTick/self.currentTick)*255)

    