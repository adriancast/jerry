# Generated by Django 3.2 on 2021-05-23 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0003_auto_20210523_1131'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='portfolioconfigurationgeneralmanagerrevision',
            name='dev_resources_hours',
        ),
        migrations.RemoveField(
            model_name='portfolioconfigurationgeneralmanagerrevision',
            name='management_resources_hours',
        ),
        migrations.RemoveField(
            model_name='portfolioconfigurationgeneralmanagerrevision',
            name='marketing_resources_hours',
        ),
        migrations.RemoveField(
            model_name='portfolioconfigurationgeneralmanagerrevision',
            name='operative_resources_hours',
        ),
        migrations.RemoveField(
            model_name='portfolioconfigurationgeneralmanagerrevision',
            name='sysops_resources_hours',
        ),
        migrations.RemoveField(
            model_name='portfolioconfigurationgeneralmanagerrevision',
            name='total_budget_eur',
        ),
    ]
