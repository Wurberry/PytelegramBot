import telebot
import requests
import time
import json
from telebot import types


bot = telebot.TeleBot("1532138139:AAHVrVN25s3YKZ1EH50dLj_JhhDRHZiRYAc")
valute = ["usd", "aud", "brl", "cad", "chf", "clp", "cny", "dkk", "eur", "gbp", "hkd", "inr", "isk", "jpy", "krw", "nzd",
          "pln", "rub", "sek", "sgd", "thb", "try", "twd"]


user_choice = ""


def getjson(source):
    return requests.get(source).text


s = json.loads(getjson("https://blockchain.info/ru/ticker"))
save_s = [s, s]


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    active = False
    last_choice = ""
    if call.data == "RUB":
        bot.send_message(call.message.chat.id, text="RUB")
        bot.send_message(call.message.chat.id, 'buy: ' + str(s["RUB"]["buy"]))
        bot.send_message(call.message.chat.id, 'sell: ' + str(s["RUB"]["sell"]))
        if not active:
            user_choice = "RUB"
            active = True;
        else: last_choice = "RUB"
    if call.data == "USD":
        bot.send_message(call.message.chat.id, text="USD")
        bot.send_message(call.message.chat.id, 'buy: ' + str(s["USD"]["buy"]))
        bot.send_message(call.message.chat.id, 'sell: ' + str(s["USD"]["sell"]))
        if not active:
            user_choice = "USD"
            active = True;
        else: last_choice = "USD"
    if call.data == "EUR":
        bot.send_message(call.message.chat.id, text="EUR")
        bot.send_message(call.message.chat.id, 'buy: ' + str(s["EUR"]["buy"]))
        bot.send_message(call.message.chat.id, 'sell: ' + str(s["EUR"]["sell"]))
        if not active:
            user_choice = "EUR"
            active = True;
        else: last_choice = "EUR"
    if active:
        time.sleep(5*60)
        bot.send_message(call.message.chat.id, text = user_choice)
        bot.send_message(call.message.chat.id, 'buy: ' + str(s[user_choice]["buy"]))
        bot.send_message(call.message.chat.id, 'sell: ' + str(s[user_choice]["sell"]))
        active = False
        user_choice = last_choice
        last_choice = ""
    if call.data == "view":
        view_valute(call)
    if call.data == "control":
        control_valute(call)


@bot.message_handler(commands=['start'])
def start_commands(message):
    bot.send_message(message.from_user.id,
                     "Привет, данный бот позволяет узнать курс биткоина в интересующей тебя валюте")
    keyboard = types.InlineKeyboardMarkup()
    key_view = types.InlineKeyboardButton(text='Просмотреть валюты', callback_data='view')
    key_control = types.InlineKeyboardButton(text='Отслеживать валюту', callback_data='control')
    keyboard.add(key_view, key_control)
    bot.send_message(message.from_user.id, text="Выбери итересующую тебя валюту. Список самых популярных валют ниже:", reply_markup=keyboard)
    bot.send_message(message.from_user.id, message)

@bot.message_handler(commands=['view_valute'])
def view_valute(message):
    bot.send_message(message.from_user.id, "Введите интересующую вас валюту данного формата 'RUB'")


@bot.message_handler(commands=['control_valute'])
def control_valute(message):
    keyboard = types.InlineKeyboardMarkup()
    key_rub = types.InlineKeyboardButton(text='RUB - ₽', callback_data='RUB')
    key_usd = types.InlineKeyboardButton(text='USD - $', callback_data='USD')
    key_eur = types.InlineKeyboardButton(text='EUR - €', callback_data='EUR')
    keyboard.add(key_rub, key_usd, key_eur)
    bot.send_message(message.from_user.id, text="Выбери итересующую тебя валюту. Список самых популярных валют ниже:",
                     reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def help_commands(message):
    bot.send_message(message.from_user.id, "Напиши 'hi'")


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if save_s[0] != s:
        save_s[0] = s
        bot.send_message((message.from_user.id, save_s[0]))
    if message.text.lower() == "hi":
        bot.send_message(message.from_user.id, "Привет")
    if message.text.lower() in valute:
        try:
            bot.send_message(message.from_user.id, s[message.text]["symbol"])
            bot.send_message(message.from_user.id, 'buy: ' + str(s[message.text]["buy"]))
            bot.send_message(message.from_user.id, 'sell: ' + str(s[message.text]["sell"]))
            user_choice = message.text
        except KeyError:
            bot.send_message(message.from_user.id, "Пожалуйста, введите валюту заглавными символами")


bot.polling(none_stop=True)