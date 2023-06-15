# -*- coding: utf-8 -*-
"""
Created on June 13, 2023

@author:
    Wesley Eliel MONTCHO, alias DevBackend7
"""

from rest_framework.routers import DefaultRouter

from apps.bets.views import FixturesViewSet, LeagueViewSet, BetViewSet

router = DefaultRouter()
# router.register(r"", viewset, basename="")"
router.register(r"bets", BetViewSet, basename="BetViewSet")
router.register(r"fixtures", FixturesViewSet, basename="FixturesViewSet")
router.register(r"leagues", LeagueViewSet, basename="LeagueViewSet")
urls_patterns = router.urls
