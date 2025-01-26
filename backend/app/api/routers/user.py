# app/api/routers/user.py
from fastapi import APIRouter
import httpx
from core.config import settings

router = APIRouter()


@router.get("/user/{handle}")
async def get_user_info(handle: str):
    """
    Récupère des infos basiques + soumissions pour l'affichage du tableau de bord.
    """
    async with httpx.AsyncClient() as client:
        # Infos utilisateur
        user_url = f"{settings.CODEFORCES_API_BASE}/user.info"
        user_resp = await client.get(user_url, params={"handles": handle})

        # Soumissions utilisateur
        status_url = f"{settings.CODEFORCES_API_BASE}/user.status"
        status_resp = await client.get(status_url, params={"handle": handle, "from": 1, "count": 1000})

        user_data = user_resp.json()
        submissions_data = status_resp.json()

    if user_data["status"] != "OK" or submissions_data["status"] != "OK":
        return {"error": "Codeforces API error or invalid handle"}

    user_info = user_data["result"][0]
    submissions = submissions_data["result"]

    return {
        "user": user_info,
        "submissions": submissions
    }
