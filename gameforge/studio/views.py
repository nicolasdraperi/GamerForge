import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import GameConcept
from .services.ai_generator import generate_concept_sections
from .models import GameConcept, Character, Location


def _to_dict_safe(maybe_json):
    if isinstance(maybe_json, dict):
        return maybe_json
    if not maybe_json or not isinstance(maybe_json, str):
        return {}
    s = maybe_json.strip()
    if s.startswith("```"):
        s = s.strip("`")
        if s.lower().startswith("json"):
            s = s[4:].lstrip()
    try:
        return json.loads(s)
    except Exception:
        return {}

def _as_text_list(value):
    """Normalise un dict ou une liste en liste de textes."""
    if isinstance(value, list):
        return [str(x).strip() for x in value if str(x).strip()]
    if isinstance(value, dict):
        out = []
        for k in sorted(value.keys()):
            v = value.get(k)
            if v:
                if isinstance(v, (list, tuple)):
                    out += [str(x).strip() for x in v if str(x).strip()]
                else:
                    out.append(str(v).strip())
        return [x for x in out if x]
    if value:
        return [str(value).strip()]
    return []

def _extract_universe_text(universe):
    """Supporte: dict avec description/histoire/paragrapheX, ou texte brut."""
    if isinstance(universe, dict):
        parts = []
        for key in ("description", "histoire"):
            if universe.get(key):
                parts.append(str(universe[key]).strip())
        para_candidates = {k: v for k, v in universe.items() if "paragraphe" in k.lower()}
        if para_candidates:
            parts += _as_text_list(para_candidates)
        return "\n\n".join([p for p in parts if p]).strip()
    return (str(universe) or "").strip()

def _extract_story_text(story):
    """Supporte: actes en dict -> listes ou phraseX; ou liste simple."""
    if isinstance(story, dict):
        lines = []
        for act_key in sorted(story.keys()):
            act_val = story[act_key]
            if isinstance(act_val, list):
                lines += [str(x).strip() for x in act_val if str(x).strip()]
            elif isinstance(act_val, dict):
                for phrase_key in sorted(act_val.keys()):
                    phrase = act_val[phrase_key]
                    if phrase:
                        lines.append(str(phrase).strip())
            elif act_val:
                lines.append(str(act_val).strip())
        return "\n".join([l for l in lines if l]).strip()
    if isinstance(story, list):
        return "\n".join([str(x).strip() for x in story if str(x).strip()]).strip()
    return (str(story) or "").strip()

def _iter_characters(chars):
    """Tolère les clés FR/minuscule/camelCase."""
    if not isinstance(chars, list):
        return
    for c in chars:
        if not isinstance(c, dict):
            continue
        lower = {str(k).lower(): v for k, v in c.items()}
        name = lower.get("nom") or lower.get("name")
        role = lower.get("rôle") or lower.get("role") or "Personnage"
        desc_parts = []
        for key in ["personnalité", "personality", "motivation", "hook gameplay", "hookgameplay", "description"]:
            if key in lower and lower[key]:
                label = "Hook gameplay" if "hook" in key else key.capitalize()
                desc_parts.append(f"{label}: {lower[key]}")
        description = "\n".join(desc_parts).strip()
        if name:
            yield {"name": str(name).strip(), "role": str(role).strip(), "description": description}

def _iter_locations_from_universe(universe):
    """Crée des lieux si universe.lieux est une liste de noms."""
    if not isinstance(universe, dict):
        return
    lieux = universe.get("lieux") or universe.get("locations") or []
    if isinstance(lieux, list):
        for name in lieux:
            name = str(name).strip()
            if name:
                yield {"name": name, "description": ""}

@login_required
def create_game(request):
    if request.method == 'POST':
        title = (request.POST.get('title') or 'Concept sans nom').strip()
        genre = (request.POST.get('genre') or '').strip()
        ambiance = (request.POST.get('ambiance') or '').strip()
        themes = (request.POST.get('themes') or '').strip()
        references = (request.POST.get('references') or '').strip()

        if not genre or not ambiance or not themes:
            messages.error(request, "Les champs Genre, Ambiance et Thèmes sont obligatoires.")
            return redirect('create_game')

        try:
            sections = generate_concept_sections(genre, ambiance, themes, references)
        except Exception as e:
            messages.error(request, f"Erreur pendant la génération IA : {e}")
            return redirect('create_game')

        data = _to_dict_safe(sections)

        universe = data.get("universe") or data.get("univers") or {}
        story = data.get("story") or data.get("histoire") or {}

        universe_text = _extract_universe_text(universe) or "L'univers de ce jeu est en cours de création..."
        story_text = _extract_story_text(story)

        keywords = themes if not references else f"{themes}, {references}"

        
        generated_image_path = None
        try:
            from . import state
            if state.generator:
                prompt = f"{genre} game, {ambiance}, {themes}, fantasy art, concept art, high quality"
                file_url = state.generator.generate(prompt)  
              
                if file_url:
                    import os
                    from django.conf import settings
                
                    generated_image_path = os.path.join(settings.BASE_DIR, file_url.lstrip('/'))
        except Exception as e:
            print(f"Erreur génération image: {e}")
            

        with transaction.atomic():
            game = GameConcept.objects.create(
                creator=request.user,
                title=title,
                genre=genre,
                theme=ambiance,
                keywords=keywords,
                universe_description=universe_text,
                story=story_text,
            )
            
        
            if generated_image_path and os.path.exists(generated_image_path):
                from django.core.files import File
                import shutil
                with open(generated_image_path, 'rb') as f:
                    game.cover_image.save(
                        f"cover_{game.id}.png",
                        File(f),
                        save=True
                    )
            for ch in _iter_characters(data.get("characters") or data.get("personnages") or []):
                Character.objects.create(
                    game_concept=game,
                    name=ch["name"],
                    role=ch["role"],
                    description=ch["description"],
                )
            for loc in _iter_locations_from_universe(universe):
                Location.objects.create(
                    game_concept=game,
                    name=loc["name"],
                    description=loc["description"],
                )

        messages.success(request, f'Le jeu "{title}" a été généré avec succès.')
        return redirect('game_detail', pk=game.pk)

    context = {
        'genre_choices': getattr(GameConcept, "GENRE_CHOICES", []),
    }
    return render(request, 'studio/create.html', context)


def game_detail(request, pk):
    game = get_object_or_404(GameConcept, pk=pk)

    if not game.is_public and game.creator != request.user:
        messages.error(request, "Vous n'avez pas accès à ce jeu.")
        return redirect('home')

    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = game.favorited_by.filter(id=request.user.id).exists()

    raw = game.keywords or ""
    keywords_list = [k.strip() for k in raw.split(",") if k.strip()]

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