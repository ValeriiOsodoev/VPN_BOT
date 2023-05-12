import os 

import telebot
from telebot import types

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
TEXT = os.getenv('TEXT')

bot = telebot.TeleBot(TOKEN, parse_mode=None)
tariff_choice = None

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
    username = message.from_user.first_name
    bot.send_message(
        message.chat.id,
        f'Привет {username}! Я ONECLICK VPN бот. Что бы вы хотели?',
        reply_markup=keyboard
    )


@bot.message_handler(func=lambda message: message.text == 'Тарифные планы')
def tariffs_button(message):
    """Функция обработки кнопки 'Тарифные планы'."""
    keyboard_tariffs = types.ReplyKeyboardMarkup(one_time_keyboard=False)
    button_individual = types.KeyboardButton('Индивидуальный')
    button_family = types.KeyboardButton('Семейный')
    button_individual_3 = types.KeyboardButton('Индивидуальный на 3 месяца')
    button_individual_6 = types.KeyboardButton('Индивидуальный на 6 месяцев')
    button_back = types.KeyboardButton('В главное меню')

    keyboard_tariffs.add(
        button_individual,
        button_family,
        button_individual_3,
        button_individual_6,
        button_back
    )
    bot.send_message(
        message.chat.id,
        TEXT,
        reply_markup=keyboard_tariffs
    )
    bot.send_message(
        message.chat.id,
        'Выберите тарифный план: ',
        reply_markup=keyboard_tariffs
    )


@bot.message_handler(func=lambda message: message.text in [
    'Индивидуальный',
    'Семейный',
    'Индивидуальный на 3 месяца',
    'Индивидуальный на 6 месяцев'
    ])
def tariffs(message):
    """Функция обработки выбора тарифного плана."""
    global tariff_choice
    keyboard_after_payment = types.ReplyKeyboardMarkup(one_time_keyboard=False)
    button_payment = types.KeyboardButton('Оплатил')
    button_back = types.KeyboardButton('В главное меню')
    keyboard_after_payment.add(
        button_payment,
        button_back
    )
    tariff_choice = message.text
    bot.send_message(
        message.chat.id,
        f'Вы выбрали тариф {tariff_choice}. '
        'Подвердите оплату нажатием кнопки "Оплатил"',
        reply_markup=keyboard_after_payment
    )


@bot.message_handler(func=lambda message: message.text == 'В главное меню')
def back(message):
    """Функция обработки кнопки 'В главное меню'."""
    bot.send_message(
        message.chat.id,
        'Возврат в главное меню',
        reply_markup = keyboard
    )


@bot.message_handler(func=lambda message: message.text == 'Оплатил')
def pay_button(message):
    """Функция обработки кнопки 'Оплатил'."""
    global tariff_choice

    keyboard_approve = types.InlineKeyboardMarkup()
    approve = types.InlineKeyboardButton(
        'Подтвердить',
        callback_data=message.chat.id
    )
    keyboard_approve.add(approve)

    username = message.from_user.first_name
    bot.send_message(
        chat_id = '5284675667',
        text = f'Клиент {username} оплатил тариф {tariff_choice}. '
        'Подтвердите оплату, нажав на кнопку "Подтвердить".',
        reply_markup=keyboard_approve
    )


@bot.callback_query_handler(func=lambda call: True)
def approve_button(call):
    """Функция обработки кнопки 'Подтвердить'."""
    if call.message.chat.id == 5284675667:
        bot.answer_callback_query(
            call.id,
            text='Оплата подтверждена.'
        )
        bot.send_message(
            chat_id=call.data,
            text='Оплата подтверждена, ожидайте дальнейших инструкций.'
        )
    else:
        bot.answer_callback_query(call.id, text='Произошла ошибка.')


@bot.message_handler(func=lambda message: message.text == 'О Нас')
def about_us_button(message):
    """Функция обработки кнопки 'О Наc'."""
    bot.send_message(
        message.chat.id,
        'Мы команда ONECLICK',
        reply_markup=keyboard
    )


@bot.message_handler(func=lambda message: message.text == 'Что такое ВПН?')
def about_vpn_button(message):
    """Функция обработки кнопки 'Что такое ВПН?'."""
    bot.send_message(
        message.chat.id,
        'VPN - это ваша безопасность в интернете',
        reply_markup=keyboard
    )


@bot.message_handler(func=lambda message: message.text == 'Поддержка')
def support_button(message):
    """Функция обработки кнопки 'Поддержка'."""
    bot.send_message(
        message.chat.id,
        'Переход в чат поддержки: @vpn_oneclick',
        reply_markup=keyboard
    )


@bot.message_handler(func=lambda message: True)
def back_message(message):
    """Функция обработки любого текстового сообщения."""
    if message.text:
        bot.reply_to(message, 'Я ещё не умею полноценно отвечать на сообщения')


bot.infinity_polling()
