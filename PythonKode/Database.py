import os



def pathToGameDataFile(folder, fileName, fileType = ".txt"):
    path = os.path.dirname(__file__).strip("\PythonKode")
    relativePath = "\GameData\\" + folder + "\\" + fileName + fileType
    return path + relativePath