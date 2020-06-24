import telebot
import httplib2


token = '1250889151:AAGCQPWShYAnd4Cgark2X8XQdaztYlLw45k'
bot = telebot.TeleBot(token)

http_connect = httplib2.Http('.cashe')


def get_url_image(tkn, image_path):
    return 'https://api.telegram.org/file/bot{}/{}'.format(tkn, image_path)


@bot.message_handler(commands=['start'])
def start_message(message):
    mes = """Вас приветствует бот Горзеленхоза. 
    
    Для того чтобы зарегистровать больное дерево:
    
    1) Отправьте команду /reg (Добавлю позднее)
    2) Отправьте до 4 его фотографий (Север, Восток, Юг, Запад)
    3) Отправьте геопозицию
    4) Отправьте комментарий
    5) Отправьте команду /regend (Добавлю позднее)
    """
    bot.send_message(message.chat.id, mes)
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = telebot.types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button_geo)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет, бос)')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Прощай, создатель')
    print(message.text)


@bot.message_handler(content_types=['photo'])
def photo(message):
    fileID = message.photo[-1].file_id
    file = bot.get_file(fileID)
    get_url_image(token, file.file_path)
    new_url_img = get_url_image(token, file.file_path)
    print('path: ', new_url_img)

    response, content = http_connect.request(new_url_img)
    with open(file.file_path, 'wb') as f:
        f.write(content)

    bot.send_message(message.chat.id, 'Фотография загружена.')


@bot.message_handler(content_types=["location"])
def location(message):
    if message.location is not None:
        print(message.location)
        print("latitude: {}; longitude: {}".format(message.location.latitude, message.location.longitude))
        bot.send_message(message.chat.id, 'Геопозиция загружена.')


bot.polling()
