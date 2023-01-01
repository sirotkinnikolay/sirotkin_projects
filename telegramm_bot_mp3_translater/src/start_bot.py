import io
import os
from loader import bot
from telebot import types
import pathlib
from pathlib import Path

language = ''
flag_file = True
flag_text = True


def action_text_markup(message):
    markup = types.ReplyKeyboardMarkup(True, False)
    markup.row('перевести текстовый файл')
    markup.add('ввести текст для перевода в ручную')
    bot.send_message(message.from_user.id, 'выберите вариант ввода текста.',
                     reply_markup=markup)
    bot.send_message(message.chat.id, reply_markup=types.ReplyKeyboardRemove())


def file_path():
    a = os.path.basename(__file__)
    b = os.path.abspath(__file__).replace(a, '')
    return b


@bot.message_handler(func=lambda message: flag_file == True, content_types=['document'])
def addfile(message):
    bot.send_message(message.chat.id, "Выберите коменду из меню "
                                      '\n /translate - Начало работы:'
                                      '\n /help - Помощь с использованием')


@bot.message_handler(commands=['translate'])
def language_selection(message):
    """При выборе команды /translate, предоставляются кнопки для выбора языка переводимого текста."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("German")
    btn2 = types.KeyboardButton('English')
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id, 'Выберите язык с которого необходимо перевести текст',
                     reply_markup=markup)


@bot.message_handler(func=lambda message: flag_text == True, content_types=['text'])
def action_text(message):

    """При выборе языка переводимого текста, предоставляются кнопки для выбора варианта введения текста,
     текст можно ввести напрямую в сообщении или загрузить .txt файл с текстом для первода."""
    global language
    global flag_file
    global flag_text
    if message.text == 'German':
        language = 'de'
        action_text_markup(message)

    elif message.text == 'English':
        language = 'en'
        action_text_markup(message)

    elif message.text == 'перевести текстовый файл':
        flag_file = False
        bot.send_message(message.chat.id, 'выберите файл для загрузки')

        @bot.message_handler(content_types=['document'])
        def add_file(message):
            try:
                folder_1 = Path(file_path(), 'text_file', message.document.file_name)
                file_info = bot.get_file(message.document.file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                with open(folder_1, 'wb') as new_file:
                    new_file.write(downloaded_file)

                bot.reply_to("Файл успешно загружен")
            except Exception as e:
                bot.reply_to(message, e)

    elif message.text == 'ввести текст для перевода в ручную':
        flag_file = True
        flag_text = False
        bot.send_message(message.chat.id, 'введите текст для перевода')

        @bot.message_handler(content_types=['text'])
        def text_write(message):
            global flag_text
            while not flag_text:
                folder_2 = Path(file_path() + 'text_file')
                filepath = os.path.join(folder_2, "text.txt")
                bot.send_message(message.chat.id, message.text)
                with open(filepath, 'w') as file:
                    file.write(message.text)
                    flag_text = True
                bot.send_message(message.chat.id, reply_markup=types.ReplyKeyboardRemove())

    else:
        bot.send_message(message.chat.id, 'Вас приветствует бот для перевода текста и прослушивания его.'
                                          '\n /translate - Начало работы:'
                                          '\n /help - Помощь с использованием')
