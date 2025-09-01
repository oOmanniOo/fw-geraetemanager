from django.apps import AppConfig


class PruefungenConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pruefungen'

    def ready(self):
        import pruefungen.signals