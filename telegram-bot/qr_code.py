import telebot
from telebot import types
from generator import qr_gen
from io import BytesIO
import requests

my_id = 259969071
with open("token.txt", mode='r') as tok:
    TOK = str(tok.read(46))

bot = telebot.TeleBot(TOK)
telebot.ENABLE_MIDDLEWARE = True


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Тут ты можешь создать QR-код в стиле Нового Физтеха.')
    markup = types.ReplyKeyboardMarkup()
    itembtna = types.KeyboardButton('Ссылка 🔗')
    itembtnv = types.KeyboardButton('Контакт')
    itembtnc = types.KeyboardButton('Текст')
    itembtnd = types.KeyboardButton('Wi-Fi')
    markup.row(itembtna, itembtnv)
    markup.row(itembtnc, itembtnd)
    bot.send_message(message.chat.id, "Выберите, для чего вам нужен код:", reply_markup=markup)


def get_ye():
    kanye = requests.get("https://api.kanye.rest/")
    kanye_tweet = kanye.text[10:-2]
    return kanye_tweet


# @bot.message_handler(commands=['command1'])
# def help(message):
#     bot.send_message(message.chat.id, 'Опишите вашу проблему, мы постараемся исправить всё в ближайшее время.')


@bot.message_handler(content_types=['text', 'image'])
def code_type(message):
    if message.text == 'Ссылка 🔗':
        msg = bot.reply_to(message, "Введите ссылку для создания QR-кода")
        bot.register_next_step_handler(msg, req_info_link)
    if message.text == 'Wi-Fi':
        msg = bot.reply_to(message, "Введите логин и пароль от WiFi сети через ';' (ex: MyWiFi;qwert54321)")
        bot.register_next_step_handler(msg, req_info_wifi)
    if message.text == 'Текст':
        msg = bot.reply_to(message, "Введите текст для создания QR-кода")
        bot.register_next_step_handler(msg, req_info_link)
    if message.text == 'Контакт':
        msg = bot.reply_to(message,
                           "Введите имя, номер телефона и почту вашего контакта через ';' (ex: Semyon;+79876543210;semyon@mail.com)")
        bot.register_next_step_handler(msg, reg_info_contact)


def req_info_link(msg):
    try:
        img = qr_gen(msg.text, type='default')
        bio = BytesIO()
        bio.name = 'image.png'
        img.save(bio, 'PNG')
        bio.seek(0)
        bot.send_photo(msg.chat.id, photo=bio)
    except Exception as e:
        bot.reply_to(msg, 'oooops')


def req_info_wifi(msg):
    try:
        text = msg.text
        wifi_name = text.split(';')[0]
        wifi_pass = text.split(';')[1]
        inp = 'WIFI:S:' + wifi_name + ';T:WPA;P:' + wifi_pass + ';;'
        img = qr_gen(inp, type='default')
        bio = BytesIO()
        bio.name = 'image.png'
        img.save(bio, 'PNG')
        bio.seek(0)
        bot.send_photo(msg.chat.id, photo=bio)
    except Exception as e:
        bot.reply_to(msg, 'oooops')


def reg_info_contact(msg):
    try:
        text = msg.text
        name = text.split(';')[0]
        phone = text.split(';')[1]
        email = text.split(';')[2]
        inp = 'BEGIN:VCARD\nN:' + name + '\nTEL:' + phone + '\nEMAIL:' + email + '\nVERSION:3.0\nEND:VCARD'
        img = qr_gen(inp, type='default')
        bio = BytesIO()
        bio.name = 'image.png'
        img.save(bio, 'PNG')
        bio.seek(0)
        bot.send_photo(msg.chat.id, photo=bio)
    except Exception as e:
        bot.reply_to(msg, 'oooops')


# RUN
if __name__ == '__main__':
    bot.polling(none_stop=True)
