# Generated by Django 3.2 on 2021-05-23 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0016_alter_project_delta_roi'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='completed_tasks',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='projectmilestone',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='milestones', to='control.project'),
        ),
    ]
