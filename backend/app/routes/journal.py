from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.database import get_db
from app.core.deps import get_current_user
from app.models import User, Reflection
from app.schemas.journal import ReflectionCreate

router = APIRouter(prefix="/api/journal", tags=["journal"])


@router.get("")
async def get_journal(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    limit: int = 30,
):
    result = await db.execute(
        select(Reflection)
        .where(Reflection.user_id == user.id)
        .order_by(Reflection.reflection_date.desc())
        .limit(limit)
    )
    entries = result.scalars().all()
    return [
        {
            "id": str(e.id),
            "reflection_date": str(e.reflection_date),
            "content": e.content,
            "mood": e.mood,
            "insights": e.insights,
            "success_reasons": e.success_reasons,
            "fail_reasons": e.fail_reasons,
            "created_at": e.created_at.isoformat(),
        }
        for e in entries
    ]


@router.post("")
async def create_journal(
    data: ReflectionCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    reflection = Reflection(
        user_id=user.id,
        reflection_date=date.today(),
        content=data.content,
        mood=data.mood,
        insights=data.insights,
        success_reasons=data.success_reasons,
        fail_reasons=data.fail_reasons,
    )
    db.add(reflection)
    await db.flush()
    return {"id": str(reflection.id), "status": "created"}


@router.get("/{target_date}")
async def get_journal_by_date(
    target_date: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        d = date.fromisoformat(target_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")
    
    result = await db.execute(
        select(Reflection).where(
            Reflection.user_id == user.id,
            Reflection.reflection_date == d,
        )
    )
    entry = result.scalar_one_or_none()
    if not entry:
        return None
    
    return {
        "id": str(entry.id),
        "reflection_date": str(entry.reflection_date),
        "content": entry.content,
        "mood": entry.mood,
        "insights": entry.insights,
        "success_reasons": entry.success_reasons,
        "fail_reasons": entry.fail_reasons,
    }
