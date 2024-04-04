import pygame
import Database
from Constants import *

class Grid:
    '''
    defines and calculates the size and location of the grid on a screen
    '''
    def __init__(self, screen):
        self.GRID_LENGTH_X=GRID_LENGTH_X
        self.GRID_LENGTH_Y=GRID_LENGTH_Y
        gridSizeX=screen.get_width()/GRID_LENGTH_X
        gridSizeY=screen.get_height()/GRID_LENGTH_Y
        self.gridSize=min(gridSizeX, gridSizeY)
        self.startX, self.startY = 0,0 

        if gridSizeX > gridSizeY:
            self.startX = (screen.get_width()-(self.gridSize*self.GRID_LENGTH_X))//2

        elif gridSizeY > gridSizeX:
            self.startY = ( screen.get_height()-(self.gridSize*self.GRID_LENGTH_Y))//2


    
    def getReal(self, gridCord=(0,0)):
        '''
        Turns a grid cordinate (0,0) into a real screen cordinate \nuses a tuple/list as input
        '''
        return ((gridCord[0] * self.gridSize + self.startX , gridCord[1] * self.gridSize + self.startY))
    
    def getGrid(self, realCord=(0,0)):
        return ((realCord[0]-self.startX)/self.gridSize,(realCord[1]-self.startY)/self.gridSize)
    
    def getRealLength(self, gridLength=(0,0)):
        return (gridLength[0]*self.gridSize, gridLength[1]*self.gridSize)
    

            


def mainMenuDraw(Input, screen, grid):
    '''
Draws the start screen\n
    '''
    frameCounter = Input.frameCounter
    brightness=abs(255-((frameCounter*3)%511))
    screen.fill((0,0,brightness))

def gamemodeScreenDraw(Input, screen, grid):
    '''
Draws the select gamemode screen\n
    '''
    frameCounter = Input.frameCounter
    brightness=abs(255-((frameCounter*3)%511))
    screen.fill((brightness,0,0))

def overlayDraw(Input, screen, grid):
    '''draws the overlay'''
    #breates the bruger meny that opens the overlay
    image=pygame.image.load(Database.pathToGameDataFile("Visuals\DevArt","ExitButton", ".png"))
    scaledImage=pygame.transform.scale(image, (grid.gridSize,grid.gridSize))
    screen.blit(scaledImage, grid.getReal((31, 0)))

    if Input.overlayOpen:
        #creates a dark seethroug layer that covers the entire screen
        alfaSurface=pygame.Surface((grid.gridSize*GRID_LENGTH_X,grid.gridSize*GRID_LENGTH_Y))
        alfaSurface.set_alpha(128)
        alfaSurface.fill((0,0,0))
        screen.blit(alfaSurface, grid.getReal((0,0)))

        #creates the underlying box for the options full screen overlay
        pygame.draw.rect(screen, (255,255,255), (grid.getReal((10,4)),grid.getReal((GRID_LENGTH_X-20,GRID_LENGTH_Y-8))), border_radius=round(grid.gridSize*0.5))

        #creates the quit game button
        image=pygame.image.load(Database.pathToGameDataFile("Visuals\DevArt","ExitButton", ".png"))
        scaledImage=pygame.transform.scale(image, (grid.gridSize*8,grid.gridSize*1))
        screen.blit(scaledImage, grid.getReal((12, 12)))
    

def drawStartScreen(screen):
    '''
Draws the start screen\n
    '''
    screen.fill((200,200,200))


def drawGame(Input, screen, grid, gameState):
    '''
Draws the game\n
    '''
    frameCounter = Input.frameCounter
    brightness=abs(255-((frameCounter*3)%511))
    screen.fill((0,brightness,0))


    #draw field base
    pygame.draw.rect(screen, (255, 192, 203), (grid.getReal((7,0)),grid.getRealLength((18,18))))

    #draw field base tiles
    tile0ImgUnscaled=pygame.image.load(Database.pathToGameDataFile("Visuals\DevArt", "TileNotPlaceble", ".png"))
    tile0Img=pygame.transform.scale( tile0ImgUnscaled, (gameState.tileSize*grid.gridSize,gameState.tileSize*grid.gridSize))
    tile1ImgUnscaled=pygame.image.load(Database.pathToGameDataFile("Visuals\DevArt", "TilePlaceble", ".png"))
    tile1Img=pygame.transform.scale( tile1ImgUnscaled, (gameState.tileSize*grid.gridSize,gameState.tileSize*grid.gridSize))

    for xField in range (gameState.field.fieldSize):
        xGrid=(xField*gameState.tileSize)+7+((xField+1)*GRID_BETWEEN_TILES)

        for yField in range (gameState.field.fieldSize):
            yGrid=(yField*gameState.tileSize)+((yField+1)*GRID_BETWEEN_TILES)

            curentTileValue=gameState.field.tileField[xField][yField]

            if curentTileValue==0:
                screen.blit(tile0Img, grid.getReal((xGrid, yGrid)))
            else:
                screen.blit(tile1Img, grid.getReal((xGrid, yGrid)))
                
            


    GRID_BETWEEN_TILES
    




def border(screen, grid):
    '''
draws the border around the grid
    '''
    if grid.startY != 0:
        pygame.draw.rect(screen, BORDER_COLOR, ((0,0),grid.getReal((GRID_LENGTH_X,0))))
        pygame.draw.rect(screen, BORDER_COLOR, (grid.getReal((0,GRID_LENGTH_Y)),(screen.get_width(), screen.get_height())))
        
    if grid.startX !=0:
        pygame.draw.rect(screen, BORDER_COLOR, ((0,0),grid.getReal((0,GRID_LENGTH_Y))))
        pygame.draw.rect(screen, BORDER_COLOR, (grid.getReal((GRID_LENGTH_X,0)),(screen.get_width(), screen.get_height())))

def DEVTOOLdrawGrid(screen, grid):
    '''
draws the underlying visual grid for development use, toggel with g at the time of writing
    '''
    for y in range (GRID_LENGTH_Y+1):
        pygame.draw.line(screen, "black", grid.getReal((0,y)), grid.getReal((GRID_LENGTH_X,y)), 1)
    for x in range (GRID_LENGTH_X+1):
        pygame.draw.line(screen, "black", grid.getReal((x,0)), grid.getReal((x,GRID_LENGTH_Y)), 1)
