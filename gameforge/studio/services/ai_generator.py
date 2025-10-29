import os
import torch
from transformers import (
    pipeline,
    AutoTokenizer,
    AutoModelForSeq2SeqLM
)
from functools import lru_cache
from threading import Lock

_MODEL_NAME = os.getenv("HF_LOCAL_MODEL", "google/flan-t5-base")
_init_lock = Lock()

@lru_cache(maxsize=1)
def get_pipe():
    with _init_lock:
        device = 0 if torch.cuda.is_available() else -1
        tok = AutoTokenizer.from_pretrained(_MODEL_NAME)
        model = AutoModelForSeq2SeqLM.from_pretrained(_MODEL_NAME)
        return pipeline(
            "text2text-generation",   # <-- clé du problème
            model=model,
            tokenizer=tok,
            device=device,
        )

def generate_text(prompt: str, max_new_tokens: int = 256, temperature: float = 0.7) -> str:
    pipe = get_pipe()
    out = pipe(
        prompt,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        temperature=temperature,
        top_p=0.9,
    )
    return out[0]["generated_text"].strip()


# --------------------- PROMPTS ---------------------

def prompt_universe(genre, ambiance, themes, references):
    refs = references or "aucune"
    return (
        f"Décris en français l'univers d'un jeu vidéo de type {genre} avec une ambiance {ambiance}. "
        f"Thèmes : {themes}. Références possibles : {refs}. "
        f"Fais une description immersive en deux paragraphes avec lieux, factions et enjeux concrets."
    )

def prompt_story(genre, ambiance):
    return (
        f"Raconte l'histoire principale d'un jeu vidéo {genre} dans une ambiance {ambiance}. "
        f"L'histoire doit être divisée en trois actes, trois phrases maximum chacun, "
        f"et contenir un retournement final inattendu."
    )

def prompt_characters(genre):
    return (
        f"Propose quatre personnages originaux pour un jeu {genre}. "
        f"Pour chacun, indique : Nom, Rôle narratif, Classe, Personnalité, Motivation et Aspect gameplay."
    )

def generate_concept_sections(genre, ambiance, themes, references):
    uni = generate_text(prompt_universe(genre, ambiance, themes, references), max_new_tokens=300, temperature=0.7)
    sto = generate_text(prompt_story(genre, ambiance), max_new_tokens=250, temperature=0.7)
    cha = generate_text(prompt_characters(genre), max_new_tokens=300, temperature=0.75)
    return {"universe": uni, "story": sto, "characters": cha}
