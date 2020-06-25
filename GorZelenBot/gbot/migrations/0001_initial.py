# Generated by Django 2.2.13 on 2020-06-25 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TreeModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(max_length=100)),
                ('text', models.CharField(max_length=512)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('latitude', models.CharField(max_length=100)),
                ('longitude', models.CharField(max_length=100)),
                ('img1', models.ImageField(default=None, null=True, upload_to='uploads/TreeModel/')),
                ('img2', models.ImageField(default=None, null=True, upload_to='uploads/TreeModel/')),
                ('img3', models.ImageField(default=None, null=True, upload_to='uploads/TreeModel/')),
                ('img4', models.ImageField(default=None, null=True, upload_to='uploads/TreeModel/')),
            ],
        ),
    ]
