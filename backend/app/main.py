# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routers import problems, user, objectives

app = FastAPI(title="CompetitiveProgrammingApp")

# Config CORS si besoin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montage des routes
app.include_router(problems.router, prefix="/api", tags=["problems"])
app.include_router(user.router, prefix="/api", tags=["user"])
app.include_router(objectives.router, prefix="/api", tags=["objectives"])

# Health check basique
@app.get("/")
def read_root():
    return {"message": "FastAPI is up and running!"}
