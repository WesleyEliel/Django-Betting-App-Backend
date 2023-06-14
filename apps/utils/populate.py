# -*- coding: utf-8 -*-
"""
Created on June 13, 2023

@author:
    Wesley Eliel MONTCHO, alias DevBackend7
"""

import json

from apps.utils.models import Country

country_json = json.load(open('apps/utils/files/countries.json', encoding='utf-8'), )


def populate_country():
    for country in country_json:
        data = {
            'name': country['name']['fr'],
            'code': country['code'],
            'prefix': country['prefix'],
            'flag': country['flag'],
        }

        print(data)

        try:
            country = Country.default_objects.create(**data)
            country.save()
            print(country)
        except Exception as exc:
            print(exc)

populate_country()

"""exec(open('apps/utils/populate.py').read())"""
"""admin@wuloevent.com, admin"""
