# ##############################################################################
# [Descrição]:
#   Script que faz o cálculo da data da páscoa, e a aprtir disse, descobre 3 datas
#     - carnaval de Byron (em Caruaru)
#     - carnaval de Recife
#     - Semana Santa
#   Uma vez que o script descobre, utiliza a API do Google para setar essas
#   datas no Google calendar
#
# [Uso]:
#   ./carnaval_api_calendar.py
#
# [Referencies]:
#   1. https://developers.google.com/calendar/quickstart/python
#   2. https://developers.google.com/calendar/v3/reference/events/insert#examples_1
# ##############################################################################

import datetime
import controller
import google_controller

# ============================================
# Função Main
# ============================================
def main():

    # ================ Init ================
    service = google_controller.google_authenticate()

    now = datetime.datetime.now()
    ano = now.year

    feriados_list = []

    print(" ========= Adicionando feriados =========")

    # ================ Feriados Dinâmicos ================
    pascoa_date = controller.calculate_pascoa()

    # Adicionando o Carnaval
    controller.add_carnaval(service, pascoa_date)

    # Adicionando a Semana Santa
    controller.add_semana_santa(service, pascoa_date)

    # Adicionando o Carnaval de Byron
    controller.add_carnaval_do_sucata(service, pascoa_date)

    # ================ Feriados Estáticos ================
    # 1 de Janeiro
    feriados_list.append({"ano": ano, "mes": 1, "dia": 1, "summary": "Ano Novo"})

    # 6 de Março
    feriados_list.append({"ano": ano, "mes": 3, "dia": 6, "summary": "Carta Magna"})

    # 21 de Abril
    feriados_list.append({"ano": ano, "mes": 4, "dia": 21, "summary": "Tiradentes"})

    # 1 de Maio
    feriados_list.append({"ano": ano, "mes": 5, "dia": 1, "summary": "Dia do Trabalhador"})

    # 24 de Junho
    feriados_list.append({"ano": ano, "mes": 6, "dia": 24, "summary": "São João"})

    # 16 de Julho
    feriados_list.append({"ano": ano, "mes": 7, "dia": 16, "summary": "Nossa Senhora do Carmo"})

    # 7 de Setembro
    feriados_list.append({"ano": ano, "mes": 9, "dia": 7, "summary": "Independência do Brasil"})

    # 12 de Outubro - Nossa Senhroa Aparecida
    feriados_list.append({"ano": ano, "mes": 10, "dia": 12, "summary": "Dia das Crianças"})

    # 2 de Novembro
    feriados_list.append({"ano": ano, "mes": 11, "dia": 2, "summary": "Finados"})

    # 15 de Novembro
    feriados_list.append({"ano": ano, "mes": 11, "dia": 15, "summary": "Proclamação da República"})

    # 8 de Dezembro
    feriados_list.append({"ano": ano, "mes": 12, "dia": 8, "summary": "Nossa Senhora da Conceição"})

    # 25 de Dezembro
    feriados_list.append({"ano": ano, "mes": 12, "dia": 25, "summary": "Natal"})

    # Ano Novo (ano seguinte)
    feriados_list.append({"ano": ano+1, "mes": 1, "dia": 1, "summary": "Ano Novo"})

    # adicionando todos os feriados d euma vez
    for index in range(len(feriados_list)):
      ano = feriados_list[index]["ano"]
      mes = feriados_list[index]["mes"]
      dia = feriados_list[index]["dia"]
      summary = feriados_list[index]["summary"]

      controller.add_feriado(service, ano, mes, dia, summary)

if __name__ == '__main__':
    main()
