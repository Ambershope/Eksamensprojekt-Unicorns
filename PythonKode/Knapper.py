import Visuals
import main


class Knapper:
    def __init__(self):
        self.buttonCollisionTest
        self.knap
        self.MousePosition = [0,0]


    def buttonCollisionTest(self, cornorButtonPositionA, cornorButtonPositionB, useUserMouse = True):
        if useUserMouse == True:
            MousePosition = Visuals.Grid.getGrid(main.Input.mousePosition)
    
        if MousePosition[0] >= min(cornorButtonPositionA[0], cornorButtonPositionB) and MousePosition[0] <= max(cornorButtonPositionA[0], cornorButtonPositionB[0]):
                
            if MousePosition[1] >= min(cornorButtonPositionA[1], cornorButtonPositionB) and MousePosition[1] <= max(cornorButtonPositionA[1], cornorButtonPositionB[1]):
                return True
        return False


    def knap(self, CornerA, CornerB, ReturnValue):
        if main.Input.mouseLeftButtonClick and self.buttonCollisionTest(CornerA, CornerB):
            return ReturnValue
        return False
    
    def antiKnap(self,CornerA, CornerB, ReturnValue):
        if main.Input.mouseLeftButtonClick and not self.buttonCollisionTest(CornerA, CornerB):
            return ReturnValue
        return False
    


    
        