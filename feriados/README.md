Feriados
===========

## Descrição
Script que adiciona todos os feriados do ano, de uma vez só, no Google Calendar.

OBS: O script adiciona os feriados num calendário à parte no Google Calendar chamado "Feriados"

OBS-2: Ele só adiciona os feriados que não caem no sábado ou domingo.

OBS-3: O script também adiciona o carnaval \o/

## Google Calendar
Antes de mais nada, crie no seu Google Calendar, um calendário chamado `Feriados`. É esse calendário que o script irá usar.

## Google Cloud Plataform

O script utiliza a API do Google Calendar pra conseguir inserir os eventos lá. O tutorial abaixo mostra como habilitar essas APIs no GCP, e gerar o arquivo `credentials.json`

1. Acesse o link: [console.cloud.google.com](https://console.cloud.google.com)

2. crie um novo Projeto

3. Vá em `APis & Library > Library`, e busque pelas API do `Google Calendar`

4. Na aba de `Credencials` crie uma nova `Credential` do tipo `Computer App`. Uma vez criada, faça o download do arquivo `credentials.json`

Pronto, basicamente aqui acaba a parte burocrática do Google.

## Dependencias

Instale as depedencias de código
```bash
pip3 install -r requirements.txt
```

## Use
```bash
python3 feriados.py
```

OBS: Ele irá abrir o browser na primeira vez, pedindo pra se autenticar no app. Siga o processo e ele ira gerar um arquivo local chamado `token.pickle`.

<HR>

## Links Úteis

### Quickstart
- https://developers.google.com/calendar/quickstart/python

### Documentação usada:

- https://developers.google.com/calendar/v3/reference/events/insert
- https://developers.google.com/calendar/v3/reference/calendarList/list
- https://developers.google.com/calendar/create-events#python