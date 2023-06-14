from django.core.validators import MinValueValidator
from django.db import models

from apps.users.models import User
from apps.utils.models import Country

from commons.models import AbstractCommonBaseModel


class League(AbstractCommonBaseModel):
    name = models.CharField(verbose_name='Nom de la ligue', max_length=256)
    identifier = models.CharField(verbose_name='Identifiant Distant de la ligue', max_length=128)
    type = models.CharField(verbose_name='Type de la ligue', max_length=256, blank=True, null=True)
    logo = models.URLField(verbose_name="Logo de la ligue", max_length=256, blank=True, null=True)
    country = models.ForeignKey(to=Country, blank=True, null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Ligue'
        verbose_name_plural = 'Ligues'


class BetHistory(AbstractCommonBaseModel):
    BET_RESULTS = (
        (0, "LOST"),
        (1, "WON"),
        (2, "PENDING")
    )
    bet_user = models.ForeignKey(to=User, related_name="bets", on_delete=models.CASCADE)
    bet_amount = models.DecimalField(validators=[MinValueValidator(90.0)], max_digits=6, decimal_places=2)
    bet_result = models.IntegerField(default=2, blank=True, choices=BET_RESULTS)

    def __str__(self):
        return f"{self.created_at}"

    class Meta:
        verbose_name = 'Historique de Paris'
        verbose_name_plural = 'Historiques de Paris'
