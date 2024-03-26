import pygame



def mainMenuDraw(Input, screen):
    '''
Draws the start screen\n
    '''
    frameCounter = Input.frameCounter
    brightness=abs(255-((frameCounter*3)%511))
    screen.fill((0,0,brightness))

def gamemodeScreenDraw(Input, screen):
    '''
Draws the select gamemode screen\n
    '''
    frameCounter = Input.frameCounter
    brightness=abs(255-((frameCounter*3)%511))
    screen.fill((brightness,0,0))

def overlayDraw(Input, screen):
    '''draws the overlay'''
    pass

def drawStartScreen(screen):
    '''
Draws the start screen\n
    '''

    screen.fill((200,200,200))


def drawGame(Input, screen):
    '''
Draws the game\n
    '''
    frameCounter = Input.frameCounter
    brightness=abs(255-((frameCounter*3)%511))
    screen.fill((0,brightness,0))