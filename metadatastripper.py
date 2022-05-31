from PIL import Image
from PIL.ExifTags import TAGS
from termcolor import colored
import os
import sys

def getArguments():
    photoPath = ""
    directoryPath = ""
    savePath = ""

    # look for tags
    for arg in sys.argv:
        # check for photo path
        if arg == "-p":
            photoPath = sys.argv[sys.argv.index(arg)+1]
        elif arg == "-d":
            directoryPath = sys.argv[sys.argv.index(arg)+1]
        elif arg == "-o":
            saveFile = sys.argv[sys.argv.index(arg)+1]


    return photoPath, directoryPath, savePath


def getData(photoPath, directoryPath, savePath):
    try:
        if photoPath != "":
            img = Image.open(photoPath)
            labeled = {}
            for (key, val) in img._getexif().items():
                labeled[TAGS.get(key)] = val
            for key in labeled:
                print(colored(f"{key}: {str(labeled[key]).encode('utf-8').decode()}"))
                if savePath != "":
                    with open(savePath, "w") as f:
                        f.write(f"{key}: {str(labeled[key]).encode('utf-8').decode()}")

        if directoryPath != "":
            imgs = []
            imgName = []
            directoryPath = f"{directoryPath}\\".replace('"', '')
            print(directoryPath)
            for f in os.listdir(directoryPath):
                newPath = directoryPath + f # creates the file path by adding the file name to the path
                imgs.append(Image.open(newPath))
                imgName.append(f)
            labeled = {}
            for img in imgs:
                labeled = {}
                for (key, val) in img._getexif().items():
                    labeled[TAGS.get(key)] = val
                for key in labeled:
                    if isinstance(labeled[key], (bytes, bytearray)):
                        print("sdhsd")
                        labeled[key].decode(encoding="utf-8")
                    print(colored(f"{key}: {(labeled[key])}"))
                    if savePath != "":
                        with open(savePath, "w") as f:
                            f.write(f"{key}: {str(labeled[key]).encode('utf-8').decode()}")



    except Exception as e:
        print(e)

try:
    photoPath, directoryPath, savePath = getArguments()
    getData(photoPath, directoryPath, savePath)
except:
    pass
