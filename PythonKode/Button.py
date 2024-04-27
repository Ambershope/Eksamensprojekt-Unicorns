import pygame


class ButtonDetection:
    def __init__(self):
        self.buttonCollisionTest
        self.knap
        self.MousePosition = [0,0]


    def buttonCollisionTest(self, cornorButtonPositionA, cornorButtonPositionB, useUserMouse = True):
        if useUserMouse == True:
            MousePosition = pygame.mouse.get_pos()
    
        if MousePosition[0] >= min(cornorButtonPositionA[0], cornorButtonPositionB[0]) and MousePosition[0] <= max(cornorButtonPositionA[0], cornorButtonPositionB[0]):
                
            if MousePosition[1] >= min(cornorButtonPositionA[1], cornorButtonPositionB[1]) and MousePosition[1] <= max(cornorButtonPositionA[1], cornorButtonPositionB[1]):
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
    


    
        