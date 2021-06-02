# Generated by Django 3.2 on 2021-06-02 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0022_auto_20210602_2059'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='total_hours',
            new_name='estimated_other_cost',
        ),
        migrations.AddField(
            model_name='project',
            name='estimated_resources_cost',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='estimated_total_cost',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='estimated_total_hours',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='dev_resources_hours',
            field=models.PositiveIntegerField(help_text='Cost €/h: 30'),
        ),
        migrations.AlterField(
            model_name='project',
            name='management_resources_hours',
            field=models.PositiveIntegerField(help_text='Cost €/h: 40'),
        ),
        migrations.AlterField(
            model_name='project',
            name='marketing_resources_hours',
            field=models.PositiveIntegerField(help_text='Cost €/h: 35'),
        ),
        migrations.AlterField(
            model_name='project',
            name='operative_resources_hours',
            field=models.PositiveIntegerField(help_text='Cost €/h: 25'),
        ),
        migrations.AlterField(
            model_name='project',
            name='sysops_resources_hours',
            field=models.PositiveIntegerField(help_text='Cost €/h: 30'),
        ),
    ]
