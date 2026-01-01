# 📚 Tutoriel Django - Projet Connecteo

## 🎯 Table des matières

1. [Qu'est-ce que Django ?](#quest-ce-que-django)
2. [Structure du projet](#structure-du-projet)
3. [Les composants principaux](#les-composants-principaux)
4. [Comment ça fonctionne ?](#comment-ça-fonctionne)
5. [Guide pratique](#guide-pratique)

---

## 🚀 Qu'est-ce que Django ?

**Django** est un framework web Python qui vous aide à créer des sites web rapidement et facilement.

### Pourquoi Django ?

- ✅ **Rapide** : Beaucoup de fonctionnalités prêtes à l'emploi
- ✅ **Sécurisé** : Protection contre les attaques courantes
- ✅ **Scalable** : Peut gérer des millions d'utilisateurs
- ✅ **Bien documenté** : Facile à apprendre

### L'architecture MTV (Model-Template-View)

```
┌─────────────┐
│  UTILISATEUR │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   URLS      │ ← Reçoit la requête
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   VIEWS     │ ← Traite la logique
└──────┬──────┘
       │
       ├─────► MODELS (Base de données)
       │
       └─────► TEMPLATES (HTML)
       │
       ▼
┌─────────────┐
│   RÉPONSE   │ ← Renvoie la page
└─────────────┘
```

---

## 📁 Structure du projet Connecteo

```
projet_app_connecteo/
│
├── 🐳 docker-compose.yml      # Configuration Docker
├── 🐳 Dockerfile              # Image Docker
├── 📋 requirements.txt        # Dépendances Python
├── 📖 README.md               # Documentation
│
├── 🌐 connecteo/              # PROJET DJANGO PRINCIPAL
│   │
│   ├── manage.py              # Commandes Django (runserver, migrate, etc.)
│   ├── db.sqlite3             # Base de données
│   │
│   ├── 📦 connecteo/          # CONFIGURATION DU PROJET
│   │   ├── __init__.py        # Package Python
│   │   ├── settings.py        # ⚙️ CONFIGURATION PRINCIPALE
│   │   ├── urls.py            # 🔗 URLs racine du projet
│   │   ├── wsgi.py            # Déploiement serveur
│   │   ├── asgi.py            # WebSockets (temps réel)
│   │   └── routing.py         # Routes WebSocket
│   │
│   ├── 📱 core/               # APPLICATION PRINCIPALE
│   │   ├── __init__.py
│   │   ├── models.py          # 🗄️ MODÈLES (base de données)
│   │   ├── views.py           # 👁️ VUES (logique métier)
│   │   ├── urls.py            # 🔗 URLs de l'application
│   │   ├── forms.py           # 📝 Formulaires
│   │   ├── serializers.py     # 📡 API REST
│   │   ├── consumers.py       # 💬 WebSocket (chat)
│   │   ├── signals.py         # 🔔 Événements automatiques
│   │   ├── admin.py           # 🔧 Interface d'administration
│   │   ├── apps.py            # Configuration de l'app
│   │   ├── tests.py           # 🧪 Tests unitaires
│   │   │
│   │   ├── 📂 templates/core/ # 🎨 TEMPLATES HTML
│   │   │   ├── home.html
│   │   │   ├── profile.html
│   │   │   ├── post_detail.html
│   │   │   ├── messages.html
│   │   │   └── ...
│   │   │
│   │   └── 📂 migrations/     # 📊 Historique base de données
│   │       ├── 0001_initial.py
│   │       ├── 0002_message_notification_post_comment.py
│   │       └── ...
│   │
│   ├── 🎨 static/core/        # FICHIERS STATIQUES (CSS, JS, images)
│   │   ├── css/
│   │   │   ├── styles.css
│   │   │   ├── profile_css.css
│   │   │   ├── post_detail.css
│   │   │   └── ...
│   │   └── images/
│   │
│   ├── 📦 staticfiles/        # Fichiers statiques collectés (production)
│   └── 📸 media/              # Fichiers uploadés (photos, vidéos)
│       ├── profiles/
│       └── posts/
│
└── 🐍 venv/                   # Environnement virtuel Python
```

---

## 🧩 Les composants principaux

### 1️⃣ **MODELS** (`models.py`) - La base de données

Les modèles définissent la structure de vos données.

```python
# Exemple : Modèle User Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True)
    followers = models.ManyToManyField(User, related_name='following')
    created_at = models.DateTimeField(auto_now_add=True)
```

**Ce que ça fait :**

- Crée une table `Profile` dans la base de données
- Chaque utilisateur a un profil
- Stocke : bio, image, followers, date de création

**Commandes importantes :**

```bash
# Créer les migrations (prépare les changements)
python manage.py makemigrations

# Appliquer les migrations (modifie la base de données)
python manage.py migrate
```

---

### 2️⃣ **VIEWS** (`views.py`) - La logique

Les vues traitent les requêtes et retournent des réponses.

```python
# Exemple : Vue pour afficher le profil
def profile(request, username):
    # 1. Récupérer l'utilisateur depuis la base de données
    user = User.objects.get(username=username)

    # 2. Récupérer les posts de l'utilisateur
    posts = Post.objects.filter(user=user).order_by('-created_at')

    # 3. Préparer les données à envoyer au template
    context = {
        'user': user,
        'posts': posts,
        'is_following': request.user in user.profile.followers.all()
    }

    # 4. Renvoyer le template avec les données
    return render(request, 'core/profile.html', context)
```

**Types de vues :**

- **Function-Based Views (FBV)** : Fonctions simples
- **Class-Based Views (CBV)** : Classes réutilisables

---

### 3️⃣ **URLS** (`urls.py`) - Les routes

Les URLs lient les adresses web aux vues.

```python
# connecteo/urls.py (racine du projet)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),  # Inclut les URLs de core
    path('', include('core.urls')),
]

# core/urls.py (application)
urlpatterns = [
    path('home/', views.home, name='home'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('messages/', views.messages, name='messages'),
]
```

**Explication :**

- `http://localhost:8000/home/` → appelle `views.home`
- `http://localhost:8000/profile/john/` → appelle `views.profile` avec `username='john'`
- `name='home'` permet d'utiliser `{% url 'home' %}` dans les templates

---

### 4️⃣ **TEMPLATES** (`.html`) - L'interface

Les templates affichent les données aux utilisateurs.

```django
<!-- core/templates/core/profile.html -->
{% load static %}
<!DOCTYPE html>
<html>
<head>
    <title>Profil - {{ user.username }}</title>
    <link rel="stylesheet" href="{% static 'core/css/profile_css.css' %}">
</head>
<body>
    <!-- En-tête du profil -->
    <div class="profile-header">
        <img src="{{ user.profile.profile_image.url }}" alt="Avatar">
        <h1>{{ user.username }}</h1>
        <p>{{ user.profile.bio }}</p>
    </div>

    <!-- Liste des posts -->
    <div class="posts">
        {% for post in posts %}
            <div class="post-card">
                <img src="{{ post.image.url }}" alt="Post">
                <p>{{ post.content }}</p>
            </div>
        {% empty %}
            <p>Aucun post</p>
        {% endfor %}
    </div>
</body>
</html>
```

**Syntaxe Django Template :**

- `{{ variable }}` : Affiche une variable
- `{% tag %}` : Balise logique (if, for, url, etc.)
- `{% load static %}` : Charge les fichiers statiques
- `{% static 'path' %}` : URL vers un fichier statique

---

### 5️⃣ **FORMS** (`forms.py`) - Les formulaires

Les formulaires gèrent les données entrées par l'utilisateur.

```python
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Quoi de neuf ?',
                'rows': 4
            })
        }
```

**Dans la vue :**

```python
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()

    return render(request, 'core/create_post.html', {'form': form})
```

---

### 6️⃣ **SETTINGS** (`settings.py`) - Configuration

Le cerveau du projet.

```python
# Configuration importante

# Applications installées
INSTALLED_APPS = [
    'django.contrib.admin',      # Interface admin
    'django.contrib.auth',       # Authentification
    'django.contrib.contenttypes',
    'django.contrib.sessions',   # Sessions utilisateur
    'django.contrib.messages',   # Messages flash
    'django.contrib.staticfiles',# Fichiers statiques
    'core',                      # Notre application
    'rest_framework',            # API REST
    'channels',                  # WebSockets
]

# Base de données
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Fichiers statiques (CSS, JS, images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Fichiers média (uploads utilisateurs)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,  # Cherche dans app/templates/
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
            ],
        },
    },
]
```

---

## ⚙️ Comment ça fonctionne ?

### Exemple complet : Créer un post

#### 1. **L'utilisateur visite la page**

```
http://localhost:8000/post/create/
```

#### 2. **Django cherche l'URL correspondante**

```python
# core/urls.py
path('post/create/', views.create_post, name='create_post'),
```

#### 3. **La vue traite la requête**

```python
# core/views.py
def create_post(request):
    if request.method == 'POST':  # Si formulaire soumis
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # Associe l'utilisateur
            post.save()  # Sauvegarde en base de données
            return redirect('home')  # Redirige vers l'accueil
    else:  # Si première visite
        form = PostForm()

    return render(request, 'core/create_post.html', {'form': form})
```

#### 4. **Le template affiche le formulaire**

```django
<!-- core/templates/core/create_post.html -->
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Publier</button>
</form>
```

#### 5. **Le modèle stocke les données**

```python
# core/models.py
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/')
    created_at = models.DateTimeField(auto_now_add=True)
```

---

## 🛠️ Guide pratique

### Démarrer le serveur

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Lancer le serveur de développement
python connecteo/manage.py runserver

# Accéder au site
# http://localhost:8000/
```

### Créer une nouvelle fonctionnalité

#### Étape 1 : Créer le modèle

```python
# core/models.py
class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='stories/')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
```

#### Étape 2 : Créer les migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

#### Étape 3 : Créer la vue

```python
# core/views.py
def create_story(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        expires_at = timezone.now() + timedelta(hours=24)
        Story.objects.create(
            user=request.user,
            image=image,
            expires_at=expires_at
        )
        return redirect('home')
    return render(request, 'core/create_story.html')
```

#### Étape 4 : Ajouter l'URL

```python
# core/urls.py
path('story/create/', views.create_story, name='create_story'),
```

#### Étape 5 : Créer le template

```django
<!-- core/templates/core/create_story.html -->
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    <input type="file" name="image" required>
    <button type="submit">Créer une story</button>
</form>
```

---

### Commandes Django essentielles

```bash
# 🚀 Démarrage
python manage.py runserver           # Lance le serveur
python manage.py runserver 8080      # Lance sur le port 8080

# 📊 Base de données
python manage.py makemigrations      # Prépare les migrations
python manage.py migrate             # Applique les migrations
python manage.py showmigrations      # Liste les migrations

# 👤 Utilisateurs
python manage.py createsuperuser     # Crée un admin
python manage.py changepassword user # Change le mot de passe

# 🗄️ Données
python manage.py dumpdata > backup.json     # Sauvegarde
python manage.py loaddata backup.json       # Restaure
python manage.py flush                      # Vide la base

# 🎨 Fichiers statiques
python manage.py collectstatic       # Collecte les fichiers statiques

# 🐚 Shell Python avec Django
python manage.py shell               # Console interactive

# 🧪 Tests
python manage.py test                # Lance les tests
```

---

## 🔍 Console interactive (shell)

Testez votre code directement :

```bash
python manage.py shell
```

```python
# Importer les modèles
from core.models import Profile, Post
from django.contrib.auth.models import User

# Créer un utilisateur
user = User.objects.create_user('john', 'john@example.com', 'password123')

# Créer un post
post = Post.objects.create(
    user=user,
    content='Mon premier post !',
    image='posts/image.jpg'
)

# Récupérer tous les posts
posts = Post.objects.all()

# Filtrer les posts
posts_john = Post.objects.filter(user__username='john')

# Compter les posts
count = Post.objects.count()

# Dernier post
last_post = Post.objects.latest('created_at')
```

---

## 📚 Concepts avancés dans Connecteo

### 1. **WebSockets** (Messages temps réel)

```python
# core/consumers.py
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        # Traite le message reçu
        await self.send(text_data=json.dumps({
            'message': text_data
        }))
```

### 2. **API REST** (pour applications mobiles)

```python
# core/serializers.py
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'image', 'created_at']

# core/views.py
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
```

### 3. **Signals** (Actions automatiques)

```python
# core/signals.py
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
```

---

## 🎯 Bonnes pratiques

### ✅ À FAIRE

- Toujours utiliser l'environnement virtuel (`venv`)
- Créer des migrations après chaque modification de modèle
- Utiliser `{% csrf_token %}` dans les formulaires POST
- Valider les données avec les formulaires Django
- Utiliser `{% url 'name' %}` au lieu de URLs en dur
- Nommer vos URLs dans `urls.py`
- Séparer la logique en petites fonctions

### ❌ À ÉVITER

- Ne jamais désactiver CSRF en production
- Ne pas stocker de mots de passe en clair
- Ne pas exposer `SECRET_KEY` dans le code
- Ne pas commiter `db.sqlite3` dans Git
- Ne pas faire de requêtes dans les templates
- Éviter les boucles N+1 (utiliser `select_related`)

---

## 🐛 Débogage

### Problème : Page 404

```
Vérifier :
1. L'URL est-elle dans urls.py ?
2. Le name correspond-il dans le template ?
3. Les paramètres sont-ils corrects ?
```

### Problème : Template non trouvé

```
Vérifier :
1. Le template est dans app/templates/app/ ?
2. L'app est dans INSTALLED_APPS ?
3. APP_DIRS = True dans TEMPLATES ?
```

### Problème : Image ne s'affiche pas

```
Vérifier :
1. MEDIA_URL et MEDIA_ROOT configurés ?
2. {% load static %} en haut du template ?
3. {{ image.url }} au lieu de {{ image }} ?
```

### Activer le mode DEBUG

```python
# settings.py
DEBUG = True  # Affiche les erreurs détaillées
```

---

## 📖 Ressources utiles

- **Documentation officielle** : https://docs.djangoproject.com/
- **Django Girls Tutorial** : https://tutorial.djangogirls.org/
- **Django for Beginners** : https://djangoforbeginners.com/
- **Stack Overflow** : https://stackoverflow.com/questions/tagged/django

---

## 🎓 Exercices pratiques

### Exercice 1 : Ajouter un système de likes

1. Créer un modèle `Like`
2. Ajouter une vue `like_post`
3. Créer un bouton dans le template
4. Afficher le nombre de likes

### Exercice 2 : Système de recherche

1. Créer une vue `search`
2. Filtrer les posts avec `Post.objects.filter(content__icontains=query)`
3. Afficher les résultats dans un template

### Exercice 3 : Pagination

1. Importer `Paginator`
2. Diviser les posts en pages
3. Ajouter des boutons précédent/suivant

---

## 🎉 Conclusion

Félicitations ! Vous connaissez maintenant :

- ✅ La structure d'un projet Django
- ✅ Le rôle de chaque fichier
- ✅ Comment créer des modèles, vues, templates et URLs
- ✅ Les commandes Django essentielles
- ✅ Comment déboguer votre application

**Prochaines étapes :**

1. Expérimentez avec le code
2. Créez vos propres fonctionnalités
3. Lisez la documentation Django
4. Rejoignez la communauté Django

**Bon développement ! 🚀**
