from django.apps import AppConfig


class KhneuPubAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'khneu_pub_app'

    def ready(self):
        import khneu_pub_app.signals
