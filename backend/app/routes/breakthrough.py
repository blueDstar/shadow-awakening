from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.core.deps import get_current_user
from app.models import User
from app.services.breakthrough_service import (
    get_breakthrough_status,
    start_breakthrough,
    select_ritual_option,
    complete_breakthrough,
)

router = APIRouter(prefix="/api/breakthrough", tags=["breakthrough"])


@router.get("/status")
async def get_status(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await get_breakthrough_status(db, user.id)


@router.post("/start")
async def start(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        return await start_breakthrough(db, user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/complete")
async def complete(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        return await complete_breakthrough(db, user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
@router.post("/select-option")
async def select_option(
    option_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        return await select_ritual_option(db, user.id, option_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
