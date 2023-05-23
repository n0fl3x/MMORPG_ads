from django.apps import AppConfig


class AdsboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AdsBoard'

    def ready(self):
        import AdsBoard.signals
