
import logging

from rest_framework import exceptions

from apps.bets.models import League
from commons.messages import Messages

logger = logging.getLogger(__name__)


def get_leagues():
    return League.objects.all()


def get_league(**kwargs):
    try:
        return League.objects.get(**kwargs)
    except League.DoesNotExist:
        raise exceptions.NotFound(Messages.LEAGUE_OBJECT_WITH_THIS_ATTRS_DOES_NOT_EXIST)
    except Exception as exc:
        logger.error(exc)
        raise exceptions.APIException(Messages.INTERNAL_ERROR)
