import os
from processify import processify

import config

@processify
def cleanCache():
    '''
        Clean the render folder so it does not get bigger
        than the limit set in the config file
    '''
    # Clean the render folder
    allFiles = []
    cacheSize = 0

    # Loop through each files and delete the oldest
    # TODO pass directory as an argument
    for _, dirs, files in os.walk(config.renderDirectory):
        # Ignore resources folder
        # TODO remove this if we want to make a generic function
        if 'resources' in dirs :
            dirs.remove('resources')

        for file in files:
            filePath = os.path.join(config.renderDirectory, file)
            fileSize = os.stat(filePath).st_size
            allFiles.append((os.path.getmtime(filePath), fileSize, file))
            cacheSize += fileSize

    allFiles.sort()

    while cacheSize >= config.cacheMaxSize:
        for file in allFiles:
            os.remove(os.path.join(config.renderDirectory, os.path.join(config.renderDirectory, file[2])))
            cacheSize -= file[1]

    
