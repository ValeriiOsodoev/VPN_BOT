import os 

import telebot
from telebot import types

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

bot = telebot.TeleBot(TOKEN, parse_mode=None)

keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=False)
button_tariffs = types.KeyboardButton('Тарифные планы')
button_about_us = types.KeyboardButton('О Нас')
button_about_vpn = types.KeyboardButton('Что такое ВПН?')
button_support = types.KeyboardButton('Поддержка')

keyboard.add(
    button_tariffs,
    button_about_us,
    button_about_vpn,
    button_support
)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Функция обработки команд /start и /help."""
    bot.send_message(
        message.chat.id,
        'Привет! Я ВПН БОТ. Что бы вы хотели?',
        reply_markup=keyboard
    )


@bot.message_handler(func=lambda message: message.text == 'О Нас')
def about_us(message):
    """Функция обработки кнопки 'О Наc'."""
    bot.send_message(
        message.chat.id,
        'Мы команда ONECLICK',
        reply_markup=keyboard
    )


@bot.message_handler(func=lambda message: message.text == 'Что такое ВПН?')
def about_vpn(message):
    """Функция обработки кнопки 'Что такое ВПН?'."""
    bot.send_message(
        message.chat.id,
        'VPN - это ваша безопасность в интернете',
        reply_markup=keyboard
    )


bot.infinity_polling()
