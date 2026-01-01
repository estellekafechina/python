
"""
STRUCTURE DE BASE DE DJANGO

Django suit le pattern MVT (Model-View-Template):

1. MODELS (models.py) - Définissent la structure de la base de données
    - Classes Python qui héritent de django.db.models.Model
    - Chaque attribut = un champ de la BD

2. VIEWS (views.py) - Logique métier de l'application
    - Fonctions ou classes qui traitent les requêtes HTTP
    - Retournent des réponses (render, redirect, JsonResponse)

3. TEMPLATES (.html) - Interface utilisateur
    - Fichiers HTML avec la syntaxe Django Template Language
    - Affichent les données passées par les views

4. URLS (urls.py) - Routage des requêtes
    - Mappent les URLs vers les views appropriées

5. SETTINGS (settings.py) - Configuration du projet
    - Base de données, apps installées, middleware, etc.

6. ADMIN (admin.py) - Interface d'administration automatique
    - Enregistrement des models pour gestion via l'admin

FLUX DE DONNÉES:
URL → View → Model (si nécessaire) → Template → Response

COMMANDES ESSENTIELLES:
- python manage.py runserver : Démarrer le serveur
- python manage.py makemigrations : Créer les migrations
- python manage.py migrate : Appliquer les migrations
- python manage.py createsuperuser : Créer un admin
- python manage.py startapp nom_app : Créer une nouvelle app
"""

