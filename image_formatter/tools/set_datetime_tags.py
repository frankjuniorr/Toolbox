################################################################################
# Descrição:
#    Ferramenta auxiliar para setar (corrigir) as datas (EXIF) de um arquivo de imagem (foto/vídeo).
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
#    python3 set_datetime_tags.py <file>
#    python3 set_datetime_tags.py <folder>
#    python3 set_datetime_tags.py --help
#
################################################################################

import exiftool
import sys
import re
import os
import click
from pathlib import Path

def validate_datetime(time):
    """
    Função que valida o formato do timedate
    """
    time = time.replace("-", ":").replace("_", " ")
    regex = "^[0-9][0-9][0-9][0-9]:[0-9][0-9]:[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9]"
    dateformat_ok = re.search(regex, time)
    if dateformat_ok != None:
        return time
    else:
        return False

# ============================================
def __set_tags_from_file(time, file):
    """
    Função que seta um timedate em um arquivo de imagem/vídeo
    """
    # se for um vídeo, a tags são umas, se for uma imagem, as tgs são outras
    if file.suffix == ".mp4":
        datetime_original_tag = "-MediaCreateDate"
    elif file.suffix == ".jpg" or file.suffix == ".png":
        datetime_original_tag = "-DateTimeOriginal"
    else:
        print(f"{file} --> file format not supported")

    # seta o timedate de fato, no arquivo
    os.system(f"exiftool {datetime_original_tag}='{time}' \"{file}\"")

# ============================================
def __set_tags_from_folder(find_glob, time, file, start_time):
    """
    Função que seta um timedate em todos os arquivo de imagem/vídeo de um diretório, incrementando os segundos pra diferenciar
    """
    seconds = start_time
    for find in find_glob:
        for filename in file.glob(find):

            # incremente os segundos do timedate, e sete nos arquivos do diretório
            date = time[:-2]
            time = f"{date}{seconds}"

            print(filename)
            __set_tags_from_file(time, filename)
            seconds += 1


# ============================================
@click.command()
@click.option('--time', required=True, help='New datetime that will be set.')
@click.option('--start-time', default=10, required=False, help='start time in seconds, in case of multiple files.')
@click.argument('filename', type=click.Path(exists=True, file_okay=True, dir_okay=True))
def set_tags(filename, time, start_time):
    """
    Ferramenta auxiliar para setar (corrigir) as datas (EXIF) de um arquivo de imagem (foto/vídeo).
    """
    # valida o timedate passado por parâmetro
    time = validate_datetime(time)
    if time == False:
        print("formato inválido. Digite o --time, nesse formato:")
        print("--time=\"0000:00:00 00:00:\"")
        sys.exit()

    # valida se é um arquivo ou diretório, pra setar a data
    file = Path(filename)
    if file.is_file():
        __set_tags_from_file(time, file)
    elif file.is_dir():
        # verifique se o start_time é maior ou igual que 60 segundos.
        # se for, volte pro valr default (10)
        if start_time >= 60:
            start_time = 10
        find_images = ('**/*.jpg', '**/*.png', '**/*.mp4')
        __set_tags_from_folder(find_images, time, file, start_time)
    

# ============================================
# MAIN
# ============================================
if __name__ == '__main__':
    set_tags()