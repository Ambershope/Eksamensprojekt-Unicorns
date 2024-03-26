import os

def pathToGameFolder(folder):
    path = os.path.dirname(__file__).strip("\PythonKode")
    relativePath = "\GameData\\" + folder
    return path + relativePath


def pathToGameDataFile(folder, fileName, fileType = ".txt"):
    path = os.path.dirname(__file__).strip("\PythonKode")
    relativePath = "\GameData\\" + folder + "\\" + fileName + fileType
    return path + relativePath