import os
import json
import re
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


class AIGenerationError(Exception):
    pass

def _groq_chat(prompt: str, max_tokens: int = 1200, temperature: float = 0.6) -> str:
    if not GROQ_API_KEY:
        raise AIGenerationError("GROQ_API_KEY manquant dans les variables d'environnement.")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "response_format": {"type": "json_object"},
    }

    resp = requests.post(GROQ_URL, headers=headers, json=payload, timeout=60)
    try:
        resp.raise_for_status()
    except requests.HTTPError as e:
        raise AIGenerationError(f"Groq API error: {resp.status_code} {resp.text}") from e

    data = resp.json()
    content = data["choices"][0]["message"]["content"]
    return (content or "").strip()


def _strip_code_fences(text: str) -> str:
    """
    Supprime les fences ``` ou ```json ... et retourne l'intérieur.
    Si pas de fences, retourne text tel quel.
    """
    t = (text or "").strip()
    if t.startswith("```"):
        lines = t.splitlines()
        if len(lines) >= 2 and lines[0].startswith("```") and lines[-1].startswith("```"):
            inner = "\n".join(lines[1:-1]).strip()
            if inner.lower().startswith("json"):
                inner = inner[4:].lstrip()
            return inner
    return t


def _extract_json_substring(text: str) -> str:
    """
    Essaie d'extraire la portion JSON entre le premier '{' et le dernier '}'.
    Utile si l'IA ajoute du bruit autour.
    """
    if not text:
        return ""
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return text[start : end + 1]
    return text


def _prompt_all(genre: str, ambiance: str, themes: str, references: str) -> str:
    refs = references.strip() if references else "aucune"
    return (
        "Tu es un game designer francophone. Génère un concept de jeu vidéo.\n"
        "Contraintes de sortie STRICTES:\n"
        "1) Retourne EXCLUSIVEMENT un JSON VALIDE UTF-8. Aucune prose hors JSON. Pas de code fences.\n"
        "2) Schéma JSON attendu (toutes les clés en français, casse et variantes tolérées côté serveur):\n"
        "{\n"
        '  "universe": {\n'
        '    "description": string,            // 1 à 2 paragraphes immersifs\n'
        '    "histoire": string,               // contexte, enjeux, factions\n'
        '    "lieux": string[],                // 3 à 5 lieux clés (noms)\n'
        '    "factions": string[]              // 2 à 4 factions (noms)\n'
        "  },\n"
        '  "story": {\n'
        '    "acte1": string[],                // 2 à 3 phrases maximum\n'
        '    "acte2": string[],                // 2 à 3 phrases maximum\n'
        '    "acte3": string[]                 // 2 à 3 phrases maximum, avec un retournement\n'
        "  },\n"
        '  "characters": [                     // 3 à 4 personnages\n'
        "    {\n"
        '      "nom": string,\n'
        '      "rôle": string,\n'
        '      "classe": string,\n'
        '      "personnalité": string,\n'
        '      "motivation": string,\n'
        '      "hookGameplay": string\n'
        "    }\n"
        "  ]\n"
        "}\n"
        "Règles supplémentaires:\n"
        "- Langue: français.\n"
        "- Interdiction d’ajouter du texte hors JSON ou des commentaires JSON.\n"
        "- Pas de virgules finales (trailing commas).\n"
        "- Longueurs: chaque phrase < 220 caractères.\n"
        "- Ton: mature et clair.\n"
        "\n"
        f"Données d'entrée:\n"
        f"- Genre: {genre}\n"
        f"- Ambiance: {ambiance}\n"
        f"- Thèmes: {themes}\n"
        f"- Références: {refs}\n"
    )


def _safe_json_loads(text: str):
    """
    Essaie de parser le JSON avec plusieurs stratégies.
    Retourne dict ou lève AIGenerationError si tout échoue.
    """
    try:
        return json.loads(text)
    except Exception:
        pass

    stripped = _strip_code_fences(text)
    if stripped != text:
        try:
            return json.loads(stripped)
        except Exception:
            pass
    sub = _extract_json_substring(stripped)
    if sub and sub != stripped:
        try:
            return json.loads(sub)
        except Exception:
            pass
    cleaned = stripped.replace("\uFEFF", "").strip()
    try:
        return json.loads(cleaned)
    except Exception as e:
        raise AIGenerationError(f"Réponse IA non JSON: {e}\nAperçu: {text[:400]}") from e


def generate_concept_sections(genre: str, ambiance: str, themes: str, references: str):
    """
    Retourne un dict conforme à ton pipeline serveur.
    Exemple de structure:
    {
      "universe": {
        "description": "...",
        "histoire": "...",
        "lieux": ["..."],
        "factions": ["..."]
      },
      "story": {
        "acte1": ["..."],
        "acte2": ["..."],
        "acte3": ["..."]
      },
      "characters": [
        {"nom": "...", "rôle": "...", "classe": "...", "personnalité": "...", "motivation": "...", "hookGameplay": "..."}
      ]
    }
    """
    prompt = _prompt_all(genre, ambiance, themes, references)
    raw = _groq_chat(prompt, max_tokens=1200, temperature=0.6)

    try:
        data = _safe_json_loads(raw)
    except AIGenerationError:
        return {
            "universe": {
                "description": "",
                "histoire": "",
                "lieux": [],
                "factions": [],
            },
            "story": {
                "acte1": [],
                "acte2": [],
                "acte3": [],
            },
            "characters": [],
        }
    universe = data.get("universe") or data.get("univers") or {}
    story = data.get("story") or data.get("histoire") or {}
    characters = data.get("characters") or data.get("personnages") or []

    if not isinstance(universe, dict):
        universe = {}
    if not isinstance(story, dict):
        story = {}
    if not isinstance(characters, list):
        characters = []

    universe.setdefault("description", "")
    universe.setdefault("histoire", "")
    universe.setdefault("lieux", [])
    universe.setdefault("factions", [])
    story.setdefault("acte1", [])
    story.setdefault("acte2", [])
    story.setdefault("acte3", [])

    return {
        "universe": universe,
        "story": story,
        "characters": characters,
    }
