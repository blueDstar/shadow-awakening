"""Stat Service - handles stat updates and breakthrough checks."""
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Character, UserStat, StatCap
from app.services.quest_engine import CORE_STATS


async def update_stats(db: AsyncSession, user_id, stat_rewards: dict, streak_bonus: float = 1.0):
    """Update user stats after quest completion."""
    result = await db.execute(select(Character).where(Character.user_id == user_id))
    character = result.scalar_one_or_none()
    if not character:
        return
    
    cap_result = await db.execute(select(StatCap).where(StatCap.character_id == character.id))
    stat_cap = cap_result.scalar_one_or_none()
    current_cap = stat_cap.current_cap if stat_cap else 100
    
    for stat_name, gain in stat_rewards.items():
        actual_gain = gain * streak_bonus
        
        stat_result = await db.execute(
            select(UserStat).where(
                UserStat.character_id == character.id,
                UserStat.stat_name == stat_name,
            )
        )
        stat = stat_result.scalar_one_or_none()
        
        if stat:
            new_val = min(stat.current_value + actual_gain, current_cap)
            stat.current_value = new_val
    
    # Check breakthrough availability
    await check_breakthrough(db, character.id)
    await db.flush()


async def check_breakthrough(db: AsyncSession, character_id):
    """Check if all core stats have reached the cap."""
    cap_result = await db.execute(select(StatCap).where(StatCap.character_id == character_id))
    stat_cap = cap_result.scalar_one_or_none()
    if not stat_cap:
        return
    
    stats_result = await db.execute(select(UserStat).where(UserStat.character_id == character_id))
    stats = stats_result.scalars().all()
    
    core_at_cap = True
    for stat in stats:
        if stat.stat_name in CORE_STATS:
            if stat.current_value < stat_cap.current_cap:
                core_at_cap = False
                break
    
    stat_cap.breakthrough_available = core_at_cap
    await db.flush()


async def get_all_stats(db: AsyncSession, user_id) -> dict:
    """Get all stats for a user."""
    result = await db.execute(select(Character).where(Character.user_id == user_id))
    character = result.scalar_one_or_none()
    if not character:
        return {"stats": [], "current_cap": 100, "phase": 1, "breakthrough_available": False}
    
    stats_result = await db.execute(select(UserStat).where(UserStat.character_id == character.id))
    stats = stats_result.scalars().all()
    
    cap_result = await db.execute(select(StatCap).where(StatCap.character_id == character.id))
    stat_cap = cap_result.scalar_one_or_none()
    
    return {
        "stats": [{"stat_name": s.stat_name, "current_value": s.current_value, "cap": stat_cap.current_cap if stat_cap else 100} for s in stats],
        "current_cap": stat_cap.current_cap if stat_cap else 100,
        "phase": stat_cap.phase if stat_cap else 1,
        "breakthrough_available": stat_cap.breakthrough_available if stat_cap else False,
    }
