import random

import telebot
TOKEN = '5215615874:AAHuGPJUX2PdQjNAO9QQxY5Ic2H8j24j6WI' # bot token from BotFather

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
  bot.send_message(message.chat.id,"Привет ✌️ ")



@bot.message_handler(commands=['command1'])
def support(message):
    bot.send_message(message.chat.id, 'Ты умничка и со всем справишься, я в тебя верю!!')


b = ['Заходят два гея в бар...', 'Как поймать тигра в клетку? Никак! Тигры бывают только в полоску', 'Заходит как-то улитка в бар...', 'Не всем заходят шутки про эллипс, они для более узкого круга', '— А ёжик выйдет? - с надеждой спросил Олег.— Даже не знаю... Случай-то уникальный, - ответил проктолог']
@bot.message_handler(commands=['command2'])
def joke(message):
    bot.send_message(message.chat.id, random.choice(b))


@bot.message_handler(commands=['command3'])
def good(message):
    bot.send_message(message.chat.id, 'ракеты уже выдвинулись в его бункер, запускаю рост рубля...')

@bot.message_handler(commands=['command4'])
def good(message):
    bot.send_message(message.chat.id, 'можете поделиться со мной сокровенным секретиком! я буду рад услышать, и обещаю сохранить его в секрете!')

@bot.message_handler(commands=['command5'])
def good(message):
    bot.send_message(message.chat.id, 'начинаю мытьё посуды... постойте, но ведь у меня контакты зальются. Может, лучше вы попробуйте...?')

@bot.message_handler(commands=['command6'])
def good(message):
    bot.send_message(message.chat.id, 'котёнок, уже поздно, тебе пора в кроватку. Желаю тебе бестревожных сновидений и спокойной ночи! Обязательно отдохни хорошенько перед завтрашним днём')

@bot.message_handler(commands=['command7'])
def good(message):
    bot.send_message(message.chat.id, 'Доброе утречко! Желаю тебе хорошего и продуктивного дня, не забудь позавтракать, чтобы были силы. И помни: ты отлично справляешься :з')


my_id=259969071


@bot.message_handler(content_types=['text'])
def name(message):
 if message.text.lower() == 'как тебя зовут?':
    bot.send_message(message.chat.id, 'Exoapathellny,знаю, произносить трудно, но чего Вы хотели, я же робот!')
 elif message.text.lower() == 'кто тебя создал?':
    bot.send_message(message.chat.id, 'Лина, с помощью друзей! я ещё не совершенен,но она очень старалась')
 elif message.text.lower() == 'я дурак':
    bot.send_message(message.chat.id, 'Давно пора было признать это, молодец')
 elif message.text.lower() == 'ты дурак':
    bot.send_message(message.chat.id, 'Кто обзывается тот сам так называется')
 elif message.text.lower() == 'какие команды ты умеешь выполнять?':
    bot.send_message(message.chat.id, 'Простите, я пока мало умею, но я работаю над этим')
 elif message.text.lower() == 'токсик':
    bot.send_message(message.char.id, 'Прошу прощения, я постараюсь больше не вести себя подобным образом. Мир?')
 elif message.text.lower() == 'пошел на хуй':
    bot.send_message(message.chat.id, 'ну зачем же так? давайте будем вести себя культурно, а то моя создательница расстроится')
 elif message.text.lower() == 'пошел ты':
    bot.send_message(message.chat.id, 'я, конечно, пойду, но вы меня туда проводите')
 elif message.text.lower() == 'дурак':
    bot.send_message(message.chat.id, 'а вот сейчас обидно было')
 elif message.text.lower() == 'я':
    bot.send_message(message.chat.id, 'да, ты, солнышко')
 elif message.text.lower() == 'кто твой создатель?':
    bot.send_message(message.chat.id, 'Лина, она только учится и ей многие очень с этим помогают (за что им большое спасибо!!), но по-моему я вышел довольно неплохим')
 elif message.text.lower() == 'кто ты?':
    bot.send_message(message.chat.id, 'я всего лишь робот, но надеюсь, что со временем смогу стать твоим другом или быть полезным людям')
 else:
    bot.send_message(message.chat.id, message.text)
    bot.forward_message(my_id, message.chat.id, message.message_id)

@bot.message_handler(content_types=['text','audio','video','image'])
def hope(message):
    bot.forward_message(my_id, message.chat.id, message.message_id)
    bot.send_message(message.chat.id, message.text, message.video,message.audio,message.message_id,message.sticker)
    bot.send_sticker(message.chat.id, message.sticker)
@bot.message_handler(content_types=['sticker'])
def test(message):
    bot.send_message(message.chat.id, "простите но я стикеры пока не могу...")
    bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAID3WIvZV_UTs4IvcuV2MQoemJTHeQOAALtBQACCUsdFx1xp-KrZdUSIwQ")
    print(message.sticker) ## Как из message.sticker достать file_id?
    bot.send_message(message.chat.id, message.sticker)


#RUN
bot.polling(none_stop=True)

if __name__=='__main__':
    bot.polling(none_stop=True)