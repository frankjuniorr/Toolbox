extract
===========

## Descrição
Extrai vários tipos de arquivos compactados (zip, rar, 7z...etc)

## Use
```bash
./extract <filename>
```

## Use - Docker

Isso é legal para resolver todas as dependencias
```bash
# build image
docker build \
  --build-arg UID=$(id -u) \
  --build-arg GID=$(id -g) \
  -t extract:1.0 .

# run image
docker run --rm -v $(pwd):/home/docker extract:1.0 <zip_filename>
```

## Dica: Use como alias no `~/.bashrc`

```bash
function extract(){
	local zip_filename="$1"
	local image_name="extract:1.0"

	# verificando se o parametro foi passado corretamente
	test -z "$zip_filename" && echo "passe um arquivo por parametro" && return 1
  test ! -f "$zip_filename" && echo "passe um arquivo válido" && return 1

	# caso não exista a imagem, builde (docker build)
	if [ ! $(docker images -q $image_name | wc -l 2> /dev/null) -eq 1 ]; then
		echo "buildando a imagem"
		echo
		docker build \
  		--build-arg UID=$(id -u) \
			--build-arg GID=$(id -g) \
			-t $image_name "<PATH/DESSE/REPO>/extract"
	fi

	# execute a imagem sem o '--rm'. Se deletar o container agora, o comando abaixo vai dar errado.
	docker run -v "$(pwd)/${zip_filename}:/home/docker/${zip_filename}" $image_name $zip_filename

	# pegue o id do container
	local container_id=$(docker container ls -a | grep "$image_name" | awk '{print $1}')

	# copie o arquivo extraído que está dentro do container para a pasta corrente
	# OBS: essa expansão de variável remove o formato do arquivo do nome.
	# Ficando assim apenas o nome da pasta que estava dentro do zip
	echo "copiando arquivo extraído"
	docker cp "${container_id}:/home/docker/${zip_filename%.*}" ${zip_filename%.*}

	# agora sim, delete o container na mão.
	echo "deletando o container"
	docker rm "$container_id"
}
```