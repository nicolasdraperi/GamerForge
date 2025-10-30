from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import GameConcept, Character, Location

# Create your views here.

@login_required
def create_game(request):
    """Vue de création de concept de jeu"""
    if request.method == 'POST':
        title = request.POST.get('title')
        genre = request.POST.get('genre')
        theme = request.POST.get('theme', '')
        keywords = request.POST.get('keywords', '')
        
        # Créer le concept de jeu
        game = GameConcept.objects.create(
            title=title,
            creator=request.user,
            genre=genre,
            theme=theme,
            keywords=keywords,
            universe_description=f"Un jeu {genre} captivant. {theme}",
            story="L'histoire de ce jeu sera générée par l'IA dans une prochaine version."
        )
        
        messages.success(request, f'Le jeu "{title}" a été créé avec succès !')
        return redirect('game_detail', pk=game.id)
    
    context = {
        'genre_choices': GameConcept.GENRE_CHOICES,
    }
    return render(request, 'studio/create.html', context)


def game_detail(request, pk):
    """Page de détail d'un concept de jeu"""
    game = get_object_or_404(GameConcept, pk=pk)
    
    # Vérifier si l'utilisateur a accès (public ou propriétaire)
    if not game.is_public and game.creator != request.user:
        messages.error(request, "Vous n'avez pas accès à ce jeu.")
        return redirect('home')
    
    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = game.favorited_by.filter(id=request.user.id).exists()
    
    # Splitter les mots-clés pour l'affichage
    keywords_list = [kw.strip() for kw in game.keywords.split(',')] if game.keywords else []
    
    context = {
        'game': game,
        'is_favorited': is_favorited,
        'keywords_list': keywords_list,
    }
    return render(request, 'studio/detail.html', context)


@login_required
def dashboard(request):
    """Tableau de bord personnel de l'utilisateur"""
    user_games = GameConcept.objects.filter(creator=request.user)
    
    context = {
        'user_games': user_games,
    }
    return render(request, 'studio/dashboard.html', context)


@login_required
def favorites(request):
    """Page des favoris de l'utilisateur"""
    favorite_games = request.user.favorite_games.all()
    
    context = {
        'favorite_games': favorite_games,
    }
    return render(request, 'studio/favorites.html', context)


@login_required
def toggle_favorite(request, pk):
    """Ajouter/retirer un jeu des favoris"""
    game = get_object_or_404(GameConcept, pk=pk)
    
    if game.favorited_by.filter(id=request.user.id).exists():
        game.favorited_by.remove(request.user)
        messages.success(request, 'Jeu retiré des favoris.')
    else:
        game.favorited_by.add(request.user)
        messages.success(request, 'Jeu ajouté aux favoris !')
    
    return redirect('game_detail', pk=pk)


@login_required
def toggle_visibility(request, pk):
    """Basculer la visibilité public/privé d'un jeu"""
    game = get_object_or_404(GameConcept, pk=pk, creator=request.user)
    game.is_public = not game.is_public
    game.save()
    
    status = "public" if game.is_public else "privé"
    messages.success(request, f'Jeu passé en {status}.')
    
    return redirect('dashboard')


@login_required
def delete_game(request, pk):
    """Supprimer un concept de jeu"""
    game = get_object_or_404(GameConcept, pk=pk, creator=request.user)
    
    if request.method == 'POST':
        title = game.title
        game.delete()
        messages.success(request, f'Le jeu "{title}" a été supprimé.')
        return redirect('dashboard')
    
    return render(request, 'studio/delete_confirm.html', {'game': game})