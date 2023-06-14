from rest_framework import serializers

from apps.bets.models import League


class LeagueSerializer(serializers.ModelSerializer):

    class Meta:
        model = League
        fields = ('name', 'identifier', 'type', 'logo', 'created_at', 'updated_at', )
