import json
from datetime import date, datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.db.database import get_db
from app.core.deps import get_current_user
from app.models import User, DailyQuest, QuestHistory, Character, ExperienceLog, Streak, StatCap
from app.services.quest_engine import generate_daily_quests
from app.services.stat_service import update_stats
from app.services.streak_service import update_streak
from app.utils.exp_calculator import check_level_up
from app.services.progression_service import check_all_progress

router = APIRouter(prefix="/api/quests", tags=["quests"])


async def _prepare_quest_response(db: AsyncSession, user_id: str, quests: list, target_date: date):
    """Common helper to format quest response with breakthrough status."""
    from uuid import UUID
    try:
        if isinstance(user_id, str):
            user_uuid = UUID(user_id)
        else:
            user_uuid = user_id
    except:
        user_uuid = user_id

    char_result = await db.execute(select(Character).where(Character.user_id == user_uuid))
    character = char_result.scalar_one_or_none()
    stat_cap = None
    if character:
        cap_result = await db.execute(select(StatCap).where(StatCap.character_id == character.id))
        stat_cap = cap_result.scalar_one_or_none()
        
    total = len(quests)
    completed = sum(1 for q in quests if q.status == "completed")
    failed = sum(1 for q in quests if q.status == "failed")
    
    return {
        "quests": [
            {
                "id": str(q.id),
                "title_vi": q.title_vi,
                "title_en": q.title_en,
                "description_vi": q.description_vi,
                "description_en": q.description_en,
                "quest_type": q.quest_type,
                "category": q.category,
                "difficulty": q.difficulty,
                "exp_reward": q.exp_reward,
                "stat_rewards": q.stat_rewards,
                "status": q.status,
                "quest_date": str(q.quest_date),
                "completed_at": q.completed_at.isoformat() if q.completed_at else None,
                "fail_reason": q.fail_reason,
                "is_rerolled": q.is_rerolled,
            }
            for q in quests
        ],
        "total": total,
        "completed": completed,
        "failed": failed,
        "day_completed": completed == total and total > 0,
        "can_refresh": all(q.status != "pending" for q in quests) and total > 0,
        "quest_date": str(target_date),
        "breakthrough_available": stat_cap.breakthrough_available if stat_cap else False,
    }


