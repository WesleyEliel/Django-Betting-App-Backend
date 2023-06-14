from django.contrib import admin

from apps.bets.models import League


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    search_fields = ('name', 'type', )
    list_filter = ('type', 'country',)
    ordering = ('name',)
