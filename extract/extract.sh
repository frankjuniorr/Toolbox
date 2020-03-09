#!/bin/bash

# ##############################################################################
# [Descrição]:
# Comando para extrair facilmente qualquer tipo de arquivo zip
#
# Uso:
# extract <nome_do_arquivo>
# ##############################################################################

file_param=$1

if [ -z "$file_param" ]; then
  # display usage if no parameters given
  echo "Usage: extract <path/file_name>.<zip|rar|bz2|gz|tar|tbz2|tgz|Z|7z|xz|ex|tar.bz2|tar.gz|tar.xz>"
  echo "       extract <path/file_name_1.ext> [path/file_name_2.ext] [path/file_name_3.ext]"
  exit 1
else
  for file in $@; do
    if [ -f "$file" ] ; then
      case "${file%,}" in
        *.tar.bz2|*.tar.gz|*.tar.xz|*.tbz2|*.tgz|*.txz|*.tar)
                     tar xvf "$file"       ;;
        *.lzma)      unlzma ./"$file"      ;;
        *.bz2)       bunzip2 ./"$file"     ;;
        *.rar)       unrar x -ad ./"$file" ;;
        *.gz)        gunzip ./"$file"      ;;
        *.zip)       unzip ./"$file"       ;;
        *.z)         uncompress ./"$file"  ;;
        *.7z|*.arj|*.cab|*.chm|*.deb|*.dmg|*.iso|*.lzh|*.msi|*.rpm|*.udf|*.wim|*.xar)
                     7z x ./"$file"        ;;
        *.xz)        unxz ./"$file"        ;;
        *.exe)       cabextract ./"$file"  ;;
        *)
           echo "extract: '$file' - unknown archive method"
           exit 1
         ;;
      esac
    else
      echo "'$file' - file does not exist"
      exit 1
    fi
  done
fi
