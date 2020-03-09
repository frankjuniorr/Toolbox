#!/bin/bash

################################################################################
#
# Descrição:
#    script to rip CDROM music files in mp3
#
################################################################################
#
# Uso:
#    ./rip_cdrom.sh
#
################################################################################
#
# Autor: Frank Junior <frankcbjunior@gmail.com>
# Desde: 07-05-2018
# Versão: 1
#
################################################################################


################################################################################
# Configurações
# set:
# -e: se encontrar algum erro, termina a execução imediatamente
  set -e


################################################################################
# Variáveis - todas as variáveis ficam aqui

# as variaveis ficam aqui...

  # mensagem de help
    nome_do_script=$(basename "$0")

    mensagem_help="
  Uso: $nome_do_script [OPÇÕES]

  Descrição: script to rip CDROM music files in mp3

  OPÇÕES: - opcionais
    -h, --help  Mostra essa mesma tela de ajuda

  Ex.: ./$nome_do_script -h
  "


################################################################################
# Utils - funções de utilidades

  # códigos de retorno
  # [condig-style] constantes devem começar com 'readonly'
  readonly SUCESSO=0
  readonly ERRO=1

  # debug = 0, desligado
  # debug = 1, ligado
  debug=0

  # ============================================
  # Função pra imprimir informação
  # ============================================
  _print_info(){
    local amarelo="\033[33m"
    local reset="\033[m"

    printf "${amarelo}$1${reset}\n"
  }

  # ============================================
  # Função pra imprimir mensagem de sucesso
  # ============================================
  _print_success(){
    local verde="\033[32m"
    local reset="\033[m"

    printf "${verde}$1${reset}\n"
  }

  # ============================================
  # Função pra imprimir erros
  # ============================================
  _print_error(){
    local vermelho="\033[31m"
    local reset="\033[m"

    printf "${vermelho}[ERROR] $1${reset}\n"
  }

  # ============================================
  # Função de debug
  # ============================================
  _debug_log(){
    [ "$debug" = 1 ] && _print_info "[DEBUG] $*"
  }

  # ============================================
  # tratamento das exceções de interrupções
  # ============================================
  _exception(){
    return "$ERRO"
  }

################################################################################
# Validações - regras de negocio até parametros

  # ============================================
  # tratamento de validacoes
  # ============================================
  validacoes(){
    # instalando o cdparanoia caso não tenha instalado
    if ! type cdparanoia > /dev/null 2>&1; then
     echo "++++ instalando o cdparanoia ++++"
     sudo apt-get install -y cdparanoia
     clear
    fi

    # instalando o lame caso não tenha instalado
    if ! type lame > /dev/null 2>&1; then
     echo "++++ instalando o lame ++++"
     sudo apt-get install -y lame
     clear
    fi
  }

################################################################################
# Funções do Script - funções próprias e específicas do script

# ============================================
# Converte os arquivos para mp3
# ============================================
  convert_files(){
    for track in *.wav; do
      lame -m s -b 320 $track
    done
  }

  # ============================================
  # Move todos os arquivo para um diretório e deleta os .wav
  # ============================================
  move_files(){
    _print_info "deletando arquivos .wav"
    rm *.wav

    mkdir disco_mp3
    mv *.mp3 disco_mp3
  }

  # ============================================
  # Função Main
  # ============================================
  main(){
    # vai ripar o cd no directorio corrente, em .wav
    if cdparanoia -B; then
      convert_files
      move_files
      _print_success "disco ripado"
    else
      _print_error "O drive de CD não tem disco nenhum"
      exit "$ERRO"
    fi
  }

  # ============================================
  # Função que exibe o help
  # ============================================
  verifyHelp(){
    case "$1" in

      # mensagem de help
      -h | --help)
        _print_info "$mensagem_help"
        exit "$SUCESSO"
      ;;

    esac
  }

################################################################################
# Main - execução do script

  # trata interrrupção do script em casos de ctrl + c (SIGINT) e kill (SIGTERM)
  trap _exception SIGINT SIGTERM
  verifyHelp "$1"
  validacoes
  main "$1"

################################################################################
# FIM do Script =D
