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

@bot.message_handler(commands=["help"])
def send_help(message):
    markup = types.InlineKeyboardMarkup()
    commands_info = {
        "about": "Эта функция позволяет Вам получить информацию о владельце этого бота",
        "help": "Эта функция позволяет Вам получить информацию обо всех доступных на данный момент кнопках и их командах",
        "joke": "Эта функция позволяет Вам получить случайную шутку или анекдот",
        "math": "Эта функция позволяет Вам получить случайное уравнение с ответом",
        "url_link": "Эта функция позволяет Вам получить ссылку на сайт-партнера"
    }
    
    for cmd, desc in commands_info.items():
        button = types.InlineKeyboardButton(cmd, callback_data=f"help-{cmd}")
        markup.add(button)
    
    bot.send_message(message.chat.id, "Выберите команду для получения информации:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("help-"))
def send_command_info(call):
    command = call.data.split("-")[1]
    commands_info = {
        "about": "Эта функция позволяет Вам получить информацию о владельце этого бота",
        "help": "Эта функция позволяет Вам получить информацию обо всех доступных на данный момент кнопках и их командах",
        "joke": "Эта функция позволяет Вам получить случайную шутку или анекдот",
        "math": "Эта функция позволяет Вам получить случайное уравнение с ответом",
        "url_link": "Эта функция позволяет Вам получить ссылку на сайт-партнера"
    }
    
    bot.send_message(call.message.chat.id, commands_info.get(command, "Информация не найдена"))


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
    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)
    result = random.randint(1, 20)
    operation = random.choice(['+', '-'])
    
    if operation == '+':
        equation = f"x {operation} {num2} = {result}"
        correct_answer = result - num2
    else:
        equation = f"x {operation} {num2} = {result}"
        correct_answer = result + num2
    
    options = [correct_answer, correct_answer + random.randint(1, 5), correct_answer - random.randint(1, 5), correct_answer + random.randint(2, 4)]
    random.shuffle(options)
    
    return equation, correct_answer, options

@bot.message_handler(commands=["math"])
def send_math(message):
    equation, correct_answer, options = generate_math_equation()
    markup = types.InlineKeyboardMarkup()
    
    for option in options:
        button = types.InlineKeyboardButton(str(option), callback_data=f"math_{option}_{correct_answer}")
        markup.add(button)
    
    bot.send_message(message.chat.id, f"Найдите x: {equation}", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("math_"))
def check_answer(call):
    try:
        _, chosen_answer, correct_answer = call.data.split("_")
        chosen_answer, correct_answer = int(chosen_answer), int(correct_answer)
        
        if chosen_answer == correct_answer:
            bot.send_message(call.message.chat.id, "Ваш ответ верный!")
        else:
            bot.send_message(call.message.chat.id, "Ответ неверный")
    except ValueError:
        bot.send_message(call.message.chat.id, "Ошибка обработки ответа.")

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