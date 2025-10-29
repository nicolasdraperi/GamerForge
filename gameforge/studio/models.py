from django.db import models
from django.conf import settings

class GameConcept(models.Model):
    GENRES = [
        ("RPG", "RPG"),
        ("FPS", "FPS"),
        ("Metroidvania", "Metroidvania"),
        ("Visual Novel", "Visual Novel"),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="concepts")
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=50, choices=GENRES)
    ambiance = models.CharField(max_length=150)
    themes = models.TextField(help_text="Mots-clés thématiques")
    references = models.TextField(blank=True, null=True)

    universe = models.TextField(blank=True, null=True)
    story = models.TextField(blank=True, null=True)
    characters = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
