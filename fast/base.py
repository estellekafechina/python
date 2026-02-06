"""
===========================================
    FASTAPI - LES BASES COMPLÈTES
===========================================

Installation:
    pip install fastapi uvicorn[standard]

Lancer le serveur:
    uvicorn base:app --reload

Documentation auto générée:
    - Swagger UI: http://127.0.0.1:8000/docs
    - ReDoc: http://127.0.0.1:8000/redoc
"""

from fastapi import FastAPI, HTTPException, Query, Path, Body, Depends, Header, status
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

# ===========================================
# 1. CRÉATION DE L'APPLICATION
# ===========================================

app = FastAPI(
    title="Mon API FastAPI",
    description="API de démonstration pour apprendre FastAPI",
    version="1.0.0"
)

# ===========================================
# 2. MIDDLEWARE CORS (pour les requêtes frontend)
# ===========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production: ["https://monsite.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===========================================
# 3. MODÈLES PYDANTIC (validation des données)
# ===========================================

class UserBase(BaseModel):
    """Modèle de base pour un utilisateur"""
    username: str = Field(..., min_length=3, max_length=50, description="Nom d'utilisateur")
    email: EmailStr = Field(..., description="Email valide")
    age: Optional[int] = Field(None, ge=0, le=150, description="Âge optionnel")

class UserCreate(UserBase):
    """Modèle pour créer un utilisateur (avec mot de passe)"""
    password: str = Field(..., min_length=8)

class UserResponse(UserBase):
    """Modèle de réponse (sans le mot de passe)"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Permet la conversion depuis ORM

class Item(BaseModel):
    """Modèle pour un article"""
    name: str
    price: float = Field(..., gt=0, description="Prix doit être positif")
    quantity: int = Field(default=1, ge=0)
    description: Optional[str] = None

# ===========================================
# 4. ENUMS (pour des choix limités)
# ===========================================

class Category(str, Enum):
    electronics = "electronics"
    clothing = "clothing"
    food = "food"

# ===========================================
# 5. BASE DE DONNÉES SIMULÉE
# ===========================================

fake_db = {
    "users": [
        {"id": 1, "username": "alice", "email": "alice@example.com", "age": 25},
        {"id": 2, "username": "bob", "email": "bob@example.com", "age": 30},
    ],
    "items": []
}

# ===========================================
# 6. ROUTES GET - Lecture de données
# ===========================================

@app.get("/", tags=["Accueil"])
def root():
    """Route racine - Page d'accueil"""
    return {"message": "Bienvenue sur FastAPI!", "docs": "/docs"}

@app.get("/users", tags=["Users"], response_model=List[dict])
def get_users(
    skip: int = Query(0, ge=0, description="Nombre d'éléments à sauter"),
    limit: int = Query(10, ge=1, le=100, description="Limite de résultats")
):
    """Récupérer la liste des utilisateurs avec pagination"""
    return fake_db["users"][skip:skip + limit]

@app.get("/users/{user_id}", tags=["Users"])
def get_user(
    user_id: int = Path(..., gt=0, description="ID de l'utilisateur")
):
    """Récupérer un utilisateur par son ID"""
    for user in fake_db["users"]:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

@app.get("/search", tags=["Recherche"])
def search_items(
    q: str = Query(..., min_length=2, description="Terme de recherche"),
    category: Optional[Category] = Query(None, description="Catégorie")
):
    """Rechercher des articles (paramètre q obligatoire)"""
    return {"query": q, "category": category}

# ===========================================
# 7. ROUTES POST - Création de données
# ===========================================

