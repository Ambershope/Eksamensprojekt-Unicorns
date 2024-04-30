import pygame


class ButtonDetection:
    def __init__(self):
        self.mousePosition = [0,0]


    def buttonCollisionTest(self, cornorButtonPositionA: tuple, cornorButtonPositionB: tuple, useUserMouse = True):
        if useUserMouse == True:
            mousePosition = pygame.mouse.get_pos()
    
        if mousePosition[0] >= min(cornorButtonPositionA[0], cornorButtonPositionB[0]) and mousePosition[0] <= max(cornorButtonPositionA[0], cornorButtonPositionB[0]):
            if mousePosition[1] >= min(cornorButtonPositionA[1], cornorButtonPositionB[1]) and mousePosition[1] <= max(cornorButtonPositionA[1], cornorButtonPositionB[1]):
                return True
        return False


    def knap(self,input, CornerA: tuple, CornerB: tuple, ReturnValue: bool = True):
        if input.mouseLeftButtonClick and self.buttonCollisionTest(cornorButtonPositionA = CornerA, cornorButtonPositionB = CornerB):
            return ReturnValue
        return False
    
    def antiKnap(self,input,CornerA: tuple, CornerB: tuple, ReturnValue: bool = True):
        if input.mouseLeftButtonClick and not self.buttonCollisionTest(cornorButtonPositionA = CornerA, cornorButtonPositionB = CornerB):
            return ReturnValue
        return False
    


    
        