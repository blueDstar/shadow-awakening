"""Progression Service - handles skill unlocks, challenge progress, and rewards."""
import json
import uuid
from datetime import datetime
from typing import Dict

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    Character,
    Challenge,
    DailyQuest,
    ExperienceLog,
    Reward,
    Skill,
    UserChallenge,
    UserReward,
    UserSkill,
    UserStat,
    StatCap,
)
from app.services.quest_engine import get_phase_value, get_reward_scaling
from app.services.stat_service import update_stats

async def check_all_progress(db: AsyncSession, user_id: uuid.UUID):
    """Main entry point to check all progression triggers."""
    character_result = await db.execute(select(Character).where(Character.user_id == user_id))
    character = character_result.scalar_one_or_none()
    if not character:
        return

    await _update_challenge_progress(db, user_id)
    await _check_skill_unlocks(db, character)
    await _check_reward_unlocks(db, user_id, character)
    await db.commit()


async def _get_stat_context(db: AsyncSession, character: Character):
    stats_result = await db.execute(select(UserStat).where(UserStat.character_id == character.id))
    stats = {s.stat_name: float(s.current_value or 0) for s in stats_result.scalars().all()}

    cap_result = await db.execute(select(StatCap).where(StatCap.character_id == character.id))
    stat_cap = cap_result.scalar_one_or_none()
    phase = get_phase_value(stat_cap)
    current_cap = stat_cap.current_cap if stat_cap else 100
    scaling = get_reward_scaling(character.level, phase)
    return stats, stat_cap, current_cap, phase, scaling


async def _update_challenge_progress(db: AsyncSession, user_id: uuid.UUID):
    """Update progress for active challenges."""
    result = await db.execute(
        select(UserChallenge).where(
            and_(UserChallenge.user_id == user_id, UserChallenge.status == "active")
        )
    )
    user_challenges = result.scalars().all()

    for uc in user_challenges:
        challenge_result = await db.execute(select(Challenge).where(Challenge.id == uc.challenge_id))
        challenge = challenge_result.scalar_one_or_none()
        if not challenge:
            continue

        reqs = json.loads(challenge.requirements or "{}")
        if challenge.challenge_type == "complete_quests":
            target = int(reqs.get("count", 10))
            q_result = await db.execute(
                select(DailyQuest).where(
                    and_(
                        DailyQuest.user_id == user_id,
                        DailyQuest.status == "completed",
                        DailyQuest.quest_date >= uc.started_at.date(),
                    )
                )
            )
            count = len(q_result.scalars().all())
            uc.days_completed = count

            if count >= target:
                uc.status = "completed"
                uc.completed_at = datetime.utcnow()
                await _grant_rewards(db, user_id, json.loads(challenge.rewards or "{}"), "challenge", str(challenge.id))


async def _check_skill_unlocks(db: AsyncSession, character: Character):
    """Check and unlock skills based on level, phase, cap, or stats."""
    unlocked_ids_result = await db.execute(
        select(UserSkill.skill_id).where(UserSkill.user_id == character.user_id)
    )
    unlocked_ids = unlocked_ids_result.scalars().all()

    available_skills_result = await db.execute(
        select(Skill).where(~Skill.id.in_(unlocked_ids) if unlocked_ids else True)
    )
    available_skills = available_skills_result.scalars().all()

    stats, _, current_cap, phase, _ = await _get_stat_context(db, character)

    for skill in available_skills:
        conds = json.loads(skill.unlock_condition or "{}")
        unlocked = True

        if "level" in conds and character.level < int(conds["level"]):
            unlocked = False
        if "phase" in conds and phase < int(conds["phase"]):
            unlocked = False
        if "cap" in conds and current_cap < int(conds["cap"]):
            unlocked = False

        required_stats = conds.get("stats", {})
        for stat_name, min_value in required_stats.items():
            if stats.get(stat_name, 0) < float(min_value):
                unlocked = False
                break

        if unlocked:
            db.add(
                UserSkill(
                    user_id=character.user_id,
                    skill_id=skill.id,
                    unlocked_at=datetime.utcnow(),
                )
            )


async def _check_reward_unlocks(db: AsyncSession, user_id: uuid.UUID, character: Character):
    """Check for general achievements / rewards."""
    unlocked_ids_result = await db.execute(
        select(UserReward.reward_id).where(UserReward.user_id == user_id)
    )
    unlocked_ids = unlocked_ids_result.scalars().all()

    available_rewards_result = await db.execute(
        select(Reward).where(~Reward.id.in_(unlocked_ids) if unlocked_ids else True)
    )
    available_rewards = available_rewards_result.scalars().all()

    stats, _, current_cap, phase, _ = await _get_stat_context(db, character)

    for reward in available_rewards:
        conds = json.loads(reward.unlock_condition or "{}")
        unlocked = True

        if "level" in conds and character.level < int(conds["level"]):
            unlocked = False
        if "phase" in conds and phase < int(conds["phase"]):
            unlocked = False
        if "cap" in conds and current_cap < int(conds["cap"]):
            unlocked = False

        required_stats = conds.get("stats", {})
        for stat_name, min_value in required_stats.items():
            if stats.get(stat_name, 0) < float(min_value):
                unlocked = False
                break

        if unlocked:
            db.add(
                UserReward(
                    user_id=user_id,
                    reward_id=reward.id,
                    unlocked_at=datetime.utcnow(),
                )
            )


async def _grant_rewards(
    db: AsyncSession,
    user_id: uuid.UUID,
    rewards_dict: Dict,
    source: str = "system",
    source_id: str | None = None,
):
    """Grant rewards (EXP, Stats, etc) to character with phase/level scaling."""
    character_result = await db.execute(select(Character).where(Character.user_id == user_id))
    character = character_result.scalar_one_or_none()
    if not character:
        return

    _, _, _, phase, scaling = await _get_stat_context(db, character)

    if "exp" in rewards_dict:
        scaled_exp = int(round(float(rewards_dict["exp"]) * scaling["exp_multiplier"]))
        character.current_exp += scaled_exp
        character.total_exp += scaled_exp
        db.add(
            ExperienceLog(
                user_id=user_id,
                amount=scaled_exp,
                source=source,
                source_id=source_id,
            )
        )

    stat_rewards = rewards_dict.get("stats") or rewards_dict.get("stat_rewards")
    if isinstance(stat_rewards, dict) and stat_rewards:
        await update_stats(
            db,
            user_id,
            stat_rewards,
            streak_bonus=1.0,
            apply_phase_scaling=True,
        )
