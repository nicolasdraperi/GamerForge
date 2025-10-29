from django.db import models
from django.contrib.auth.models import User


class GameConcept(models.Model):
    """Modèle représentant un concept de jeu généré par IA"""
    
    GENRE_CHOICES = [
        ('RPG', 'RPG'),
        ('FPS', 'FPS'),
        ('Metroidvania', 'Metroidvania'),
        ('Visual Novel', 'Visual Novel'),
        ('Platformer', 'Platformer'),
        ('Strategy', 'Strategy'),
        ('Adventure', 'Adventure'),
        ('Puzzle', 'Puzzle'),
        ('Dark Fantasy', 'Dark Fantasy'),
    ]
    
    # Informations de base
    title = models.CharField(max_length=200, verbose_name="Titre", default="Unseen")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_concepts')
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
    theme = models.TextField(verbose_name="Thème", blank=True)
    keywords = models.CharField(max_length=500, verbose_name="Mots-clés", blank=True)
    
    # Contenu généré par IA
    universe_description = models.TextField(verbose_name="Description de l'univers", blank=True)
    story = models.TextField(verbose_name="Histoire", blank=True)
    
    # Métadonnées
    is_public = models.BooleanField(default=True, verbose_name="Public")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    favorited_by = models.ManyToManyField(User, related_name='favorite_games', blank=True)
    
    # Images générées
    cover_image = models.ImageField(upload_to='concepts/covers/', blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Concept de jeu"
        verbose_name_plural = "Concepts de jeux"
    
    def __str__(self):
        return f"{self.title} - {self.genre}"
    
    def favorite_count(self):
        return self.favorited_by.count()


class Character(models.Model):
    """Modèle représentant un personnage d'un concept de jeu"""
    
    game_concept = models.ForeignKey(GameConcept, on_delete=models.CASCADE, related_name='characters')
    name = models.CharField(max_length=200, verbose_name="Nom")
    role = models.CharField(max_length=100, verbose_name="Rôle")
    description = models.TextField(verbose_name="Description")
    
    class Meta:
        verbose_name = "Personnage"
        verbose_name_plural = "Personnages"
    
    def __str__(self):
        return f"{self.name} - {self.role}"


class Location(models.Model):
    """Modèle représentant un lieu emblématique d'un concept de jeu"""
    
    game_concept = models.ForeignKey(GameConcept, on_delete=models.CASCADE, related_name='locations')
    name = models.CharField(max_length=200, verbose_name="Nom")
    description = models.TextField(verbose_name="Description")
    
    class Meta:
        verbose_name = "Lieu"
        verbose_name_plural = "Lieux"
    
    def __str__(self):
        return self.name
