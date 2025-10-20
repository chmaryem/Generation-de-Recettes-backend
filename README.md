#  Générateur de Recettes IA — FastAPI + Mistral (OpenRouter)

##  Introduction

Ce projet est une **API FastAPI** qui génère automatiquement des **recettes de cuisine personnalisées** à partir des ingrédients, contraintes et objectifs nutritionnels de l’utilisateur.

L’API communique avec **Mistral (via OpenRouter)** pour produire trois recettes :
- **Simple** – équilibrée et facile à préparer  
-  **Créative** – originale et inspirante  
-  **Express** – réalisable en ≤ 5 minutes  

---

##  Architecture du projet

fastapi-recipes/
│
├── main.py # Point d'entrée FastAPI
├── models.py # Modèles Pydantic (entrée/sortie)
├── services/
│ └── llm_service.py # Service d'appel à l'API Mistral
├── .env # Clé API OpenRouter
├── requirements.txt # Dépendances Python
└── README.md # Documentation du projet

---

##  Technologies utilisées

| Technologie | Usage |
|--------------|--------|
| **FastAPI** | Framework backend Python rapide et asynchrone |
| **Pydantic** | Validation et typage des modèles |
| **HTTPX** | Client HTTP asynchrone pour interagir avec OpenRouter |
| **OpenRouter + Mistral** | Génération de contenu IA |
| **Uvicorn** | Serveur ASGI |
| **dotenv** | Gestion des variables d’environnement |

---

##  Configuration

###  Fichier `.env`
Crée un fichier `.env` à la racine avec ta clé OpenRouter


###  Installation
pip install -r requirements.txt

### Lancement du serveur
uvicorn main:app --reload

### Endpoint principal
POST /generate

Génère trois recettes basées sur les ingrédients et contraintes fournis par l’utilisateur.

###  Exemple de requête (RecipeRequest)
{
  "ingredients": ["poulet", "riz", "tomate"],
  "constraints": {
    "sans_lactose": true,
    "halal": true,
    "vegan": false
  },
  "maxTime": 30,
  "equipment": "poêle, casserole",
  "nutritionalGoal": "riche en protéines"
}

###  Exemple de réponse (RecipeResponse)
{
  "simple": {
    "title": "Poulet sauté au riz et tomate",
    "time": 25,
    "difficulty": "facile",
    "ingredients": ["poulet", "riz", "tomate", "huile d’olive", "épices"],
    "steps": [
      "Cuire le riz.",
      "Faire revenir le poulet dans l’huile.",
      "Ajouter les tomates et mélanger."
    ],
    "justification": "Respecte les contraintes halal et sans lactose.",
    "macros": {
      "calories": 420,
      "protein": 38,
      "carbs": 45,
      "fat": 10
    }
  },
  "creative": { ... },
  "express": { ... }
}
