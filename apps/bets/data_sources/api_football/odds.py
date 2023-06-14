from .api import api_football, TIMEZONE
import operator


def format_result(data: dict):
    def formatter(raw_odds: dict):
        return raw_odds['odds']

    return list(map(formatter, data['response']))


def get_pre_match_bets_list(fixture_id: str, bet_id: str):
    endpoint = "/odds"
    params = {
        'timezone': TIMEZONE,
        'fixture': fixture_id,
        'bookmaker': 11,
    }
    data = api_football.perform_request(method='GET', route=endpoint, params=params)
    return format_result(data)


def get_in_play_match_bets_list(fixture_id: str, bet_id: str):
    endpoint = "/odds/live"
    params = {
        'fixture': fixture_id,
    }
    data = api_football.perform_request(method='GET', route=endpoint, params=params)
    print(data)
    return format_result(data)


def get_odds_for_bet_of_pre_match_type(fixture_id: str, bet_id: str):
    endpoint = "/odds"
    params = {
        'timezone': TIMEZONE,
        'fixture': fixture_id,
        'bookmaker': 11,
    }
    data = api_football.perform_request(method='GET', route=endpoint, params=params)
    return format_result(data)


def get_odds_for_bet_of_in_play_match_type(fixture_id: str, bet_id: str):
    endpoint = "/odds/live"
    params = {
        'fixture': fixture_id,
    }
    data = api_football.perform_request(method='GET', route=endpoint, params=params)
    print(data)
    return format_result(data)
