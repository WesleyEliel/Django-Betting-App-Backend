from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from model_utils import FieldTracker

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
    DEFAULT_BET_DATA_STRUCTURE = {
        "id": "",
        "name": "",
        "value": {
            "odd": "",
            "value": "",
            "handicap": ""
        }
    }

    BET_STATUS_INITIALIZED = 'BET_STATUS_INITIALIZED'
    BET_STATUS_PROCESSED = 'BET_STATUS_PROCESSED'
    BET_STATUS_CREATED = 'BET_STATUS_CREATED'

    BET_RESULT_WON = 1
    BET_RESULT_LOST = 0
    BET_RESULT_PENDING = 2

    BET_RESULTS_CHOICES = (
        (BET_RESULT_WON, "WON"),
        (BET_RESULT_LOST, "LOST"),
        (BET_RESULT_PENDING, "PENDING")
    )
    BET_STATUS_CHOICES = (
        (BET_STATUS_CREATED, BET_STATUS_CREATED),
        (BET_STATUS_INITIALIZED, BET_STATUS_INITIALIZED),
        (BET_STATUS_PROCESSED, BET_STATUS_PROCESSED)
    )
    user = models.ForeignKey(to=User, related_name="bets", on_delete=models.CASCADE)
    bet_id = models.CharField(verbose_name="Identifiant du type de paris", max_length=128)
    fixture_id = models.CharField(verbose_name="Identifiant du match", max_length=128)
    competition_id = models.CharField(verbose_name="Identifiant de la competition", max_length=128)
    bet_data = models.JSONField(verbose_name="Informations de Paris", blank=True, null=True,
                                default=DEFAULT_BET_DATA_STRUCTURE)
    amount = models.DecimalField(verbose_name="Montant du paris", validators=[MinValueValidator(90.0)], max_digits=6,
                                 decimal_places=2)
    result = models.IntegerField(verbose_name="Résultat", default=2, blank=True, choices=BET_RESULTS_CHOICES)
    status = models.CharField(verbose_name="Status", max_length=128, default=BET_STATUS_CREATED, blank=False,
                              choices=BET_STATUS_CHOICES)
    tracker = FieldTracker()

    def __str__(self):
        return f"{self.uuid}"

    @staticmethod
    def is_eligible_to_bet(user: User, amount: int):
        return user.is_active and user.related_financial_account.can_withdraw_amount(amount)

    @property
    def is_created(self):
        return self.status == BetHistory.BET_STATUS_CREATED

    @property
    def is_initialized(self):
        return self.status == BetHistory.BET_STATUS_INITIALIZED

    @property
    def is_processed(self):
        return self.status == BetHistory.BET_STATUS_PROCESSED

    def initialize(self):
        if self.is_created:
            fees = Decimal(self.amount)

            admin_account = User.get_admin_account()
            admin_financial_account = admin_account.related_financial_account
            user_financial_account = self.user.related_financial_account

            user_financial_account.balance -= fees
            admin_financial_account.balance += fees

            user_financial_account.save()
            admin_financial_account.save()

            self.status = BetHistory.BET_STATUS_INITIALIZED
            self.save()

    def process_the_income(self):
        if self.result == BetHistory.BET_RESULT_PENDING:
            raise ValueError("Paris toujours en cours")
        if not self.is_processed:
            financial_account = self.user.related_financial_account

            if self.result == BetHistory.BET_RESULT_WON:
                odd = Decimal(self.bet_data['value']['odd'])
                rewards = Decimal(self.amount * odd)
                financial_account.balance += rewards
            financial_account.save()
            self.status = BetHistory.BET_STATUS_PROCESSED
            self.save()

    def save(self, *args, **kwargs):
        return super(BetHistory, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Historique de Paris'
        verbose_name_plural = 'Historiques de Paris'


# These models are for testing the behavior of django models foreign key relations chip, especially how the on_delete
# attr work

"""
class BetHistoryChecker(AbstractCommonBaseModel):
    history = models.ForeignKey(verbose_name='Historique', to=BetHistory, on_delete=models.CASCADE)

    def __str__(self):
        return self.history.__str__()

    class Meta:
        verbose_name = "Vérificateur d'Historiques de Paris"
        verbose_name_plural = "Vérificateurs d'Historiques de Paris"


class BetHistoryViewer(AbstractCommonBaseModel):
    viewer = models.ForeignKey(verbose_name='Viewer', to=BetHistory, on_delete=models.CASCADE)

    def __str__(self):
        return self.viewer.__str__()

    class Meta:
        verbose_name = "Visionneur d'Historiques de Paris"
        verbose_name_plural = "Visionneurs d'Historiques de Paris"
"""
