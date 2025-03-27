import telebot
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
    bot.reply_to(
        message,
        "Владельцем этого бота является пользователь @nmadnorangen. Бот ещё дорабатывается, поэтому ждите новых функций!",
    )


@bot.message_handler(commands=["help"])
def send_help(message):
    bot.reply_to(
        message,
        'Вам доступны следующие команды:\n/about\n/help\n/joke\n/math\nИх функционал описан в меню по кнопке слева от области "Сообщения"',
    )


html_anekdoti = requests.get(
    f"https://xn--b1agaykvq.xn--p1ai/anekdoty/shutki/{random.randint(1,1200)}"
).text

anekdot = re.findall(r"<p itemprop=\"articleBody\">(.+)</p>", html_anekdoti)
counter = 0
for i in range(len(anekdot)):
    counter += 1


@bot.message_handler(commands=["joke"])
def send_joke(message):
    anek = anekdot[random.randint(0, counter - 1)]
    anek = anek.replace("&quot;", '"')
    anek = anek.replace("<br/>", "\n")
    anek = anek.replace("<br />", "\n")
    bot.reply_to(message, anek)


def generate_math_equation():
    num1 = random.randint(1, 50)
    num2 = random.randint(1, 50)
    operation = random.choice(['\+', '\-'])
    
    if operation == '\+':
        result = num1 + num2
        equation = f"x {operation} {num2} \= {result}"
    else:
        result = num1 - num2
        equation = f"x {operation} {num2} \= {result}"
    
    return equation, num1


@bot.message_handler(commands=["math"])
def send_math(message):
    equation, num1 = generate_math_equation()
    bot.reply_to(message, f"{equation} \| x \= ||{num1}||", parse_mode = "MarkdownV2")

@bot.message_handler(func=lambda message: True)
def answers(message):
    if message.text == "Как дела?":
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
