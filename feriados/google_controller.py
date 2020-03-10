from __future__ import print_function

import os.path
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# arquivo de credencial do Google, que pode ser obtido aqui: https://developers.google.com/calendar/quickstart/python
GOOGLE_CREDENTIAL_FILE = 'credentials.json'

# Arquivo de token gerado automaticamente pelo Google,
# depois do primeiro login
GOOGLE_TOKEN_FILE = 'token.pickle'

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

service = None

# ============================================
# Função que autentica na API do Google
# ============================================
def google_authenticate():
  creds = None
  # The file token.pickle stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists(GOOGLE_TOKEN_FILE):
      with open(GOOGLE_TOKEN_FILE, 'rb') as token:
          creds = pickle.load(token)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
          creds.refresh(Request())
      else:
          flow = InstalledAppFlow.from_client_secrets_file(
              GOOGLE_CREDENTIAL_FILE, SCOPES)
          creds = flow.run_local_server(port=0)
      # Save the credentials for the next run
      with open(GOOGLE_TOKEN_FILE, 'wb') as token:
          pickle.dump(creds, token)

  service = build('calendar', 'v3', credentials=creds)
  return service

# ============================================
# Função que cria um evento no Google Calendar
# ============================================
def setGoogleCalendar(objeto, service):
  event = {
      'summary': f"[FERIADO] {objeto['summary']}",
      'description': objeto["description"],
      'start': {'date': objeto["startDate"]},
      'end': {'date': objeto["endDate"]}
  }

  event = service.events().insert(calendarId='primary', body=event).execute()
  event_link = event.get('htmlLink')
  feriado_summary = objeto["summary"]
  feriado_start_date = objeto["startDate"]

  print(f"[LOG]: {feriado_summary} ({feriado_start_date})")
  print(f"link: {event_link}")
  print("--------------------------------------------------")

  return
