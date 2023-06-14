# -*- coding: utf-8 -*-
"""
Created on April 26 2022

@author:
    Wesley Eliel MONTCHO, alias DevBackend7
"""

from rest_framework.routers import DefaultRouter

from apps.utils import views

router = DefaultRouter()
router.register(r"countries", views.CountryViewSetViewSet, basename="CountriesViewSet")
urls_patterns = router.urls
