"""Stat Service - handles stat updates and breakthrough checks."""
from typing import Dict, Optional, Tuple

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Character, UserStat, StatCap
from app.services.quest_engine import CORE_STATS, get_phase_value, get_reward_scaling


async def _get_character_and_cap(db: AsyncSession, user_id) -> Tuple[Optional[Character], Optional[StatCap]]:
    result = await db.execute(select(Character).where(Character.user_id == user_id))
    character = result.scalar_one_or_none()
    if not character:
        return None, None

    cap_result = await db.execute(select(StatCap).where(StatCap.character_id == character.id))
    stat_cap = cap_result.scalar_one_or_none()
    if not stat_cap:
        stat_cap = StatCap(character_id=character.id, current_cap=100, phase=0, breakthrough_available=False)
        db.add(stat_cap)
        await db.flush()

    return character, stat_cap


async def get_scaling_snapshot(db: AsyncSession, user_id) -> Dict[str, float]:
    character, stat_cap = await _get_character_and_cap(db, user_id)
    level = character.level if character else 1
    phase = get_phase_value(stat_cap)
    scaling = get_reward_scaling(level, phase)
    return {
        "level": level,
        "phase": phase,
        "exp_multiplier": scaling["exp_multiplier"],
        "stat_multiplier": scaling["stat_multiplier"],
        "stat_cap": stat_cap.current_cap if stat_cap else 100,
        "breakthrough_available": stat_cap.breakthrough_available if stat_cap else False,
    }


async def update_stats(
    db: AsyncSession,
    user_id,
    stat_rewards: dict,
    streak_bonus: float = 1.0,
    apply_phase_scaling: bool = False,
):
    """Update user stats after quest completion or rewards.

    Quests already arrive pre-scaled by quest_engine, so `apply_phase_scaling`
    defaults to False to avoid double-scaling.
    """
    character, stat_cap = await _get_character_and_cap(db, user_id)
    if not character:
        return

    current_cap = stat_cap.current_cap if stat_cap else 100
    phase = get_phase_value(stat_cap)
    scaling = get_reward_scaling(character.level, phase)
    phase_multiplier = scaling["stat_multiplier"] if apply_phase_scaling else 1.0

    for stat_name, gain in (stat_rewards or {}).items():
        actual_gain = float(gain) * float(streak_bonus) * float(phase_multiplier)

        stat_result = await db.execute(
            select(UserStat).where(
                UserStat.character_id == character.id,
                UserStat.stat_name == stat_name,
            )
        )
        stat = stat_result.scalar_one_or_none()

        if not stat:
            stat = UserStat(character_id=character.id, stat_name=stat_name, current_value=0.0)
            db.add(stat)
            await db.flush()

        stat.current_value = min(float(stat.current_value or 0) + actual_gain, current_cap)

    await check_breakthrough(db, character.id)
    await db.flush()


async def check_breakthrough(db: AsyncSession, character_id):
    """Check if all core stats have reached the cap and toggle breakthrough."""
    cap_result = await db.execute(select(StatCap).where(StatCap.character_id == character_id))
    stat_cap = cap_result.scalar_one_or_none()
    if not stat_cap:
        return False

    stats_result = await db.execute(select(UserStat).where(UserStat.character_id == character_id))
    stats = stats_result.scalars().all()
    stats_by_name = {s.stat_name: float(s.current_value or 0) for s in stats}

    core_at_cap = all(stats_by_name.get(stat_name, 0) >= stat_cap.current_cap for stat_name in CORE_STATS)
    stat_cap.breakthrough_available = core_at_cap
    await db.flush()
    return core_at_cap


async def get_all_stats(db: AsyncSession, user_id) -> dict:
    """Get all stats for a user."""
    character, stat_cap = await _get_character_and_cap(db, user_id)
    if not character:
        scaling = get_reward_scaling(1, 0)
        return {
            "stats": [],
            "stat_cap": 100,
            "phase": 0,
            "breakthrough_available": False,
            "reward_scaling": scaling,
        }

    stats_result = await db.execute(select(UserStat).where(UserStat.character_id == character.id))
    stats = stats_result.scalars().all()
    phase = get_phase_value(stat_cap)
    scaling = get_reward_scaling(character.level, phase)

    return {
        "stats": [
            {
                "stat_name": s.stat_name,
                "current_value": s.current_value,
                "cap": stat_cap.current_cap if stat_cap else 100,
            }
            for s in stats
        ],
        "stat_cap": stat_cap.current_cap if stat_cap else 100,
        "phase": phase,
        "breakthrough_available": stat_cap.breakthrough_available if stat_cap else False,
        "reward_scaling": scaling,
    }
