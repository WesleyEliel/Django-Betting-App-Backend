# Generated by Django 3.2.19 on 2023-06-15 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bets', '0002_auto_20230615_1154'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bethistory',
            options={'verbose_name': 'Historique de Paris', 'verbose_name_plural': 'Historiques de Paris'},
        ),
        migrations.RemoveField(
            model_name='bethistory',
            name='is_income_processed',
        ),
        migrations.AddField(
            model_name='bethistory',
            name='status',
            field=models.IntegerField(blank=True, choices=[('BET_STATUS_CREATED', 'BET_STATUS_CREATED'), ('BET_STATUS_INITIALIZED', 'BET_STATUS_INITIALIZED'), ('BET_STATUS_PROCESSED', 'BET_STATUS_PROCESSED')], default=2, verbose_name='Status'),
        ),
    ]