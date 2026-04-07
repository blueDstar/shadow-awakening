from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.database import get_db
from app.core.deps import get_current_user
from app.models import User, Skill, UserSkill

router = APIRouter(prefix="/api/skills", tags=["skills"])


@router.get("")
async def get_all_skills(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve all available skills and their unlock status for the current user."""
    # Get all skills
    result = await db.execute(select(Skill))
    skills = result.scalars().all()
    
    # Get user's unlocked skills
    user_skill_result = await db.execute(
        select(UserSkill).where(UserSkill.user_id == user.id)
    )
    unlocked_skill_ids = {us.skill_id for us in user_skill_result.scalars().all()}
    
    # Format response
    formatted_skills = []
    for skill in skills:
        formatted_skills.append({
            "id": str(skill.id),
            "name_vi": skill.name_vi,
            "name_en": skill.name_en,
            "description_vi": skill.description_vi,
            "description_en": skill.description_en,
            "unlock_condition": skill.unlock_condition,
            "icon": skill.icon,
            "effect": skill.effect,
            "is_locked": skill.id not in unlocked_skill_ids
        })
        
    return formatted_skills
