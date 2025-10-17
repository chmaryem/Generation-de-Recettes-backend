import os
import httpx
import json
from dotenv import load_dotenv
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Charger les variables d'environnement
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

async def generate_recipes_with_mistral(prompt: str) -> dict:
    """
    Appelle l'API Mistral Small 3.2 via OpenRouter pour générer des recettes.
    """
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY non défini dans les variables d'environnement.")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",  # Optionnel, pour OpenRouter
        "X-Title": "Recipe Generator"  # Optionnel, pour OpenRouter
    }

    payload = {
        "model": "mistralai/mixtral-8x7b-instruct",  # À confirmer via OpenRouter
        "messages": [
            {"role": "system", "content": "Tu es un chef cuisinier expert."},
            {"role": "user", "content": prompt}
        ],
        "response_format": {"type": "json_object"},  # Forcer une sortie JSON
        "temperature": 0.7,
        "max_tokens": 1500,  # Suffisant pour des recettes détaillées
        "timeout": 60
    }

    async with httpx.AsyncClient(timeout=60) as client:
        try:
            response = await client.post(API_URL, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            logger.info("Réponse brute de l'API : %s", data)

            # Extraire le contenu JSON
            content = data["choices"][0]["message"]["content"]
            if isinstance(content, str):
                return json.loads(content)
            return content

        except httpx.HTTPStatusError as e:
            logger.error("Erreur HTTP : %s", e)
            raise HTTPException(status_code=e.response.status_code, detail=f"Erreur API OpenRouter : {e}")
        except json.JSONDecodeError as e:
            logger.error("Erreur de parsing JSON : %s", e)
            raise HTTPException(status_code=500, detail="La réponse de l'API n'est pas un JSON valide.")
        except Exception as e:
            logger.error("Erreur inattendue : %s", e)
            raise HTTPException(status_code=500, detail=f"Erreur serveur : {str(e)}")