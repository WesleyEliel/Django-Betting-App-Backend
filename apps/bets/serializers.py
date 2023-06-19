from rest_framework import serializers
from rest_framework.exceptions import NotAcceptable

from apps.bets.models import BetHistory, League
from apps.users.models import User

from commons.messages import Messages


class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = ('name', 'identifier', 'type', 'logo', 'created_at', 'updated_at',)


class BetHistorySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, default=None)

    class Meta:
        model = BetHistory
        fields = ('user', 'bet_id', 'fixture_id', 'competition_id', 'amount', 'result', 'status',)

        read_only_fiels = ('result', 'status',)

    def validate_user(self, value):
        if not self.context['request'].user.is_anonymous:
            return self.context['request'].user

    def create(self, validated_data):
        user = validated_data.get('user')
        amount = validated_data.get('amount')

        if not BetHistory.is_eligible_to_bet(user=user, amount=amount):
            NotAcceptable(Messages.NOT_ENOUGH_CASH_IN_YOUR_ACCOUNT)

        instance = super(BetHistorySerializer, self).create(validated_data)
        instance.initialize()
        return instance
