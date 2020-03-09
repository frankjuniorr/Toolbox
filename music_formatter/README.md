music_formatter
===========

## Descrição
Script usado pra consertar tags ID3 de arquivos MP3. Ele escreve as tags, e cria uma estrutura de diretório própria.
De acordo com as seguintes padrão de nomeclatura:

### 1. Para um disco comum:

```
[+] <artista>
  [+] <ano> - <disco>
  [-] <numero> - <nome>.mp3
```

Ex:
```
[+] Gilberto Gil
  [+] 1972 - Expresso 2222
  [-] 01 - Pipoca Moderna.mp3
```

## Uso
```
  ./music_formatter.sh <disco>
```

Ex:
```
  ./music_formatter.sh Gilberto\ Gil\ Expresso\ 2222
```

## Funcionalidades
  1. O script ler as tags e salva em um arquivo.json criado na hora
  2. o usuário edita esse arquivo json manualmente, enquanto o terminal está bloqueante esperando.
  3. Uma vez o json salvo, o script ler essas novas informações escritas pelo usuário.
  4. Escreve as tags em todos os arquivos de mp3.
  5. cria a estrutura de diretório descrita acima.

## Dependência
1. [jq](https://stedolan.github.io/jq/) --> ferramenta que facilita a leitura de json.
  
2. [funcoeszz](http://funcoeszz.net/) do [@aureliojargas](https://github.com/aureliojargas) --> Série de funções úteis para linha de comando no linux. No caso, esse escript usa uma função específica para auxiliar na renomeação de arquivos
  
3. id3v2 --> ferramenta que ler e escreve tags ID3.
  
4. [eyeD3](http://eyed3.nicfit.net/) --> ferramenta que ler e escreve tags ID3.
