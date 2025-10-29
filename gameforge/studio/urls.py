from django.urls import path
from . import views

urlpatterns = [
    # Gestion des jeux
    path('create/', views.create_game, name='create_game'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('game/<int:pk>/', views.game_detail, name='game_detail'),
    path('game/<int:pk>/delete/', views.delete_game, name='delete_game'),
    path('game/<int:pk>/toggle-visibility/', views.toggle_visibility, name='toggle_visibility'),
    
    # Favoris
    path('favorites/', views.favorites, name='favorites'),
    path('game/<int:pk>/toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
]

