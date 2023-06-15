# Generated by Django 3.2.19 on 2023-06-15 10:54

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bets', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='league',
            options={'verbose_name': 'Ligue', 'verbose_name_plural': 'Ligues'},
        ),
        migrations.CreateModel(
            name='BetHistory',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Date de suppression')),
                ('active', models.BooleanField(default=True, verbose_name="Désigne si l'instance est active")),
                ('is_deleted', models.BooleanField(default=False, verbose_name="Désigne si l'instance est supprimée")),
                ('bet_id', models.CharField(max_length=128, verbose_name='Identifiant distant du type de paris')),
                ('fixture_id', models.CharField(max_length=128, verbose_name='Identifiant distant du match')),
                ('competition_id', models.CharField(max_length=128, verbose_name='Identifiant distant de la competition')),
                ('bet_data', models.JSONField(default={'id': '', 'name': '', 'value': {'handicap': '', 'odd': '', 'value': ''}}, verbose_name='Informations de Paris')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(90.0)], verbose_name='Montant du paris')),
                ('result', models.IntegerField(blank=True, choices=[(1, 'WON'), (0, 'LOST'), (2, 'PENDING')], default=2, verbose_name='Résultat')),
                ('is_income_processed', models.BooleanField(default=False, verbose_name='Désigne si les gains sont traités')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bets', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Historique de Paris',
                'verbose_name_plural': 'Historiques* de Paris',
            },
        ),
    ]