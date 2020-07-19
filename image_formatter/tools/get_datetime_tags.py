################################################################################
# Descrição:
#    Ferramenta auxiliar para extrair APENAS as datas das tags EXIF de um arquivo de imagem (foto/vídeo).
#    Sugestão: colocar esse script num alias.
#
################################################################################
# Uso:
#    python3 get_datetime_tags.py <file>
#
################################################################################

import exiftool
import sys
from pathlib import Path

class GetDatetimeTags:
    """
    Get EXIF tags from midia file
    """

    # ============================================
    def __init__(self, file):
        self.file = file

    # ============================================
    def print_tags(self):
        """
        Function to print exif tags
        """
        file = str(self.file)
        with exiftool.ExifTool() as exif:
            info = exif.get_metadata(file)

        originalTimeDate = info['EXIF:DateTimeOriginal']
        createDate = info['EXIF:CreateDate']
        modifyDate = info['File:FileModifyDate']
        filename = info['SourceFile']

        print(f"filename = {filename}")
        print(f"originalTimeDate = {originalTimeDate}")
        print(f"createDate = {createDate}")
        print(f"modifyDate = {modifyDate}")
        print("=================================")

# ============================================
# MAIN
# ============================================
if __name__ == '__main__':

    # get file from script arguments
    file = None
    try:
        file = sys.argv[1]
    except IndexError:
        print("type a valid file as argument")
        sys.exit()

    file = Path(file)
    if not file.is_file():
        print(f"Path not found: {file}")
        sys.exit()

    getDatetimeTags = GetDatetimeTags(file)
    getDatetimeTags.print_tags()