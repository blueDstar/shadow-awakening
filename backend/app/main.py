from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.db.database import init_db
from app.routes import auth, quests, dashboard, stats, streaks, breakthrough, journal, settings as settings_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    print("🌑 Shadow Awakening API is rising...")
    yield
    # Shutdown
    print("🌑 Shadow Awakening API is shutting down...")


app = FastAPI(
    title="Shadow Awakening API",
    description="Hệ Thống Thức Tỉnh — Gamified Self-Development Platform",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(quests.router)
app.include_router(stats.router)
app.include_router(streaks.router)
app.include_router(breakthrough.router)
app.include_router(journal.router)
app.include_router(settings_routes.router)


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
