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


def check_day_period(initial, end):
    if((initial.hour < 22 and end.hour < 22) and (initial.hour >= 6 and end.hour >= 6)):
        return 'normal_rate'
    if((initial.hour >= 22 and end.hour >= 22) or (initial.hour < 6 and end.hour < 6)):
        return 'low_rate'
    else:
        return 'mixed_rate'


def calculate_final_price(initial, end):
    duration = int(math.floor((end - initial).seconds/60))
    final_price = (duration*0.09) + 0.36
    return final_price


def calculate_price(initial, end):

    initial = datetime.fromtimestamp(int(initial))
    end = datetime.fromtimestamp(int(end))
    period = check_day_period(initial, end)

    if(period == 'low_rate'):
        return 0.36

    if(period == 'normal_rate'):
        final_price = calculate_final_price(initial, end)
        return final_price

    if(period == 'mixed_rate'):

        if (end.hour >= 22, end.minute >= 1):
            end = datetime(
                end.year, end.month, end.day, 22, 00, 59)

        if (initial.hour < 6):
            initial = datetime(
                initial.year, initial.month, initial.day, 6)

        final_price = calculate_final_price(initial, end)
        return final_price


def classify_by_phone_number(records):
    results = []

    for record in records:
        i = 0
        price = calculate_price(record['start'], record['end'])

        for result in results:

            if result['source'] == record['source']:
                i = 1
                previous = result['total']
                updated = round((previous + price), 2)
                result['total'] = updated
                break

        if i == 0:
            price_rounded = round(price, 2)
            results.append(
                {'source': record['source'], 'total': price_rounded})

    final_result = sorted(results, key=lambda i: i['total'], reverse=True)
    return final_result
