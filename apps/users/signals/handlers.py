from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.users.models import DepositTransaction, WithdrawTransaction


@receiver(post_save, sender=DepositTransaction)
def complete_deposit_transaction(sender, instance: DepositTransaction, created, **kwargs):
    """
    Update user financial account when  deposit transaction status moved from initialized to paid.
    Set the status to completed when everything goes well

    """
    if created:
        return None
    if instance.tracker.has_changed('status') and instance.tracker.previous(
            'status') == DepositTransaction.DEPOSIT_TRANSACTION_INITIALIZED:
        if instance.status == DepositTransaction.DEPOSIT_TRANSACTION_PAID:
            instance.update_user_financial_account()
        DepositTransaction.objects.filter(pk=instance.pk).update(status=DepositTransaction.DEPOSIT_TRANSACTION_COMPLETED)


@receiver(post_save, sender=WithdrawTransaction)
def complete_withdraw_transaction(sender, instance: WithdrawTransaction, created, **kwargs):
    """
    Update the user financial account after Withdraw transaction is status has moved from initialized to finished.
    Et the status to UPDATED when everything goes well
    """

    if instance.tracker.has_changed('status') and instance.status == WithdrawTransaction.STATUS_FINISHED:
        instance.update_user_financial_account()
