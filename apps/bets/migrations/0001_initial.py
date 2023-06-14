# Generated by Django 3.2.19 on 2023-06-13 20:50

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('utils', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='League',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Date de suppression')),
                ('active', models.BooleanField(default=True, verbose_name="Désigne si l'instance est active")),
                ('is_deleted', models.BooleanField(default=False, verbose_name="Désigne si l'instance est supprimée")),
                ('name', models.CharField(max_length=256, verbose_name='Nom de la ligue')),
                ('identifier', models.CharField(max_length=128, verbose_name='Identifiant Distant de la ligue')),
                ('type', models.CharField(blank=True, max_length=256, null=True, verbose_name='Type de la ligue')),
                ('logo', models.URLField(blank=True, max_length=256, null=True, verbose_name='Logo de la ligue')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='utils.country')),
            ],
            options={
                'verbose_name': 'League',
                'verbose_name_plural': 'Leagues',
            },
        ),
    ]