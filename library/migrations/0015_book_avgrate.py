# Generated by Django 3.2.5 on 2021-08-14 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0014_auto_20210813_2141'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='avgrate',
            field=models.IntegerField(default=0, max_length=100),
        ),
    ]
