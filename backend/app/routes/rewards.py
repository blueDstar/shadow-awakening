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

@router.post("/{reward_id}/equip")
async def equip_reward(
    reward_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    import uuid
    from fastapi import HTTPException
    from sqlalchemy import and_
    from app.models import Character
    
    # Verify unlocked
    try:
        r_uuid = uuid.UUID(reward_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID")
        
    ur_result = await db.execute(
        select(UserReward).where(
            and_(UserReward.user_id == user.id, UserReward.reward_id == r_uuid)
        )
    )
    if not ur_result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Reward not unlocked")
        
    # Get reward details
    reward_result = await db.execute(select(Reward).where(Reward.id == r_uuid))
    reward = reward_result.scalar_one_or_none()
    if not reward:
        raise HTTPException(status_code=404, detail="Reward not found")
        
    # Get character
    char_result = await db.execute(select(Character).where(Character.user_id == user.id))
    character = char_result.scalar_one_or_none()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
        
    if reward.reward_type == "title":
        character.title = reward.name_vi
    elif reward.reward_type == "aura":
        # Extract aura key from unlock_condition or name if unstructured. Defaulting logic:
        # Here we just use the reward name or a mapping. Let's use name for now.
        character.aura = reward.name_en.lower().replace(" ", "_")
        
    await db.commit()
    return {"status": "equipped", "type": reward.reward_type, "value": reward.name_vi}
