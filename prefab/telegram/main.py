import telebot
from db import db

bot = telebot.TeleBot("1694522039:AAFU-eV0PTLZQyWZWamMMklhfLHPLeKyKQE")


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start')


@bot.message_handler(commands=['subscribe'])
def a(message):
    db1 = db("users.db")
    if db1.create_user(message.from_user.id, message.chat.id) is True:
        bot.send_message(message.chat.id, 'ты уже подписан')
    else:
        bot.send_message(message.chat.id, 'ты подписался')


@bot.message_handler(commands=['unsubscribe'])
def a(message):
    db1 = db("users.db")
    if db1.delete_user(message.from_user.id) is True:
        bot.send_message(message.chat.id, 'ты уже отподписан')
    else:
        bot.send_message(message.chat.id, 'ты отписался')


@bot.message_handler(commands=['spend_all_message'])
def a(message):
    bot.send_message(message.chat.id, 'введите сообщение')

    @bot.message_handler(content_types=['text'])
    def b(message_):
        db1 = db("users.db")
        for user in db1.get_text():
            bot.send_message(user[1], message_.text)


'''@bot.message_handler(content_types=['text'])
def send_text(message):
    bot.send_message(message.chat.id, message.text)'''


bot.polling()
