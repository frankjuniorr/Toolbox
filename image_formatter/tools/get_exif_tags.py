################################################################################
# Descrição:
#    Ferramenta auxiliar para extrair as tags EXIF de um arquivo de imagem (foto/vídeo).
#    Sugestão: colocar esse script num alias.
#
################################################################################
# Uso:
#    python3 get_exif_tags.py <file>
#
################################################################################

import exiftool
import sys
import json
from pathlib import Path

class GetExifTags:
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
            info = json.dumps(info, sort_keys=True, indent=4)
        print(info)

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

    getExifTags = GetExifTags(file)
    getExifTags.print_tags()