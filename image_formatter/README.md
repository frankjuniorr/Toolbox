Image File Formatter
==============

## Descrição
Renomeia de forma padronizada todos os arquivos de imagem/vídeo de acordo com algumas regras.

O script se baseia nas tags [EXIF](https://en.wikipedia.org/wiki/Exif) de cada arquivo, extraindo a data de criação deles. Caso o arquivo não tenha data de criação pra ser extraída, será usado a data de modificação, e aplicando no nome do arquivo. Com isso, o objetivo é ter todas as suas fotos/vídeos com a data que ela foi tirada no próprio nome do arquivo =D

Basicamente, as regras são:
- Pegar o `CreateDate` do EXIF e aplicar no nome do arquivo, nesse formato `YYYY-mm-dd_HH:MM:SS`
- Se o `CreateDate` não conseguir ser extraído, será usado o `ModificationDate`
- Concatena isso com o nome da pasta onde o arquivo está localizado.
- Remove todos os caracteres especiais do nome do arquivo, e passa tudo pra letra minúscula.

O objetivo é deixar o arquivo assim, ex: `2018-07-23_15:50:10_aniversario_de_fulano.jpg`

## Log

Existe a possibilidade de alguns arquivos terem exatamente o mesmo timedate (mesmo "ano-mes-dia-hora-minuto-segundo"). Para esses casos, os arquivos **NÃO** serão renomeados (apenas 1 deles, o arquivo repetido não) e terão seus endereços logados em outro arquivo de log sugerindo que são repetidos.

E todos os log serão salvos nessa pasta: `$HOME/log/image_formatter`

O arquivo de log é:
| Arquivo | Descrição |
| ------ | ------ |
| `%Y-%m-%d_%H:%M:%S_duplicated_files.log` | log contendo os arquivos "duplicados" (mesma data)  |


**Exemplo:**
- `2020-05-07_15:26:01_duplicated_files.log`

**Exemplo de Log:**

- `2020-05-07_15:26:01_duplicated_files.log`:
```
File 1.jpg
2020-05-07_15:26:01_aniversario_de_fulano.jpg

File 2.jpg
2020-05-07_20:10:12_aniversario_de_fulano.jpg
```

## Ferramentas:
o script contém +4 ferramentas auxiliares que devem ser executadas separadamente.
A descrição detalhada de cada uma pode ser acessa [aqui](https://github.com/frankjuniorr/Toolbox/tree/master/image_formatter/tools).

## Recomendações:

1. É recomendado sempre rodar a ferramenta `analyze` à parte sempre que necessário para fazer uma análise mais cautelosa sobre os arquivos.

2. Todo e qualquer software que renomeia arquivos é perigoso, qualquer bug inesperado um arquivo desse pode ser removido sem passar pela lixeira, logo, é sempre bom fazer um backup antes.

---

## Usando:

### Dependências:
Para instalar as depêndencias, só precisa executar:
```
./install_dependencies.sh
```

### Executando:
```
python3 app.py <diretorio_de_imagem>
```

Exemplo de saída desse script:
```
[LOG]: Standardize fileformats...
[LOG]: Before: /home/usuario/Documents/backup_photos/f28e6152-d7d4-4e54-ae94-7ef1e902260d.jpeg
[LOG]: After: /home/usuario/Documents/backup_photos/f28e6152-d7d4-4e54-ae94-7ef1e902260d.jpg
[LOG]: =======================

[LOG]: Renaming folders...
[LOG]: Extract dates from files...
[LOG]: Finding files...
[LOG]: Extracting exif...: 100%|████████████████████████████████████████████████████████████████████████████████████| 595/595 [00:11<00:00, 52.33it/s]

[LOG]: Renaming files...
[LOG]: Before: /home/usuario/Documents/backup_photos/f28e6152-d7d4-4e54-ae94-7ef1e902260d.jpg
[LOG]: After: /home/usuario/Documents/backup_photos/2016-12-17_21:32:11_backup_photos.jpg
[LOG]: =======================
[LOG]: Before: /home/usuario/Documents/backup_photos/2017-01-29 19.25.53.jpg
[LOG]: After: /home/usuario/Documents/backup_photos/2017-01-29_19:25:53_backup_photos.jpg
[LOG]: =======================
[LOG]: Before: /home/usuario/Documents/backup_photos/VID_20191123_180229.mp4
[LOG]: After: /home/usuario/Documents/backup_photos/2019-11-23_21:02:50_backup_photos.mp4
[LOG]: =======================
[LOG]: Before: /home/usuario/Documents/backup_photos/VID_20191123_195642.mp4
[LOG]: After: /home/usuario/Documents/backup_photos/2019-11-23_22:57:01_backup_photos.mp4
[LOG]: =======================

----------- SUMMARY -----------
Total files analyzed: 595
Files already ok: 0
Folders Renamed: 0
Files Renamed: 250
Files in Log : 333
Files in Log [Duplicated]: 12
```

---

## Saída Esperada no diretório
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
        |--- 2019-11-23_22:57:01_churrasco_2012.jpg
        |--- 2019-11-23_14:32:01_churrasco_2012.jpg
        |--- 2019-11-23_09:10:25_churrasco_2012.jpg
        |--- 2019-11-23_15:42:10_churrasco_2012.jpg
        |--- 2019-11-23_13:23:05_churrasco_2012.jpg
        |--- 2019-11-23_20:25:54_churrasco_2012.jpg
        |--- 2019-11-23_15:50:10_churrasco_2012.jpg
  |--- aniversario_de_fulano
        |--- 2018-07-23_15:50:10_aniversario_de_fulano.jpg
        |--- 2018-07-23_15:54:10_aniversario_de_fulano.jpg
        |--- 2018-07-23_16:00:15_aniversario_de_fulano.jpg
        |--- 2018-07-23_16:25:34_aniversario_de_fulano.jpg
```
