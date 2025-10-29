from django.contrib import admin
from .models import GameConcept, Character, Location


class CharacterInline(admin.TabularInline):
    model = Character
    extra = 1


class LocationInline(admin.TabularInline):
    model = Location
    extra = 1


@admin.register(GameConcept)
class GameConceptAdmin(admin.ModelAdmin):
    list_display = ['title', 'genre', 'owner', 'created_at']
    list_filter = ['genre', 'created_at']
    search_fields = ['title', 'themes', 'owner__username']
    inlines = [CharacterInline, LocationInline]
    readonly_fields = ['created_at']


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'game_concept']
    list_filter = ['role']
    search_fields = ['name', 'game_concept__title']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'game_concept']
    search_fields = ['name', 'game_concept__title']
