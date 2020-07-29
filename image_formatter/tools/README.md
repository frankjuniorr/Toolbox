## Ferramentas:
o script contém +4 ferramentas auxiliares que devem ser executadas separadamente.

### **1. `Analyze`**

Esse script, eu recomendo sempre rodar ele primeiro. Ele faz uma primeira análise do diretório passado por parâmetro mostrando algumas sugestões e sugerindo um backup. 

Exemplo de saída desse script:

```
Analyze folder:
/home/usuario/Images
===================================
Total files in this folder: 595
All file formats in folder: jpeg PNG png jpg mp4
Folder Size: 3.13 GB
===================================

Make the Backup?:
```

Se responder `yes` a essa entrada, ele criará uma cópia/backup desse path para `$HOME/Documents/backup_photos`.

Para usar essa ferramenta, é só rodar:
```
python3 tools/analyze.py <diretorio_das_fotos>
```

### **2. `get_exif_tags`**
Esse script exibe todas as tags EXIF de um arquivo único (pode ser imagem ou vídeo).

Exemplo de saída desse script:

```javascript
{
    "Composite:ImageSize": "1280 960",
    "Composite:Megapixels": 1.2288,
    "EXIF:ColorSpace": 1,
    "EXIF:Compression": 6,
    "EXIF:ExifImageHeight": 960,
    "EXIF:ExifImageWidth": 1280,
    "EXIF:ExifVersion": "0220",
    "EXIF:ImageUniqueID": "8702be0f7148f4ad0000000000000000",
    "EXIF:Orientation": 1,
    "EXIF:ResolutionUnit": 2,
    "EXIF:Software": "Picasa",
    "EXIF:ThumbnailImage": "(Binary data 5057 bytes, use -b option to extract)",
    "EXIF:ThumbnailLength": 5057,
    "EXIF:ThumbnailOffset": 282,
    "EXIF:XResolution": 72,
    "EXIF:YResolution": 72,
    "ExifTool:ExifToolVersion": 11.88,
    "File:BitsPerSample": 8,
    "File:ColorComponents": 3,
    "File:CurrentIPTCDigest": "d41d8cd98f00b204e9800998ecf8427e",
    "File:Directory": "<DIR>",
    "File:EncodingProcess": 0,
    "File:ExifByteOrder": "MM",
    "File:FileAccessDate": "2020:07:28 20:54:14-03:00",
    "File:FileInodeChangeDate": "2020:07:25 17:56:23-03:00",
    "File:FileModifyDate": "2020:05:25 09:43:18-03:00",
    "File:FileName": "<FILENAME>",
    "File:FilePermissions": 664,
    "File:FileSize": 131358,
    "File:FileType": "JPEG",
    "File:FileTypeExtension": "JPG",
    "File:ImageHeight": 960,
    "File:ImageWidth": 1280,
    "File:MIMEType": "image/jpeg",
    "File:YCbCrSubSampling": "2 2",
    "JFIF:JFIFVersion": "1 1",
    "JFIF:ResolutionUnit": 0,
    "JFIF:XResolution": 1,
    "JFIF:YResolution": 1,
    "Photoshop:IPTCDigest": "d41d8cd98f00b204e9800998ecf8427e",
    "SourceFile": "<PATH>",
    "XMP:XMPToolkit": "XMP Core 5.5.0"
}
```

### **3. `get_datetime_tags`**

Ferramenta auxiliar para extrair APENAS as datas das tags EXIF de um arquivo de imagem (foto/vídeo). Aceita um arquivo único ou um diretório. Caso seja um diretório, ele exibirá os dados de todas as imagens dentro do diretório.

Exemplo de saída desse script:

```
=================================
filename = <FILENAME>
originalTimeDate = None
createDate = None
modifyDate = 2020:05:25 09:43:18-03:00
```