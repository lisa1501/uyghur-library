# Generated by Django 3.2.5 on 2021-08-16 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_auto_20210816_1537'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='favorite',
        ),
    ]
