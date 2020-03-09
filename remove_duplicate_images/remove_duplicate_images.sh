#!/bin/bash

# ##############################################################################
# [Descrição]:
#   Esse script indentifica as imagens/vídeos duplicados do diretório
#   "~/Dropbox/Camera Uploads". Uma vez identiificado,o objetivo é remover
#   desse diretório.
#
# Uso:
# ./remove_duplicate_images.sh
# ##############################################################################

# resolvendo as dependencias
if ! which fdupes > /dev/null 2>&1 ;then
    echo "instalando dependencias"
    sudo apt install fdupes
fi

camera_uploads="$HOME/Dropbox/Camera Uploads"
images="$HOME/Dropbox/Images"

# criando arquivo e pasta temporária
arquivos_duplicados_lista="$HOME/arquivos_duplicados.txt"
arquivos_duplicados_pasta="$HOME/arquivos_duplicados_lixo"

# identificando os arquivos duplicados
fdupes -r "$camera_uploads" "$images" > "$arquivos_duplicados_lista"

# se não tiver arquivo duplicado, avise e saia do script
# Esse if verifica se o arquivo está vazio em bytes
if [ $(du -sh "$arquivos_duplicados_lista" | awk '{print $1}') == "0" ];then
    echo "não existe arquivo duplicado"
    rm -rf "$arquivos_duplicados_lista"
    exit 0
fi

# criando a pasta temporária com os arquivos duplicados pra dar uma olhada depois.
test -d "$arquivos_duplicados_pasta" || mkdir "$arquivos_duplicados_pasta"

echo "movendo os arquivos..."
for arquivo in $(grep "Camera Uploads" "$arquivos_duplicados_lista" | sed 's/ /@/g');do
    arquivo=$(echo $arquivo | sed 's/@/ /g')

    mv "$arquivo" "$arquivos_duplicados_pasta"
done


quantidade=$(grep "Camera Uploads" $arquivos_duplicados_lista | wc -l)
tamanho=$(du -sh $arquivos_duplicados_pasta | awk '{print $1}')

# imprimindo um sumário
clear
echo "Sumário:"
echo "quantidade de arquivos: $quantidade"
echo "Tamanho: $tamanho"

rm -rf "$arquivos_duplicados_lista"