# Generated by Django 3.2 on 2021-06-05 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0040_auto_20210605_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('IN_PROGRESS', 'In progress'), ('BLOCKED', 'Blocked'), ('DONE', 'Done'), ('CANCELLED', 'Cancelled'), ('NOT_ACCEPTED', 'Not accepted')], default='PENDING', max_length=32),
        ),
    ]
