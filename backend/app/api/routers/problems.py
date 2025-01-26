# app/api/routers/problems.py
from fastapi import APIRouter, Query
import httpx
from app.core.config import settings

router = APIRouter()


@router.get("/problems")
async def get_problems(
        tags: str = Query(None),
        min_difficulty: int = Query(None),
        max_difficulty: int = Query(None)
):
    """
    Récupère les problèmes Codeforces avec des filtres simples
    (tags, min_difficulty, max_difficulty).
    """
    url = f"{settings.CODEFORCES_API_BASE}/problemset.problems"
    params = {}

    if tags:
        params["tags"] = tags
    # Note: Codeforces n'a pas d'endpoint direct pour min/max difficulty,
    # on filtre après la récupération de toutes les données ou on agit différemment.

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
        data = resp.json()

    if data["status"] != "OK":
        return {"error": "Codeforces API error"}

    # Filtre local sur la difficulté
    problems = data["result"]["problems"]
    if min_difficulty:
        problems = [p for p in problems if "rating" in p and p["rating"] >= min_difficulty]
    if max_difficulty:
        problems = [p for p in problems if "rating" in p and p["rating"] <= max_difficulty]

    return problems
