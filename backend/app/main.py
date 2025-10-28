from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from .shared_kernel import config, init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Démarrage de l'application Sustaain...")
    print(f"📊 Database URL: {config.database_url}")
    print(f"🐛 Debug mode: {config.debug}")
    
    try:
        init_db()
        print("✅ Base de données initialisée")
    except Exception as e:
        print(f"⚠️  Erreur lors de l'initialisation de la DB: {e}")
    
    yield
    
    print("👋 Arrêt de l'application Sustaain...")


app = FastAPI(
    title="Sustaain Assessment API",
    version="1.0.0",
    description="API pour le calcul de l'empreinte carbone et la traçabilité du cacao",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "Bienvenue sur l'API Sustaain Assessment",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": config.database_url.split("@")[-1] if "@" in config.database_url else "configured"
    }

