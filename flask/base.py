"""
===========================================
    FLASK - LES BASES COMPLÈTES
===========================================

Installation:
    pip install flask flask-cors

Lancer le serveur:
    python base.py
    ou
    flask --app base run --debug

Le serveur sera accessible sur:
    http://127.0.0.1:5000
"""

from flask import Flask, request, jsonify, render_template_string, redirect, url_for, abort, make_response, session, g
from flask_cors import CORS
from functools import wraps
from datetime import datetime
import json

# ===========================================
# 1. CRÉATION DE L'APPLICATION
# ===========================================

app = Flask(__name__)
app.secret_key = "ma_cle_secrete_a_changer_en_production"  # Nécessaire pour les sessions

# ===========================================
# 2. CONFIGURATION CORS
# ===========================================

CORS(app)  # Permet les requêtes cross-origin

# ===========================================
# 3. CONFIGURATION DE L'APPLICATION
# ===========================================

app.config.update(
    DEBUG=True,
    JSON_SORT_KEYS=False,  # Garde l'ordre des clés JSON
    MAX_CONTENT_LENGTH=16 * 1024 * 1024  # Limite upload à 16MB
)

# ===========================================
# 4. BASE DE DONNÉES SIMULÉE
# ===========================================

fake_db = {
    "users": [
        {"id": 1, "username": "alice", "email": "alice@example.com", "age": 25},
        {"id": 2, "username": "bob", "email": "bob@example.com", "age": 30},
    ],
    "items": []
}

# ===========================================
# 5. ROUTES GET - Lecture de données
# ===========================================

@app.route("/")
def home():
    """Route racine - Page d'accueil"""
    return jsonify({
        "message": "Bienvenue sur Flask!",
        "endpoints": {
            "users": "/users",
            "items": "/items",
            "html": "/html"
        }
    })

@app.route("/users", methods=["GET"])
def get_users():
    """Récupérer tous les utilisateurs avec pagination optionnelle"""
    # Récupérer les paramètres de query string
    skip = request.args.get("skip", 0, type=int)
    limit = request.args.get("limit", 10, type=int)

    users = fake_db["users"][skip:skip + limit]
    return jsonify({
        "total": len(fake_db["users"]),
        "skip": skip,
        "limit": limit,
        "users": users
    })

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """Récupérer un utilisateur par son ID"""
    for user in fake_db["users"]:
        if user["id"] == user_id:
            return jsonify(user)

    # Utilisateur non trouvé
    return jsonify({"error": "Utilisateur non trouvé"}), 404

@app.route("/search")
def search():
    """Recherche avec paramètres obligatoires et optionnels"""
    # Paramètre obligatoire
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Le paramètre 'q' est obligatoire"}), 400

    # Paramètre optionnel
    category = request.args.get("category")

    return jsonify({
        "query": query,
        "category": category,
        "results": []  # Résultats de recherche ici
    })

# ===========================================
# 6. ROUTES POST - Création de données
# ===========================================

