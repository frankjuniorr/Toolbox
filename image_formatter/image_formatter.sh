#!/bin/bash

# Cabeçalho
# ----------------------------------------------------------------------------
# Padroniza todo o diretório de imagem, e todas as ".jpg"
# deixando no padrão da "zzarrumanome" e "zzarrumafoto"
#
# Uso: image_formatter <diretorio_de_imagem>
# Ex.: ./image_formatter $HOME/minha-imagens/
#
# Autor: Frank <frankcbjunior (a) gmail com>
# Desde: 2-10-2013
# Versão: 1
# ----------------------------------------------------------------------------

# Configurações
# ----------------------------------------------------------------------------

# set:
# -e: se encontrar algum erro, termina a execução imediatamente
set -e

# Variáveis
# ----------------------------------------------------------------------------

funcoeszz_dir=$(echo $ZZPATH | sed 's/\/funcoeszz$//')
diretorio_de_imagem="$1"
script_dir=$(pwd)

# debug = 0, desligado
# debug = 1, ligado
debug=0

# Cores
cor_vermelho="\033[31m"
cor_verde="\033[32m"
cor_amarelo="\033[33m"
fecha_cor="\033[m"

# funções
# ----------------------------------------------------------------------------

# **** Utils
# usada pra imprimir informação
function print_info(){
	printf "${cor_amarelo}$1${fecha_cor}\n"
}

# usada pra imprimir mensagem de sucesso
function print_success(){
	printf "${cor_verde}$1${fecha_cor}\n"
}

# usada pra imprimir erros
function print_error(){
	printf "${cor_vermelho}$1${fecha_cor}\n"
}

# funcao de debug
function debug_log(){
	[ "$debug" = 1 ] && print_info "[DEBUG] $*"
}
# **** [FIM] Utils


function validacoes(){
	# validação para saber se as funcoeszz estão instaladas
	if [ -z "$ZZPATH" ];then
		print_error "Provavelmente você não instalou as funcoeszz - esse script depende dela =("
		exit 1
	fi

	# checando se o parametro foi passado
	if [ "$diretorio_de_imagem" = "" ];then
		print_error "Uso: padronizador_de_diretorio_de_imagem <diretorio_de_imagem>"
		exit 1
	fi

	# verificando se o diretorio de imagem existe
	if [ ! -e "$diretorio_de_imagem" ];then
		print_error "diretorio nao existe"
		exit 1
	fi
}

# funcao para trocar o ".1" de lugar.
# eles são usados pelas zz para prevenir perda de arquivo.
# Mas eles são colocadas no final pelo zzarrumanome ficando assim: 'arquivo.jpg.1'.
# Logo, quando o script ia pra o proximo passo chamando a zznomefoto, ela ficava assim: 'foto-001.1'
# comendo a extensão. A solução foi criar essa função e mover os ".1" de lugar ficando assim:
# 'arquivo.jpg.1 --> arquivo.1.jpg', e quem faz isso é esses seds aí de baixo.
# Dessa maneira, a extensão não é "comida" pelas zz, e quando a zznomefoto executar, vai ficar certinho, assim:
# 'foto-001.jpg'. ;)
function retirar_ponto_1(){
	for arquivo_ponto_1 in $(find "$diretorio_de_imagem" -type "f" -iname "*.1");
	do
		path=$(echo $arquivo_ponto_1 | sed 's/\(.*\/\).*$/\1/');
		nome_novo=$(echo $arquivo_ponto_1 | sed 's/.*\/\(.*$\)/\1/;s/\./.1./1;s/.1$//g');
		mv -v $arquivo_ponto_1 "$path$nome_novo"
	done

}

# funcao para renomear também o diretório de imagem,
# substituindo os espaços em branco por underline.
# Se não fizer, o script quebra.
function padroniza_nome_diretorio(){
	local nome_novo=""
	if [ $(echo "$diretorio_de_imagem" | grep " " | wc -l) == "1" ];then
		nome_novo=$(echo "$diretorio_de_imagem" | tr ' ' '_')
		mv "$diretorio_de_imagem" "$nome_novo"
		diretorio_de_imagem="$nome_novo"
	fi
}

# padronizando todos os diretorios com o zzarrumanome
# OBS: Teoricamente, não precisa do parametro '-r'
# para a azzarrumanome, pois nesse caso, eu só quero
# renomear os diretorio. Mas se eu não fizer isso,
# eu precisarei rodar a 'zzminusculas' e o loop se bobear
# ficaria até maior. Com o '-r' ele roda a 'zzminusculas' por baixo.
function padroniza_nome(){
	print_info '##### Colocando todo mundo pra nome minusculo'
	cd $funcoeszz_dir
	./funcoeszz zzarrumanome -d -r "$diretorio_de_imagem"*
	cd "$script_dir"
}

# renomeando todos os arquivos
function renomea_todos_os_arquivos(){
	print_info '##### Padronizando todo os arquivos'
	cd $funcoeszz_dir
	for diretorio in "$diretorio_de_imagem"*;
	do
		if [ -d "$diretorio" ];then
			nome_do_diretorio=$(echo "$diretorio" | sed 's/.*\/\(.*$\)/\1/')
			./funcoeszz zznomefoto -p ""$diretorio"/"$nome_do_diretorio"-" "$diretorio"/*
		else
			nome_do_diretorio=$(echo "$diretorio_de_imagem" | sed 's/.*\/\(.*\)\/$/\1/')
			./funcoeszz zznomefoto -p ""$diretorio_de_imagem""$nome_do_diretorio"-" "$diretorio_de_imagem"*
			exit 0
		fi
	done
	cd "$script_dir"
}

# Main
# ----------------------------------------------------------------------------

validacoes

padroniza_nome_diretorio
padroniza_nome
retirar_ponto_1
renomea_todos_os_arquivos
