# Generated by Django 3.2 on 2021-06-05 19:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0038_auto_20210605_1937'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectRevision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_validated', models.BooleanField(default=False)),
                ('comment', models.TextField(blank=True, null=True)),
                ('portfolio_configuration', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cio_revision', to='control.portfolioconfiguration')),
            ],
        ),
    ]
