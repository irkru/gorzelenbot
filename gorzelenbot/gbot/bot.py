import telebot
from telebot import types
import tempfile
import urllib.request
import os

from django.core.files import File
from django.conf import settings
from .models import UserModel, TreeModel

bot = telebot.TeleBot(settings.BOT_TOKEN)


def get_url_image(tkn, image_path):
    return 'https://api.telegram.org/file/bot{}/{}'.format(tkn, image_path)


def save_img_from_url_to_imagefield(imgfield, url):
    img_name = os.path.basename(url)
    img_temp = tempfile.TemporaryFile()
    img_temp.write(urllib.request.urlopen(url).read())
    img_temp.flush()
    imgfield.save(img_name, File(img_temp))


@bot.message_handler(commands=['start'])
def start_message(message):
    cu_id = message.from_user.id

    # Проверка на бота
    cu_is_bot = message.from_user.is_bot
    if cu_is_bot:
        return

    # Проверяем есть ли пользователь в базе.
    # Если нету создаём нового.
    # Записиваем его в перменную current_user.
    if not len(UserModel.objects.filter(user_id=cu_id)):
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
    else:
        current_user = UserModel.objects.get(user_id=cu_id)

    # Создаём <<новое дерево>>.
    if len(TreeModel.objects.filter(sender=current_user, status='C')) < 1:
        current_tree = TreeModel(
            sender=current_user,
            status='C',
        )
        current_tree.save()
    else:
        print('**** Уже есть дерево ****')

    mes = """Вас приветствует бот Горзеленхоза

    Для того чтобы зарегистровать больное дерево:

    1) Отправьте до 4 его фотографий (Желательно с разных сторон)
    2) Отправьте геопозицию
    3) Отправьте комментарий, в нём следует подробно описать где находится дерево
    4) Отправьте команду /check, чтобы проверить все ли данные заполнены
    5) Отправьте команду /save
    """
    bot.send_message(message.chat.id, mes)


@bot.message_handler(commands=['save'])
def save_message(message):
    cu_id = message.from_user.id
    cu_user = UserModel.objects.get(user_id=cu_id)

    if len(TreeModel.objects.filter(sender=cu_user, status='C')) == 1:
        cu_tree = TreeModel.objects.get(sender=cu_user, status='C')

        message_to_user = "Все данные приянты. Заявка принята"


        if cu_tree.text != "" and cu_tree.latitude != "" and cu_tree.longitude != "" and cu_tree.img1.name != "":
            cu_tree.status = 'F'
            cu_tree.save()
            bot.send_message(message.chat.id, message_to_user, reply_markup=keyboard())
        else:
            message_to_user = cu_tree.check_fields()
            bot.send_message(message.chat.id, message_to_user, reply_markup=keyboard())


@bot.message_handler(content_types=['text'])
def send_text(message):
    cu_id = message.from_user.id
    cu_user = UserModel.objects.get(user_id=cu_id)

    if len(TreeModel.objects.filter(sender=cu_user, status='C')) == 1:
        cu_tree = TreeModel.objects.get(sender=cu_user, status='C')

        old_text = cu_tree.text
        new_text = old_text + '\n' + message.text
        cu_tree.text = new_text
        cu_tree.save()

        if old_text == '':
            bot.send_message(message.chat.id, 'Комментарий отправлен', reply_markup=keyboard())
        else:
            bot.send_message(message.chat.id, 'Комментарий дополнен', reply_markup=keyboard())


@bot.message_handler(content_types=['photo'])
def photo(message):

    cu_id = message.from_user.id
    cu_user = UserModel.objects.get(user_id=cu_id)

    if len(TreeModel.objects.filter(sender=cu_user, status='C')) == 1:
        cu_tree = TreeModel.objects.get(sender=cu_user, status='C')

        fileID = message.photo[-1].file_id
        file_img = bot.get_file(fileID)
        cu_url = get_url_image(settings.BOT_TOKEN, file_img.file_path)

        if cu_tree.img1.name == '':
            save_img_from_url_to_imagefield(cu_tree.img1, cu_url)
            mes_to_user = 'Фотография 1 загружена'
        elif cu_tree.img2.name == '':
            save_img_from_url_to_imagefield(cu_tree.img2, cu_url)
            mes_to_user = 'Фотография 2 загружена'
        elif cu_tree.img3.name == '':
            save_img_from_url_to_imagefield(cu_tree.img3, cu_url)
            mes_to_user = 'Фотография 3 загружена'
        elif cu_tree.img4.name == '':
            save_img_from_url_to_imagefield(cu_tree.img4, cu_url)
            mes_to_user = 'Фотография 4 загружена'
        else:
            mes_to_user = 'Последняя фотография не была сохранена, можно сохранить только 4 фотографии'

        cu_tree.save()
        bot.send_message(message.chat.id, mes_to_user, reply_markup=keyboard())


@bot.message_handler(content_types=["location"])
def location(message):
    cu_id = message.from_user.id
    cu_user = UserModel.objects.get(user_id=cu_id)

    if len(TreeModel.objects.filter(sender=cu_user, status='C')) == 1:
        cu_tree = TreeModel.objects.get(sender=cu_user, status='C')

        if message.location is not None:
            if cu_tree.latitude == '' and cu_tree.longitude == '':
                message_to_user = 'Геопозиция загружена'
            else:
                message_to_user = 'Геопозиция обновлена'

            cu_tree.latitude = message.location.latitude
            cu_tree.longitude = message.location.longitude
            cu_tree.save()

            bot.send_message(message.chat.id, message_to_user, reply_markup=keyboard())


def keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn1 = types.KeyboardButton('/save')
    markup.add(btn1)
    return markup












