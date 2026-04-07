from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.database import get_db
from app.core.deps import get_current_user
from app.models import User, Challenge, UserChallenge

router = APIRouter(prefix="/api/challenges", tags=["challenges"])


@router.get("")
async def get_all_challenges(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve all challenges and their progress for the current user."""
    # Get all challenges
    result = await db.execute(select(Challenge))
    challenges = result.scalars().all()
    
    # Get user's active/completed challenges
    user_challenge_result = await db.execute(
        select(UserChallenge).where(UserChallenge.user_id == user.id)
    )
    user_challenges = {uc.challenge_id: uc for uc in user_challenge_result.scalars().all()}
    
    # Format response
    formatted_challenges = []
    for challenge in challenges:
        user_c = user_challenges.get(challenge.id)
        formatted_challenges.append({
            "id": str(challenge.id),
            "name_vi": challenge.name_vi,
            "name_en": challenge.name_en,
            "description_vi": challenge.description_vi,
            "description_en": challenge.description_en,
            "challenge_type": challenge.challenge_type,
            "duration_days": challenge.duration_days,
            "requirements": challenge.requirements,
            "rewards": challenge.rewards,
            "min_level": challenge.min_level,
            "category": challenge.category,
            "status": user_c.status if user_c else "not_started",
            "days_completed": user_c.days_completed if user_c else 0,
            "is_active": user_c is not None
        })
        
    return formatted_challenges