@app.post("/users", tags=["Users"], status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    """Créer un nouvel utilisateur"""
    new_id = len(fake_db["users"]) + 1
    new_user = {
        "id": new_id,
        "username": user.username,
        "email": user.email,
        "age": user.age
    }
    fake_db["users"].append(new_user)
    return {"message": "Utilisateur créé", "user": new_user}

@app.post("/items", tags=["Items"])
def create_item(item: Item):
    """Créer un nouvel article"""
    fake_db["items"].append(item.model_dump())
    return {"message": "Article créé", "item": item}

# ===========================================
# 8. ROUTES PUT - Mise à jour complète
# ===========================================

@app.put("/users/{user_id}", tags=["Users"])
def update_user(user_id: int, user: UserBase):
    """Mettre à jour un utilisateur (remplacement complet)"""
    for i, existing_user in enumerate(fake_db["users"]):
        if existing_user["id"] == user_id:
            fake_db["users"][i] = {"id": user_id, **user.model_dump()}
            return fake_db["users"][i]
    raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

# ===========================================
# 9. ROUTES PATCH - Mise à jour partielle
# ===========================================

@app.patch("/users/{user_id}", tags=["Users"])
def partial_update_user(
    user_id: int,
    username: Optional[str] = Body(None),
    email: Optional[EmailStr] = Body(None),
    age: Optional[int] = Body(None)
):
    """Mettre à jour partiellement un utilisateur"""
    for user in fake_db["users"]:
        if user["id"] == user_id:
            if username:
                user["username"] = username
            if email:
                user["email"] = email
            if age is not None:
                user["age"] = age
            return user
    raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

# ===========================================
# 10. ROUTES DELETE - Suppression
# ===========================================

@app.delete("/users/{user_id}", tags=["Users"], status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    """Supprimer un utilisateur"""
    for i, user in enumerate(fake_db["users"]):
        if user["id"] == user_id:
            fake_db["users"].pop(i)
            return
    raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

# ===========================================
# 11. DÉPENDANCES (Dependency Injection)
# ===========================================

def get_current_user(authorization: str = Header(None)):
    """Dépendance pour vérifier l'authentification"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Non authentifié")
    # En réalité, on vérifierait le token JWT ici
    return {"username": "user_from_token", "role": "admin"}

@app.get("/protected", tags=["Auth"])
def protected_route(current_user: dict = Depends(get_current_user)):
    """Route protégée nécessitant une authentification"""
    return {"message": f"Bienvenue {current_user['username']}!"}

# ===========================================
# 12. GESTION DES ERREURS PERSONNALISÉES
# ===========================================

class CustomException(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(CustomException)
def custom_exception_handler(request, exc: CustomException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Erreur personnalisée: {exc.name}"}
    )

@app.get("/error", tags=["Erreurs"])
def trigger_error():
    """Déclencher une erreur personnalisée"""
    raise CustomException(name="Test d'erreur")

# ===========================================
# 13. RÉPONSES HTML
# ===========================================

@app.get("/html", response_class=HTMLResponse, tags=["HTML"])
def get_html():
    """Retourner une page HTML"""
    return """
    <!DOCTYPE html>
    <html>
        <head><title>FastAPI HTML</title></head>
        <body>
            <h1>Hello depuis FastAPI!</h1>
            <p>Ceci est une réponse HTML</p>
        </body>
    </html>
    """

# ===========================================
# 14. ÉVÉNEMENTS DE CYCLE DE VIE
# ===========================================

@app.on_event("startup")
async def startup_event():
    """Exécuté au démarrage de l'application"""
    print("🚀 Application FastAPI démarrée!")

@app.on_event("shutdown")
async def shutdown_event():
    """Exécuté à l'arrêt de l'application"""
    print("👋 Application FastAPI arrêtée!")

# ===========================================
# 15. EXÉCUTION DIRECTE
# ===========================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("base:app", host="0.0.0.0", port=8000, reload=True)


"""
===========================================
    RÉSUMÉ DES CONCEPTS CLÉS
===========================================

1. DÉCORATEURS DE ROUTES:
   @app.get()    - Lire des données
   @app.post()   - Créer des données
   @app.put()    - Remplacer des données
   @app.patch()  - Modifier partiellement
   @app.delete() - Supprimer des données

2. PARAMÈTRES:
   - Path: /users/{user_id}  → valeur dans l'URL
   - Query: /search?q=test   → après le ?
   - Body: données JSON envoyées

3. VALIDATION PYDANTIC:
   - Field(...) = obligatoire
   - Field(None) = optionnel
   - gt, ge, lt, le = comparaisons numériques
   - min_length, max_length = longueur strings

4. CODES HTTP:
   - 200: OK
   - 201: Créé
   - 204: Pas de contenu
   - 400: Mauvaise requête
   - 401: Non authentifié
   - 403: Interdit
   - 404: Non trouvé
   - 500: Erreur serveur

5. TESTER AVEC CURL:
   curl http://localhost:8000/users
   curl -X POST http://localhost:8000/users -H "Content-Type: application/json" -d '{"username":"test","email":"test@test.com","password":"12345678"}'
"""
