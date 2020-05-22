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

    # checka se o path existe
    if not os.path.isdir(path):
        print(f"Path not found: {path}")
        sys.exit()

    # instacia o objeto
    imageFormatter = ImageFormatter(path)
    imageFormatter.enableDebugMode(False)

    # Verifica se há arquivos duplicados (verificação por byte).
    # Não prossegue enquanto houver arquivo duplicado
    # para serem resolvidos manualmente
    print("Verificando arquivos duplicados (por byte)...")
    existFileDuplicated = imageFormatter.checkDuplicateFilesByBytes()

    if existFileDuplicated == "":
        imageFormatter.standardizeFileFormats()
        imageFormatter.renameAllFolders()
        imageFormatter.renameAllFiles()
        LogManager.instance().log_clean()
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print()
        print("----------- Arquivos Duplicados (por Byte) -----------")
        print()
        print(existFileDuplicated)


