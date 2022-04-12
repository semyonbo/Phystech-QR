import telebot
from generator import qr_gen
from telebot import types
my_id=259969071
TOKEN = '5203819376:AAGyk1tIh1XoEag5xmSofxlK2noM5JQvqC8'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Выберите среди команд, что именно вам нужно.')

@bot.message_handler(commands=['command2'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    itembtna = types.KeyboardButton('контакт')
    itembtnv = types.KeyboardButton('геопозиция')
    itembtnc = types.KeyboardButton('сайт')
    itembtnd = types.KeyboardButton('другое')
    markup.row(itembtna, itembtnv)
    markup.row(itembtnc, itembtnd)
    bot.send_message(message.chat.id, "Выберите, для чего вам нужен код:", reply_markup=markup)


@bot.message_handler(commands=['command1'])
def help(message):
    bot.send_message(message.chat.id, 'Опишите вашу проблему, мы постараемся исправить всё в ближайшее время.')

@bot.message_handler(content_types=['text','audio','video','image'])
def hope(message):
    bot.forward_message(my_id, message.chat.id, message.message_id)
    bot.send_message(message.text, message.message_id)



#RUN
if __name__=='__main__':
    bot.polling(none_stop=True)