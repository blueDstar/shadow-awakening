from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.core.deps import get_current_user
from app.models import User
from app.services.stat_service import get_all_stats

router = APIRouter(prefix="/api/stats", tags=["stats"])


@router.get("")
async def get_stats(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all user stats."""
    return await get_all_stats(db, user.id)
