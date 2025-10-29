from django.apps import AppConfig

class AiappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "aiapp"

    def ready(self):
        # charge le modèle Stable Diffusion 1 fois au démarrage
        from .services.generate_local import LocalImageGenerator
        from . import state
        state.generator = LocalImageGenerator()
