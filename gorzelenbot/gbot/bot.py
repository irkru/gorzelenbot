import telebot
from telebot import types

import urllib.request
import logging
import os

from django.core.files import File
from django.conf import settings
from .models import UserModel, TreeModel
from .messages import *

bot = telebot.TeleBot(settings.BOT_TOKEN)
log = logging.getLogger(__name__)


def get_url_image(tkn, image_path):
    return 'https://api.telegram.org/file/bot{}/{}'.format(tkn, image_path)


def update_or_create_user(user):
    """
    Создает пользователя, если его нет в базе данных, или обновляет его данные,
    если он есть
    """
    log.debug('Creating user id=%d', user.id)

    update = {
        'is_bot': user.is_bot,
        'first_name': value_or_empty(user.first_name),
        'last_name': value_or_empty(user.last_name),
        'username': user.username,
        'language_code': user.language_code,

    }
    obj, created = UserModel.objects.update_or_create(
        user_id=user.id,
        defaults=update,
    )

    return obj


def get_or_create_tree(user):
    """
    Возвращает последнее дерево пользователя, или создает новое
    """
    return TreeModel.objects.get_or_create(sender=user, status='C')


def value_or_empty(value):
    return value if value else ''


def what_next(tree, last_event):
    """
    Проверяет, какие данные уже отправлены на текущий момент для дерева,
    и подсказывает пользователю, что отправить еще
    """
    return ''

@bot.message_handler(commands=['start'])
def start_message(message):

    # Проверка на бота
    cu_is_bot = message.from_user.is_bot
    if cu_is_bot:
        return

    # создаем или получаем пользователя
    user = update_or_create_user(message.from_user)
    tree, created = get_or_create_tree(user)

    if not created:
        # открытое дерево уже есть, зачем пользователь вызывает старт?
        bot.send_message(message.chat.id, MSG_ALREADY_STARTED)
        return

    bot.send_message(message.chat.id, MSG_HELLO)


@bot.message_handler(commands=['save'])
def save_message(message):

    user = update_or_create_user(message.from_user)
    tree, created = get_or_create_tree(user)

    message_to_user = MSG_SAVED.format(tree.id)

    if tree.text != "" and tree.latitude != "" and tree.longitude != "" and tree.img1.name != "":
        tree.status = 'F'
        print('save', tree.status)
        tree.save()
        bot.send_message(message.chat.id, message_to_user, reply_markup=keyboard())
    else:
        message_to_user = tree.check_fields()
        bot.send_message(message.chat.id, message_to_user, reply_markup=keyboard())


@bot.message_handler(content_types=['text'])
def send_text(message):

    user = update_or_create_user(message.from_user)
    tree, created = get_or_create_tree(user)

    old_text = tree.text
    new_text = old_text + '\n' + message.text
    tree.text = new_text
    tree.save()

    if not old_text:
        bot.send_message(message.chat.id, 'Комментарий отправлен', reply_markup=keyboard())
    else:
        bot.send_message(message.chat.id, 'Комментарий дополнен', reply_markup=keyboard())


@bot.message_handler(content_types=['photo'])
def photo(message):

    user = update_or_create_user(message.from_user)
    tree, created = get_or_create_tree(user)

    file_img = bot.get_file(message.photo[-1].file_id)
    url = get_url_image(settings.BOT_TOKEN, file_img.file_path)

    if not tree.img1:
        TreeModel.download_imagefield(tree.img1, url)
        msg = 'Фотография 1 загружена'
    elif not tree.img2:
        TreeModel.download_imagefield(tree.img2, url)
        msg = 'Фотография 2 загружена'
    elif not tree.img3:
        TreeModel.download_imagefield(tree.img3, url)
        msg = 'Фотография 3 загружена'
    elif not tree.img4:
        TreeModel.download_imagefield(tree.img4, url)
        msg = 'Фотография 4 загружена'
    else:
        msg = 'Последняя фотография не была сохранена, можно сохранить только 4 фотографии'

    tree.save()
    reply_message = what_next(tree, 'photo_uploaded')

    bot.send_message(message.chat.id, msg+'\n'+reply_message, reply_markup=keyboard())



@bot.message_handler(content_types=["location"])
def location(message):
    user = update_or_create_user(message.from_user)
    tree, created = get_or_create_tree(user)

    if message.location is not None:
        if not tree.latitude and not tree.longitude:
            msg = 'Геопозиция загружена'
        else:
            msg = 'Геопозиция обновлена\nМожете сохранить заявку: /save'

        tree.latitude = message.location.latitude
        tree.longitude = message.location.longitude
        tree.save()

        bot.send_message(message.chat.id, msg, reply_markup=keyboard())


def keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn1 = types.KeyboardButton('/save')
    markup.add(btn1)
    return markup












