Formatador de diretório de imagens
==============

## Objetivo
Renomear de forma padroniazda todos os arquivos de um diretório de imagem

## Uso
Uso: `image_formatter <diretorio_de_imagem>`

Ex.: `./image_formatter $HOME/minhas-imagens/`

## Dependências
* [**funcoeszz**](https://github.com/aureliojargas/funcoeszz) do [@oreio](https://twitter.com/oreio)

  depende da `zzarrumanome` e `zznomefoto`

## Saída Esperada
Ex de diretório:

```
/minhas-imagens
  |--- Churrasco 2012
        |--- PIC0123.jpg
        |--- PIC456789.jpg
        |--- PIC78912458.jpg
        |--- PIC002345.jpg
        |--- Churrasco 1.jpg
        |--- Churrasco 2.jpg
        |--- ChUrrAscO 3.jpg
  |--- Aniversário de Fulano
        |--- IMG1.JPG
        |--- IMG 2.JPG
        |--- IMG-3.JPG
        |--- Aniversário de Fúlano.JPG
```

Depois do script:

```
/minhas-imagens
  |--- churrasco_2012
        |--- churrasco_2012-001.jpg
        |--- churrasco_2012-002.jpg
        |--- churrasco_2012-003.jpg
        |--- churrasco_2012-004.jpg
        |--- churrasco_2012-005.jpg
        |--- churrasco_2012-006.jpg
        |--- churrasco_2012-007.jpg
  |--- aniversario_de_fulano
        |--- aniversario_de_fulano-001.jpg
        |--- aniversario_de_fulano-002.jpg
        |--- aniversario_de_fulano-003.jpg
        |--- aniversario_de_fulano-004.jpg
```
