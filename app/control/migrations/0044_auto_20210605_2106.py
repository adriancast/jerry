# Generated by Django 3.2 on 2021-06-05 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0043_auto_20210605_2004'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectwallet',
            name='not_assigned_dev_resources_hours',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectwallet',
            name='not_assigned_management_resources_hours',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectwallet',
            name='not_assigned_marketing_resources_hours',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectwallet',
            name='not_assigned_operative_resources_hours',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectwallet',
            name='not_assigned_sysops_resources_hours',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectwallet',
            name='not_assigned_total_costs',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectwallet',
            name='projects_operative_resources_hours',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
