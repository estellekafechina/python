# Django - Notes Importantes

## 1. Structure de Projet Django

- `manage.py` : Script pour gérer le projet (runserver, migrations, etc.)
- `settings.py` : Configuration du projet (BD, apps, middleware, etc.)
- `urls.py` : Routage des URLs
- `wsgi.py` / `asgi.py` : Points d'entrée pour le déploiement

## 2. Applications Django

- Créer une app : `python manage.py startapp nom_app`
- Enregistrer dans `INSTALLED_APPS` (settings.py)
- Structure : models.py, views.py, urls.py, templates/, static/

## 3. Gestion des Fichiers Statiques

- `STATIC_URL` : URL pour accéder aux fichiers statiques
- `STATIC_ROOT` : Dossier de collecte en production
- `STATICFILES_DIRS` : Dossiers additionnels de fichiers statiques
- Commande : `python manage.py collectstatic`

## 4. Gestion des Fichiers Médias (uploads)

- `MEDIA_URL` : URL pour accéder aux fichiers uploadés
- `MEDIA_ROOT` : Chemin où stocker les fichiers uploadés
- Dans models.py : `FileField` ou `ImageField`
- Configurer urls.py en développement :
    ```python
    from django.conf import settings
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    ```

## 5. Base de Données

- ORM Django : manipulation de BD via Python
- Créer migrations : `python manage.py makemigrations`
- Appliquer migrations : `python manage.py migrate`
- Shell interactif : `python manage.py shell`

## 6. Commandes Essentielles

- `python manage.py runserver` : Lancer serveur développement
- `python manage.py createsuperuser` : Créer admin
- `python manage.py test` : Lancer les tests
