# Generated by Django 3.2.5 on 2021-08-06 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_auto_20210806_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover',
            field=models.ImageField(default='media/books/covers/default.png', upload_to='books/covers/'),
        ),
    ]
