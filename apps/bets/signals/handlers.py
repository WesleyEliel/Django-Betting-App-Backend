import time
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.bets.models import BetHistory


@receiver(post_save, sender=BetHistory)
def update_bet_data_or_take_betting_process_to_final_state(sender, instance, created, **kwargs):
    """
    Update bet data if the bet is just created
    Complete the betting process by processing the incoming and/or actualizing the status and the results
    """
    if created:
        instance.initialize()
    else:
        if instance.tracker.has_changed('result') and instance.result != BetHistory.BET_RESULT_PENDING:
            instance.process_the_income()
