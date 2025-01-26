# app/api/routers/objectives.py
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

# Stockage temporaire en mémoire
OBJECTIVES_DB = []

class Objective(BaseModel):
    id: int
    description: str
    completed: bool = False

@router.get("/objectives")
async def list_objectives():
    return OBJECTIVES_DB

@router.post("/objectives")
async def create_objective(obj: Objective):
    OBJECTIVES_DB.append(obj.dict())
    return {"msg": "Objective created", "data": obj}

@router.delete("/objectives/{obj_id}")
async def delete_objective(obj_id: int):
    global OBJECTIVES_DB
    OBJECTIVES_DB = [o for o in OBJECTIVES_DB if o["id"] != obj_id]
    return {"msg": f"Objective {obj_id} deleted"}
