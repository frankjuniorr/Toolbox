#!/bin/bash

cd $HOME

# verifique se o diretório bin existe
if [ -d bin ];then
	cd bin

	echo "deletando diretório Postman"
	test -d "Postman" && rm -rf $_

	echo "download Postman"
	curl https://dl.pstmn.io/download/latest/linux64 -o postman.tar.gz

	echo "extraindo arquivo"
	tar -xzf postman.tar.gz

	echo "deletando o zip"
	rm -rf postman.tar.gz

else
	echo "Diretório bin não existe no HOME"
fi


echo "gerando o arquivo .desktop"

postman_desktop_file="$HOME/.local/share/applications/postman.desktop"

if [ -f "$postman_desktop_file" ];then
	rm -rf "$postman_desktop_file"
fi

cat <<EOF >> "$postman_desktop_file"
[Desktop Entry]
Encoding=UTF-8
Name=Postman
Exec=$HOME/bin/Postman/app/Postman %U
Icon=$HOME/bin/Postman/app/resources/app/assets/icon.png
Terminal=false
Type=Application
Categories=Development;
EOF

echo "postman atualizado!"

