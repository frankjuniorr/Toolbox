#!/bin/bash
# ----------------------------------------------------------------------------
# Monitor do Sistema
#
# Uso: ./monitor
#
# Autor: Frank Junior <frankcbjunior@gmail.com>
# Desde: 2013-07-22
# Versão: 1
# ----------------------------------------------------------------------------

# Configurações
# ----------------------------------------------------------------------------

# set:
# -e: se encontrar algum erro, termina a execução imediatamente
set -e

# Variáveis
# ----------------------------------------------------------------------------

# cores
# ----------------------------------------------------------------------------
# Bold
bold_yellow="$(tput setaf 3 2>/dev/null)$(tput bold 2>/dev/null || echo '\e[1;33m')"  # Yellow
bold_purple="$(tput setaf 5 2>/dev/null)$(tput bold 2>/dev/null || echo '\e[1;35m')"  # Purple
bold_cyan="$(tput setaf 6 2>/dev/null)$(tput bold 2>/dev/null || echo '\e[1;36m')"  # Cyan

# Reset
text_reset="$(tput sgr 0 2>/dev/null || echo '\e[0m')"  # text_ Resets

# Funcoes
# ----------------------------------------------------------------------------

# imprime msg amarelo
function print_info(){
echo -e "$1$2${text_reset}"
}

# Função que imprime as versões do DesktopEnvironment instalado
# pra dar suporte a outras DE, adicionar nessa função.
function desktop_environment_version(){
	if type gnome-shell > /dev/null 2>&1; then
			gnome_shell_version="\t$(gnome-shell --version)"
			print_info "\t${bold_yellow}Gnome Shell:" "${bold_cyan}${gnome_shell_version}"
	fi
}

# Função usada pra imprimir versões das ferramentas de desenvolvimento
function development_versions(){
	# versão do Node
	if type node > /dev/null 2>&1; then
		node_version="\t\t$(node --version)"
		print_info "\t${bold_yellow}Node: " "${bold_cyan}${node_version}"
	fi

	# versão do Npm
	if type npm > /dev/null 2>&1; then
		npm_version="\t\t$(npm --version)"
		print_info "\t${bold_yellow}Npm: " "${bold_cyan}${npm_version}"
	fi

	# versão do Python
	if type python3 > /dev/null 2>&1; then
		python3_version="\t$(python3 --version)"
		print_info "\t${bold_yellow}Python 3: " "${bold_cyan}${python3_version}"
	fi
}

# funcao para verificar o SO corrente e chamar seus respectivos comandos
function verifica_so(){
local current_so="$(uname -s)"
local memoria_valor=""

case "$current_so" in
		Linux)
			# comandos do Linux
			usuario_comando="\t"$(whoami)" - "$(uptime | cut -d " " -f4-5 | sed s/,//)""
			hostname_comando="\t"$(hostname)""
			SO_comando="\t\t"$(uname -s)""
			distribuicao_comando="\t"$(lsb_release -sd)" - ($(lsb_release -sc))"
			kernel="\t\t$(uname -r)"
			memoria_valor=$(free -m | grep "Mem" | awk '{print $2}')
			memoria_comando="\t$(echo "scale=2; $memoria_valor/1000" | bc) GB"
			processador_comando="\t$(grep 'model name' /proc/cpuinfo | uniq | cut -d ':' -f2 | sed s/\ //) x$(grep 'model name' /proc/cpuinfo | wc -l)"
			arquitetura_comando="\t"$(arch)""
			network_interfaces=$(ifconfig | cut -d " " -f1 | xargs -n 1 | grep -v "lo\|docker")
			;;
		Darwin)
			# comandos do Mac
			usuario_comando="\t"$(whoami)" - "$(uptime | cut -d " " -f5-6 | sed s/,//)""
			hostname_comando="\t"$(hostname)""
			computador_comando="\t$(get_info_mac 'SPHardwareDataType' 'Model Name')"
			versao_comando="\t\t$(get_info_mac 'SPSoftwareDataType' 'System Version')"
			memoria_comando="\t$(get_info_mac 'SPHardwareDataType' 'Memory')"
			processador_comando="\t$(get_info_mac 'SPHardwareDataType' 'Processor Name') \
				$(get_info_mac 'SPHardwareDataType' 'Processor Speed')"
			arquitetura_comando="\t"$(arch)""
			;;
		cygwin)
			# comandos do Cygwin
			usuario_comando="ainda nao implementado"
			hostname_comando="ainda nao implementado"
			SO_comando="ainda nao implementado"
			distribuicao_comando="ainda nao implementado"
			memoria_comando="ainda nao implementado"
			processador_comando="ainda nao implementado"
			arquitetura_comando="ainda nao implementado"
			echo "estou no cygwin"
			;;
		*)
			echo "Sistema Operacional incompatível com o script"
			exit 1
			;;
esac
}

# funcao para pegar as informacoes do MacOS baseado no 'system_profiler'
function get_info_mac(){
	system_profiler "$1" | grep "$2" | cut -d ":" -f2 | cut -c2-
}

# Main
# ----------------------------------------------------------------------------

clear
verifica_so

print_info "${bold_purple}Computador:"
print_info "\t${bold_yellow}usuario:" "${bold_cyan}${usuario_comando}"
print_info "\t${bold_yellow}hostname:" "${bold_cyan}${hostname_comando}"
if [ $(uname -s) = 'Linux' ]; then
	print_info "\t${bold_yellow}SO:" "${bold_cyan}${SO_comando}"
	print_info "\t${bold_yellow}Kernel:" "${bold_cyan}${kernel}"
	print_info "\t${bold_yellow}distribuicao:" "${bold_cyan}${distribuicao_comando}"
	desktop_environment_version
elif [ $(uname -s) = 'Darwin' ]; then
	print_info "computador:" "${computador_comando}"
	print_info "versao:" "${versao_comando}"
fi

print_info "${bold_purple}Hardware:"
print_info "\t${bold_yellow}memoria:" "${bold_cyan}${memoria_comando}"
print_info "\t${bold_yellow}processador:" "${bold_cyan}${processador_comando}"
print_info "\t${bold_yellow}arquitetura:" "${bold_cyan}${arquitetura_comando}"

print_info "${bold_purple}Rede:"
for interface in $network_interfaces;do
	local_ip=$(ifconfig $interface | grep "inet addr" | cut -d ":" -f2 | cut -d " " -f1)
	print_info "\t${bold_yellow}${interface}: ${bold_cyan}\t$local_ip"
done

print_info "${bold_purple}Versions:"
development_versions

