import requests
import json
import telebot
from config import keys, TOKEN

bot = telebot.TeleBot(TOKEN)


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def converter(values):
        if len(values) != 3:
            raise APIException('Количество параметров некорректно')

        quote, base, amount = values

        if quote == base:
            raise APIException('Указаны одинаковые валюты')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Валюта {quote} не опознана')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Валюта {base} не опознана')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException('Количество валюты указано некорректно')
        r = requests.get('https://www.cbr-xml-daily.ru/latest.js')
        if keys[base] == 'RUB':
            rub_base = 1
        else:
            rub_base = json.loads(r.content)['rates'][base_ticker]
        if keys[quote] == 'RUB':
            rub_quote = 1
        else:
            rub_quote = json.loads(r.content)['rates'][quote_ticker]

        total_base = float(rub_base)/float(rub_quote)

        return total_base
