from rest_framework.exceptions import APIException

from apps.bets.data_sources.api_football import fixtures


def get_live_fixtures():
    try:
        return fixtures.get_live_fixtures_for_proposal()
    except Exception as exc:
        print(exc)
        raise APIException('Erreur Interne, Veuillez réessayer ultérieurement')


def get_fixtures_by_league(league_id: str):
    try:
        return fixtures.get_fixtures_by_league(league_id)
    except Exception as exc:
        print(exc)
        raise APIException('Erreur Interne, Veuillez réessayer ultérieurement')


def get_fixture():
    pass

