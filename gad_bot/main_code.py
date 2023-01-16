@bot.message_handler(content_types=['text'])
def handle_text(message):

# Если пользователь отправил "привет, как тебя зовут?" отвечаем "робот я"
if message.text == "привет, как тебя зовут?":
   bot.send_message(message.from_user.id, 'робот я'

# Если пользователь отправил "и чо?" отвечаем "да ничо"
elif message.text == "и чо?":
   bot.send_message(message.from_user.id, 'да ничо'

#Если пользователь отправил слово/фразу, на которое(ую) нет ответа
else:
   bot.send_message(message.from_user.id, "Извините, я Вас не понимаю")