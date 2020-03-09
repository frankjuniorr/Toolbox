#!/bin/bash

  # Cabeçalho
  # ----------------------------------------------------------------------------
  # Descrição:
  #    Script para preparar os arquivos para distribuir no OneRPM
  #
  # Funcionalidade:
  #    1. converte arquivos .mp3 para .wav com 44100 sample rate
  #    2. converte a imagem da capa do disco para 1400x1400 px
  #
  # ----------------------------------------------------------------------------
  # Uso:
  #    ./onerpm_build_files -h
  #    ./onerpm_build_files /path/do/disco
  # ----------------------------------------------------------------------------
  # Autor: Frank Junior <fcbj@cesar.org.br>
  # Desde: 26-02-2018
  # Versão: 1
  #
  # ----------------------------------------------------------------------------
  # Dependências:
  # ffmpeg --> utilitário de vídeo/audio converter
  # instalação: 'sudo apt-get install ffmpeg'
  #
  # imagemagick --> utilitário de vídeo/audio converter
  # instalação: 'sudo apt-get install imagemagick'
  # ----------------------------------------------------------------------------


  # Configurações
  # ----------------------------------------------------------------------------
  # set:
  # -e: se encontrar algum erro, termina a execução imediatamente
  set -e


  # Variáveis
  # ----------------------------------------------------------------------------

  disco=$1
  directory_name='onerpm_files'

# mensagem de help
  nome_do_script=$(basename "$0")

  mensagem_help="
Uso: $nome_do_script [OPÇÕES] <NOME_DO_SCRIPT>

OPÇÕES: - opcionais
  -h, --help  Mostra essa mesma tela de ajuda

DISCO_DIRETÒRIO - obrigatório
  - Diretório do disco

Ex.: ./$nome_do_script -h
Ex.: ./$nome_do_script /path/do/disco
"


  # Utils
  # ****************************************************************************

  # códigos de retorno
  SUCESSO=0
  ERRO=1

  # debug = 0, desligado
  # debug = 1, ligado
  debug=0

  # ============================================
  # Função pra imprimir informação
  # ============================================
  function print_info(){
    local cor_amarelo="\033[33m"
    local fecha_cor="\033[m"

    printf "${cor_amarelo}$1${fecha_cor}\n"
  }

  # ============================================
  # Função pra imprimir mensagem de sucesso
  # ============================================
  function print_success(){
    local cor_verde="\033[32m"
    local fecha_cor="\033[m"

    printf "${cor_verde}$1${fecha_cor}\n"
  }

  # ============================================
  # Função pra imprimir erros
  # ============================================
  function print_error(){
    local cor_vermelho="\033[31m"
    local fecha_cor="\033[m"

    printf "${cor_vermelho}[ERROR] $1${fecha_cor}\n"
  }

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

    # verificando o parâmetro
    if [ -z "$disco" ];then
      print_error "paramêtro vazio. Passe um diretório de disco."
      exit $ERRO
    fi

    # verificando o parâmetro
    if [ ! -d "$disco" ];then
      print_error "paramêtro não é um diretório. Passe um diretório de disco."
      exit $ERRO
    fi

    # instalando o ffmpeg caso não tenha instalado
    if ! type ffmpeg > /dev/null 2>&1; then
      echo "++++ instalando o ffmpeg ++++"
      sudo apt-get install -y ffmpeg
      clear
    fi

    # instalando o imagemagick caso não tenha instalado
    if ! type convert > /dev/null 2>&1; then
      echo "++++ instalando o imagemagick: ++++"
      sudo apt-get install -y imagemagick:
      clear
    fi

  }

  # ============================================
  # tratamento das exceções de interrupções
  # ============================================
  function exception(){
    echo ""
  }
  # ******************* [FIM] Utils *******************




  # Funções do Script
  # ----------------------------------------------------------------------------

  # ============================================
  # Função que converte os arquivos para wav,
  # e coloca-os em uma pasta separada chamada "wav"
  # ============================================
  function convert_files(){

    # se já existir a pasta 'wav', delete ela.
    if [ -d "$disco"/${directory_name} ];then
      rm -rf "$disco"/${directory_name}
    fi

    # criando a pasta wav
    mkdir "$disco"/${directory_name}

    print_info "converting music files..."
    for musica in "$disco"/*.mp3 ; do

      # Expanção de variável, retira a extensão do arquivo de mp3
      local musica_wav="${disco}/${directory_name}/$(basename "${musica%.mp3}")"

      # ffmpeg parameters:
      # [-loglevel panic] só exibe saída no STDOUT para erros tipo "panic"
      # [-i] input file
      # [-acodec pcm_s16le] 16 bits little endian
      # [-ar 44100] a sample rate of 44100 Hz
      # [-ac 2] 2 channels (stereo)
      ffmpeg -i "$musica" -acodec pcm_s16le -ar 44100 -ac 2 "$musica_wav".wav
    done

    print_info "creating album cover..."
    for cover in "$disco"/*.{jpg,png} ; do
      if [ -f "$cover" ];then
        local onerpm_cover="onerpm_cover_$(basename "$cover")"
        local extension="${cover#*.}"

        # convert image to 1400x1400 px
        # this image size is needed to upload in oneRPM
        convert "$cover" \
          -resize 1400x1400! \
          -verbose \
          -units PixelsPerInch \
          -density 600 "$onerpm_cover"

        mv "$onerpm_cover" "${disco}/${directory_name}/cover.${extension}"
      fi
    done
    print_info "Done!"
  }

  # ============================================
  # Função Main
  # ============================================
  function main(){
    case "$1" in

      # mensagem de help
      -h | --help)
        print_info "$mensagem_help"
        exit "$SUCESSO"
      ;;

      # se não for help, é o caminho feliz \o/
      *)
        validacoes
        convert_files
        exit "$SUCESSO"
      ;;

    esac
  }

  # Main
  # ----------------------------------------------------------------------------
  # trata interrrupção do script em casos de ctrl + c (SIGINT) e kill (SIGTERM)
  trap exception SIGINT SIGTERM
  main "$1"

  # ----------------------------------------------------------------------------
  # FIM do Script =D
