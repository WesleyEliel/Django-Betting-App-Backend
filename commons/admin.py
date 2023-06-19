from django.contrib.admin import ModelAdmin


class BaseModelAdmin(ModelAdmin):
    exclude = ('active', 'deleted_at', 'is_deleted')
