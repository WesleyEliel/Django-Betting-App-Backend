from rest_framework.exceptions import APIException

from apps.bets.data_sources.api_football import odds
from apps. bets.models import BetHistory


def get_available_bets_list_for_fixture(fixture_id: str, odd_type: str):
    try:
        if odd_type == 'pre':
            return odds.get_pre_odds(fixture_id)
        else:
            return odds.get_live_odds(fixture_id)
    except Exception as exc:
        print(exc)
        raise APIException('Erreur Interne, Veuillez réessayer ultérieurement')


def get_odds_for_a_bet(fixture_id: str, bet_id: str, odd_type: str):
    try:
        if odd_type == 'pre':
            return odds.get_pre_odds(fixture_id)
        else:
            return odds.get_live_odds(fixture_id)
    except Exception as exc:
        print(exc)
        raise APIException('Erreur Interne, Veuillez réessayer ultérieurement')
