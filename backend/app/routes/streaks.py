from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.core.deps import get_current_user
from app.models import User
from app.services.streak_service import get_all_streaks

router = APIRouter(prefix="/api/streaks", tags=["streaks"])


@router.get("")
async def get_streaks(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all streaks."""
    streaks = await get_all_streaks(db, user.id)
    return {"streaks": streaks}
