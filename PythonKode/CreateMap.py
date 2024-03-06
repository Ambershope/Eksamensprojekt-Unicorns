import os
class Kort:
    def __init__ (self, MapId=0):
        self.mapId=MapId
        self.felter=self.getStartKort()

    #returnere en string med et flot formateret kort
    def __str__ (self):
        tekst="\n"

        for y in range (self.mapSize):
            for x in range (self.mapSize):
                tekst = tekst + " " + str(self.felter[x][y]) + " "
            tekst = tekst + "\n"

        return tekst
        
    def getStartKort(self):
        #finder stien til kortet 
        path=os.path.dirname(__file__).split("\PythonKode")[0]
        relativePath = "\GameData\Maps\Map"+str(self.mapId)+".txt"
        
        #læser kortet ind i mapData
        Fil=open(path+relativePath, 'r')
        mapData=Fil.read().split("\n")
        Fil.close()

        #finder sidelængden på kortet
        sizeX=len(mapData)
        sizeY=len(mapData[0])
        if sizeX == sizeY:
            self.mapSize=sizeX
        else:
            print("Error: map not square. Entire map wont load")
            if sizeX > sizeY:
                self.mapSize=sizeY
            else:
                self.mapSize=sizeX

        #formaterer kortet og sørger for at lave en tabel med int's
        kort=[]
        for x in range (self.mapSize):
            kolonne=[]
            for y in range (self.mapSize):
                kolonne.insert(0,int(mapData[x][self.mapSize-y-1]))
            kort.insert(0,kolonne)
        
        return kort
    

if __name__ == '__main__':
    kort=Kort(1)
    print(kort)      

