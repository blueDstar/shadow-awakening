import json
import math
import uuid
from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.db.database import get_db
from app.models import (
    BreakthroughRitual,
    BreakthroughTrial,
    Character,
    DailyQuest,
    ExperienceLog,
    Reflection,
    StatCap,
    Streak,
    User,
    UserStat,
)
from app.utils.exp_calculator import check_level_up

router = APIRouter(prefix="/api/breakthrough", tags=["breakthrough"])


def _loads_json(raw: Optional[str], default: Dict[str, Any]) -> Dict[str, Any]:
    if not raw:
        return default
    try:
        parsed = json.loads(raw)
        return parsed if isinstance(parsed, dict) else default
    except Exception:
        return default


async def _get_character_bundle(db: AsyncSession, user_id: Any):
    char_result = await db.execute(select(Character).where(Character.user_id == user_id))
    character = char_result.scalar_one_or_none()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    stats_result = await db.execute(select(UserStat).where(UserStat.character_id == character.id))
    stats = stats_result.scalars().all()

    cap_result = await db.execute(select(StatCap).where(StatCap.character_id == character.id))
    stat_cap = cap_result.scalar_one_or_none()
    if not stat_cap:
        stat_cap = StatCap(character_id=character.id, current_cap=100, phase=0, breakthrough_available=False)
        db.add(stat_cap)
        await db.flush()

    return character, stats, stat_cap


async def _get_current_trial(db: AsyncSession, user_id: Any, phase: int) -> Optional[BreakthroughTrial]:
    result = await db.execute(
        select(BreakthroughTrial)
        .where(
            BreakthroughTrial.user_id == user_id,
            BreakthroughTrial.phase == phase,
            BreakthroughTrial.status.in_(["available", "in_progress"]),
        )
    )
    return result.scalar_one_or_none()


async def _get_overall_streak(db: AsyncSession, user_id: Any) -> int:
    result = await db.execute(
        select(Streak).where(
            and_(Streak.user_id == user_id, Streak.streak_type == "overall")
        )
    )
    streak = result.scalar_one_or_none()
    return streak.current_streak if streak else 0


async def _count_recent_completed_quests(db: AsyncSession, user_id: Any, days: int) -> int:
    start_date = date.today() - timedelta(days=max(days - 1, 0))
    result = await db.execute(
        select(DailyQuest).where(
            DailyQuest.user_id == user_id,
            DailyQuest.quest_date >= start_date,
            DailyQuest.status == "completed",
        )
    )
    return len(result.scalars().all())


async def _recent_reflections(db: AsyncSession, user_id: Any, days: int) -> List[Reflection]:
    start_date = date.today() - timedelta(days=max(days - 1, 0))
    result = await db.execute(
        select(Reflection).where(
            Reflection.user_id == user_id,
            Reflection.reflection_date >= start_date,
        )
    )
    return result.scalars().all()


async def _find_ritual(db: AsyncSession, next_phase: int) -> Optional[BreakthroughRitual]:
    result = await db.execute(
        select(BreakthroughRitual).where(BreakthroughRitual.phase == next_phase)
    )
    return result.scalar_one_or_none()


