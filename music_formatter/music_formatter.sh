#!/bin/bash

  # Cabeçalho
  # ----------------------------------------------------------------------------
  # Descrição:
  #    Script usado pra consertar tags ID3 de arquivos MP3.
  #    Esse é o script principal que usa dois módulos ('mt_load.sh' e 'mt_save.sh').
  #    Escrever as tags, e criar uma estrutura de diretório própria.
  #    Por ser o módulo de start, pode ser facilmente substituído por uma GUI no futuro
  #     adicionando uma modificação de teste
  #
  # ----------------------------------------------------------------------------
  # Uso:
  #    ./music_formatter.sh <disco>
  #
  #    PARAMS:
  #     [1] <disco>: O diretório do disco a ser consertado
  #
  # Dependencias:
  #     1. jq [https://stedolan.github.io/jq/] --> ferramenta que facilita a leitura de json.
  #     2. funcoeszz [http://funcoeszz.net/] --> ferramenta que facilita o rename dos arquivos.
  #     3. id3v2 --> ferramenta que ler e escreve tags ID3.
  #     4. eyeD3 --> [http://eyed3.nicfit.net/] ferramenta que ler e escreve tags ID3.
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
  diretorio_do_disco="$1"
  disco="$diretorio_do_disco"

  funcoeszz_dir=$(echo $ZZPATH | sed 's/\/funcoeszz$//')
  script_dir=$(pwd)

  # contants
  declare -r IMAGE='cover.jpg'
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
    local jqIsInstall=$(which jq > /dev/null; echo $?)
    local id3v2IsInstall=$(which id3v2 > /dev/null; echo $?)
    local eyeD3IsInstall=$(which eyeD3 > /dev/null; echo $?)

    # 1. verificar a instalação das funcoeszz, jq e id3v2.
    if [ "$jqIsInstall" != "0" ] || [ "$id3v2IsInstall" != "0" ]; then
      print_info "instalando dependencias"
      sudo apt-get update > /dev/null
      sudo apt-get install jq id3v2 > /dev/null
    fi

    # no caso do eyeD3, garantir a instalação da versão '0.7.11'
    # a versão 0.8 dá problema com unicode UTF-8.

    # pra desinstalar use:
    # $ pip uninstall eyeD3

    if [ "$eyeD3IsInstall" != "0" ];then
      print_info "instalando dependencias do eyeD3"
      wget http://eyed3.nicfit.net/releases/eyeD3-0.7.11.tar.gz > /dev/null
      tar -xzf eyeD3-0.7.11.tar.gz
      cd eyeD3-0.7.11
      python setup.py install
      cd ..
      rm -rf  eyeD3-0.7.11 eyeD3-0.7.11.tar.gz
      clear
    fi

    # Instalando as funcoeszz
    if [ -z "$ZZPATH" ];then
      print_info "instalando dependencias das funcoeszz"
      cd ~/Downloads
      wget http://funcoeszz.net/download/funcoeszz-15.5.sh > /dev/null
      mv funcoeszz-15.5.sh funcoeszz
      chmod +x funcoeszz
      ./funcoeszz zzzz --bashrc
      source ~/.bashrc
      clear
      cd "$script_dir"
    fi

    if [ "$disco"  == "" ];then
      echo "Faltou passar um disco por parametro"
      exit "$ERRO"
    fi
  }

  # ============================================
  # tratamento das exceções de interrupções
  # ============================================
  function exception(){
    deleteTempFiles
    exit "$ERRO"
  }
  # ******************* [FIM] Utils *******************




  # Funções do Script
  # ----------------------------------------------------------------------------

  # ============================================
  # Função que cria uma pasta temporária com nomes
  # arrumados em minusculos, pra ficar mais fácil
  # de capturar os arquivos de mp3, e salvar num json depois.
  #
  # OBS: essa função por via de regra era pra ficar no mt_load.sh
  # mas precisa ficar aqui, porque o $disco tem que ir pronto
  # sem a barra do final da string, pro mt_save.sh.
  # ============================================
  function preparaDiretorio(){
    local complete_path=''

    # pega o ultimo caractere de $diretorio_do_disco
    local last_char="${diretorio_do_disco: -1}"

    # verifica se o ultmo caractere é uma barra.
    # Precisa garantir que foi passado o diretório
    # sem a barra no final, pra não dar erro no cp.
    if [ "$last_char" == "/" ];then
      # string sem o ultimo caractere
      diretorio_do_disco="${diretorio_do_disco:: -1}"
    fi

    # verifica se no path contem espaços, e remove.
    # se não, dá erro.
    # e cria uma pasta temporária onde vai ser feita
    # as operações.
		disco=$(echo "$diretorio_do_disco" | tr ' ' '_')
    cp -r "$diretorio_do_disco" "$disco"_temp

    # arruma o nome delas, pra ficar mais fácil de capturar.
    cd "$disco"_temp
    complete_path=$(pwd)
    cd $funcoeszz_dir
    ./funcoeszz zzarrumanome -r $complete_path* > /dev/null
    cd "$script_dir"
  }

  # ============================================
  # Função que trata as entradas do usuário no menu
  # ============================================
  function handleUserInput(){
    local msg=$(print_info "Digite 'ok' para salvar o conteúdo ou 'c' para cancelar: ")

    while true; do
      echo ""
      print_info "[INFORMAÇÕES]:"
      print_info "As tags foram extraídas para o arquivo.json"
      print_info "coloque a imagem da capa do disco .jpg no mesmo diretório do json"
      echo ""

      read -p "$msg" resposta
      case $resposta in
        ok )
          ./mt_save.sh "$disco"
          exit $SUCESSO
        ;;

        [cC] )
          deleteTempFiles
          exit $SUCESSO
        ;;

        * )
          print_error "Responda apenas 'ok' ou 'c'"
          deleteTempFiles
          exit $ERRO
        ;;
      esac
    done
  }

  # ============================================
  # Função que deleta arquivos temporários.
  # ============================================
  function deleteTempFiles(){
    if [ -f "$JSON" ];then
      rm "$JSON"
    fi

    if [ -d "$disco"_temp ];then
      rm -rf "$disco"_temp
    fi
  }

  # ============================================
  # Função Main
  # ============================================
  function main(){
    preparaDiretorio

    ./mt_load.sh "$disco"
    handleUserInput
  }

  # Main
  # ----------------------------------------------------------------------------
  # trata interrrupção do script em casos de ctrl + c (SIGINT) e kill (SIGTERM)
  trap exception SIGINT SIGTERM
  validacoes
  main

  # ----------------------------------------------------------------------------
  # FIM do Script =D
