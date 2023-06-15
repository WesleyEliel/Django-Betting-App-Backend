from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from apps.users.models import User, UserFinancialAccount
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
    DEFAULT_BET_DATA_STRUCTURE = {
        "id": "",
        "name": "",
        "value": {
            "odd": "",
            "value": "",
            "handicap": ""
        }
    }
    BET_RESULT_WON = 1
    BET_RESULT_LOST = 0
    BET_RESULT_PENDING = 2

    BET_RESULTS_CHOICES = (
        (BET_RESULT_WON, "WON"),
        (BET_RESULT_LOST, "LOST"),
        (BET_RESULT_PENDING, "PENDING")
    )
    user = models.ForeignKey(to=User, related_name="bets", on_delete=models.CASCADE)
    bet_id = models.CharField(verbose_name="Identifiant distant du type de paris", max_length=128)
    fixture_id = models.CharField(verbose_name="Identifiant distant du match", max_length=128)
    competition_id = models.CharField(verbose_name="Identifiant distant de la competition", max_length=128)
    bet_data = models.JSONField(verbose_name="Informations de Paris", blank=False, null=False,
                                default=DEFAULT_BET_DATA_STRUCTURE)
    amount = models.DecimalField(verbose_name="Montant du paris", validators=[MinValueValidator(90.0)], max_digits=6, decimal_places=2)
    result = models.IntegerField(verbose_name="Résultat", default=2, blank=True, choices=BET_RESULTS_CHOICES)
    is_income_processed = models.BooleanField(verbose_name="Désigne si les gains sont traités", default=False)

    def __str__(self):
        return f"{self.created_at}"

    @staticmethod
    def is_eligible_to_bet(user: User, amount: int):
        return user.is_active and user.financial_account.can_withdraw_amount(amount)

    def process_the_income(self):
        if self.result == BetHistory.BET_RESULT_PENDING:
            raise ValueError("Paris toujours en cours")
        if not self.is_income_processed:
            financial_account = UserFinancialAccount.get_for_user(user=self.user)

            if self.result == BetHistory.BET_RESULT_LOST:
                loses = Decimal(self.amount)
                financial_account -= Decimal(loses)
            else:
                odd = Decimal(self.bet_data['value']['odd'])
                rewards = Decimal(self.amount*odd)
                financial_account.balance += rewards

            financial_account.save()

    class Meta:
        verbose_name = 'Historique de Paris'
        verbose_name_plural = 'Historiques* de Paris'
