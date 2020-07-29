################################################################################
# Descrição:
#    Ferramenta auxiliar para extrair APENAS as datas das tags EXIF de um arquivo de imagem (foto/vídeo).
#    Sugestão: colocar esse script num alias.
# 
# Paramêtros:
#    Arquivos ou Diretórios
# 
# Formatos:
#    imagem: .png ou .jpg
#    video: .mp4
#
################################################################################
# Uso:
#    python3 get_datetime_tags.py <file>
#    python3 get_datetime_tags.py <folder>
#    python3 get_datetime_tags.py --help
#
################################################################################

import exiftool
import sys
from pathlib import Path
import click

# ============================================
def __get_tags_from_file(file):
    # se for um vídeo, a tags são umas, se for uma imagem, as tgs são outras
    if file.suffix == ".mp4":
        datetime_original_tag = "QuickTime:MediaCreateDate"
        datetime_modify_date_tag = "QuickTime:ModifyDate"
        datetime_media_create_date_tag = "QuickTime:MediaCreateDate"
    elif file.suffix == ".jpg" or file.suffix == ".png":
        datetime_original_tag = "EXIF:DateTimeOriginal"
        datetime_modify_date_tag = "File:FileModifyDate"
        datetime_media_create_date_tag = "EXIF:CreateDate"
    else:
        print("file format not supported")

    # extraindo as tags
    file = str(file)
    with exiftool.ExifTool() as exif:
        info = exif.get_metadata(file)

    # buscando apenas as datas
    originalTimeDate = None
    createDate = None
    try:
        originalTimeDate = info[datetime_original_tag]
        createDate = info[datetime_media_create_date_tag]
    except KeyError:
        pass

    modifyDate = info[datetime_modify_date_tag]
    filename = info['SourceFile']

    # imprimindo tudo
    print("=================================")
    print(f"filename = {filename}")
    print(f"originalTimeDate = {originalTimeDate}")
    print(f"createDate = {createDate}")
    print(f"modifyDate = {modifyDate}")

# ============================================
def __get_tags_from_folder(find_glob, file):
    for find in find_glob:
        for filename in file.glob(find):
            __get_tags_from_file(filename)


# ============================================
@click.command()
@click.argument('filename', type=click.Path(exists=True, file_okay=True, dir_okay=True))
def print_tags(filename):
    """
    Ferramenta auxiliar para extrair APENAS as datas das tags EXIF de um arquivo de imagem (foto/vídeo).
    """
    file = Path(filename)
    if file.is_file():
        __get_tags_from_file(file)
    elif file.is_dir():
        find_images = ('**/*.jpg', '**/*.png', '**/*.mp4')
        __get_tags_from_folder(find_images, file)
    

# ============================================
# MAIN
# ============================================
if __name__ == '__main__':
    print_tags()