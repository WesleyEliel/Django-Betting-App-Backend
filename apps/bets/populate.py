# -*- coding: utf-8 -*-
"""
Created on June 13, 2023

@author:
    Wesley Eliel MONTCHO, alias DevBackend7
"""

import json
from apps.bets.models import League
from apps.utils.models import Country

league_json = json.load(open('apps/bets/external_data_apis/first/leagues.json', encoding='utf-8'), )


def populate_league():
    for league in league_json['response']:
        try:
            print(league['country']['code'])
            country = Country.objects.get(code=league['country']['code'])
        except Exception as exc:
            print(exc)
            country = None
        data = {
            'name': league['league']['name'],
            'identifier': league['league']['id'],
            'type': league['league']['type'],
            'logo': league['league']['logo'],
            'country': country
        }

        League.objects.create(**data)
populate_league()

"""exec(open('apps/bets/populate.py').read())"""
"""admin@wuloevent.com, admin"""