@app.route("/users", methods=["POST"])
def create_user():
    """Créer un nouvel utilisateur"""
    # Vérifier que c'est du JSON
    if not request.is_json:
        return jsonify({"error": "Content-Type doit être application/json"}), 415

    data = request.get_json()

    # Validation manuelle (Flask n'a pas de validation intégrée comme FastAPI)
    required_fields = ["username", "email"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Le champ '{field}' est obligatoire"}), 400

    # Créer l'utilisateur
    new_id = len(fake_db["users"]) + 1
    new_user = {
        "id": new_id,
        "username": data["username"],
        "email": data["email"],
        "age": data.get("age")  # Optionnel
    }
    fake_db["users"].append(new_user)

    return jsonify({
        "message": "Utilisateur créé",
        "user": new_user
    }), 201  # 201 = Created

@app.route("/items", methods=["POST"])
def create_item():
    """Créer un nouvel article"""
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({"error": "Le champ 'name' est obligatoire"}), 400

    item = {
        "id": len(fake_db["items"]) + 1,
        "name": data["name"],
        "price": data.get("price", 0),
        "quantity": data.get("quantity", 1),
        "created_at": datetime.now().isoformat()
    }
    fake_db["items"].append(item)

    return jsonify({"message": "Article créé", "item": item}), 201

# ===========================================
# 7. ROUTES PUT - Mise à jour complète
# ===========================================

@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    """Remplacer complètement un utilisateur"""
    data = request.get_json()

    for i, user in enumerate(fake_db["users"]):
        if user["id"] == user_id:
            # Remplacement complet
            fake_db["users"][i] = {
                "id": user_id,
                "username": data.get("username", ""),
                "email": data.get("email", ""),
                "age": data.get("age")
            }
            return jsonify(fake_db["users"][i])

    return jsonify({"error": "Utilisateur non trouvé"}), 404

# ===========================================
# 8. ROUTES PATCH - Mise à jour partielle
# ===========================================

@app.route("/users/<int:user_id>", methods=["PATCH"])
def partial_update_user(user_id):
    """Mettre à jour partiellement un utilisateur"""
    data = request.get_json()

    for user in fake_db["users"]:
        if user["id"] == user_id:
            # Mise à jour uniquement des champs fournis
            if "username" in data:
                user["username"] = data["username"]
            if "email" in data:
                user["email"] = data["email"]
            if "age" in data:
                user["age"] = data["age"]
            return jsonify(user)

    return jsonify({"error": "Utilisateur non trouvé"}), 404

# ===========================================
# 9. ROUTES DELETE - Suppression
# ===========================================

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Supprimer un utilisateur"""
    for i, user in enumerate(fake_db["users"]):
        if user["id"] == user_id:
            deleted = fake_db["users"].pop(i)
            return jsonify({"message": "Utilisateur supprimé", "user": deleted})

    return jsonify({"error": "Utilisateur non trouvé"}), 404

# ===========================================
# 10. DÉCORATEURS PERSONNALISÉS (Auth)
# ===========================================

def require_auth(f):
    """Décorateur pour protéger les routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"error": "Non authentifié"}), 401
        # En réalité, on vérifierait le token ici
        g.current_user = {"username": "user_from_token", "role": "admin"}
        return f(*args, **kwargs)
    return decorated_function

@app.route("/protected")
@require_auth
def protected_route():
    """Route protégée nécessitant une authentification"""
    return jsonify({
        "message": f"Bienvenue {g.current_user['username']}!",
        "role": g.current_user["role"]
    })

# ===========================================
# 11. GESTION DES SESSIONS
# ===========================================

@app.route("/login", methods=["POST"])
def login():
    """Connexion et création de session"""
    data = request.get_json()
    username = data.get("username")

    if username:
        session["username"] = username
        session["logged_in"] = True
        return jsonify({"message": f"Bienvenue {username}!"})

    return jsonify({"error": "Username requis"}), 400

@app.route("/logout", methods=["POST"])
def logout():
    """Déconnexion et suppression de session"""
    session.clear()
    return jsonify({"message": "Déconnecté"})

@app.route("/profile")
def profile():
    """Afficher le profil de l'utilisateur connecté"""
    if not session.get("logged_in"):
        return jsonify({"error": "Non connecté"}), 401
    return jsonify({"username": session.get("username")})

# ===========================================
# 12. RÉPONSES HTML
# ===========================================

@app.route("/html")
def get_html():
    """Retourner une page HTML"""
    html = """
    <!DOCTYPE html>
    <html>
        <head><title>Flask HTML</title></head>
        <body>
            <h1>Hello depuis Flask!</h1>
            <p>Ceci est une réponse HTML</p>
            <ul>
                <li><a href="/users">Voir les utilisateurs (JSON)</a></li>
                <li><a href="/html/form">Formulaire</a></li>
            </ul>
        </body>
    </html>
    """
    return render_template_string(html)

@app.route("/html/form", methods=["GET", "POST"])
def form_example():
    """Exemple de formulaire HTML"""
    if request.method == "POST":
        name = request.form.get("name")
        return f"<h1>Bonjour {name}!</h1><a href='/html/form'>Retour</a>"

    return render_template_string("""
        <h1>Formulaire de test</h1>
        <form method="POST">
            <input type="text" name="name" placeholder="Votre nom">
            <button type="submit">Envoyer</button>
        </form>
    """)

# ===========================================
# 13. GESTION DES ERREURS
# ===========================================

@app.errorhandler(404)
def not_found(error):
    """Gestionnaire d'erreur 404"""
    return jsonify({"error": "Page non trouvée", "code": 404}), 404

@app.errorhandler(500)
def internal_error(error):
    """Gestionnaire d'erreur 500"""
    return jsonify({"error": "Erreur interne du serveur", "code": 500}), 500

@app.errorhandler(400)
def bad_request(error):
    """Gestionnaire d'erreur 400"""
    return jsonify({"error": "Requête invalide", "code": 400}), 400

# Route pour tester les erreurs
@app.route("/error/<int:code>")
def trigger_error(code):
    """Déclencher une erreur HTTP spécifique"""
    abort(code)

