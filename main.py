import telebot
from telebot import types
import config
import random
import requests
import re

bot = telebot.TeleBot(config.TG_API_TOKEN)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Доброго времени суток! Чего желаете?")


@bot.message_handler(commands=["about"])
def send_about(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("VK", url="https://vk.com/nmadnorangen")
    button2 = types.InlineKeyboardButton("Steam", url="https://steamcommunity.com/nmadnorangen")
    markup.add(button1, button2)
    bot.reply_to(
        message,
        "Владельцем этого бота является пользователь @nmadnorangen. Бот ещё дорабатывается, поэтому ждите новых функций!\nНиже представлены ссылки на владельца:".format(message.from_user), reply_markup=markup
    )

# # @bot.callback_query_handler()
# # def 

# @bot.message_handler(commands=["help"])
# def send_help(message):
#     markup = types.InlineKeyboardMarkup()
#     button1 = types.InlineKeyboardButton("about", None, "Эта функция позволяет Вам получить информацию о владельце этого бота")
#     button2 = types.InlineKeyboardButton("help", None, "Эта функция позволяет Вам получить информацию обо всех доступных на данный момент кнопках и их командах")
#     button3 = types.InlineKeyboardButton("joke", None, "Эта функция позволяет Вам получить случайную шутку или анекдот")
#     button4 = types.InlineKeyboardButton("math", None, "Эта функция позволяет Вам получить случайное уравнение с ответом")
#     button5 = types.InlineKeyboardButton("url_link", None, "Эта функция позволяет Вам получить ссылку на сайт-партнера")
#     markup.add(button1, button2, button3, button4, button5)
#     bot.send_message(
#         message.chat.id,
#         "Вам доступны следующие команды:".format(message.from_user), reply_markup=markup
#     )



@bot.message_handler(commands=["joke"])
def send_joke(message):
    html = requests.get(
        f"https://xn--b1agaykvq.xn--p1ai/anekdoty/shutki/{random.randint(1,1200)}"
    )
    html.encoding = "utf-8"
    html_anekdoti = html.text

    anekdot = re.findall(r"<p itemprop=\"articleBody\">(.+)</p>", html_anekdoti)
    counter = 0
    for i in range(len(anekdot)):
        counter += 1
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Ещё один анекдот")
    button2 = types.KeyboardButton("Хватит анекдотов")
    markup.add(button1, button2)
    anek = anekdot[random.randint(0, counter - 1)]
    anek = anek.replace("&quot;", '"')
    anek = anek.replace("<br/>", "\n")
    anek = anek.replace("<br />", "\n")
    bot.send_message(message.chat.id, anek.format(message.from_user), reply_markup=markup)


def generate_math_equation():
    num1 = random.randint(1, 50)
    num2 = random.randint(1, 50)
    operation = random.choice(['\\+', '\\-'])
    
    if operation == '\\+':
        result = num1 + num2
        equation = f"x {operation} {num2} \\= \\{result}"
    else:
        result = num1 - num2
        equation = f"x {operation} {num2} \\= \\{result}"
    
    return equation, num1


@bot.message_handler(commands=["math"])
def send_math(message):
    equation, num1 = generate_math_equation()
    bot.reply_to(message, f"{equation} \\| x \\= ||{num1}||", parse_mode = "MarkdownV2")

@bot.message_handler(commands=['url_link'])
def link_give(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Сайт Moodle НТИ УрФУ", url='https://moodle.ntiustu.ru/')
    markup.add(button1)
    bot.send_message(message.chat.id, "Здравствуйте, {0.first_name}! Нажмите на кнопку, чтобы перейти на сайт Дистанционного обучения НТИ УрФУ.".format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types=["text"])
def answers(message):
    if(message.text == "Ещё один анекдот"):
        send_joke(message)
    elif(message.text == "Хватит анекдотов"):
        bot.send_message(message.chat.id, text="Что будем делать дальше?", reply_markup=telebot.types.ReplyKeyboardRemove())

    elif message.text == "Как дела?":
        bot.reply_to(message, "У меня всё супер! А как Ваши?")
    elif message.text == "Хорошо":
        bot.reply_to(message, "Я рад за Вас!")
    elif message.text == "Нормально":
        bot.reply_to(message, "Понятно. Держите шутку!")
        send_joke(message)
    elif message.text == "Плохо":
        bot.reply_to(message, "Не расстраивайтесь! Всё наладится!")
    else:
        bot.reply_to(message, "Я пока не знаю, как отвечать на это (")

bot.infinity_polling()