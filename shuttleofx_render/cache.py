import os
from processify import processify

import config

@processify
def cleanCache(cachePath):
    '''
        Clean the folder so it does not get bigger
        than the limit set in the config file
    '''
    # Clean the render folder
    allFiles = []
    cacheSize = 0

    # Loop through each files and delete the oldest
    for path, dirs, files in os.walk(cachePath):
        for file in files:
            filePath = os.path.join(path, file)
            fileSize = os.stat(filePath).st_size
            # List all file : timestamp | size | filename
            allFiles.append((os.path.getmtime(filePath), fileSize, filePath))
            cacheSize += fileSize

    allFiles.sort()

    # TODO : Maybe pass the max size as an argument
    while cacheSize >= config.cacheMaxSize:
        for file in allFiles:
            os.remove(os.path.join(cachePath, os.path.join(cachePath, file[2])))
            cacheSize -= file[1]

    removeEmptyFolders(cachePath)

def cachePathFromFile(filename):
    '''
        Create a path from a file
        example : convert 123456789.png to 1234/5678/9.png
    '''
    
    file, extension = os.path.splitext(filename)
    # Split hash in strings of 4 characters
    length = 4
    charactersList = [file[i:i+length] for i in range(0, len(file), length)]
    # Add the extension to the last element of the list
    charactersList[len(charactersList)-1] += extension

    return os.path.join(*charactersList)

def removeEmptyFolders(path, removeRoot=True):
    '''
        Function to remove empty folders
        https://gist.github.com/jacobtomlinson/9031697
    '''
    if not os.path.isdir(path):
        return

    # remove empty subfolders
    files = os.listdir(path)
    if len(files):
        for f in files:
            fullpath = os.path.join(path, f)
            if os.path.isdir(fullpath):
                removeEmptyFolders(fullpath)

    # if folder empty, delete it
    files = os.listdir(path)
    if len(files) == 0 and removeRoot:
        os.rmdir(path)
