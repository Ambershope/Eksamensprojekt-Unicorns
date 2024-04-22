import Database
from GameObjects import Field
from Visuals import Grid
import pygame
from Constants import *

def tvearVektor(v:tuple | list):
    return (-v[1],v[0])

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
    
    def SelectPiece(self):
        '''
        
        '''
        return

    def isPlacable(self):
        tileMousedOver = Grid.getGrid(pygame.mouse.get_pos())
        if Field.pieceField[tileMousedOver] == 0:
            return True
        else:
            return False
        

    
class Piece:
    def __init__ (self, pieceId_, isYours_=True):
        cardData = Database.databaseCardFinder('pieces','pieceId',pieceId_)[0]
        print(cardData)
        self.pieceName = cardData[1]
        print(self.pieceName)
        self.pieceId = pieceId_
        self.isYours = isYours_
        self.persuasion = [cardData[2], cardData[3], cardData[4], cardData[5]] #N E S W
        self.artworkPath = Database.pathToGameDataFile("Visuals\PieceArtwork", cardData[6], ".png")
        self.artwork = pygame.image.load(self.artworkPath)
        self.effectFunctionId = cardData[7]
        self.flavorText = cardData[8]
        self.calculatePowerArrowSurface()

    def __str__ (self):
        return str(self.pieceId)
    
    def calculatePowerArrowSurface(self):
        triangleColor = LUKEWARM_PINK
        triangleSize = 16*4
        spaceBetweenTriangles= 16
        pieceSize = 64*8
        edgeSize = pieceSize//20
        overlapSize = pieceSize // 32
        surfaceSize=pieceSize+((edgeSize+overlapSize)*2)
        self.powerArrowSurface = pygame.surface.Surface((surfaceSize,surfaceSize), pygame.SRCALPHA)
        pieceCenterX , pieceCenterY = surfaceSize // 2, surfaceSize // 2
        edgeCenterY = -(0.5*(pieceSize+edgeSize))
        edgeCenterX = 0
        self.listOfAllTriangles=[]
 
        for direction in range (len(self.persuasion)):
            power = self.persuasion[direction]

            for triangle in range (power):
                triangleCenterX=spaceBetweenTriangles*triangle+((triangle+0.5)*triangleSize) - (((power*triangleSize)+((power-1)*spaceBetweenTriangles))*0.5)
                triangleCords = []

                for point in range (3):    
                    if point == 2:
                        pointY= - overlapSize - (edgeSize*0.5)
                        pointX= 0
                    else:
                        pointY= overlapSize + (edgeSize*0.5)
                        pointX= (triangleSize * (point-0.5))

                    currentPoint = (pointX+triangleCenterX+edgeCenterX, pointY+edgeCenterY)
                    for i in range (direction):
                        currentPoint = tvearVektor(currentPoint)

                    triangleCords.append((currentPoint[0]+pieceCenterX, currentPoint[1]+pieceCenterY))

                self.listOfAllTriangles.append(tuple(triangleCords))
            
        for tri in self.listOfAllTriangles:
            pygame.draw.polygon(self.powerArrowSurface, triangleColor, tri)
            pygame.draw.polygon(self.powerArrowSurface, "black", tri, 4)
            

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

        scaledTriangels=pygame.transform.scale(self.powerArrowSurface,(realSize+realSize//16,realSize+realSize//16))
        gameScreen.blit(scaledTriangels, (realCords[0]-realSize//32,realCords[1]-realSize//32))


if __name__ == "__main__":
    print(Piece(1).pieceName)