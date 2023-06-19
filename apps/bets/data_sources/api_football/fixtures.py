from .api import api_football, TIMEZONE
from datetime import datetime, timedelta
import operator


def get_current_year():
    now = datetime.now()
    return now.year


def estimate_some_date(days: int, operand):
    now = datetime.now()
    date = operand(now, timedelta(days))
    return date.date().__str__()


def format_result(data: dict):
    def formatter(raw_fixture: dict):
        odd_type = 'live'
        if raw_fixture['fixture']['status']['short'] in ['TBD', 'NS', None]:
            odd_type = 'pre'
        return {
            "id": raw_fixture['fixture']['id'],
            "date": raw_fixture['fixture']['date'],
            "status": raw_fixture['fixture']['status'],
            'odd_type': odd_type,
            "league": {
                "id": raw_fixture['league']['id'],
                "name": raw_fixture['league']['name'],
                "season": raw_fixture['league']['season'],
            },
            "teams": raw_fixture['teams'],
            "goals": raw_fixture['goals'],
            "score": raw_fixture['score']
        }

    return list(map(formatter, data['response']))


def get_live_fixtures_for_proposal():
    current_year = get_current_year()
    endpoint = "/fixtures"
    params = {
        'timezone': TIMEZONE,
        'season': current_year,
        'live': 'all',
    }
    # conn.request("GET", "/fixtures?timezone=Africa/Porto-Novo&season=2023&live=all", headers=headers)
    data = api_football.perform_request(method='GET', route=endpoint, params=params)
    return format_result(data)


def get_fixtures_by_league(league_id: str):
    current_year = get_current_year()
    endpoint = "/fixtures"
    params = {
        'timezone': TIMEZONE,
        'from': estimate_some_date(1, operator.sub),
        'to': estimate_some_date(90, operator.add),
        'status': 'TBD-NS-1H-HT-2H-ET-BT-P-SUSP-INT-LIVE',
        'season': current_year,
        'league': league_id,
    }
    data = api_football.perform_request(method='GET', route=endpoint, params=params)
    return format_result(data)
