# -*- coding: utf-8 -*-
"""
Created on June 13, 2022

@author:
    Wesley Eliel MONTCHO, alias DevBackend7
"""

from rest_framework import serializers

from apps.utils.models import Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('pk', 'name', 'prefix', 'code',)
