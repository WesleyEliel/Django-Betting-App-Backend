from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.bets.business_logics import fixtures as fixtures_bl
from apps.bets.business_logics import bets as bets_bl
from apps.bets.models import League
from apps.bets.serializers import LeagueSerializer
from commons.mixings import BaseModelMixin
from commons.views import BaseGenericViewSet


class FixturesViewSet(ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    @action(methods=["GET"], detail=False, url_path='live')
    def live(self, request, *args, **kwargs):
        data = fixtures_bl.get_live_fixtures()
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, url_path='by-league')
    def by_league(self, request, *args, **kwargs):
        league = request.GET.get('league')
        if league is None:
            raise APIException('Vous devez entrer l\' identifiant de la ligue')
        data = fixtures_bl.get_fixtures_by_league(league_id=league)
        return Response(data=data, status=status.HTTP_200_OK)


class BetViewSet(ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    @action(methods=["GET"], detail=False, url_path='possibles-for-fixture')
    def possible_for_fixture(self, request, *args, **kwargs):
        fixture = request.GET.get('fixture')
        odd_type = request.GET.get('odd_type')
        if fixture is None:
            raise APIException('Vous devez entrer l\' identifiant du match')
        data = bets_bl.get_available_bets_list_for_fixture(fixture_id=fixture, odd_type=odd_type)
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, url_path='possible-bet-for-fixture-detail')
    def possible_bets_for_fixture_details(self, request, *args, **kwargs):
        fixture = request.GET.get('fixture')
        bet = request.GET.get('bet')
        odd_type = request.GET.get('odd_type')
        if fixture is None:
            raise APIException('Vous devez entrer l\' identifiant du match')
        if bet is None:
            raise APIException('Vous devez entrer l\' identifiant du type de paris choisi')
        data = bets_bl.get_odds_for_a_bet(fixture_id=fixture, bet_id=bet, odd_type=odd_type)
        return Response(data=data, status=status.HTTP_200_OK)


class LeagueViewSet(ListModelMixin, RetrieveModelMixin, BaseModelMixin, BaseGenericViewSet):
    object_class = League
    serializer_default_class = LeagueSerializer
    lookup_field = 'identifier'
