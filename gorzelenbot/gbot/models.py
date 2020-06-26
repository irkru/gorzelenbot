from django.db import models


class UserModel(models.Model):
    user_id = models.PositiveIntegerField()
    is_bot = models.BooleanField()
    first_name = models.CharField(max_length=32)
    username = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    language_code = models.CharField(max_length=5)



class TreeModel(models.Model):
    sender = models.CharField(max_length=100)
    text = models.CharField(max_length=512)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    img1 = models.ImageField(upload_to='uploads/TreeModel/', null=True, blank=True)
    img2 = models.ImageField(upload_to='uploads/TreeModel/', null=True, blank=True)
    img3 = models.ImageField(upload_to='uploads/TreeModel/', null=True, blank=True)
    img4 = models.ImageField(upload_to='uploads/TreeModel/', null=True, blank=True)


