import os
import tempfile
import urllib.request

from django.core.files import File
from django.db import models


class UserModel(models.Model):
    user_id = models.PositiveIntegerField(primary_key=True)
    is_bot = models.BooleanField()
    first_name = models.CharField(max_length=32, blank=True)
    username = models.CharField(max_length=32, blank=True)
    last_name = models.CharField(max_length=32, blank=True)
    language_code = models.CharField(max_length=5, blank=True)


class TreeModel(models.Model):
    VALUE_STATUS = (
        ('C', 'Is being created'),
        ('F', 'Filled'),
        ('P', 'Processed'),
    )
    # Самозаполняющиеся поля
    sender = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=VALUE_STATUS, default='C')
    # Время. Заполняется автоматически
    create_time = models.DateTimeField(auto_now_add=True, blank=True)
    update_time = models.DateTimeField(auto_now=True, blank=True)
    # Поля для заполнения пользователем через телеграмм бот
    text = models.TextField(max_length=2048, blank=True)
    latitude = models.CharField(max_length=100, blank=True)
    longitude = models.CharField(max_length=100, blank=True)
    img1 = models.ImageField(upload_to='uploads/TreeModel/', null=True, blank=True)
    img2 = models.ImageField(upload_to='uploads/TreeModel/', null=True, blank=True)
    img3 = models.ImageField(upload_to='uploads/TreeModel/', null=True, blank=True)
    img4 = models.ImageField(upload_to='uploads/TreeModel/', null=True, blank=True)

    def check_fields(self):
        message_to_user = ""

        if not self.text:
            message_to_user += "Отправьте комментарий \n"

        if not self.latitude or not self.longitude:
            message_to_user += "Отправьте геопозицию \n"

        if not self.img1:
            message_to_user += "Отправьте фотографию дерева"

        if message_to_user == "":
            message_to_user = "Все необходимые данные заполненны, можете воспользоваться командой /save, чтобы закончить редактирование и наши сотрудники увидят заявку"

        return message_to_user

    def download_imagefield(imgfield, url):
        img_name = os.path.basename(url)
        img_temp = tempfile.TemporaryFile()
        img_temp.write(urllib.request.urlopen(url).read())
        img_temp.flush()
        imgfield.save(img_name, File(img_temp))