# ===========================================
# 14. COOKIES
# ===========================================

@app.route("/cookie/set")
def set_cookie():
    """Définir un cookie"""
    response = make_response(jsonify({"message": "Cookie créé"}))
    response.set_cookie(
        "mon_cookie",
        "valeur_du_cookie",
        max_age=3600,  # 1 heure
        httponly=True  # Non accessible en JavaScript
    )
    return response

@app.route("/cookie/get")
def get_cookie():
    """Lire un cookie"""
    cookie_value = request.cookies.get("mon_cookie", "Pas de cookie")
    return jsonify({"cookie": cookie_value})

# ===========================================
# 15. BEFORE/AFTER REQUEST (Middleware)
# ===========================================

@app.before_request
def before_request_func():
    """Exécuté avant chaque requête"""
    g.start_time = datetime.now()

@app.after_request
def after_request_func(response):
    """Exécuté après chaque requête"""
    if hasattr(g, 'start_time'):
        duration = datetime.now() - g.start_time
        response.headers["X-Request-Duration"] = str(duration.total_seconds())
    return response

# ===========================================
# 16. BLUEPRINTS (pour modulariser)
# ===========================================

from flask import Blueprint

# Créer un blueprint
api_v2 = Blueprint("api_v2", __name__, url_prefix="/api/v2")

@api_v2.route("/hello")
def api_v2_hello():
    """Route dans le blueprint API v2"""
    return jsonify({"message": "Hello depuis API v2!", "version": "2.0"})

# Enregistrer le blueprint
app.register_blueprint(api_v2)

# ===========================================
# 17. UPLOAD DE FICHIERS
# ===========================================

@app.route("/upload", methods=["POST"])
def upload_file():
    """Upload de fichier"""
    if "file" not in request.files:
        return jsonify({"error": "Pas de fichier"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Fichier vide"}), 400

    # En production: file.save(f"./uploads/{secure_filename(file.filename)}")
    return jsonify({
        "message": "Fichier reçu",
        "filename": file.filename,
        "content_type": file.content_type
    })

# ===========================================
# 18. REDIRECTIONS
# ===========================================

@app.route("/old-page")
def old_page():
    """Redirection vers une nouvelle page"""
    return redirect(url_for("home"))

@app.route("/redirect/<path:url>")
def redirect_to(url):
    """Rediriger vers une URL externe"""
    return redirect(f"https://{url}")

# ===========================================
# 19. EXÉCUTION DIRECTE
# ===========================================

if __name__ == "__main__":
    print("🚀 Démarrage du serveur Flask...")
    print("📖 Documentation: http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)


"""
===========================================
    RÉSUMÉ DES CONCEPTS CLÉS
===========================================

1. DÉCORATEURS DE ROUTES:
   @app.route("/path", methods=["GET"])     - Lire
   @app.route("/path", methods=["POST"])    - Créer
   @app.route("/path", methods=["PUT"])     - Remplacer
   @app.route("/path", methods=["PATCH"])   - Modifier
   @app.route("/path", methods=["DELETE"])  - Supprimer

2. RÉCUPÉRER DES DONNÉES:
   request.args.get("param")     - Query string (?param=value)
   request.get_json()            - Corps JSON
   request.form.get("field")     - Formulaire HTML
   request.files["file"]         - Fichier uploadé
   request.headers.get("Header") - En-tête HTTP
   request.cookies.get("cookie") - Cookie

3. TYPES DE RÉPONSES:
   return jsonify({...})                    - JSON
   return render_template_string(html)      - HTML
   return redirect(url_for("route_name"))   - Redirection
   return "texte", 200                      - Texte simple

4. CODES HTTP:
   return jsonify(...), 200   # OK
   return jsonify(...), 201   # Created
   return jsonify(...), 400   # Bad Request
   return jsonify(...), 401   # Unauthorized
   return jsonify(...), 404   # Not Found
   return jsonify(...), 500   # Server Error

5. VARIABLES D'URL:
   /users/<int:user_id>     - Entier
   /files/<path:filepath>   - Chemin avec /
   /page/<string:name>      - Chaîne de caractères

6. TESTER AVEC CURL:
   curl http://localhost:5000/users
   curl -X POST http://localhost:5000/users -H "Content-Type: application/json" -d '{"username":"test","email":"test@test.com"}'

7. DIFFÉRENCES AVEC FASTAPI:
   - Flask: plus simple, plus de code manuel
   - FastAPI: validation auto, docs auto, plus moderne
   - Flask: synchrone par défaut
   - FastAPI: asynchrone par défaut
"""
