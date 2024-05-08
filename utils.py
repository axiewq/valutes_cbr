import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def get_historical_data(start_date, end_date, currency):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    historical_data = {}
    current_date = start_date

    while current_date <= end_date:
        date_str = current_date.strftime('%d/%m/%Y')
        url = f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={date_str}'
        response = requests.get(url)
        root = ET.fromstring(response.content)

        for valute in root.findall('Valute'):
            if valute.find('CharCode').text == currency:
                value = valute.find('Value').text.replace(',', '.')
                historical_data[current_date.date().strftime('%d.%m.%Y')] = float(value)

        current_date += timedelta(days=1)

    return historical_data

def plot_historical_data(start_date, end_date, currency):
    data_dict = get_historical_data(start_date, end_date, currency)
    dates = list(data_dict.keys())
    values = list(data_dict.values())

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(dates, values)
    ax.set_title(f'График изменения курса валюты {currency}', fontsize=16)
    ax.set_xlabel('Date', fontsize=14)
    ax.set_ylabel('Exchange Rate', fontsize=14)
    ax.tick_params(axis='both', which='major', labelsize=8)
    ax.grid(True)
    plt.xticks(rotation=45)
    plt.show()

def convert_currencies(from_currency, to_currency): #Конвертер валют
    url = 'https://www.cbr.ru/scripts/XML_daily.asp'
    response = requests.get(url)
    root = ET.fromstring(response.content)

    from_value = None
    to_value = None

    for valute in root.findall('Valute'):
        if valute.find('CharCode').text == from_currency:
            from_value = float(valute.find('Value').text.replace(',', '.'))
        elif valute.find('CharCode').text == to_currency:
            to_value = float(valute.find('Value').text.replace(',', '.'))

    if from_value and to_value:
        ratio_from_to = to_value / from_value
        ratio_to_from = from_value / to_value

        return f"1 {from_currency} = {ratio_from_to:.4f} {to_currency}\n1 {to_currency} = {ratio_to_from:.4f} {from_currency}"

    elif from_currency == 'RUB':
        return f"1 RUB = {(1/to_value):.4f} {to_currency}\n1 {to_currency} = {to_value:.4f} RUB"

    elif to_currency == 'RUB':
        return f"1 {from_currency} = {(1/from_value):.4f} RUB\n1 RUB = {from_value:.4f} {from_currency}"

    else:
        return "Ошибка: одна или обе валюты не найдены."
