# Generated by Django 2.2.13 on 2020-06-25 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gbot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='treemodel',
            name='img1',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/TreeModel/'),
        ),
        migrations.AlterField(
            model_name='treemodel',
            name='img2',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/TreeModel/'),
        ),
        migrations.AlterField(
            model_name='treemodel',
            name='img3',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/TreeModel/'),
        ),
        migrations.AlterField(
            model_name='treemodel',
            name='img4',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/TreeModel/'),
        ),
    ]