async def _build_requirements(
    db: AsyncSession,
    user_id: Any,
    level: int,
    current_phase: int,
    current_cap: int,
) -> Dict[str, Any]:
    next_phase = current_phase + 1
    ritual = await _find_ritual(db, next_phase)

    required_completed_quests = 6 + (next_phase * 2) + min(level // 8, 6)
    required_reflections = 2 + next_phase
    required_reflection_words = 180 + (next_phase * 60)
    required_overall_streak = min(5 + (next_phase * 2), 30)
    tracking_window_days = 7 + min(next_phase, 7)

    title_vi = f"Nghi thức đột phá Giai đoạn {next_phase}"
    title_en = f"Breakthrough Ritual Phase {next_phase}"
    if ritual:
        title_vi = ritual.title_vi
        title_en = ritual.title_en

    return {
        "title_vi": title_vi,
        "title_en": title_en,
        "phase": next_phase,
        "tracking_window_days": tracking_window_days,
        "required_completed_quests": required_completed_quests,
        "required_reflections": required_reflections,
        "required_reflection_words": required_reflection_words,
        "required_overall_streak": required_overall_streak,
        "all_stats_must_reach_cap": True,
        "current_cap": current_cap,
        "next_cap": max(math.ceil(current_cap * 1.2), current_cap + 1),
        "stat_retention_ratio": 0.30,
        "exp_multiplier": round(1 + (next_phase * 0.15) + (level * 0.02), 3),
        "stat_multiplier": round(1 + (next_phase * 0.10) + (level * 0.015), 3),
        "ritual_aura": ritual.aura_name if ritual else f"phase_{next_phase}_awakened",
    }


async def _build_progress(
    db: AsyncSession,
    user_id: Any,
    stats: List[UserStat],
    stat_cap: StatCap,
    requirements: Dict[str, Any],
) -> Dict[str, Any]:
    cap_value = stat_cap.current_cap
    stats_payload = []
    all_stats_maxed = True

    for stat in stats:
        current_value = float(stat.current_value or 0)
        reached_cap = current_value >= cap_value
        if not reached_cap:
            all_stats_maxed = False
        stats_payload.append(
            {
                "stat_name": stat.stat_name,
                "current_value": current_value,
                "cap": cap_value,
                "reached_cap": reached_cap,
            }
        )

    completed_quests = await _count_recent_completed_quests(
        db, user_id, int(requirements.get("tracking_window_days", 7))
    )
    reflections = await _recent_reflections(
        db, user_id, int(requirements.get("tracking_window_days", 7))
    )
    reflection_word_counts = [len((r.content or "").split()) for r in reflections]
    max_reflection_words = max(reflection_word_counts) if reflection_word_counts else 0
    overall_streak = await _get_overall_streak(db, user_id)

    progress = {
        "all_stats_maxed": all_stats_maxed,
        "stats": stats_payload,
        "completed_quests": completed_quests,
        "required_completed_quests": int(requirements.get("required_completed_quests", 0)),
        "reflections": len(reflections),
        "required_reflections": int(requirements.get("required_reflections", 0)),
        "max_reflection_words": max_reflection_words,
        "required_reflection_words": int(requirements.get("required_reflection_words", 0)),
        "overall_streak": overall_streak,
        "required_overall_streak": int(requirements.get("required_overall_streak", 0)),
    }

    progress["ready_to_breakthrough"] = (
        progress["all_stats_maxed"]
        and progress["completed_quests"] >= progress["required_completed_quests"]
        and progress["reflections"] >= progress["required_reflections"]
        and progress["max_reflection_words"] >= progress["required_reflection_words"]
        and progress["overall_streak"] >= progress["required_overall_streak"]
    )
    return progress


def _serialize_trial(trial: BreakthroughTrial) -> Dict[str, Any]:
    return {
        "id": str(trial.id),
        "phase": trial.phase,
        "from_cap": trial.from_cap,
        "to_cap": trial.to_cap,
        "requirements": _loads_json(trial.requirements, {}),
        "current_progress": _loads_json(trial.current_progress, {}),
        "selected_option_id": trial.selected_option_id,
        "status": trial.status,
        "started_at": trial.started_at.isoformat() if trial.started_at else None,
        "completed_at": trial.completed_at.isoformat() if trial.completed_at else None,
    }


def _calculate_breakthrough_bonus(level: int, next_phase: int) -> int:
    base = 250 + (next_phase * 120)
    multiplier = 1 + max(level - 1, 0) * 0.04 + (next_phase * 0.15)
    return int(base * multiplier)


def _apply_level_ups(character: Character) -> Dict[str, Any]:
    leveled_up = False
    level_before = character.level
    while True:
        new_level, remaining_exp, did_level_up = check_level_up(character.level, character.current_exp)
        if not did_level_up:
            break
        leveled_up = True
        character.level = new_level
        character.current_exp = remaining_exp
    return {
        "leveled_up": leveled_up,
        "level_before": level_before,
        "level_after": character.level,
        "remaining_exp": character.current_exp,
    }


async def _ensure_trial(db: AsyncSession, user: User):
    character, stats, stat_cap = await _get_character_bundle(db, user.id)
    requirements = await _build_requirements(db, user.id, character.level, stat_cap.phase, stat_cap.current_cap)
    progress = await _build_progress(db, user.id, stats, stat_cap, requirements)

    stat_cap.breakthrough_available = progress["all_stats_maxed"]
    trial = await _get_current_trial(db, user.id, requirements["phase"])

    if not trial and progress["all_stats_maxed"]:
        trial = BreakthroughTrial(
            user_id=user.id,
            ritual_id=None,
            phase=requirements["phase"],
            from_cap=stat_cap.current_cap,
            to_cap=int(requirements["next_cap"]),
            requirements=json.dumps(requirements),
            current_progress=json.dumps(progress),
            selected_option_id=None,
            status="available",
        )
        db.add(trial)
        await db.flush()
    elif trial:
        trial.requirements = json.dumps(requirements)
        trial.current_progress = json.dumps(progress)

    return character, stats, stat_cap, trial, requirements, progress


@router.get("/status")
async def get_breakthrough_status(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    character, stats, stat_cap, trial, requirements, progress = await _ensure_trial(db, user)
    await db.commit()

    return {
        "phase": stat_cap.phase,
        "current_cap": stat_cap.current_cap,
        "breakthrough_available": stat_cap.breakthrough_available,
        "trial": _serialize_trial(trial) if trial else None,
        "requirements_preview": requirements,
        "progress": progress,
        "reward_scaling": {
            "exp_multiplier": requirements["exp_multiplier"],
            "stat_multiplier": requirements["stat_multiplier"],
        },
        "next_phase_effects": {
            "next_phase": requirements["phase"],
            "next_cap": requirements["next_cap"],
            "retained_stat_ratio": requirements["stat_retention_ratio"],
        },
    }


@router.post("/check")
async def check_breakthrough_eligibility(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    character, stats, stat_cap, trial, requirements, progress = await _ensure_trial(db, user)
    await db.commit()
    return {
        "status": "checked",
        "breakthrough_available": stat_cap.breakthrough_available,
        "trial": _serialize_trial(trial) if trial else None,
        "progress": progress,
    }


@router.post("/start")
async def start_breakthrough(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    character, stats, stat_cap, trial, requirements, progress = await _ensure_trial(db, user)

    if not progress["all_stats_maxed"]:
        raise HTTPException(
            status_code=400,
            detail="All stats must reach the current cap before a breakthrough mission can begin",
        )

    if not trial:
        raise HTTPException(status_code=400, detail="No breakthrough mission is available")

    if trial.status == "completed":
        raise HTTPException(status_code=400, detail="This breakthrough trial is already completed")

    if not trial.started_at:
        trial.started_at = datetime.utcnow()
    trial.status = "in_progress"
    trial.current_progress = json.dumps(progress)
    await db.commit()

    return {
        "status": "started",
        "trial": _serialize_trial(trial),
        "message_vi": "Nghi thức đột phá đã bắt đầu.",
        "message_en": "The breakthrough ritual has begun.",
    }


@router.post("/complete")
async def complete_breakthrough(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    character, stats, stat_cap, trial, requirements, progress = await _ensure_trial(db, user)

    if not trial:
        raise HTTPException(status_code=404, detail="No breakthrough trial found")

    if trial.status == "completed":
        raise HTTPException(status_code=400, detail="Breakthrough trial already completed")

    if not progress["ready_to_breakthrough"]:
        trial.current_progress = json.dumps(progress)
        await db.commit()
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Breakthrough requirements are not complete yet",
                "progress": progress,
            },
        )

    old_phase = stat_cap.phase
    old_cap = stat_cap.current_cap
    next_phase = requirements["phase"]
    next_cap = int(requirements["next_cap"])
    retention_ratio = float(requirements["stat_retention_ratio"])

    retained_stats = []
    for stat in stats:
        old_value = float(stat.current_value or 0)
        retained_value = round(min(next_cap, max(1.0, old_value * retention_ratio)), 2)
        stat.current_value = retained_value
        retained_stats.append(
            {
                "stat_name": stat.stat_name,
                "old_value": old_value,
                "retained_value": retained_value,
            }
        )

    stat_cap.phase = next_phase
    stat_cap.current_cap = next_cap
    stat_cap.breakthrough_available = False

    breakthrough_bonus_exp = _calculate_breakthrough_bonus(character.level, next_phase)
    character.current_exp += breakthrough_bonus_exp
    character.total_exp += breakthrough_bonus_exp
    character.aura = requirements.get("ritual_aura", f"phase_{next_phase}_awakened")

    level_info = _apply_level_ups(character)

    trial.status = "completed"
    trial.completed_at = datetime.utcnow()
    progress["ready_to_breakthrough"] = True
    progress["completed_at"] = trial.completed_at.isoformat()
    progress["retained_stats"] = retained_stats
    progress["new_cap"] = next_cap
    progress["old_cap"] = old_cap
    progress["old_phase"] = old_phase
    progress["new_phase"] = next_phase
    progress["breakthrough_bonus_exp"] = breakthrough_bonus_exp
    progress["reward_scaling"] = {
        "exp_multiplier": requirements["exp_multiplier"],
        "stat_multiplier": requirements["stat_multiplier"],
    }
    trial.current_progress = json.dumps(progress)

    exp_log = ExperienceLog(
        user_id=user.id,
        amount=breakthrough_bonus_exp,
        source="breakthrough",
        source_id=str(trial.id),
    )
    db.add(exp_log)

    await db.commit()

    return {
        "status": "completed",
        "message_vi": "Đột phá thành công. Bạn đã bước sang giai đoạn mới.",
        "message_en": "Breakthrough complete. You have advanced to a new phase.",
        "old_phase": old_phase,
        "new_phase": next_phase,
        "old_cap": old_cap,
        "new_cap": next_cap,
        "retained_stat_ratio": retention_ratio,
        "retained_stats": retained_stats,
        "breakthrough_bonus_exp": breakthrough_bonus_exp,
        "level_info": level_info,
        "reward_scaling": {
            "exp_multiplier": requirements["exp_multiplier"],
            "stat_multiplier": requirements["stat_multiplier"],
        },
        "trial": _serialize_trial(trial),
    }


@router.get("/history")
async def get_breakthrough_history(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(BreakthroughTrial)
        .where(BreakthroughTrial.user_id == user.id)
        .order_by(BreakthroughTrial.phase.desc())
    )
    trials = result.scalars().all()
    return {"history": [_serialize_trial(trial) for trial in trials]}
