from django.shortcuts import render
from django.db.models import Q
from studio.models import GameConcept


def home(request):
    """Page d'accueil affichant tous les jeux publics"""
    search_query = request.GET.get('search', '')
    genre_filter = request.GET.get('genre', '')
    
    games = GameConcept.objects.filter(is_public=True)
    
    if search_query:
        games = games.filter(
            Q(title__icontains=search_query) |
            Q(keywords__icontains=search_query) |
            Q(creator__username__icontains=search_query)
        )
    
    if genre_filter:
        games = games.filter(genre=genre_filter)
    
    context = {
        'games': games,
        'search_query': search_query,
        'genre_filter': genre_filter,
        'genre_choices': GameConcept.GENRE_CHOICES,
    }
    return render(request, 'core/home.html', context)
