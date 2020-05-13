from datetime import datetime
import math

records = [
    {'source': '48-996355555', 'destination': '48-666666666',
        'end': 1564610974, 'start': 1564610674},
    {'source': '41-885633788', 'destination': '41-886383097',
        'end': 1564506121, 'start': 1564504821},
    {'source': '48-996383697', 'destination': '41-886383097',
        'end': 1564630198, 'start': 1564629838},
    {'source': '48-999999999', 'destination': '41-885633788',
        'end': 1564697158, 'start': 1564696258},
    {'source': '41-833333333', 'destination': '41-885633788',
        'end': 1564707276, 'start': 1564704317},
    {'source': '41-886383097', 'destination': '48-996384099',
        'end': 1564505621, 'start': 1564504821},
    {'source': '48-999999999', 'destination': '48-996383697',
        'end': 1564505721, 'start': 1564504821},
    {'source': '41-885633788', 'destination': '48-996384099',
        'end': 1564505721, 'start': 1564504821},
    {'source': '48-996355555', 'destination': '48-996383697',
        'end': 1564505821, 'start': 1564504821},
    {'source': '48-999999999', 'destination': '41-886383097',
        'end': 1564610750, 'start': 1564610150},
    {'source': '48-996383697', 'destination': '41-885633788',
        'end': 1564505021, 'start': 1564504821},
    {'source': '48-996383697', 'destination': '41-885633788',
        'end': 1564627800, 'start': 1564626000}
]


def calculate_price(initial, end):

    initial = datetime.fromtimestamp(int(initial))
    end = datetime.fromtimestamp(int(end))

    # início e final da chamada em horário de tarifa comum
    if((initial.hour < 22 and end.hour < 22) and (initial.hour >= 6 and end.hour >= 6)):
        rawMinutesDuration = (end - initial).seconds/60
        minutesDuration = math.floor(rawMinutesDuration)
        finalPrice = (minutesDuration*0.09) + 0.36
        return finalPrice

    # Início e fim de chamado no horário sem tarifa
    elif((initial.hour >= 22 and end.hour >= 22) or (initial.hour < 6 and end.hour < 6)):
        return 0.36

    # casos especiais com inicio em horario sem tarifa e fim em horario
    # com tarifa comum e vice-versa
    else:
        # se terminar a chamada as 22:00:xx, verificar se o último pulso será
        # cobrado
        if (end.hour == 22 and end.minute == 0):
            if(end.second >= initial.second):
                end = datetime(
                    end.year, end.month, end.day, 22, 00, 59)
            else:
                end = datetime(
                    end.year, end.month, end.day, 22)

        # caso seja depois das 22:01, cobrar até as 22:00:59
        elif (end.hour >= 22):
            end = datetime(
                end.year, end.month, end.day, 22, 00, 59)

        # caso a ligação tenha início antes das 6:00, considerar inicio de
        # cobraça às 6:00
        if (initial.hour < 6):
            initial = datetime(
                initial.year, initial.month, initial.day, 6)

        duration = int(math.floor((end - initial).seconds/60))
        finalPrice = (duration*0.09) + 0.36
        return finalPrice


def classify_by_phone_number(records):
    results = []

    # percorrer todo o array records para registrar as chamadas
    for record in records:
        i = 0  # variável para verificar se encontrou o source no results

        # percorrer todo o array de results para verificar se temos o source
        for result in results:

            # caso já tenha o source em results, somará o valor da chamada
            # ao total
            if result['source'] == record['source']:
                i = 1
                previous = result['total']
                current = calculate_price(record['start'], record['end'])
                updated = round((previous + current), 2)
                result['total'] = updated
                break

        # c caso não encontre o source em results, irá criar um novo registro e
        # inserir o valor da ligação
        if i == 0:
            price = calculate_price(record['start'], record['end'])
            priceRounded = round(price, 2)
            results.append(
                {'source': record['source'], 'total': priceRounded})

    finalResult = sorted(results, key=lambda i: i['total'], reverse=True)
    return finalResult
