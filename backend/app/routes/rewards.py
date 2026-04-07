from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.database import get_db
from app.core.deps import get_current_user
from app.models import User, Reward, UserReward

router = APIRouter(prefix="/api/rewards", tags=["rewards"])


@router.get("")
async def get_all_rewards(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve all rewards and their unlock status for the current user."""
    # Get all rewards
    result = await db.execute(select(Reward))
    rewards = result.scalars().all()
    
    # Get user's unlocked rewards
    user_reward_result = await db.execute(
        select(UserReward).where(UserReward.user_id == user.id)
    )
    unlocked_reward_ids = {ur.reward_id for ur in user_reward_result.scalars().all()}
    
    # Format response
    formatted_rewards = []
    for reward in rewards:
        formatted_rewards.append({
            "id": str(reward.id),
            "name_vi": reward.name_vi,
            "name_en": reward.name_en,
            "reward_type": reward.reward_type,
            "description_vi": reward.description_vi,
            "description_en": reward.description_en,
            "unlock_condition": reward.unlock_condition,
            "icon": reward.icon,
            "rarity": reward.rarity,
            "is_unlocked": reward.id in unlocked_reward_ids
        })
        
    return formatted_rewards
