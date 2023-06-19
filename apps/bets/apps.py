from django.apps import AppConfig


class BetsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.bets'

    def ready(self):
        import apps.bets.signals.handlers
