import Database
from GameObjects import Field
import pygame
from Constants import *

def tvearVektor(v:tuple | list):
    '''
    finder tværvektoren til en given vektor
    '''
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
        self.holdingPiece = 0
        self.newestPiece = (-1,-1)
        
        self.tileSize = (GRID_LENGTH_Y-1-((self.field.fieldSize-1)*GRID_BETWEEN_TILES))/self.field.fieldSize
        
    def newTurnStep(self):
        '''
        increments the turnCycleStep by 1
        '''
        if self.turnCycleStep >= len(self.turnCycleTable)-1:
            self.turnCycleStep = 0
        else:
            self.turnCycleStep += 1
        return self.turnCycleStep
    
    
    def placePiece(self, fieldPosition : list | tuple):
        '''
        places the held piece on the specified field position,
        also updates newestPiece 
        '''
        self.field.pieceField[fieldPosition[0]][fieldPosition[1]] = self.holdingPiece
        self.holdingPiece = 0
        self.newestPiece=fieldPosition

    def fillHand(self):
        '''
        fills the players hand by drawing cards from the deck
        '''
        for i in range (len(self.hand)):
            if self.hand[i] == 0:
                self.hand[i] = Piece(self.playerPile.drawPiece())

    
class Piece:
    def __init__ (self, pieceId_, isYours_=True):
        cardData = Database.databaseCardFinder('pieces','pieceId',pieceId_)[0]
        #print(cardData)
        self.pieceName = cardData[1]
        #print(self.pieceName)
        self.pieceId = pieceId_
        self.isYours = isYours_
        self.persuasion = [cardData[2], cardData[5], cardData[4], cardData[3]] #N W S E
        self.artworkPath = Database.pathToGameDataFile("Visuals\PieceArtwork", cardData[6], ".png")
        self.artwork = pygame.image.load(self.artworkPath)
        self.Border = pygame.image.load(Database.pathToGameDataFile("Visuals/DevArt", "HeartsBorder_Grey", ".png")).convert_alpha()
        self.hueBorderAlly = pygame.image.load(Database.pathToGameDataFile("Visuals/DevArt", "HeartsBorder_Blue_Turquise", ".png")).convert_alpha()
        self.hueBorderOpponent = pygame.image.load(Database.pathToGameDataFile("Visuals/DevArt", "HeartsBorder_Red_Green", ".png")).convert_alpha()
        self.effectId = cardData[7]
        self.flavorText = cardData[8]
        self.calculatePowerArrowSurface()

        if self.effectId == 3:
            self.persuasionRange = 2
        else:
            self.persuasionRange = 1


    def __str__ (self):
        return str(self.pieceId)
    
    def calculatePowerArrowSurface(self):
        '''
        Calculates the persuasion displaying triangles.\n 
        It dose so by make-ing a surface, and stores it, so it can be displayed each turn, by drawMe().\n
        If persuasion is updated, update this
        '''
        #constants that can be changed
        triangleColor = LUKEWARM_PINK
        triangleSize = 16*4
        spaceBetweenTriangles= 16
        pieceSize = 64*8
        overlapSize = pieceSize // 32

        #constants that shouldent be changed
        edgeSize = pieceSize//20
        surfaceSize=pieceSize+((edgeSize+overlapSize)*2)

        self.powerArrowSurface = pygame.surface.Surface((surfaceSize,surfaceSize), pygame.SRCALPHA)
        pieceCenterX , pieceCenterY = surfaceSize // 2, surfaceSize // 2
        '''the rest of the coordinates are relative, compared to the previous cordinate
        edgecenter is relative to piece center
        triangle center is relative to the edge center
        the points on the triangles are relative to the triangle center
        
        this makes it possible to find each points position relative to the center, and rotate them aroud it
        '''
        edgeCenterY = -(0.5*(pieceSize+edgeSize))
        edgeCenterX = 0

        #actually calculete the triangles
        self.listOfAllTriangles=[]
        #for each direction find the number of triangles needed
        for direction in range (len(self.persuasion)):
            power = self.persuasion[direction]

            for triangle in range (power):
                #for each triangle calculate the center
                triangleCenterX = spaceBetweenTriangles*triangle+((triangle+0.5)*triangleSize) - (((power*triangleSize)+((power-1)*spaceBetweenTriangles))*0.5)
                triangleCenterY = 0
                triangleCords = []

                for point in range (3):  
                    #for each corner on the triangle calculate the position relative to the TRIANGLEcenter 
                    if point == 2:
                        pointY= - overlapSize - (edgeSize*0.5)
                        pointX= 0
                    else:
                        pointY= overlapSize + (edgeSize*0.5)
                        pointX= (triangleSize * (point-0.5))
                    
                    #finds the triangle corner relative to the center of the piece
                    currentPoint = (pointX+triangleCenterX+edgeCenterX, pointY+triangleCenterY+edgeCenterY)

                    #rotates the triangle aroud the piece center so its pointing in the right direction 
                    for i in range (direction):
                        currentPoint = tvearVektor(currentPoint)

                    triangleCords.append((currentPoint[0]+pieceCenterX, currentPoint[1]+pieceCenterY))
                
                #adds the triangle to the list of triangles
                self.listOfAllTriangles.append(tuple(triangleCords))
        
        #draw the triangles
        for tri in self.listOfAllTriangles:
            #draw center color
            pygame.draw.polygon(self.powerArrowSurface, triangleColor, tri)
            #draw edge
            pygame.draw.polygon(self.powerArrowSurface, "black", tri, 4)
    
    def drawMe(self, gameScreen:pygame.Surface, realCords:tuple, realSize:float|int, neutralBorder:bool = False):
        '''
        draws the piece on the given surface
        '''
        #draws the artwork
        scaledArt=pygame.transform.scale(self.artwork,(realSize,realSize))
        
        #Decides the color of the border
        if neutralBorder:
            border = self.Border
        elif self.isYours:
            border = self.hueBorderAlly
        else:
            border = self.hueBorderOpponent

        border = pygame.transform.scale(border, (realSize, realSize))
        scaledArt.blit(border, (0, 0))
        gameScreen.blit(scaledArt, realCords)
        
        

        scaledTriangels=pygame.transform.scale(self.powerArrowSurface,(realSize+realSize//16,realSize+realSize//16))
        gameScreen.blit(scaledTriangels, (realCords[0]-realSize//32,realCords[1]-realSize//32))


if __name__ == "__main__":
    print(Piece(1).pieceName)