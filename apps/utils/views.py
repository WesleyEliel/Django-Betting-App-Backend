from django.shortcuts import render

# Create your views here.
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework import permissions

from apps.utils.models import Country
from apps.utils.serializers import CountrySerializer
from commons.mixings import BaseModelMixin
from commons.views import BaseGenericViewSet


class CountryViewSetViewSet(ListModelMixin, RetrieveModelMixin, BaseModelMixin, BaseGenericViewSet):
    object_class = Country
    serializer_default_class = CountrySerializer
    lookup_field = 'pk'
    permission_classes = (permissions.AllowAny, )