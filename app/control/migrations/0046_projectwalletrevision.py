# Generated by Django 3.2 on 2021-06-05 21:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0045_alter_project_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectWalletRevision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_validated', models.BooleanField(default=False)),
                ('comment', models.TextField(blank=True, null=True)),
                ('project_wallet', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='general_manager_revision', to='control.projectwallet')),
            ],
        ),
    ]
