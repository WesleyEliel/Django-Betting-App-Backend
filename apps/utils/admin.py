from django.contrib import admin

# Register your models here.
from apps.utils.models import Country
from commons.admin import BaseModelAdmin


@admin.register(Country)
class CountryAdmin(BaseModelAdmin):
    pass
