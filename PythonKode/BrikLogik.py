import Database
import pygame
from Constants import GRID_BETWEEN_TILES , GRID_LENGTH_Y
class Piece:
    def __init__ (self, pieceId_, isYours_=True):
        cardData = Database.databaseCardFinder(pieceId_)[0]
        print(cardData)
        self.pieceName = cardData[1]
        print(self.pieceName)
        self.pieceName = pieceId_
        self.isYours=isYours_
        self.persuasion= [cardData[2], cardData[3], cardData[4], cardData[5]]
        self.artworkPath = Database.pathToGameDataFile("Visuals\PieceArtwork", cardData[6], ".png")
        self.artwork = pygame.image.load(self.artworkPath)
        self.effectFunctionId = cardData[7]
        self.explainingText = cardData[8]

class GameState:
    def __init__(self, field_, playerPile_):
        self.field=field_
        self.playerPile=playerPile_
        self.turnCycleStep=-2
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
    
if __name__ == "__main__":
    print(Piece(1).pieceName)
