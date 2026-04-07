"""Breakthrough Service - handles stat cap progression."""
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Character, StatCap, BreakthroughTrial


async def get_breakthrough_status(db: AsyncSession, user_id) -> dict:
    """Get current breakthrough status."""
    result = await db.execute(select(Character).where(Character.user_id == user_id))
    character = result.scalar_one_or_none()
    if not character:
        return {"available": False}
    
    cap_result = await db.execute(select(StatCap).where(StatCap.character_id == character.id))
    stat_cap = cap_result.scalar_one_or_none()
    
    if not stat_cap:
        return {"available": False}
    
    # Check for active trial
    trial_result = await db.execute(
        select(BreakthroughTrial).where(
            BreakthroughTrial.user_id == user_id,
            BreakthroughTrial.status == "in_progress",
        )
    )
    active_trial = trial_result.scalar_one_or_none()
    
    return {
        "available": stat_cap.breakthrough_available,
        "current_cap": stat_cap.current_cap,
        "next_cap": stat_cap.current_cap + 100,
        "phase": stat_cap.phase,
        "active_trial": {
            "id": str(active_trial.id),
            "from_cap": active_trial.from_cap,
            "to_cap": active_trial.to_cap,
        } if active_trial else None,
    }


async def start_breakthrough(db: AsyncSession, user_id) -> dict:
    """Start a breakthrough trial."""
    result = await db.execute(select(Character).where(Character.user_id == user_id))
    character = result.scalar_one_or_none()
    if not character:
        raise ValueError("Character not found")
    
    cap_result = await db.execute(select(StatCap).where(StatCap.character_id == character.id))
    stat_cap = cap_result.scalar_one_or_none()
    
    if not stat_cap or not stat_cap.breakthrough_available:
        raise ValueError("Breakthrough not available")
    
    trial = BreakthroughTrial(
        id=uuid.uuid4(),
        user_id=user_id,
        phase=stat_cap.phase + 1,
        from_cap=stat_cap.current_cap,
        to_cap=stat_cap.current_cap + 100,
        status="in_progress",
        started_at=datetime.utcnow(),
    )
    db.add(trial)
    
    stat_cap.breakthrough_available = False
    await db.flush()
    
    return {
        "trial_id": str(trial.id),
        "from_cap": trial.from_cap,
        "to_cap": trial.to_cap,
        "phase": trial.phase,
    }


async def complete_breakthrough(db: AsyncSession, user_id) -> dict:
    """Complete a breakthrough trial and increase stat cap."""
    # Find active trial
    trial_result = await db.execute(
        select(BreakthroughTrial).where(
            BreakthroughTrial.user_id == user_id,
            BreakthroughTrial.status == "in_progress",
        )
    )
    trial = trial_result.scalar_one_or_none()
    
    if not trial:
        raise ValueError("No active breakthrough trial")
    
    # Update trial
    trial.status = "completed"
    trial.completed_at = datetime.utcnow()
    
    # Update stat cap
    result = await db.execute(select(Character).where(Character.user_id == user_id))
    character = result.scalar_one_or_none()
    
    cap_result = await db.execute(select(StatCap).where(StatCap.character_id == character.id))
    stat_cap = cap_result.scalar_one_or_none()
    
    if stat_cap:
        stat_cap.current_cap = trial.to_cap
        stat_cap.phase = trial.phase
    
    await db.flush()
    
    return {
        "new_cap": trial.to_cap,
        "new_phase": trial.phase,
        "message": f"Breakthrough complete! Stat cap increased to {trial.to_cap}",
    }
