from django.contrib import admin

# Register your models here.
from apps.utils.models import Country


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass
