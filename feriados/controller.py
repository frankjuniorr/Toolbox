import datetime
import math
import google_controller

# ============================================
# Função que calcula a data da páscoa,
# segundo o algoritmo de
# Jean Baptiste Joseph Delambre (1749-1822)
# link: (http://www.ghiorzi.org/portug2.htm)
# ============================================
def calculate_pascoa():
    pascoa_dia = pascoa_mes = a = b = c = d = e = f = g = h = i = k = l = m = p = q = r = s = None

    now = datetime.datetime.now()
    ano = now.year

    a = math.trunc(ano % 19)
    b = math.trunc(ano / 100)
    c = math.trunc(ano % 100)
    d = math.trunc(b / 4)
    e = math.trunc(b % 4)
    f = math.trunc((b + 8) / 25)
    g = math.trunc((b - f + 1) / 3)
    h = math.trunc((19*a + b - d - g + 15) % 30)
    i = math.trunc(c / 4)
    k = math.trunc(c % 4)
    l = math.trunc((32 + 2*e + 2*i - h - k) % 7)
    m = math.trunc((a + 11*h + 22*l) / 451)
    p = math.trunc((h + l - 7*m + 114) / 31)
    q = math.trunc((h + l - 7*m + 114) % 31)

    pascoa_dia = q+1
    pascoa_mes = p

    return datetime.date(ano, pascoa_mes, pascoa_dia)

# ============================================
# Função auxiliar que verifica se o feriado é
# diferente de sabado e domingo.
#
# return: dictionary - datas
# ============================================
def feriado_check(feriado_data):
  datas = start_date = end_date = None
  feriado_dia = feriado_data.strftime("%A")

  # se não for sabado e domingo, adicione
  if feriado_dia != 'Saturday' and feriado_dia != 'Sunday':
    if feriado_dia == 'Monday' or feriado_dia == 'Wednesday' or feriado_dia == 'Friday':

      start_date = feriado_data.strftime("%Y-%m-%d")
      end_date = feriado_data.strftime("%Y-%m-%d")

    # quinta-feira é feriado emendado
    elif feriado_dia == 'Thursday':
      # esse "dia a mais" é necessaŕio, pq o "end-date" não é inclusive, é "exclusive" na Api do Google
      friday = feriado_data + datetime.timedelta(days=2)

      start_date = feriado_data.strftime("%Y-%m-%d")
      end_date = friday.strftime("%Y-%m-%d")

    # terça-feria é feriado emendado
    elif feriado_dia == 'Tuesday':
      monday = feriado_data - datetime.timedelta(days=1)
      # esse "dia a mais" é necessaŕio, pq o "end-date" não é inclusive, é "exclusive" na Api do Google
      tuesday = feriado_data + datetime.timedelta(days=1)

      start_date = monday.strftime("%Y-%m-%d")
      end_date = tuesday.strftime("%Y-%m-%d")

  datas = {"start_date": start_date, "end_date": end_date}
  return datas

# ============================================
# Função que adiciona a data do carnaval
# ============================================
def add_carnaval(service, pascoa_date):
  carnaval_inicio = pascoa_date - datetime.timedelta(days=51)
  carnaval_fim = carnaval_inicio + datetime.timedelta(days=6)

  carnaval_inicio_string = carnaval_inicio.strftime("%Y-%m-%d")
  carnaval_fim_string = carnaval_fim.strftime("%Y-%m-%d")

  event = {
      "summary": "Carnaval",
      "description": "Carnaval do Recife",
      "startDate": carnaval_inicio_string,
      "endDate": carnaval_fim_string,
  }

  google_controller.setGoogleCalendar(event, service)

# ============================================
# Função que adiciona a data do carnaval do Sucata
# ============================================
def add_carnaval_do_sucata(service, pascoa_date):
  carnaval_inicio = pascoa_date - datetime.timedelta(days=51)

  carnaval_de_byron = carnaval_inicio - datetime.timedelta(days=6)
  carnaval_de_byron_string = carnaval_de_byron.strftime("%Y-%m-%d")

  event = {
    "summary": "Carnaval do Sucata",
    "description": "Carnaval de caruaru",
    "startDate": carnaval_de_byron_string,
    "endDate": carnaval_de_byron_string,
  }

  google_controller.setGoogleCalendar(event, service)

# ============================================
# Função que adiciona a data da Semana Santa
# ============================================
def add_semana_santa(service, pascoa_date):
  semana_santa_inicio = pascoa_date - datetime.timedelta(days=7)
  semana_santa_fim = pascoa_date

  semana_santa_inicio_string = semana_santa_inicio.strftime("%Y-%m-%d")
  semana_santa_fim_string = semana_santa_fim.strftime("%Y-%m-%d")

  event = {
    "summary": "Semana Santa",
    "description": "Semana Santa",
    "startDate": semana_santa_inicio_string,
    "endDate": semana_santa_fim_string,
  }

  google_controller.setGoogleCalendar(event, service)


# ============================================
# Função genérica que adiciona qualquer feriado
# ============================================
def add_feriado(service, ano, mes, dia, summary):

  feriado = datetime.date(ano, mes, dia)
  feriado_datas = feriado_check(feriado)

  if feriado_datas["start_date"] != None:
    event = {
        "summary": f"[FERIADO] {summary}",
        "description": summary,
        "startDate": feriado_datas["start_date"],
        "endDate": feriado_datas["end_date"],
    }

    google_controller.setGoogleCalendar(event, service)
