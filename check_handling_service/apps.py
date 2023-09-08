from django.apps import AppConfig


class CheckHandlingServiceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "check_handling_service"

    def ready(self):
        import signals
