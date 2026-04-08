""" Progression Service - handles skill unlocks, challenge progress, and rewards. """
import json
import uuid
from datetime import datetime, date
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, update

from app.models import (
    User, Character, DailyQuest, UserStat, 
    Challenge, UserChallenge, Reward, UserReward, Skill, UserSkill,
    ExperienceLog
)

async def check_all_progress(db: AsyncSession, user_id: uuid.UUID):
    """ Main entry point to check all progression triggers. """
    character_result = await db.execute(select(Character).where(Character.user_id == user_id))
    character = character_result.scalar_one_or_none()
    if not character:
        return
        
    # 1. Update Challenge Progress
    await _update_challenge_progress(db, user_id)
    
    # 2. Check for Skill Unlocks
    await _check_skill_unlocks(db, character)
    
    # 3. Check for Reward Unlocks
    await _check_reward_unlocks(db, user_id, character)
    
    await db.commit()

async def _update_challenge_progress(db: AsyncSession, user_id: uuid.UUID):
    """ Update progress for active challenges. """
    # Get active challenges
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
            
        reqs = json.loads(challenge.requirements)
        # Simple logic: If challenge type is 'complete_quests', count them
        if challenge.challenge_type == "complete_quests":
            target = reqs.get("count", 10)
            # Count historical completed quests for this user within the challenge duration
            q_result = await db.execute(
                select(DailyQuest).where(
                    and_(
                        DailyQuest.user_id == user_id,
                        DailyQuest.status == "completed",
                        DailyQuest.quest_date >= uc.started_at.date()
                    )
                )
            )
            count = len(q_result.scalars().all())
            uc.days_completed = count
            
            if count >= target:
                uc.status = "completed"
                uc.completed_at = datetime.utcnow()
                # Grant rewards from challenge
                await _grant_rewards(db, user_id, json.loads(challenge.rewards))

async def _check_skill_unlocks(db: AsyncSession, character: Character):
    """ Check and unlock skills based on level or stats. """
    # Get all skills not yet unlocked
    unlocked_ids_result = await db.execute(
        select(UserSkill.skill_id).where(UserSkill.user_id == character.user_id)
    )
    unlocked_ids = unlocked_ids_result.scalars().all()
    
    available_skills_result = await db.execute(
        select(Skill).where(~Skill.id.in_(unlocked_ids) if unlocked_ids else True)
    )
    available_skills = available_skills_result.scalars().all()
    
    for skill in available_skills:
        conds = json.loads(skill.unlock_condition)
        # Logic: level requirement
        if "level" in conds and character.level >= conds["level"]:
            # Unlock!
            new_us = UserSkill(
                user_id=character.user_id,
                skill_id=skill.id,
                level=1,
                unlocked_at=datetime.utcnow()
            )
            db.add(new_us)

async def _check_reward_unlocks(db: AsyncSession, user_id: uuid.UUID, character: Character):
    """ Check for general achievements / rewards. """
    unlocked_ids_result = await db.execute(
        select(UserReward.reward_id).where(UserReward.user_id == user_id)
    )
    unlocked_ids = unlocked_ids_result.scalars().all()
    
    available_rewards_result = await db.execute(
        select(Reward).where(~Reward.id.in_(unlocked_ids) if unlocked_ids else True)
    )
    available_rewards = available_rewards_result.scalars().all()
    
    for reward in available_rewards:
        conds = json.loads(reward.unlock_condition)
        unlocked = False
        
        if "level" in conds and character.level >= conds["level"]:
            unlocked = True
        
        # Add more conditions like 'total_quests', 'streak', etc.
        
        if unlocked:
            new_ur = UserReward(
                user_id=user_id,
                reward_id=reward.id,
                unlocked_at=datetime.utcnow()
            )
            db.add(new_ur)

async def _grant_rewards(db: AsyncSession, user_id: uuid.UUID, rewards_dict: dict):
    """ Grant rewards (EXP, Stats, etc) to character. """
    character_result = await db.execute(select(Character).where(Character.user_id == user_id))
    character = character_result.scalar_one_or_none()
    if not character:
        return
        
    if "exp" in rewards_dict:
        character.current_exp += rewards_dict["exp"]
    
    # Handle more reward types if needed (e.g. direct stat boosts)
