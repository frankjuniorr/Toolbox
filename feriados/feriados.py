# ##############################################################################
# [Descrição]:
#   Script que adiciona todos os feriados do ano, de uma vez só, no Google Calendar.
#     OBS: Ele só adiciona os feriados que não caem no sábado ou domingo.
#     OBS2: O script também adiciona o carnaval \o/
#
# [Uso]:
#   ./feriados.py
#
# [Referencias]:
#   1. https://developers.google.com/calendar/quickstart/python
#   2. https://developers.google.com/calendar/v3/reference/events/insert#examples_1
# ##############################################################################

import datetime
import controller
import google_controller

# ============================================
# Função que adiciona todos os feriados que tem data dinâmica
# ============================================
def feriados_dinamicos(service, ano):
  pascoa_date = controller.calculate_pascoa(ano)

  # Adicionando o Carnaval
  controller.add_carnaval(service, pascoa_date)

  # Adicionando a Semana Santa
  controller.add_semana_santa(service, pascoa_date)

# ============================================
# Função que adiciona todos os feriados que tem data fixa.
# ============================================
def feriados_estaticos(service, ano):
    feriados_list = []

    # 1 de Janeiro
    feriados_list.append({"mes": 1, "dia": 1, "summary": "Ano Novo"})

    # 6 de Março
    feriados_list.append({"mes": 3, "dia": 6, "summary": "Carta Magna"})

    # 21 de Abril
    feriados_list.append({"mes": 4, "dia": 21, "summary": "Tiradentes"})

    # 1 de Maio
    feriados_list.append({"mes": 5, "dia": 1, "summary": "Dia do Trabalhador"})

    # 24 de Junho
    feriados_list.append({"mes": 6, "dia": 24, "summary": "São João"})

    # 16 de Julho
    feriados_list.append({"mes": 7, "dia": 16, "summary": "Nossa Senhora do Carmo"})

    # 7 de Setembro
    feriados_list.append({"mes": 9, "dia": 7, "summary": "Independência do Brasil"})

    # 12 de Outubro - Nossa Senhroa Aparecida
    feriados_list.append({"mes": 10, "dia": 12, "summary": "Dia das Crianças"})

    # 2 de Novembro
    feriados_list.append({"mes": 11, "dia": 2, "summary": "Finados"})

    # 15 de Novembro
    feriados_list.append({"mes": 11, "dia": 15,"summary": "Proclamação da República"})

    # 8 de Dezembro
    feriados_list.append({"mes": 12, "dia": 8,"summary": "Nossa Senhora da Conceição"})

    # 25 de Dezembro
    feriados_list.append({"mes": 12, "dia": 25, "summary": "Natal"})

    # adicionando todos os feriados d euma vez
    for index in range(len(feriados_list)):
      mes = feriados_list[index]["mes"]
      dia = feriados_list[index]["dia"]
      summary = feriados_list[index]["summary"]

      controller.add_feriado(service, ano, mes, dia, summary)

# ============================================
# Função Main
# ============================================
def main():
    # Autenticação e obtenção do ID referente a um calendário chamado "feriado"
    service = google_controller.google_authenticate()
    google_controller.GetFeriadosCalendarId(service)

    print(" ========= Adicionando feriados =========")
    ano = datetime.datetime.now().year

    # se eu rodar esse script no mês de dezembro, ele incrementa o 'ano'
    # e já adiciona os feriados do ano seguinte.
    mes = datetime.datetime.now().month
    DEZEMBRO = 12
    if mes == DEZEMBRO:
      ano = ano + 1

    # # ================ Feriados Dinâmicos ================
    feriados_dinamicos(service, ano)

    # # ================ Feriados Estáticos ================
    feriados_estaticos(service, ano)

if __name__ == '__main__':
    main()
