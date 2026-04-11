from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.db.database import init_db
from app.routes import (
    auth,
    breakthrough,
    challenges,
    dashboard,
    journal,
    profile,
    quests,
    rewards,
    settings as settings_routes,
    skills,
    stats,
    streaks,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    print("🌑 Shadow Awakening API is rising...")
    yield
    print("🌑 Shadow Awakening API is shutting down...")


app = FastAPI(
    title="Shadow Awakening API",
    description="Hệ Thống Thức Tỉnh — Gamified Self-Development Platform",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(quests.router)
app.include_router(stats.router)
app.include_router(streaks.router)
app.include_router(breakthrough.router)
app.include_router(journal.router)
app.include_router(settings_routes.router)
app.include_router(skills.router)
app.include_router(challenges.router)
app.include_router(rewards.router)
app.include_router(profile.router)

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
async def root():
    return {
        "app": "Shadow Awakening",
        "version": "1.0.0",
        "status": "online",
        "message": "Bóng Tối Thức Tỉnh — Hệ Thống Đang Hoạt Động",
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
