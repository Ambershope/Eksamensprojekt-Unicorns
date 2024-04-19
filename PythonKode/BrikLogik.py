import Database
import pygame
from Constants import *


class GameState:
    def __init__(self, field_, playerPile_):
        self.field=field_
        self.playerPile=playerPile_
        self.turnCycleStep=-2
        self.hand=[0,0,0,0,0]
        self.startCycle=["Draw Start Hands", "Select First Player"]
        self.turnCycleTable=["You Select Piece", "You Select Tile", "Send To Opponent", "Piece ETB (A)", "Test Win(A)", "Draw Card", 
                             "Wait For Opponent", "Piece ETB (B)", "Test Win (B)"]
        
        self.tileSize = (GRID_LENGTH_Y-1-((self.field.fieldSize-1)*GRID_BETWEEN_TILES))/self.field.fieldSize
        
    def newTurnStep(self):
        if self.turnCycleStep >= len(self.turnCycleTable)+1:
            self.turnCycleStep = 0
        else:
            self.turnCycleStep += 1
        return self.turnCycleStep
    def fillHand(self):
        for i in range (len(self.hand)):
            if self.hand[i] == 0:
                self.hand[i] = Piece(self.playerPile.drawPiece())

    
class Piece:
    def __init__ (self, pieceId_, isYours_=True):
        cardData = Database.databaseCardFinder('pieces','pieceId',pieceId_)[0]
        print(cardData)
        self.pieceName = cardData[1]
        print(self.pieceName)
        self.pieceId = pieceId_
        self.isYours=isYours_
        self.persuasion= [cardData[2], cardData[3], cardData[4], cardData[5]]
        self.artworkPath = Database.pathToGameDataFile("Visuals\PieceArtwork", cardData[6], ".png")
        self.artwork = pygame.image.load(self.artworkPath)
        self.effectFunctionId = cardData[7]
        self.flavorText = cardData[8]

    def __str__ (self):
        return str(self.pieceId)
    
    def placeOnField(self, gameState:GameState ,fieldPosition:tuple):
        gameState.field.pieceField[fieldPosition[0]][fieldPosition[1]]=self
        return gameState
    
    def drawMe(self, gameScreen:pygame.Surface, realCords:tuple, realSize:float|int, neutralBorder:bool = False):
        #draws the artwork
        scaledArt=pygame.transform.scale(self.artwork,(realSize,realSize))
        gameScreen.blit(scaledArt, realCords)
        
        #Decides the color of the border
        if neutralBorder:
            borderColor = NEUTRAL_COLOR
        elif self.isYours:
            borderColor = YOUR_COLOR
        else:
            borderColor = OPPONENT_COLOR
        #draws the border
        pygame.draw.rect(gameScreen, borderColor, (realCords, (int(realSize), int(realSize))),int(realSize/20))


if __name__ == "__main__":
    print(Piece(1).pieceName)
