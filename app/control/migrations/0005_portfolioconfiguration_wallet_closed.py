# Generated by Django 3.2 on 2021-05-23 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0004_auto_20210523_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolioconfiguration',
            name='wallet_closed',
            field=models.BooleanField(default=False),
        ),
    ]