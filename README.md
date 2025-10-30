# 🎮 GameForge - Générateur de Jeux Vidéo par IA

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Django](https://img.shields.io/badge/Django-5.2.7-green)
![Python](https://img.shields.io/badge/Python-3.12+-yellow)

**GameForge** est une plateforme web complète développée avec Django permettant de créer des concepts de jeux vidéo originaux à l'aide de modèles d'intelligence artificielle. L'application génère automatiquement un univers cohérent, une histoire immersive, des personnages, et des illustrations conceptuelles.

---

## 📋 Table des matières

- [Fonctionnalités](#-fonctionnalités)
- [Technologies utilisées](#-technologies-utilisées)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Structure du projet](#-structure-du-projet)
- [Utilisation](#-utilisation)
- [Modèles de données](#-modèles-de-données)
- [API IA utilisées](#-api-ia-utilisées)
- [Screenshots](#-screenshots)
- [Contributeurs](#-contributeurs)

---
## schéma de la transitions des données

<img width="830" height="464" alt="image" src="https://github.com/user-attachments/assets/7f6b3d8f-c17c-4da9-bfe2-00fd54ab0f54" />

---

## ✨ Fonctionnalités

### 🎨 Interface utilisateur complète
- ✅ **Page d'accueil** : Galerie de tous les jeux publics créés par la communauté
- ✅ **Recherche & Filtres** : Recherche par titre et filtrage par genre
- ✅ **Création de jeu** : Formulaire guidé avec génération IA en temps réel
- ✅ **Page de détail** : Vue complète de chaque concept (univers, histoire, personnages, lieux)
- ✅ **Tableau de bord** : Gestion personnelle de ses créations
- ✅ **Système de favoris** : Sauvegarder ses jeux préférés
- ✅ **Visibilité Public/Privé** : Contrôle de la publication de ses projets
- ✅ **Design moderne** : Interface dark/fantasy responsive et immersive

### 🤖 Génération IA
- 🧠 **Génération de texte** : Univers, histoire structurée, personnages et lieux via **Groq API**
- 🎨 **Génération d'images** : Illustrations conceptuelles via **Stable Diffusion** (local)
- ⚡ **Barre de progression** : Indicateur visuel pendant la génération

### 🔐 Authentification & Sécurité
- 👤 Inscription / Connexion / Déconnexion
- 🔒 Protection des projets (seul l'auteur peut modifier/supprimer)
- 🌐 Partage public optionnel
- 🔑 API JWT ready (pour extension future)

---

## 🛠 Technologies utilisées

### Backend
- **Django 5.2.7** - Framework web Python
- **Django REST Framework 3.16.1** - API REST
- **SQLite** - Base de données (dev)
- **Pillow 12.0.0** - Traitement d'images

### IA & Machine Learning
- **Groq API** - Génération de texte (modèle llama-3.3-70b-versatile)
- **Stable Diffusion** - Génération d'images (via diffusers 0.35.2)
- **PyTorch 2.9.0** - Framework ML
- **Transformers 4.57.1** - Modèles Hugging Face

### Frontend
- **HTML5 / CSS3** - Structure et style
- **JavaScript (Vanilla)** - Interactivité
- **Design responsive** - Compatible mobile/tablette/desktop

### Outils
- **python-dotenv** - Gestion des variables d'environnement
- **django-cors-headers** - Support CORS pour API

---

## 📥 Installation

### Prérequis
- **Python 3.12+** installé
- **Git** installé
- **10 GB d'espace disque libre** (pour les modèles IA)
- **Clés API Groq** (gratuite sur [groq.com](https://groq.com))

### 1️⃣ Cloner le projet

```bash
git clone https://github.com/nicolasdraperi/GamerForge.git
cd GamerForge
```

### 2️⃣ Créer un environnement virtuel

```bash
python -m venv venv
```

**Windows (PowerShell) :**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD) :**
```cmd
venv\Scripts\activate.bat
```

**macOS / Linux :**
```bash
source venv/bin/activate
```

### 3️⃣ Installer les dépendances

```bash
pip install -r requirements.txt
```

> ⚠️ **Note** : L'installation de PyTorch et Stable Diffusion peut prendre 10-15 minutes et télécharger environ 6-8 GB de données.

### 4️⃣ Créer les dossiers nécessaires

```bash
cd gameforge
mkdir media
mkdir media\generated
mkdir media\concepts
mkdir media\concepts\covers
```

### 5️⃣ Configurer les variables d'environnement

Créer un fichier `.env` à la racine du projet (dans le dossier `GamerForge/`) :

```env
# Django
SECRET_KEY=votre-secret-key-django-tres-securisee-ici
DEBUG=True

# Groq API (génération de texte)
GROQ_API_KEY=votre_cle_api_groq_ici

# Optionnel : Base de données (par défaut SQLite)
# DATABASE_URL=postgres://user:password@localhost/gameforge
```

> 💡 **Obtenir une clé Groq** : Créez un compte gratuit sur [console.groq.com](https://console.groq.com) et générez une clé API.

### 6️⃣ Préparer la base de données

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7️⃣ Créer un super-utilisateur (admin)

```bash
python manage.py createsuperuser
```

Suivez les instructions et notez bien vos identifiants.

### 8️⃣ Lancer le serveur

```bash
python manage.py runserver
```

✅ **Le site est accessible sur** : [http://127.0.0.1:8000](http://127.0.0.1:8000)

🔧 **Interface admin** : [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

---

## ⚙️ Configuration

### Performance - Génération d'image

**Première génération** : ~3-5 minutes (téléchargement du modèle Stable Diffusion)
**Générations suivantes** : ~20-40 secondes (selon votre matériel)

Pour accélérer (optionnel) :
- Utiliser un GPU NVIDIA avec CUDA
- Réduire la résolution dans `studio/services/ai_image.py`

### Désactiver temporairement la génération d'image

Si vous voulez tester sans attendre le téléchargement du modèle :

1. Ouvrir `gameforge/studio/apps.py`
2. Commenter les lignes d'initialisation :

```python
def ready(self):
    # from .services.ai_image import LocalImageGenerator
    # from . import state
    # state.generator = LocalImageGenerator()
    pass
```

---

## 📁 Structure du projet

```
GamerForge/
├── gameforge/                    # Projet Django principal
│   ├── gameforge/                # Configuration du projet
│   │   ├── settings.py          # ✅ Paramètres Django
│   │   ├── urls.py              # ✅ Routes principales
│   │   ├── wsgi.py / asgi.py    # ✅ Serveurs
│   │   └── __init__.py
│   │
│   ├── studio/                   # 🎨 App principale (création de jeux)
│   │   ├── models.py            # ✅ GameConcept, Character, Location
│   │   ├── views.py             # ✅ Logique métier (CRUD, génération)
│   │   ├── urls.py              # ✅ Routes studio
│   │   ├── admin.py             # ✅ Interface admin
│   │   ├── apps.py              # ✅ Configuration (init IA)
│   │   ├── state.py             # ✅ Singleton générateur d'images
│   │   ├── services/
│   │   │   ├── ai_generator.py  # 🤖 Génération texte (Groq)
│   │   │   └── ai_image.py      # 🎨 Génération images (Stable Diffusion)
│   │   └── migrations/
│   │
│   ├── accounts/                 # 👤 Authentification
│   │   ├── views.py             # ✅ Login, Register, Logout
│   │   ├── urls.py              # ✅ Routes auth
│   │   └── serializers.py       # ✅ API JWT (bonus)
│   │
│   ├── core/                     # 🏠 Page d'accueil
│   │   ├── views.py             # ✅ Home avec recherche/filtres
│   │   └── urls.py              # ✅ Route home
│   │
│   ├── templates/                # 📄 Templates HTML
│   │   ├── base.html            # ✅ Template parent
│   │   ├── core/
│   │   │   └── home.html        # ✅ Page d'accueil
│   │   ├── accounts/
│   │   │   ├── login.html       # ✅ Connexion
│   │   │   └── register.html    # ✅ Inscription
│   │   └── studio/
│   │       ├── create.html      # ✅ Formulaire création
│   │       ├── detail.html      # ✅ Détail d'un jeu
│   │       ├── dashboard.html   # ✅ Mes projets
│   │       ├── favorites.html   # ✅ Mes favoris
│   │       └── delete_confirm.html # ✅ Confirmation suppression
│   │
│   ├── static/                   # 🎨 Fichiers statiques
│   │   ├── styles.css           # ✅ CSS principal (dark theme)
│   │   └── scripts.js           # ✅ JavaScript
│   │
│   ├── media/                    # 📁 Fichiers uploadés/générés
│   │   ├── generated/           # Images générées temporaires
│   │   └── concepts/
│   │       └── covers/          # Images de couverture
│   │
│   ├── manage.py                 # ⚙️ CLI Django
│   └── db.sqlite3                # 📊 Base de données (dev)
│
├── venv/                         # Environnement virtuel (ignoré)
├── requirements.txt              # 📦 Dépendances Python
├── .gitignore                    # 🚫 Fichiers à ignorer
├── .env                          # 🔑 Variables d'environnement (ignoré)
└── README.md                     # 📖 Ce fichier
```

---

## 🎮 Utilisation

### Créer un concept de jeu

1. **Se connecter** ou créer un compte
2. Cliquer sur **"Nouveau Jeu"** (bouton jaune en haut à droite)
3. Remplir le formulaire :
   - **Titre** : Nom de votre jeu
   - **Genre** : RPG, FPS, Strategy, etc.
   - **Ambiance** : dark fantasy, cyberpunk, post-apocalyptique...
   - **Mots-clés** : boucle temporelle, vengeance, IA rebelle...
   - **Références** (optionnel) : Zelda, Hollow Knight...
4. Cliquer sur **"Générer le concept"**
5. **Patienter 30-60 secondes** pendant la génération IA
6. Votre jeu est créé ! 🎉

### Gérer ses projets

- **Tableau de bord** : Voir tous ses jeux créés
- **Modifier la visibilité** : Public ↔ Privé (bouton 🔓/🔒)
- **Supprimer** : Bouton poubelle avec confirmation
- **Voir les détails** : Cliquer sur une carte

### Explorer la galerie

- **Page d'accueil** : Tous les jeux publics
- **Recherche** : Barre de recherche par titre
- **Filtres** : Dropdown par genre
- **Favoris** : Cliquer sur ⭐ pour ajouter/retirer

---

## 📊 Modèles de données

### GameConcept (Concept de jeu)

```python
class GameConcept(models.Model):
    title = models.CharField(max_length=200)           # Titre du jeu
    creator = models.ForeignKey(User)                  # Créateur
    genre = models.CharField(max_length=100)           # RPG, FPS, etc.
    theme = models.CharField(max_length=200)           # Ambiance
    keywords = models.TextField()                      # Mots-clés
    universe_description = models.TextField()          # Univers (généré)
    story = models.TextField()                         # Histoire (générée)
    cover_image = models.ImageField()                  # Image générée
    is_public = models.BooleanField(default=False)     # Visibilité
    favorited_by = models.ManyToManyField(User)        # Favoris
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Character (Personnage)

```python
class Character(models.Model):
    game_concept = models.ForeignKey(GameConcept)      # Jeu parent
    name = models.CharField(max_length=200)            # Nom
    role = models.CharField(max_length=200)            # Rôle/Classe
    description = models.TextField()                   # Description
```

### Location (Lieu)

```python
class Location(models.Model):
    game_concept = models.ForeignKey(GameConcept)      # Jeu parent
    name = models.CharField(max_length=200)            # Nom du lieu
    description = models.TextField()                   # Description
```

---

## 🤖 API IA utilisées

### Groq API (Génération de texte)

- **Modèle** : `llama-3.3-70b-versatile`
- **Endpoint** : `https://api.groq.com/openai/v1/chat/completions`
- **Coût** : Gratuit (avec limites)
- **Génère** : Univers, histoire structurée en 3 actes, personnages, lieux

### Stable Diffusion (Génération d'images)

- **Modèle** : `stabilityai/stable-diffusion-2-1-base` (via Hugging Face)
- **Execution** : Locale (CPU ou GPU)
- **Résolution** : 512x512 pixels
- **Format** : PNG
- **Génère** : Image de couverture pour chaque jeu

---

## 📸 Screenshots

### Page d'accueil
<img width="1893" height="865" alt="image" src="https://github.com/user-attachments/assets/8f607929-f90e-42d1-9b87-da562d0bfe76" />

*Galerie de concepts avec recherche et filtres*

### Formulaire de création
<img width="802" height="746" alt="image" src="https://github.com/user-attachments/assets/e5110be8-58e1-4bb4-a561-5fa5d3ea3f6f" />
<img width="515" height="566" alt="image" src="https://github.com/user-attachments/assets/ef44d3b6-07bf-4994-9618-5e783e81f19e" />

*Interface de création guidée avec barre de progression*

### Détail d'un jeu
<img width="951" height="690" alt="image" src="https://github.com/user-attachments/assets/1ec3994a-7f3f-4b55-9f65-77accefa2562" />
<img width="886" height="713" alt="image" src="https://github.com/user-attachments/assets/de81cd59-511a-44f3-826f-3e131eafc8c2" />

*Vue complète : univers, histoire, personnages, lieux*

### Tableau de bord
<img width="994" height="704" alt="image" src="https://github.com/user-attachments/assets/b0819d27-e979-4444-b816-82389155757b" />

*Gestion personnelle des créations*

---

## 👥 Contributeurs

**Projet développé dans le cadre du TP Django - IPSSI**

- **Frontend & Intégration** : Hugo K. ([@hugok](https://github.com/hugok))
- **Backend & IA** : Nicolas Draperi ([@nicolasdraperi](https://github.com/nicolasdraperi))
- **IA & Intégration** : Nail Benamer ([@nbenamer](https://github.com/nbenamer))


---

## 📝 License

Ce projet est développé à des fins éducatives dans le cadre d'un TP IPSSI.

---

## 🐛 Problèmes connus

- ⏱️ La première génération d'image est lente (téléchargement du modèle)
- 💾 Les modèles IA prennent ~6-8 GB d'espace disque
- 🖥️ La génération d'image sur CPU est lente (~30-60s)

## 🚀 Améliorations futures

- [ ] Export PDF des concepts de jeu
- [ ] Système de notation/commentaires
- [ ] Génération de plusieurs images par concept
- [ ] Support de plus de modèles IA
- [ ] Mode "exploration libre" (génération aléatoire complète)
- [ ] Game Design Document (GDD) complet
- [ ] Partage sur réseaux sociaux

---

## 📞 Support

Pour toute question ou problème :
- 📧 Email : [contact@example.com](mailto:contact@example.com)
- 🐛 Issues : [GitHub Issues](https://github.com/nicolasdraperi/GamerForge/issues)

---

**Fait avec ❤️ et 🤖 IA**




