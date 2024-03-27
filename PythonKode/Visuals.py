import pygame
import Database
from Constants import *

class Grid:
    def __init__(self, screen):
        self.GRID_LENGTH_X=GRID_LENGTH_X
        self.GRID_LENGTH_Y=GRID_LENGTH_Y
        gridSizeX=screen.get_width()/GRID_LENGTH_X
        gridSizeY=screen.get_height()/GRID_LENGTH_Y
        print(gridSizeX, gridSizeY)
        self.gridSize=min(gridSizeX, gridSizeY)
        self.startX, self.startY = 0,0 

        if gridSizeX > gridSizeY:
            self.startX = ((self.gridSize*GRID_LENGTH_X) - screen.get_width())

        elif gridSizeY > gridSizeX:
            self.startY = ((self.gridSize*GRID_LENGTH_Y) - screen.get_height())


    
    def getReal(self, gridCord=(0,0)):
        '''
        Turns a grid cordinate (0,0) into a real screen cordinate \nuses a tuple/list as input
        '''
        return ((gridCord[0] * self.gridSize + self.startX , gridCord[1] * self.gridSize + self.startY))
            


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
    image=pygame.image.load(Database.pathToGameDataFile("Visuals\DevArt","ExitButton", ".png"))
    screen.blit(image, grid.getReal((31, 0)))

    if grid.startY != 0:
        pygame.draw.rect(screen, "pink", ((0,0),grid.getReal((GRID_LENGTH_X,0))))
        #pygame.draw.rect(screen, "pink", (grid.getReal((0,GRID_LENGTH_Y)),(screen.get_width(), screen.get_height())))
        
    elif grid.startX !=0:
        pygame.draw.rect(screen, "pink", ((0,0),grid.getReal((0,GRID_LENGTH_Y))))
        pygame.draw.rect(screen, "pink", (grid.getReal((GRID_LENGTH_X,0)),(screen.get_width(), screen.get_height())))

    

def drawStartScreen(screen):
    '''
Draws the start screen\n
    '''

    screen.fill((200,200,200))


def drawGame(Input, screen, grid):
    '''
Draws the game\n
    '''
    frameCounter = Input.frameCounter
    brightness=abs(255-((frameCounter*3)%511))
    screen.fill((0,brightness,0))

def DEVTOOLdrawGrid(screen, grid):
    for y in range (GRID_LENGTH_Y+1):
        pygame.draw.line(screen, "black", grid.getReal((0,y)), grid.getReal((GRID_LENGTH_X,y)), 1)
    for x in range (GRID_LENGTH_X+1):
        pygame.draw.line(screen, "black", grid.getReal((x,0)), grid.getReal((x,GRID_LENGTH_Y)), 1)
