# Generated by Django 3.2 on 2021-06-05 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0035_auto_20210605_1732'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='is_safe',
            new_name='is_in_risk',
        ),
        migrations.RemoveField(
            model_name='project',
            name='is_safe_msg',
        ),
        migrations.AddField(
            model_name='project',
            name='is_in_risk_msg',
            field=models.CharField(default='', max_length=256),
        ),
    ]
