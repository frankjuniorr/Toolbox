import os
import sys

from image_formatter import ImageFormatter
from log_manager import LogManager

if __name__ == '__main__':

    # get path from script arguments
    path = None
    try:
        path = sys.argv[1]
    except IndexError:
        print("type a valid path as argument")
        sys.exit()

    if not os.path.isdir(path):
        print(f"Path not found: {path}")
        sys.exit()

    imageFormatter = ImageFormatter(path)

    imageFormatter.enableDebugMode(False)

    imageFormatter.standardizeFileFormats()
    imageFormatter.renameAllFolders()
    imageFormatter.renameAllFiles()

    LogManager.instance().log_clean()


