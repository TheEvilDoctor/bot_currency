import telebot

from extentions import APIException, CryptoConverter
from config import keys, TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = f'''Для того, чтобы узнать стоимость опр. кол-ва валюты в другой валюте (по данным ЦБР), \
Вам необходимо отправить сообщение боту в виде:\n
<имя валюты, стоимость которой хотите узнать> <имя валюты, в которой нужно узнать стоимость> <кол-во первой валюты> \n
/help или /start - вызов справки \n
/values - список доступных валют'''
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):

    # base - имя валюты, цену на которую надо узнать
    # total_base - цена на base
    # quote - имя валюты, цену в которой надо узнать
    # amount - количество переводимой валюты — amount

    try:
        values_mes = message.text.split(' ')
        total_base = CryptoConverter.converter(values_mes)
        quote, base, amount = values_mes
    except APIException as e:
        bot.reply_to(message, e)
    except Exception as e:
        bot.reply_to(message, 'Не удалось обработать запрос')
    else:
        text = f'{amount} ({quote}) = {total_base * amount} ({base})'
        bot.send_message(message.chat.id, text)


bot.polling()
