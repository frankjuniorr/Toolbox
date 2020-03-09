#!/bin/bash

  # Cabeçalho
  # ----------------------------------------------------------------------------
  # Descrição:
  #    Módulo do script 'music_formatter.sh' responsável por:
  #    1. escrever as tags novas nos arquivos de mp3.
  #    2. criar uma estrutura de pastas baseado nas tags.
  #
  # ----------------------------------------------------------------------------
  # Uso:
  #    ./mt_save.sh "$disco"
  #
  #    PARAMS:
  #     [1] <disco>: O diretório do disco a ser consertado
  #
  # Dependencias:
  #     1. jq [https://stedolan.github.io/jq/] --> ferramenta que facilita a leitura de json.
  #     2. funcoeszz [http://funcoeszz.net/] --> ferramenta que facilita o rename dos arquivos.
  #     3. id3v2 --> ferramenta que ler e escreve tags ID3.
  #     4. eyeD3 --> ferramenta que ler e escreve tags ID3.
  #
  # ----------------------------------------------------------------------------
  # Autor: Frank Junior <frankcbjunior@gmail.com>
  # Desde: 31-07-2017
  # Versão: 1
  # ----------------------------------------------------------------------------


  # Configurações
  # ----------------------------------------------------------------------------
  # set:
  # -e: se encontrar algum erro, termina a execução imediatamente
  set -e


  # Variáveis
  # ----------------------------------------------------------------------------

  # Params
  disco="$1"

  # tags
  artist=''
  album=''
  album_artist=''
  genre=''
  year=''
  track_total=''
  image=''

  script_dir=$(pwd)

  # contants
  declare -r JSON='arquivo.json'
  declare -r IMAGE='cover.jpg'


  # Utils
  # ****************************************************************************

  # códigos de retorno
  SUCESSO=0
  ERRO=1

  # debug = 0, desligado
  # debug = 1, ligado
  debug=0

  # ============================================
  # Função de debug
  # ============================================
  function debug_log(){
    [ "$debug" = 1 ] && print_info "[DEBUG] $*"
  }

  # ============================================
  # tratamento de validacoes
  # ============================================
  function validacoes(){
    if [ "$disco"  == "" ];then
      echo "Faltou passar um disco por parametro"
      exit "$ERRO"
    fi
  }

  # ============================================
  # tratamento das exceções de interrupções
  # ============================================
  function exception(){
    exit "$ERRO"
  }
  # ******************* [FIM] Utils *******************




  # Funções do Script
  # ----------------------------------------------------------------------------

  # ============================================
  # função que ler as tags do arquivo.json
  # ============================================
  function getTags(){
    artist=$(jq -r '.artist' "$JSON")
    album=$(jq -r '.album' "$JSON")
    album_artist=$(jq -r '.album_artist' "$JSON")
    genre=$(jq -r '.genre' "$JSON")
    year=$(jq -r '.year' "$JSON")
    track_total=$(jq -r '.track_total' "$JSON")
    image=$(jq -r '.image' "$JSON")
  }

  # ============================================
  # Função que seta as tags nos arquivos de mp3
  # ============================================
  function setTags(){

    if [ ! -f "$image" ];then
      echo "defina uma imagem para os mp3 no arquivo.json"
      exit $ERRO
    fi

    mv "$IMAGE" "$disco"_temp

    local i=1
    # setando as tags
    cd "$disco"_temp
    for arquivo in *.mp3; do
      title=$(jq -r ".track$i.title" ../"$JSON")
      track=$(jq -r ".track$i.track" ../"$JSON")
      composer=$(jq -r ".track$i.composer" ../"$JSON")

      eyeD3 -l 'error' \
       --artist "$artist" \
       --album "$album" \
       --album-artist "$album_artist"\
       --genre "$genre" \
       --recording-date "$year" \
       --title "$title" \
       --add-image="$IMAGE":FRONT_COVER \
       "$arquivo" > /dev/null

       # setando composer e as tracks, é melhor por aqui.
       id3v2 --TCOM "$composer" \
       --TRCK "$track/$track_total" "$arquivo"

       # incrementa o i
       i=$((i+1))
    done
    cd "$script_dir"
  }

  # ============================================
  # Função que renomeia os arquivos de acordo com
  # a estrutura correta de diretórios.
  # ============================================
  function renameFiles(){
    mkdir "$artist"
    mv "$disco"_temp "$artist"
    cd "$artist"

    disco_dir="$year - $album"
    mv "$disco"_temp "$disco_dir"
    cd "$disco_dir"

    for arquivo in *.mp3; do

      track=$(id3v2 -l "$arquivo" | grep "TRCK" | cut -d ":" -f2 | sed 's/^\s//' | cut -d "/" -f1)
      faixa=$(id3v2 -l "$arquivo" | grep "TIT2" | cut -d ":" -f2 | sed 's/^\s//')

      mv "$arquivo" "$track $faixa.mp3"
    done

    cd "$script_dir"
    rm "$JSON"
  }

  # ============================================
  # Função Main
  # ============================================
  function main(){
    getTags
    setTags
    renameFiles
  }

  # Main
  # ----------------------------------------------------------------------------
  # trata interrrupção do script em casos de ctrl + c (SIGINT) e kill (SIGTERM)
  trap exception SIGINT SIGTERM
  validacoes
  main

  # ----------------------------------------------------------------------------
  # FIM do Script =D
