# -*- coding: utf-8 -*-
"""
Created on June 5, 2023

@author:
    Wesley Eliel MONTCHO, alias DevBackend7
"""

import logging
from decimal import Decimal

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from model_utils import FieldTracker
from model_utils.managers import InheritanceManager

from apps.users import verify
from apps.users.managers import CustomUserManager
from apps.utils.models import Country

from commons.models import AbstractCommonBaseModel

logger = logging.getLogger(__name__)
logger.setLevel('INFO')

SEX_CHOICES = (
    ("F", "Féminin"),
    ("M", "Masculin"),
    ("A", "Autres"),
)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(
        verbose_name='Prénoms', max_length=30, blank=True)
    last_name = models.CharField(
        verbose_name='Nom', max_length=150, blank=True)
    email = models.EmailField(
        verbose_name='Adresse mail', blank=False, null=False, unique=True)
    sex = models.CharField(verbose_name='Sexe', max_length=10,
                           choices=SEX_CHOICES, blank=True, null=False)
    birthday = models.DateField(
        verbose_name='Date de Naissance', blank=True, null=True)
    country = models.ForeignKey(to=Country, blank=True, null=True, verbose_name="Pays de résidence",
                                on_delete=models.SET_NULL)
    conf_num = models.CharField(
        verbose_name='Numéro de confirmation', max_length=128)
    password = models.CharField(
        verbose_name='Mot de passe', max_length=128, blank=False)
    is_active = models.BooleanField(
        verbose_name="Désigne si l'utilisateur est actif",
        default=True,
        help_text="Désigne si cet utilisateur doit être traité comme actif. Désélectionnez cette option au lieu de "
                  "supprimer les comptes. "
    )
    objects = CustomUserManager()
    date_joined = models.DateTimeField(
        verbose_name="Date d'inscription", default=timezone.now)

    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    def is_eligible_for_subactions(self):
        return self.is_active

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def set_phone(self, phone):
        self.phone = phone
        self.save()

    def set_conf_num(self, code):
        if code and code != '':
            self.conf_num = code
            self.save()
        else:
            raise ValueError('Le code de confirmation est vide.')

    def ask_verification(self):
        verification = verify.send(
            **{"email": self.email, 'full_name': self.get_full_name()})
        self.conf_num = verification['code']
        self.save()

    def validate(self):
        self.is_active = True
        self.save()

    def __str__(self) -> str:
        return f'{self.email} & {self.get_full_name()}'


class UserFinancialAccount(AbstractCommonBaseModel):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, verbose_name='Utilisateur',
                                related_name='financial_account')
    balance = models.DecimalField(
        verbose_name='Solde', default=0, max_digits=12, decimal_places=2)

    # percentage = models.DecimalField(
    #    verbose_name="Pourcentage sur vente par ticket", max_digits=15, decimal_places=5, default=3.0)

    def __str__(self) -> str:
        return str("Compte financier de " + self.user.get_full_name())

    @staticmethod
    def get_for_user(user):
        return UserFinancialAccount.objects.get_or_create(user=user)[0]

    def can_withdraw_amount(self, amount: int) -> bool:
        return self.user.is_eligible_for_subactions() and self.balance > amount

    class Meta:
        verbose_name = 'Compte financier'
        verbose_name_plural = 'Comptes financiers'


class Transaction(AbstractCommonBaseModel):
    WITHDRAW = 'WITHDRAW'
    DEPOSIT = 'DEPOSIT'

    TRANSACTION_TYPES = [WITHDRAW, DEPOSIT]

    TRANSACTION_TYPES_CHOICES = (
        (WITHDRAW, WITHDRAW),
        (DEPOSIT, DEPOSIT),
    )

    type = models.CharField(verbose_name="Type de la transaction",
                            max_length=220, choices=TRANSACTION_TYPES_CHOICES, blank=False)
    date = models.DateTimeField(
        verbose_name="Date d'inscription", auto_now_add=True, auto_now=False)
    description = models.CharField(max_length=255, blank=True, null=True)
    local_id = models.CharField(
        verbose_name="Identifiant local", max_length=255, blank=True, null=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=False,
                             verbose_name="Utilisateur", related_name='transactions')
    amount = models.CharField(verbose_name="Montant",
                              max_length=128, blank=False, null=False)
    inheritance_objects = InheritanceManager()

    def __str__(self) -> str:
        return str(
            str(self.date) + ", Transaction financière lié au compte financier de " + self.user.get_full_name())

    def save(self, *args, **kwargs):
        if self.type not in self.TRANSACTION_TYPES:
            raise ValueError('Type de transaction invalide')

        if self.local_id == "" or self.local_id is None:
            self.local_id = get_random_string(15)
        super().save(*args, **kwargs)

    def process(self):
        raise NotImplementedError()

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"


