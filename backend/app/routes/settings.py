from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.database import get_db
from app.core.deps import get_current_user
from app.models import User, UserSettings

router = APIRouter(prefix="/api/settings", tags=["settings"])


@router.get("")
async def get_settings(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(UserSettings).where(UserSettings.user_id == user.id))
    s = result.scalar_one_or_none()
    if not s:
        return {"language": "vi", "timezone": "Asia/Ho_Chi_Minh"}
    return {
        "language": s.language,
        "timezone": s.timezone,
        "difficulty_preference": s.difficulty_preference,
        "notification_enabled": s.notification_enabled,
        "daily_reset_hour": s.daily_reset_hour,
    }


@router.put("/language")
async def update_language(
    language: str = "vi",
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(UserSettings).where(UserSettings.user_id == user.id))
    s = result.scalar_one_or_none()
    if s:
        s.language = language
        await db.flush()
    return {"language": language}


@router.put("/timezone")
async def update_timezone(
    tz: str = "Asia/Ho_Chi_Minh",
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(UserSettings).where(UserSettings.user_id == user.id))
    s = result.scalar_one_or_none()
    if s:
        s.timezone = tz
        await db.flush()
    return {"timezone": tz}