@router.get("/today")
async def get_today_quests(
    client_date: str = None,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get or generate today's quests."""
    target_date = date.fromisoformat(client_date) if client_date else date.today()
    quests = await generate_daily_quests(db, user, target_date)
    return await _prepare_quest_response(db, user.id, quests, target_date)


@router.post("/refresh")
async def refresh_quests(
    client_date: str = None,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Generate 3 more quests if all current ones are completed."""
    from app.services.quest_engine import refresh_daily_quests
    
    target_date = date.fromisoformat(client_date) if client_date else date.today()
    quests = await refresh_daily_quests(db, user, target_date)
    return await _prepare_quest_response(db, user.id, quests, target_date)


@router.post("/{quest_id}/reroll")
async def reroll_quest(
    quest_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Replace a quest with a new one."""
    from app.services.quest_engine import reroll_daily_quest
    import uuid
    
    try:
        q_uuid = uuid.UUID(quest_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid quest ID")
        
    new_quest = await reroll_daily_quest(db, user, q_uuid)
    if not new_quest:
        raise HTTPException(status_code=404, detail="Quest not found or cannot be rerolled")
        
    await db.commit()
    return {
        "status": "success",
        "quest": {
            "id": str(new_quest.id),
            "title_vi": new_quest.title_vi,
            "title_en": new_quest.title_en,
            "status": new_quest.status,
        }
    }


@router.post("/{quest_id}/complete")
async def complete_quest(
    quest_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Mark a quest as completed and award EXP + stats."""
    import uuid as uuid_lib
    try:
        q_uuid = uuid_lib.UUID(quest_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid quest ID")

    result = await db.execute(
        select(DailyQuest).where(
            and_(DailyQuest.id == q_uuid, DailyQuest.user_id == user.id)
        )
    )
    quest = result.scalar_one_or_none()
    
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")
    if quest.status == "completed":
        raise HTTPException(status_code=400, detail="Quest already completed")
    
    # Mark complete
    quest.status = "completed"
    quest.completed_at = datetime.utcnow()
    
    # Award EXP
    char_result = await db.execute(select(Character).where(Character.user_id == user.id))
    character = char_result.scalar_one_or_none()
    
    leveled_up = False
    new_level = character.level if character else 1
    
    if character:
        character.current_exp += quest.exp_reward
        character.total_exp += quest.exp_reward
        
        # Check level up
        new_level, remaining_exp, leveled_up = check_level_up(character.level, character.current_exp)
        if leveled_up:
            character.level = new_level
            character.current_exp = remaining_exp
        
        # Log EXP
        exp_log = ExperienceLog(
            user_id=user.id,
            amount=quest.exp_reward,
            source="quest",
            source_id=str(quest.id),
        )
        db.add(exp_log)
    
    # Award stats
    stat_rewards = json.loads(quest.stat_rewards) if quest.stat_rewards else {}
    if stat_rewards:
        # Get overall streak for bonus
        streak_result = await db.execute(
            select(Streak).where(
                and_(Streak.user_id == user.id, Streak.streak_type == "overall")
            )
        )
        overall = streak_result.scalar_one_or_none()
        streak_bonus = 1 + min((overall.current_streak if overall else 0) * 0.02, 0.5)
        await update_stats(db, user.id, stat_rewards, streak_bonus)
    
    # Update category streak
    category_to_streak = {
        "wisdom": "reading",
        "fitness": "fitness",
        "focus": "deep_work",
        "discipline": "journal",
        "exploration": "research",
        "confidence": "overall",
    }
    streak_type = category_to_streak.get(quest.category, "overall")
    await update_streak(db, user.id, streak_type)
    
    # Check if all quests completed today
    all_quests_result = await db.execute(
        select(DailyQuest).where(
            and_(DailyQuest.user_id == user.id, DailyQuest.quest_date == date.today())
        )
    )
    all_quests = all_quests_result.scalars().all()
    all_completed = all(q.status == "completed" for q in all_quests)
    
    if all_completed:
        await update_streak(db, user.id, "overall")
    
    # Check for Skills, Challenges, and Rewards!
    await check_all_progress(db, user.id)
    
    await db.commit()  # CRITICAL: persist to PostgreSQL
    
    return {
        "status": "completed",
        "exp_earned": quest.exp_reward,
        "stat_rewards": stat_rewards,
        "leveled_up": leveled_up,
        "new_level": new_level,
        "day_completed": all_completed,
    }


@router.post("/{quest_id}/fail")
async def fail_quest(
    quest_id: str,
    fail_reason: str = "forgot",
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Mark a quest as failed."""
    import uuid as uuid_lib
    try:
        q_uuid = uuid_lib.UUID(quest_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid quest ID")

    result = await db.execute(
        select(DailyQuest).where(
            and_(DailyQuest.id == q_uuid, DailyQuest.user_id == user.id)
        )
    )
    quest = result.scalar_one_or_none()
    
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")
    
    quest.status = "failed"
    quest.fail_reason = fail_reason
    await db.commit()  # CRITICAL: persist to PostgreSQL
    
    return {"status": "failed", "fail_reason": fail_reason}


@router.get("/history")
async def get_quest_history(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    limit: int = 30,
):
    """Get quest history."""
    result = await db.execute(
        select(QuestHistory)
        .where(QuestHistory.user_id == user.id)
        .order_by(QuestHistory.quest_date.desc())
        .limit(limit)
    )
    histories = result.scalars().all()
    
    return [
        {
            "quest_date": str(h.quest_date),
            "total_quests": h.total_quests,
            "completed_quests": h.completed_quests,
            "failed_quests": h.failed_quests,
            "exp_earned": h.exp_earned,
            "day_completed": h.day_completed,
        }
        for h in histories
    ]