class DepositTransaction(Transaction):
    DEPOSIT_TRANSACTION_INITIALIZED = 'DEPOSIT_TRANSACTION_INITIALIZED'
    DEPOSIT_TRANSACTION_PAID = 'DEPOSIT_TRANSACTION_PAID'
    DEPOSIT_TRANSACTION_COMPLETED = 'DEPOSIT_TRANSACTION_COMPLETED'

    DEPOSIT_TRANSACTION_STATUS_CHOICES = (
        (DEPOSIT_TRANSACTION_INITIALIZED, DEPOSIT_TRANSACTION_INITIALIZED),
        (DEPOSIT_TRANSACTION_PAID, DEPOSIT_TRANSACTION_PAID),
        (DEPOSIT_TRANSACTION_COMPLETED, DEPOSIT_TRANSACTION_COMPLETED),
    )

    status = models.CharField(verbose_name="Status de la transaction", max_length=256,
                              choices=DEPOSIT_TRANSACTION_STATUS_CHOICES,
                              default=DEPOSIT_TRANSACTION_INITIALIZED)
    url = models.URLField(
        verbose_name='Adresse de paiement', max_length=25, blank=True)
    tracker = FieldTracker()

    def process(self):
        pass

    @property
    def is_completed(self):
        return self.status == DepositTransaction.DEPOSIT_TRANSACTION_COMPLETED

    @property
    def is_paid(self):
        return self.status == DepositTransaction.DEPOSIT_TRANSACTION_PAID

    @property
    def is_payment_initialized(self):
        return self.status == DepositTransaction.DEPOSIT_TRANSACTION_INITIALIZED

    class Meta:
        verbose_name = "Paiement"
        verbose_name_plural = "Paiements"


class WithdrawTransaction(Transaction):
    STATUS_INITIALIZED = 'STATUS_INITIALIZED'
    STATUS_CREATE = 'STATUS_CREATE'
    STATUS_FINISHED = 'STATUS_FINISHED'
    STATUS_UPDATE = 'STATUS_UPDATE'

    STATUS_CHOICES = (
        (STATUS_CREATE, STATUS_CREATE),
        (STATUS_INITIALIZED, STATUS_INITIALIZED),
        (STATUS_FINISHED, STATUS_FINISHED),
        (STATUS_UPDATE, STATUS_UPDATE),
    )

    way = models.CharField(verbose_name="Moyen Utilisé Pour la transaction",
                           max_length=220, blank=False)
    tracker = FieldTracker()

    status = models.CharField(
        max_length=120, choices=STATUS_CHOICES, default=STATUS_CREATE)

    def process(self):
        pass

    def retrieve_related_financial_account(self):
        return UserFinancialAccount.get_for_user(self.user)

    def can_be_processed(self):
        return self.retrieve_related_financial_account().can_withdraw_amount(float(self.amount))

    def update_user_financial_account(self):
        if not self.status == WithdrawTransaction.STATUS_UPDATE:
            financial_account = self.retrieve_related_financial_account()

            financial_account.amount -= Decimal(self.amount)
            self.status = WithdrawTransaction.STATUS_UPDATE
            financial_account.save()
            self.save()

    def __str__(self) -> str:
        return f'{self.uuid}'

    def save(self, *args, **kwargs):
        if self.type is None:
            self.type = Transaction.WITHDRAW
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Paiement de Retrait"
        verbose_name_plural = "Paiements de Retraits"
