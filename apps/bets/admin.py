from django.contrib import admin

from apps.bets.models import BetHistory, League
from commons.admin import BaseModelAdmin


@admin.register(League)
class LeagueAdmin(BaseModelAdmin):
    search_fields = ('name', 'type',)
    list_filter = ('type', 'country',)
    ordering = ('name',)


@admin.register(BetHistory)
class BetHistoryAdmin(BaseModelAdmin):
    pass

"""
@admin.register(BetHistoryChecker)
class BetHistoryCheckerAdmin(BaseModelAdmin):
    pass


@admin.register(BetHistoryViewer)
class BetHistoryViewerAdmin(BaseModelAdmin):
    pass
"""