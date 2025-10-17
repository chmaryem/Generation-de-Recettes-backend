import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import RecipeRequest, RecipeResponse
from services.llm_service import generate_recipes_with_mistral
import traceback

app = FastAPI(title="Générateur de Recettes IA (Mistral via OpenRouter)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # remplacer par ton front Angular
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate", response_model=RecipeResponse)
async def generate_recipes(request: RecipeRequest):
    constraints_list = [k for k, v in request.constraints.items() if v]
    prompt = f"""
Tu es un chef cuisinier expert. L'utilisateur fournit :
- Ingrédients : {', '.join(request.ingredients)}
- Contraintes : {', '.join(constraints_list) or 'Aucune'}
- Temps max : {request.maxTime} minutes
- Matériel : {request.equipment or 'non spécifié'}
- Objectif nutritionnel : {request.nutritionalGoal or 'non spécifié'}

Génère 3 recettes au format JSON :
{{
  "simple": {{
    "title": "...",
    "time": ...,
    "difficulty": "...",
    "ingredients": ["..."],
    "steps": ["..."],
    "justification": "..."
  }},
  "creative": {{ ... }},
  "express": {{ ... }}
}}

⚠️ Respecte toutes les contraintes et propose des substitutions si nécessaire.
⚠️ La recette express doit ≤ 5 min.
    """

    try:
        data = await generate_recipes_with_mistral(prompt)
        return data
    except Exception as e:
        print("ERREUR :", e)
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
