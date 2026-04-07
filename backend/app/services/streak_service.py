"""Streak Service - handles streak tracking and updates."""
from datetime import date, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.models import Streak, StreakLog


async def update_streak(db: AsyncSession, user_id, streak_type: str, active_date: date = None):
    """Update a streak for the given type."""
    if active_date is None:
        active_date = date.today()
    
    result = await db.execute(
        select(Streak).where(
            and_(Streak.user_id == user_id, Streak.streak_type == streak_type)
        )
    )
    streak = result.scalar_one_or_none()
    
    if not streak:
        return
    
    yesterday = active_date - timedelta(days=1)
    
    if streak.last_active_date == active_date:
        # Already counted today
        return
    
    if streak.last_active_date == yesterday:
        # Continue streak
        streak.current_streak += 1
    elif streak.last_active_date is None or streak.last_active_date < yesterday:
        # Streak broken, start new one
        streak.current_streak = 1
        streak.started_at = active_date
    
    streak.last_active_date = active_date
    
    if streak.current_streak > streak.best_streak:
        streak.best_streak = streak.current_streak
    
    # Log the streak
    log = StreakLog(
        user_id=user_id,
        streak_type=streak_type,
        log_date=active_date,
        streak_value=streak.current_streak,
    )
    db.add(log)
    await db.flush()


async def check_and_break_streak(db: AsyncSession, user_id, streak_type: str):
    """Break a streak if no activity yesterday."""
    result = await db.execute(
        select(Streak).where(
            and_(Streak.user_id == user_id, Streak.streak_type == streak_type)
        )
    )
    streak = result.scalar_one_or_none()
    
    if streak and streak.last_active_date:
        yesterday = date.today() - timedelta(days=1)
        if streak.last_active_date < yesterday:
            streak.current_streak = 0
            await db.flush()


async def get_all_streaks(db: AsyncSession, user_id) -> list:
    """Get all streaks for a user."""
    result = await db.execute(select(Streak).where(Streak.user_id == user_id))
    streaks = result.scalars().all()
    return [
        {
            "streak_type": s.streak_type,
            "current_streak": s.current_streak,
            "best_streak": s.best_streak,
            "last_active_date": str(s.last_active_date) if s.last_active_date else None,
        }
        for s in streaks
    ]
