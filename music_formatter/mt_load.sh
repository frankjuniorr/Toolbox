#!/bin/bash

  # Cabeçalho
  # ----------------------------------------------------------------------------
  # Descrição:
  #    Módulo do script 'music_formatter.sh' responsável por carregar as tags dos
  #    dos arquivos de mp3 e criar um arquivo json com essas tags.
  #
  # ----------------------------------------------------------------------------
  # Uso:
  #    ./mt_load.sh "$disco"
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
  # Desde: 28-07-2017
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

  script_dir=$(pwd)
  json_stream=''

  # tags
  artist=''
  album=''
  album_artist=''
  genre=''
  year=''
  track=''
  composer=''

  # contants
  declare -r JSON='arquivo.json'


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

  function printJson(){
    local message=$1
    echo "$message" >> ../"$JSON"
  }
  # ******************* [FIM] Utils *******************




  # Funções do Script
  # ----------------------------------------------------------------------------

  # ============================================
  # Função que constrói o arquivo json.
  # ============================================
  function buildJsonFile(){
    # a 'image' eu coloquei sempre nula, porque mesmo se aparecer
    # vai aparecer apenas o nome do arquivo.jpg, que não quer dizer nada.
    # Sendo assim, vou tornar a escrita da imagem, um item obrigatório,
    # na hora de escrever a tag.
    local album_tags='{
  "artist": "@artistTag@",
  "album": "@albumTag@",
  "album_artist": "@album_artistTag@",
  "image": "",
  "genre": "@genreTag@",
  "year": "@yearTag@",
  "track_total": "@track_total@",
'

    album_tags=$(echo "$album_tags" | sed "s/@artistTag@/$artist/" 2> /dev/null ||\
      echo "$album_tags" | sed "s/@artistTag@/null/")

    album_tags=$(echo "$album_tags" | sed "s/@albumTag@/$album/" 2> /dev/null ||\
      echo "$album_tags" | sed "s/@albumTag@/null/")

    album_tags=$(echo "$album_tags" | sed "s/@album_artistTag@/$album_artist/" 2> /dev/null ||\
      echo "$album_tags" | sed "s/@album_artistTag@/null/")

    album_tags=$(echo "$album_tags" | sed "s/@genreTag@/$genre/" 2> /dev/null ||\
      echo "$album_tags" | sed "s/@genreTag@/null/")

    album_tags=$(echo "$album_tags" | sed "s/@yearTag@/$year/" 2> /dev/null ||\
      echo "$album_tags" | sed "s/@yearTag@/null/")

    json_stream="$album_tags"
  }

  # ============================================
  # Função que constrói o arquivo json das faixas.
  # ============================================
  function buildFaixas(){
    local faixa="$1"
    local title="$2"

    local track_array='
    "@faixa@":
    {
      "title": "@titleTag@",
      "track": "@trackTag@",
      "composer": "@composerTag@"
    },'

    track_array=$(echo "$track_array" | sed "s/@faixa@/track$faixa/")
    track_array=$(echo "$track_array" | sed "s/@titleTag@/$title/")
    track_array=$(echo "$track_array" | sed "s/@trackTag@/$track/")
    track_array=$(echo "$track_array" | sed "s/@composerTag@/$composer/")

    json_stream="$json_stream""$track_array"
  }

  # ============================================
  # Função para ler as tags dos arquivos de mp3.
  # ============================================
  function readTags(){
    local i=1
    local faixa=''
    local close_json='}'

    cd "$disco"_temp

    # convertendo todas as tags para 'ID3 version 2.3'
    # 1. pra caso apareça alguma version 1.1 que é dificil de ler já resolve
    # 2. o 'id3v2' não ler direito a version 2.4, então é mais garantia a version 2.3
    eyeD3 -l 'error' --to-v2.3 *.mp3 > /dev/null

    # esse loop para na primeira ocorrencia pra pegar as tags referente ao disco todo.
    for arquivo in *.mp3; do
      artist=$(id3v2 -l "$arquivo" | grep "TPE1" | cut -d ":" -f2 | sed 's/^\s//')
      album=$(id3v2 -l "$arquivo" | grep "TALB" | cut -d ":" -f2 | sed 's/^\s//')
      album_artist=$(id3v2 -l "$arquivo" | grep "TPE2" | cut -d ":" -f2 | sed 's/^\s//')
      genre=$(id3v2 -l "$arquivo" | grep "TCON" | cut -d ":" -f2 | sed 's/^\s//')
      year=$(id3v2 -l "$arquivo" | grep "TYER" | cut -d ":" -f2 | sed 's/^\s//')
      break
    done

    buildJsonFile

    # esse loops para pegar as tags individuais de cada faixa
    for arquivo in *.mp3; do
      faixa=$(id3v2 -l "$arquivo" | grep "TIT2" | cut -d ":" -f2 | sed 's/^\s//')
      track=$(id3v2 -l "$arquivo" | grep "TRCK" | cut -d ":" -f2 | sed 's/^\s//' | cut -d "/" -f1)
      composer=$(id3v2 -l "$arquivo" | grep "TCOM" | cut -d ":" -f2 | sed 's/^\s//')

      buildFaixas "$i" "$faixa"

      # incrementa o i
      i=$((i+1))
    done

    # retira a virgula da ultima iteração de faixas.
    # se não fizer isso, o 'jq' se quebra pra ler o json.
    json_stream="${json_stream:: -1}"

    echo "$json_stream" > ../"$JSON"

    # esse decremento é necessário, porque quando o loop anterior escrever no json
    # a ultima faixa, o incrementa mais uma vez. Ou seja, pra saber a quantidade de
    # faixas, precisa-se desse decremento.
    i=$((i-1))
    sed -i "s/@track_total@/$i/" ../"$JSON"
    printJson "$close_json"

    cd "$script_dir"
  }

  # ============================================
  # Função que cria o arquivo json com as informações
  # ============================================
  function initFile(){
    if [ -f "$JSON" ];then
      rm "$JSON"
    fi
    touch "$JSON"
  }

  # ============================================
  # Função Main
  # ============================================
  function main(){
    initFile
    readTags
  }

  # Main
  # ----------------------------------------------------------------------------
  # trata interrrupção do script em casos de ctrl + c (SIGINT) e kill (SIGTERM)
  trap exception SIGINT SIGTERM
  validacoes
  main

  # ----------------------------------------------------------------------------
  # FIM do Script =D
