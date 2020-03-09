#!/bin/bash

# ##############################################################################
# [Descrição]:
#   Comando para atualizar o Visual Studio Code.
#   Esse script é necessário, pois sempre que lança umaversão nova do vscode,
#   ele pede pra baixar o arquivo .deb do site.
#   Esse script faz isso automaticamente
#
# Uso:
# ./update_vscode.sh
# ##############################################################################

vscode_url_download="https://vscode-update.azurewebsites.net/latest/linux-deb-x64/stable"
temp_file="/tmp/code_latest_amd64.deb"

# baixa a versão nova do vscode do site, para o /tmp
wget "$vscode_url_download" -O "$temp_file"

# instala o novo pacote .deb
sudo dpkg -i "$temp_file"

# remove o arquivo temporário
rm -rf "$temp_file"
