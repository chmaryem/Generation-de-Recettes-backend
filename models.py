from pydantic import BaseModel
from typing import List, Dict, Optional, Union

class Macros(BaseModel):
    calories: float
    protein: float
    carbs: float
    fat: float
class Recipe(BaseModel):
    title: str
    time: Union[int, str]  # <-- accepte int ou "20 minutes"
    difficulty: str
    ingredients: List[str]
    steps: List[str]
    justification: str
    macros: Macros  


class RecipeRequest(BaseModel):
    ingredients: List[str]
    constraints: Dict[str, bool]
    maxTime: int
    equipment: str
    nutritionalGoal: str

class RecipeResponse(BaseModel):
    simple: Recipe
    creative: Recipe
    express: Recipe
    warning: Optional[str] = None  # <-- facultatif


