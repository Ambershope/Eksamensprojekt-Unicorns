import os

# Finder pathen til en fil, som fx. kortene. Det gør vi fordi programmet kan ligge forskellige steder
def pathToGameDataFile(folder, fileName, fileType = ".txt"):
    # Finder først pathen til denne fil
    path = os.path.dirname(__file__).strip("\PythonKode")

    # Derefter finder den pathen til den ting vi vil havde relativt til denne fil
    relativePath = "\GameData\\" + folder + "\\" + fileName + fileType
    return path + relativePath

# Nogle gange vil vi gerne kun finde en folder (som fx til databaser)
def pathToGameFolder(folder):
    path = os.path.dirname(__file__).strip("\PythonKode")
    relativePath = "\GameData\\" + folder
    return path + relativePath

# find noget i databasen