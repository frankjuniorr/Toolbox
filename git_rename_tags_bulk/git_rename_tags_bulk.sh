#!/bin/bash
# ##############################################################################
# [Descrição]:
# Comando para renomear tags do git de forma dinâmica
#
# Uso:
# ./git_rename_tags_bulk
#
# Funcionamento:
#   0. OBS: Garanta que esse scrip está sendo chamando por uma alias, só faz sentido se for assim
#   1. Rode o script uma vez pra criar um arquivo .txt com a listagem de tags
#   2. Edite manualmente o arquivo .txt gerado com o nome das novas tags
#   3. Rode o script novamente pra ele renomear
#   4. delete o arquivo .txt gerado
# ##############################################################################

# arquivo .txt com a lista de tags à serem modificadas
git_tag_file="git_tags.txt"

# ============================================
# Função que renomea uma tag única no git
# ============================================
function git_rename_tags(){
    local old_tag="$1"
    local new_tag="$2"
​
    test -z "$old_tag" && echo "digite a tag antiga no 1º parametro" && return 1
    test -z "$new_tag" && echo "digite a tag nova no 2º parametro" && return 1
​
    git tag "$new_tag" "$old_tag"
    git tag -d "$old_tag"
    git push origin ":refs/tags/${old_tag}"
    git push --tags
  }

# ============================================
# Função que renomea várias tags de uma vez
# ============================================
function rename_tags_loop(){
  while read line; do
    old_tag=$(echo $line | cut -d "=" -f1)
    new_tag=$(echo $line | cut -d "=" -f2)

    # validações
    if [ -z "$new_tag" ];then
      echo "[$old_tag] nome novo dessa tag está em branco"
      exit 1
    fi

    echo $old_tag
    echo $new_tag
    echo "======================"
    git_rename_tags "$old_tag" "$new_tag"
  done < "$git_tag_file"
}

# ============================================
# MAIN
# ============================================
function main(){

  # se o arquivo não existir, crie
  if [ ! -f "$git_tag_file" ];then
    git tag --list > "$git_tag_file"
    sed -i 's/$/=<DIGITE_AQUI_A_TAG_NOVA>/g' "$git_tag_file"
    exit 0
    
  else

    # validações
    if grep -q "<DIGITE_AQUI_A_TAG_NOVA>" "$git_tag_file";then
        echo "digite o nome das novas tags no arquivo de texto"
        exit 1
    fi

    # se o arquivo já existir, rode o loop
    rename_tags_loop
  fi
}

main

