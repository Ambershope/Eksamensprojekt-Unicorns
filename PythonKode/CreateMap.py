import os
class Map:
    def __init__ (self, MapId=0):
        self.mapId=MapId
        #self.tiles=self.getMap()

        
    def getMap(self):
        #finder stien til kortet med mapIdet
        path=os.path.dirname(__file__).split("\PythonKode")[0]
        relativePath = "\GameData\Maps\Map"+str(self.mapId)+".txt"
        print (path)
        Fil=open(path+relativePath, 'r')
        mapData=Fil.read().split("\n")
        Fil.close()

        sizeX=len(mapData)
        sizeY=len(mapData[0])
        if sizeX != sizeY:
            print("Error map not square, may not work")
        self.mapSize=sizeX

        print(mapData)
        cloumn=[]
        for i in range (sizeX):
            cloumn.append(0)
        
        return i
kort=Map()
kort.getMap()       

