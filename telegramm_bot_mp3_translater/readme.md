# Telegramm bot конвертации текста в .MP3 файл.

Пользователь может выбрать вариает ввода текста а так же
необходимость перевести текст на Русский язык.


### /start запускает программу и предлагает перевести текст.
Взаимодействие с ботом осуществляется с помощью кнопок выбора.

### /help - выводит информацию по работе бота и поддерживаемых языках.
Вводится информация о работе бота и команда /start для начала работ.


## Пример полученного результата поиска:


>![alt text](https://i.postimg.cc/sxf3SZd4/photo-2023-01-07-22-25-33.jpg)
>![alt text](https://i.postimg.cc/7hBwNYq8/photo-2023-01-07-22-25-28.jpg)
>![alt text](https://i.postimg.cc/qRxkzxY7/photo-2023-01-07-22-25-23.jpg)
>![alt text](https://i.postimg.cc/SshSSvg5/photo-2023-01-07-22-25-13.jpg)
>![alt text](https://i.postimg.cc/nL7VtJGB/photo-2023-01-07-22-25-04.jpg)


# Настройка бота.
1. В консоли выполните клонирование репопозитория.

```git clone https://github.com/sirotkinnikolay/sirotkin_projects/tree/main/telegramm_bot_mp3_translater```


2. Установите необходимые библиотеки
#```pip install gTTS```
#```pip install pyttsx3 ```
#```pip install pyTelegramBotAPI```


4. Создайте в папке файл config.py и добавьте туда :
>token = 'токен, который вы получили у BotFather'

# Запуск бота.

1. В консоли перейдите в папку с проектом
2. Выполните в консоли:

```python3 main.py```










