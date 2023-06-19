import builtins

from rest_framework.exceptions import APIException

from apps.bets.data_sources.api_football import odds
from apps. bets.models import BetHistory


def get_available_bets_list_for_fixture(odd_type: str):
    try:
        if odd_type == 'pre':
            return odds.get_pre_match_bets_list()
        else:
            return odds.get_in_play_match_bets_list()
    except Exception as exc:
        print(exc)
        raise APIException('Erreur Interne, Veuillez réessayer ultérieurement')


def get_odds_for_a_bet(fixture_id: str, bet_id: str, odd_type: str):
    try:
        if odd_type == 'pre':
            return odds.get_odds_for_bet_of_pre_match_type(fixture_id, bet_id)
        else:
            return odds.get_odds_for_bet_of_in_play_match_type(fixture_id, bet_id)
    except Exception as exc:
        print(exc)
        raise APIException('Erreur Interne, Veuillez réessayer ultérieurement')


def create_and_fill_bet_data(bet_history_id: str) -> None:
    bet_history = None
    try:
        bet_history = BetHistory.objects.get(pk=bet_history_id)
    except Exception as exc:
        print(exc)

    if bet_history is not None:
        # call the api for getting information about the bet user want to place and format the datas
        pass

