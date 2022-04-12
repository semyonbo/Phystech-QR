import telebot
from telebot import types
from generator import qr_gen
from io import BytesIO
import requests
my_id=259969071
TOKEN = '5203819376:AAGyk1tIh1XoEag5xmSofxlK2noM5JQvqC8'


bot = telebot.TeleBot(TOKEN)
telebot.ENABLE_MIDDLEWARE = True

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Выберите среди команд, что именно вам нужно.')

@bot.message_handler(commands=['command2'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    itembtna = types.KeyboardButton('Ссылка 🔗')
    itembtnv = types.KeyboardButton('Контакт ')
    itembtnc = types.KeyboardButton('сайт')
    itembtnd = types.KeyboardButton('другое')
    markup.row(itembtna, itembtnv)
    markup.row(itembtnc, itembtnd)
    bot.send_message(message.chat.id, "Выберите, для чего вам нужен код:", reply_markup=markup)

def get_ye():
    kanye = requests.get("https://api.kanye.rest/")
    kanye_tweet = kanye.text[10:-2]
    return kanye_tweet

@bot.message_handler(commands=['command1'])
def help(message):
    bot.send_message(message.chat.id, 'Опишите вашу проблему, мы постараемся исправить всё в ближайшее время.')


@bot.message_handler(content_types=['text','image'])
def hope(message):
    if message.text == 'Ссылка 🔗':
        bot.send_message(message.chat.id, 'Введите текст для создания QR-кода')
        msg = bot.reply_to(message, """\
        Hi there, I am Example bot.
        What's your name?
        """)
        bot.register_next_step_handler(msg, req_info)
        # img=qr_gen(message.text,type='default')
        # bio = BytesIO()
        # bio.name = 'image.png'
        # img.save(bio, 'PNG')
        # bio.seek(0)
        # bot.send_photo(message.chat.id, photo=bio)
    if message.text == 'другое':
        bot.send_message(message.chat.id, get_ye())



#RUN
if __name__=='__main__':
    bot.polling(none_stop=True)
