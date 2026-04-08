import json
from datetime import date, datetime, timezone, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.db.database import get_db
from app.core.deps import get_current_user
from app.models import User, Character, UserStat, StatCap, DailyQuest, Streak, UserSettings
from app.services.quest_engine import get_daily_quote
from app.utils.exp_calculator import exp_to_next_level

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/summary")
async def get_dashboard_summary(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get comprehensive dashboard summary."""
    # Character
    char_result = await db.execute(select(Character).where(Character.user_id == user.id))
    character = char_result.scalar_one_or_none()
    
    # Stats
    stats = []
    stat_cap = 100
    phase = 1
    breakthrough_available = False
    
    if character:
        stats_result = await db.execute(select(UserStat).where(UserStat.character_id == character.id))
        stats_list = stats_result.scalars().all()
        
        cap_result = await db.execute(select(StatCap).where(StatCap.character_id == character.id))
        cap = cap_result.scalar_one_or_none()
        if cap:
            stat_cap = cap.current_cap
            phase = cap.phase
            breakthrough_available = cap.breakthrough_available
        
        stats = [{"stat_name": s.stat_name, "current_value": s.current_value, "cap": stat_cap} for s in stats_list]
    
    # Timezone adjustment (Vietnam UTC+7)
    vn_tz = timezone(timedelta(hours=7))
    now = datetime.now(vn_tz)
    today = now.date()
    
    # Today's quests
    today_result = await db.execute(
        select(DailyQuest).where(
            and_(DailyQuest.user_id == user.id, DailyQuest.quest_date == today)
        )
    )
    today_quests = today_result.scalars().all()
    total_q = len(today_quests)
    completed_q = sum(1 for q in today_quests if q.status == "completed")
    failed_q = sum(1 for q in today_quests if q.status == "failed")
    
    # Streaks
    streak_result = await db.execute(select(Streak).where(Streak.user_id == user.id))
    streaks = streak_result.scalars().all()
    overall_streak = 0
    best_streak = 0
    for s in streaks:
        if s.streak_type == "overall":
            overall_streak = s.current_streak
            best_streak = s.best_streak
    
    # Settings for timezone
    settings_result = await db.execute(select(UserSettings).where(UserSettings.user_id == user.id))
    settings = settings_result.scalar_one_or_none()
    tz_name = settings.timezone if settings else "Asia/Ho_Chi_Minh"
    
    # Calculate reset countdown (seconds until midnight in user's timezone)
    midnight = datetime.combine(today + timedelta(days=1), datetime.min.time(), tzinfo=vn_tz)
    countdown = int((midnight - now).total_seconds())
    
    # Quote
    quote = get_daily_quote()
    
    exp_needed = exp_to_next_level(character.level) if character else 110
    
    return {
        "character_name": character.name if character else "Unknown",
        "title": character.title if character else "Kẻ Thức Tỉnh",
        "level": character.level if character else 1,
        "current_exp": character.current_exp if character else 0,
        "exp_to_next_level": exp_needed,
        "total_exp": character.total_exp if character else 0,
        "aura": character.aura if character else "shadow_basic",
        "stats": stats,
        "stat_cap": stat_cap,
        "phase": phase,
        "breakthrough_available": breakthrough_available,
        "today_quests_total": total_q,
        "today_quests_completed": completed_q,
        "today_quests_failed": failed_q,
        "day_completed": completed_q == total_q and total_q > 0,
        "overall_streak": overall_streak,
        "best_streak": best_streak,
        "streaks": [
            {
                "streak_type": s.streak_type,
                "current_streak": s.current_streak,
                "best_streak": s.best_streak,
            }
            for s in streaks
        ],
        "reset_countdown_seconds": max(0, countdown),
        "quote_vi": quote["vi"],
        "quote_en": quote["en"],
    }


@router.get("/reset-countdown")
async def get_reset_countdown(
    user: User = Depends(get_current_user),
):
    """Get seconds until daily reset."""
    vn_tz = timezone(timedelta(hours=7))
    now = datetime.now(vn_tz)
    today = now.date()
    midnight = datetime.combine(today + timedelta(days=1), datetime.min.time(), tzinfo=vn_tz)
    countdown = int((midnight - now).total_seconds())
    return {"reset_countdown_seconds": max(0, countdown)}


@router.post("/set-title")
async def set_character_title(
    title: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Set the character's active title."""
    from app.models import UserReward, Reward
    
    # Verify title exists in user's rewards
    reward_result = await db.execute(
        select(Reward).join(UserReward).where(
            and_(
                UserReward.user_id == user.id,
                Reward.reward_type == "title",
                (Reward.name_vi == title) | (Reward.name_en == title)
            )
        )
    )
    reward = reward_result.scalar_one_or_none()
    
    if not reward:
        raise HTTPException(status_code=400, detail="Title not unlocked or invalid")
        
    # Update character
    char_result = await db.execute(select(Character).where(Character.user_id == user.id))
    character = char_result.scalar_one_or_none()
    
    if character:
        character.title = title
        await db.commit()
    
    return {"status": "success", "new_title": title}
