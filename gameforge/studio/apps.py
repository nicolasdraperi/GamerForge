import os
from django.apps import AppConfig

class StudioConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "studio"

    def ready(self):
        if os.environ.get("RUN_MAIN") != "true":
            return
        from .services.ai_image import LocalImageGenerator
        from . import state
        if state.generator is None:
            state.generator = LocalImageGenerator()
