"""Breakthrough Service - handles advanced ritual system."""
import uuid
import json
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models import Character, StatCap, BreakthroughTrial, BreakthroughRitual, UserStat, Streak, DailyQuest, Reflection


async def get_breakthrough_status(db: AsyncSession, user_id) -> dict:
    """Get current breakthrough and ritual status."""
    result = await db.execute(select(Character).where(Character.user_id == user_id))
    character = result.scalar_one_or_none()
    if not character:
        return {"available": False}
    
    cap_result = await db.execute(select(StatCap).where(StatCap.character_id == character.id))
    stat_cap = cap_result.scalar_one_or_none()
    
    if not stat_cap:
        return {"available": False}
    
    # Check for active trial and linked ritual
    trial_result = await db.execute(
        select(BreakthroughTrial).where(
            BreakthroughTrial.user_id == user_id,
            BreakthroughTrial.status == "in_progress",
        )
    )
    active_trial = trial_result.scalar_one_or_none()
    
    ritual = None
    if active_trial:
        ritual_result = await db.execute(select(BreakthroughRitual).where(BreakthroughRitual.phase == active_trial.phase))
        ritual = ritual_result.scalar_one_or_none()
    else:
        # If not in progress, check if a breakthrough is available
        if stat_cap.breakthrough_available:
            ritual_result = await db.execute(select(BreakthroughRitual).where(BreakthroughRitual.phase == stat_cap.phase + 1))
            ritual = ritual_result.scalar_one_or_none()

    return {
        "available": stat_cap.breakthrough_available,
        "current_phase": stat_cap.phase,
        "next_phase": stat_cap.phase + 1,
        "active_trial": _format_trial(active_trial, ritual) if active_trial else None,
        "ritual_template": _format_ritual(ritual) if ritual else None,
    }


def _format_ritual(ritual: BreakthroughRitual):
    if not ritual: return None
    return {
        "id": str(ritual.id),
        "phase": ritual.phase,
        "title_vi": ritual.title_vi,
        "aura_name": ritual.aura_name,
        "foundation": json.loads(ritual.foundation_req),
        "mandatory": json.loads(ritual.mandatory_reqs),
        "options": json.loads(ritual.optional_paths),
        "min_reflection": ritual.min_reflection_words
    }


def _format_trial(trial: BreakthroughTrial, ritual: BreakthroughRitual):
    return {
        "id": str(trial.id),
        "ritual_id": str(ritual.id) if ritual else None,
        "selected_option_id": trial.selected_option_id,
        "progress": json.loads(trial.current_progress) if trial.current_progress else {},
        "status": trial.status,
    }


async def start_breakthrough(db: AsyncSession, user_id) -> dict:
    """Start a ritual for the next phase."""
    result = await db.execute(select(Character).where(Character.user_id == user_id))
    character = result.scalar_one_or_none()
    
    cap_result = await db.execute(select(StatCap).where(StatCap.character_id == character.id))
    stat_cap = cap_result.scalar_one_or_none()
    
    if not stat_cap or not stat_cap.breakthrough_available:
        raise ValueError("Breakthrough not available")
    
    next_phase = stat_cap.phase + 1
    ritual_result = await db.execute(select(BreakthroughRitual).where(BreakthroughRitual.phase == next_phase))
    ritual = ritual_result.scalar_one_or_none()
    
    if not ritual:
        raise ValueError(f"Ritual for phase {next_phase} not defined")
        
    trial = BreakthroughTrial(
        id=uuid.uuid4(),
        user_id=user_id,
        ritual_id=ritual.id,
        phase=next_phase,
        from_cap=stat_cap.current_cap,
        to_cap=int(stat_cap.current_cap * 1.2),
        status="in_progress",
        started_at=datetime.utcnow(),
        current_progress="{}"
    )
    db.add(trial)
    
    stat_cap.breakthrough_available = False
    await db.flush()
    
    return {"status": "success", "trial_id": str(trial.id), "ritual": _format_ritual(ritual)}


async def select_ritual_option(db: AsyncSession, user_id, option_id: str) -> dict:
    """Select one of the 3 optional paths in a ritual."""
    trial_result = await db.execute(
        select(BreakthroughTrial).where(
            BreakthroughTrial.user_id == user_id,
            BreakthroughTrial.status == "in_progress",
        )
    )
    trial = trial_result.scalar_one_or_none()
    if not trial:
        raise ValueError("No active breakthrough trial")
        
    trial.selected_option_id = option_id
    await db.flush()
    return {"status": "success", "selected_option_id": option_id}


async def complete_breakthrough(db: AsyncSession, user_id) -> dict:
    """Complete ritual, reset stats (30% retention), and grow cap."""
    trial_result = await db.execute(
        select(BreakthroughTrial).where(
            BreakthroughTrial.user_id == user_id,
            BreakthroughTrial.status == "in_progress",
        )
    )
    trial = trial_result.scalar_one_or_none()
    if not trial:
        raise ValueError("No active breakthrough trial")

    # 1. Update character progression
    result = await db.execute(select(Character).where(Character.user_id == user_id))
    character = result.scalar_one_or_none()
    
    cap_result = await db.execute(select(StatCap).where(StatCap.character_id == character.id))
    stat_cap = cap_result.scalar_one_or_none()
    
    # 2. Reset stats with 30% retention
    stats_result = await db.execute(select(UserStat).where(UserStat.character_id == character.id))
    stats = stats_result.scalars().all()
    for stat in stats:
        stat.current_value = stat.current_value * 0.3
    
    # 3. Increase cap and phase
    stat_cap.current_cap = trial.to_cap
    stat_cap.phase = trial.phase
    
    # 4. Update Title and Aura
    ritual_result = await db.execute(select(BreakthroughRitual).where(BreakthroughRitual.id == trial.ritual_id))
    ritual = ritual_result.scalar_one_or_none()
    if ritual:
        character.title = ritual.title_vi
        character.aura = ritual.aura_name
        
    trial.status = "completed"
    trial.completed_at = datetime.utcnow()
    
    await db.flush()
    
    return {
        "status": "success",
        "new_cap": stat_cap.current_cap,
        "new_phase": stat_cap.phase,
        "new_title": character.title,
        "new_aura": character.aura,
        "message": f"Nghi thức hoàn tất! Bạn đã đột phá lên {character.title}."
    }
