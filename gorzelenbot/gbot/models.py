from django.db import models


class UserModel(models.Model):
    user_id = models.PositiveIntegerField()
    is_bot = models.BooleanField()
    first_name = models.CharField(max_length=32)
    username = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    language_code = models.CharField(max_length=5)


class TreeModel(models.Model):
    VALUES_STATUS = (
        ('C', 'Is being created'),
        ('F', 'Filled'),
        ('P', 'Processed'),
    )
    # Самозаполняющиеся поля
    sender = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=VALUES_STATUS, default='C')
    # Время. Заполняется автоматически
    create_time = models.DateTimeField(auto_now_add=True, blank=True)
    update_time = models.DateTimeField(auto_now=True, blank=True)
    # Поля для заполнения пользователем через телеграмм бот
    text = models.CharField(max_length=512, blank=True)
    latitude = models.CharField(max_length=100, blank=True)
    longitude = models.CharField(max_length=100, blank=True)
    img1 = models.ImageField(upload_to='uploads/TreeModel/', null=True, blank=True)
    img2 = models.ImageField(upload_to='uploads/TreeModel/', null=True, blank=True)
    img3 = models.ImageField(upload_to='uploads/TreeModel/', null=True, blank=True)
    img4 = models.ImageField(upload_to='uploads/TreeModel/', null=True, blank=True)

    def check_fields(self):
        message_to_user = ""

        if self.text == "":
            message_to_user += "Отправьте комментарий \n"

        if self.latitude == "" or self.longitude == "":
            message_to_user += "Отправьте геопозицию \n"

        if self.img1.name == "":
            message_to_user += "Отправьте фотографию дерева"

        if message_to_user == "":
            message_to_user = "Все необходимые данные заполненны, можете воспользоваться командой /save, чтобы закончить редактирование и наши сотрудники увидят заявку"

        return message_to_user



