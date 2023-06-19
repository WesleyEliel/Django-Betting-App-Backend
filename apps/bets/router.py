# -*- coding: utf-8 -*-
"""
Created on June 13, 2023

@author:
    Wesley Eliel MONTCHO, alias DevBackend7
"""

from rest_framework.routers import DefaultRouter

from apps.bets.views import FixturesViewSet, LeagueViewSet, BetHistoryViewSet
from apps.users.views import TransactionViewSet

router = DefaultRouter()
# router.register(r"", ViewSet, basename="ViewSet")"
router.register(r"bets", BetHistoryViewSet, basename="BetViewSet")
router.register(r"leagues", LeagueViewSet, basename="LeagueViewSet")
router.register(r"fixtures", FixturesViewSet, basename="FixturesViewSet")
router.register(r"transactions", TransactionViewSet, basename="TransactionViewSet")
urls_patterns = router.urls
