import httplib2
import sys
import telebot
from django.conf import settings

from .models import UserModel

bot = telebot.TeleBot(settings.BOT_TOKEN)

http_connect = httplib2.Http('.cache')

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

    cu_id = message.from_user.id

    if not len(UserModel.objects.filter(user_id=cu_id)):
        cu_is_bot = message.from_user.is_bot

        if not cu_is_bot:

            cu_username = message.from_user.username if (message.from_user.username != None) else ''
            cu_first_name = message.from_user.first_name if (message.from_user.first_name != None) else ''
            cu_last_name = message.from_user.last_name if (message.from_user.last_name != None) else ''
            cu_language_code = message.from_user.language_code if (message.from_user.language_code != None) else ''

            current_user = UserModel(
                user_id=cu_id,
                is_bot=cu_is_bot,
                first_name=cu_first_name,
                username=cu_username,
                last_name=cu_last_name,
                language_code=cu_language_code
            )
            current_user.save()


@bot.message_handler(content_types=['text'])
def send_text(message):
    print('*** dir(message) :', dir(message))
    print('*** message :', message)
    print('*** message.text :', message.text)


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


def get_url_image(tkn, image_path):
    return 'https://api.telegram.org/file/bot{}/{}'.format(tkn, image_path)
