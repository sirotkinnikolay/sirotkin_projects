import io
import os
from loader import bot
from telebot import types
import gtts
from gtts import gTTS


def action_text_markup(message):
    markup = types.ReplyKeyboardMarkup(True, False)
    markup.row('воспроизвести текстовый файл')
    markup.add('ввести текст для воспроизведения в ручную')
    bot.send_message(message.from_user.id, 'выберите вариант ввода текста.',
                     reply_markup=markup)
    bot.send_message(message.chat.id, reply_markup=types.ReplyKeyboardRemove())


def file_path():
    a = os.path.basename(__file__)
    b = os.path.abspath(__file__).replace(a, '')
    return b


def language_selection(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("German")
    btn2 = types.KeyboardButton('English')
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id, 'Выберите язык ввода.',
                     reply_markup=markup)


def command_choice(message):
    bot.send_message(message.chat.id, "Выберите команду"
                                      '\n /start - Начало работы:'
                                      '\n /help - Помощь с использованием')


def mp3_transformation(lang, text):
    mp3_file = gtts.gTTS(text, lang=lang, slow=False)
    mp3_file.save('text_translation.mp3')
