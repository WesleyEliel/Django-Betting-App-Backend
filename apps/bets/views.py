from django.db import transaction
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.bets.business_logics import fixtures as fixtures_bl
from apps.bets.business_logics import bets as bets_bl
from apps.bets.models import League, BetHistory
from apps.bets.serializers import LeagueSerializer, BetHistorySerializer
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


class BetHistoryViewSet(CreateModelMixin, BaseModelMixin, BaseGenericViewSet):
    object_class = BetHistory
    serializer_default_class = BetHistorySerializer
    permission_classes = (permissions.IsAuthenticated,)

    @transaction.atomic
    def create(self, *args, **kwargs):
        return super(BetHistoryViewSet, self).create(*args, **kwargs)

    @action(methods=["GET"], detail=False, url_path='possibles-bets-for-fixtures')
    def possible_bets_for_fixtures(self, request, *args, **kwargs):
        match_status = request.GET.get('status')
        print(match_status)
        if match_status is None:
            raise APIException("Vous devez entrer le paramètre 'status' relatif au statut du match.")
        data = bets_bl.get_available_bets_list_for_fixture(odd_type=match_status)
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, url_path='get-odds-for-a-bet')
    def get_odds_for_a_bet(self, request, *args, **kwargs):
        fixture = request.GET.get('fixture')
        bet = request.GET.get('bet')
        match_status = request.GET.get('status')
        if fixture is None:
            raise APIException('Vous devez entrer l\' identifiant du match')
        if bet is None:
            raise APIException('Vous devez entrer l\' identifiant du type de paris choisi')
        if match_status is None:
            raise APIException("Vous devez entrer le paramètre 'status' relatif au statut du match.")
        data = bets_bl.get_odds_for_a_bet(fixture_id=fixture, bet_id=bet, odd_type=match_status)
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, url_path='by-me')
    def list_by_user(self, request, *args, **kwargs):
        user = request.user
        queryset = self.filter_queryset(self.get_queryset().filter(user=user))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class LeagueViewSet(ListModelMixin, RetrieveModelMixin, BaseModelMixin, BaseGenericViewSet):
    object_class = League
    serializer_default_class = LeagueSerializer
    lookup_field = 'identifier'
