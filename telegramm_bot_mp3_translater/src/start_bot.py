import io
import os
import pathlib
from pathlib import Path
from loader import bot
from telebot import types
import gtts
from gtts import gTTS
from googletrans import Translator
from src.utils import action_text_markup, file_path,\
    language_selection, command_choice, mp3_transformation


LANGUAGE = ''
FLAG_FILE = True
FLAG_TEXT = True
FLAG_TRANSLATE = False


@bot.message_handler(func=lambda message: FLAG_FILE is True, content_types=['document'])
def addfile(message):
    """При попытке загрузки текстового файла раньше его запроса, выводится стартовое меню"""
    command_choice(message)


@bot.message_handler(commands=['help'])
def help_func(message):
    """При выборе команды /help, выводится информация про данного бота и его работу"""
    bot.send_message(message.from_user.id, 'Данный телеграмм-бот предназначен для конвертации'
                                           ' текста в .mp3 файл, и дальнейшего его воспроизведения,'
                                           ' возможет вариант ввода текста вручную'
                                           'или возможна загрузка .txt файла, так же можно'
                                           ' перевести текст на Русский язык перед его '
                                           'конвертацией, доступны два языка, Английский и'
                                           ' Немецкий, для начала работы'
                                           ' воспользуйтесь командой  /start  и следуйте'
                                           ' дальнейшим инструкциям')


@bot.message_handler(commands=['start'])
def translate(message):
    """При запуске команды /start, запрашивается необходим перевод текста перед его конвертацией,
     выбор реализуется кнопками 'да' и 'нет'"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('да')
    btn2 = types.KeyboardButton('нет')
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id, 'Перевести на Русский язык ?',
                     reply_markup=markup)


@bot.message_handler(func=lambda message: FLAG_TEXT is True, content_types=['text'])
def action_text(message):
    """Обработка ввода текста с кнопок по необходимости перевода, языка с которого
     требуется конвертация и варианта ввода текста, исходя из этого запускается
      необходимая функция для дальнейшего выбора параметров или
      обработки текста"""
    global LANGUAGE
    global FLAG_FILE
    global FLAG_TEXT
    global FLAG_TRANSLATE
    translator = Translator()

    if message.text == 'да':
        FLAG_TRANSLATE = True
        language_selection(message)

    elif message.text == 'нет':
        FLAG_TRANSLATE = False
        language_selection(message)

    elif message.text == 'German':
        LANGUAGE = 'de'
        action_text_markup(message)

    elif message.text == 'English':
        LANGUAGE = 'en'
        action_text_markup(message)

    elif message.text == 'воспроизвести текстовый файл':
        FLAG_FILE = False
        bot.send_message(message.chat.id, 'выберите файл для загрузки')

        @bot.message_handler(content_types=['document'])
        def add_file(message):
            """Если был выбран вариан загрузки текста .txt файлом ,
             загружается выбранный файл и происходит
             его конвертация, при необходимости перевод на русский язык"""
            global LANGUAGE
            try:
                folder_1 = Path(file_path(), 'text_file', message.document.file_name)
                file_info = bot.get_file(message.document.file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                with open(folder_1, 'wb') as new_file:
                    new_file.write(downloaded_file)
                with open(folder_1, 'r') as file:
                    one = file.read()
                    if FLAG_TRANSLATE:
                        trans = translator.translate(one, src=LANGUAGE, dest='ru')
                        one = trans.text
                        LANGUAGE = 'ru'

                mp3_transformation(lang=LANGUAGE, text=one)
                mp3_path = os.path.abspath(os.path.join("text_translation.mp3"))
                bot.send_audio(message.from_user.id, audio=open(mp3_path, 'rb'),
                               reply_markup=types.ReplyKeyboardRemove(), parse_mode='Markdown')
                os.remove(folder_1)
                command_choice(message)

            except Exception as fail:
                bot.reply_to(message, fail)

    elif message.text == 'ввести текст для воспроизведения в ручную':
        FLAG_FILE = True
        FLAG_TEXT = False
        bot.send_message(message.chat.id, 'введите текст')

        @bot.message_handler(content_types=['text'])
        def text_write(message):
            """Если текст введен и отправлен после его запроса, то текст
             обрабатывается как текст для конвертации,
             если текст введен раньше запроса, то выводится стартовое меню"""
            global FLAG_TEXT
            global LANGUAGE
            while not FLAG_TEXT:
                folder_2 = Path(file_path() + 'text_file')
                filepath = os.path.join(folder_2, "text.txt")
                two = message.text
                if FLAG_TRANSLATE:
                    trans = translator.translate(two, src=LANGUAGE, dest='ru')
                    two = trans.text
                    LANGUAGE = 'ru'

                mp3_path = os.path.abspath(os.path.join("text_translation.mp3"))
                mp3_transformation(lang=LANGUAGE, text=two)

                with open(filepath, 'w') as file:
                    file.write(message.text)
                    FLAG_TEXT = True
                bot.send_audio(message.from_user.id, audio=open(mp3_path, 'rb'),
                               reply_markup=types.ReplyKeyboardRemove(), parse_mode='Markdown')
                command_choice(message)

    else:
        command_choice(message)
