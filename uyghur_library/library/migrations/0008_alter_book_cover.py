# Generated by Django 3.2.5 on 2021-08-06 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0007_alter_book_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover',
            field=models.ImageField(blank=True, default='books/covers/default.png', upload_to='books/covers/'),
        ),
    ]
