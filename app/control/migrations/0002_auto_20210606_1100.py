# Generated by Django 3.2 on 2021-06-06 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectwallet',
            name='not_assigned_dev_resources_hours',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='projectwallet',
            name='not_assigned_management_resources_hours',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='projectwallet',
            name='not_assigned_marketing_resources_hours',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='projectwallet',
            name='not_assigned_operative_resources_hours',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='projectwallet',
            name='not_assigned_sysops_resources_hours',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='projectwallet',
            name='not_assigned_total_costs',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='projectwallet',
            name='projects_dev_resources_hours',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='projectwallet',
            name='projects_management_resources_hours',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='projectwallet',
            name='projects_marketing_resources_hours',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='projectwallet',
            name='projects_operative_resources_hours',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='projectwallet',
            name='projects_sysops_resources_hours',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='projectwallet',
            name='projects_total_estimated_costs',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
