"""
Quest Engine - Core quest generation system
Generates daily quests based on user profile, stats, streaks, and history.
Now updated to use PostgreSQL backend database.
"""
import json
import uuid
import random
from datetime import date, datetime, timedelta
from typing import List, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_

from app.models import (
    User, UserProfile, Character, UserStat, StatCap,
    DailyQuest, QuestHistory, Streak, UserChallenge, Quest
)
from app.utils.exp_calculator import calculate_quest_exp, calculate_stat_gain
from app.utils.difficulty_scaler import (
    calculate_base_difficulty,
    apply_dynamic_adjustment,
    scale_quest_requirements,
)

# ============================================================
# QUEST TEMPLATES HARDCODED FALLBACKS
# ============================================================

PENALTY_TEMPLATES = [
    {
        "title_vi": "Phạt: Squat 15 cái",
        "title_en": "Penalty: 15 squats",
        "desc_vi": "Bạn chưa hoàn thành nhiệm vụ hôm qua. Hoàn thành 15 squat để chuộc lỗi.",
        "desc_en": "You didn't complete yesterday's quests. Do 15 squats as penalty.",
        "category": "fitness",
        "stat_rewards": {"strength": 1, "discipline": 2},
        "base_exp": 15, "param": None, "severity": "light",
    },
    {
        "title_vi": "Phạt: Plank 45 giây",
        "title_en": "Penalty: Plank 45 seconds",
        "desc_vi": "Giữ plank trong 45 giây để rèn luyện kỷ luật.",
        "desc_en": "Hold plank for 45 seconds to build discipline.",
        "category": "fitness",
        "stat_rewards": {"strength": 1, "discipline": 2},
        "base_exp": 15, "param": None, "severity": "light",
    },
    {
        "title_vi": "Phạt: Viết 5 dòng reflection vì sao thất bại",
        "title_en": "Penalty: Write 5 lines about why you failed",
        "desc_vi": "Viết ít nhất 5 dòng phân tích lý do thất bại và bài học rút ra.",
        "desc_en": "Write at least 5 lines analyzing your failure reasons and lessons learned.",
        "category": "discipline",
        "stat_rewards": {"discipline": 2, "mental_resilience": 1},
        "base_exp": 15, "param": None, "severity": "moderate",
    },
]

# Daily motivational quotes
DAILY_QUOTES = [
    {"vi": "Mỗi ngày không tiến bộ là một ngày thụt lùi.", "en": "Every day without progress is a day of regression."},
    {"vi": "Kẻ mạnh không phải người không sợ, mà là người hành động dù sợ.", "en": "The strong are not those without fear, but those who act despite it."},
    {"vi": "Kỷ luật là cầu nối giữa mục tiêu và thành tựu.", "en": "Discipline is the bridge between goals and accomplishment."},
    {"vi": "Bóng tối chỉ ở nơi ánh sáng chưa chạm tới.", "en": "Darkness only exists where light hasn't reached."},
    {"vi": "Thức tỉnh không phải điểm đến, mà là hành trình mỗi ngày.", "en": "Awakening is not a destination, but a daily journey."},
    {"vi": "Giới hạn chỉ tồn tại trong tâm trí kẻ chưa vượt qua.", "en": "Limits only exist in the mind of those who haven't transcended them."},
    {"vi": "Hôm nay bạn rèn luyện, ngày mai bạn chiến thắng.", "en": "Today you train, tomorrow you conquer."},
    {"vi": "Sức mạnh thật sự đến từ những gì bạn lặp lại mỗi ngày.", "en": "True power comes from what you repeat daily."},
]

CORE_STATS = ["wisdom", "confidence", "strength", "discipline", "focus"]
EXTENDED_STATS = ["stamina", "knowledge", "consistency", "mental_resilience", "social_courage"]
ALL_STATS = CORE_STATS + EXTENDED_STATS

async def _get_quest_templates(db: AsyncSession) -> dict:
    result = await db.execute(select(Quest).where(Quest.is_template == True))
    templates = result.scalars().all()
    pool = {}
    for t in templates:
        cat = t.category
        if cat not in pool:
            pool[cat] = []
        
        try:
            stat_rewards_dict = json.loads(t.stat_rewards) if t.stat_rewards else {}
        except:
            stat_rewards_dict = {}
            
        pool[cat].append({
            "title_vi": t.title_vi,
            "title_en": t.title_en,
            "desc_vi": t.description_vi or "",
            "desc_en": t.description_en or "",
            "category": cat,
            "stat_rewards": stat_rewards_dict,
            "base_n": 0,
            "param": None,
            "base_exp": t.exp_reward or 15
        })
    return pool


async def generate_daily_quests(db: AsyncSession, user: User, target_date: Optional[date] = None) -> List[DailyQuest]:
    """Main quest generation function. Creates daily quests for a user."""
    today = target_date or date.today()
    
    existing = await db.execute(
        select(DailyQuest).where(
            and_(DailyQuest.user_id == user.id, DailyQuest.quest_date == today)
        )
    )
    existing_quests = existing.scalars().all()
    if existing_quests:
        return existing_quests
    
    character = await _get_character(db, user.id)
    stats = await _get_stats(db, character.id if character else None)
    stat_cap = await _get_stat_cap(db, character.id if character else None)
    streaks = await _get_streaks(db, user.id)
    yesterday_quests = await _get_yesterday_quests(db, user.id, today)
    profile = await _get_profile(db, user.id)
    
    level = character.level if character else 1
    overall_streak = _get_overall_streak(streaks)
    
    base_diff = calculate_base_difficulty(level, overall_streak)
    fails, successes = await _get_recent_performance(db, user.id)
    completion_rate = await _get_7d_completion_rate(db, user.id, today)
    difficulty = apply_dynamic_adjustment(base_diff, fails, successes, completion_rate)
    
    weak_stats = _find_weak_stats(stats, stat_cap.current_cap if stat_cap else 100)
    strong_stats = _find_strong_stats(stats, stat_cap.current_cap if stat_cap else 100)
    
    templates_pool = await _get_quest_templates(db)
    quests = []
    
    # 1. Mandatory Fitness Quests (at least 2)
    fitness_templates = templates_pool.get("fitness", [])
    if fitness_templates:
        selected_fitness = random.sample(fitness_templates, min(2, len(fitness_templates)))
        for template in selected_fitness:
            quest = _build_quest_from_template(template, difficulty, level, "main")
            quests.append(quest)
    
    # 2. Main Quests
    remaining_main = 3 - len(quests)
    if remaining_main > 0:
        quests.extend(_generate_main_quests(weak_stats, difficulty, level, profile, remaining_main, templates_pool))
    
    # 3. Side Quests
    quests.extend(_generate_side_quests(stats, difficulty, level, profile, 1, templates_pool))
    
    # 4. Habit Quests
    quests.extend(_generate_habit_quests(difficulty, level, profile, 2, templates_pool))
    
    # 5. Penalty
    failed_yesterday = [q for q in yesterday_quests if q.status == "failed"]
    if failed_yesterday:
        quests.extend(_generate_penalty_quests(len(failed_yesterday), difficulty, level, profile))
    
    # 6. Apply chain continuity
    quests = _apply_chain_continuity(quests, yesterday_quests, difficulty, level, templates_pool)
    
    max_quests = min(5 + level // 5, 10)
    quests = quests[:max_quests]
    
    daily_quests = []
    for q in quests:
        exp = calculate_quest_exp(difficulty, q["quest_type"], level, q.get("base_exp"))
        
        # Scale stat rewards based on the new logic
        stat_rewards = q.get("stat_rewards", {})
        scaled_stat_rewards = {}
        for stat_name, val in stat_rewards.items():
            base_gain = float(val)
            scaled_gain = calculate_stat_gain(base_gain, difficulty, overall_streak, level)
            scaled_stat_rewards[stat_name] = max(1, int(round(scaled_gain)))

        dq = DailyQuest(
            id=uuid.uuid4(),
            user_id=user.id,
            quest_date=today,
            title_vi=q["title_vi"],
            title_en=q["title_en"],
            description_vi=q.get("desc_vi", ""),
            description_en=q.get("desc_en", ""),
            quest_type=q["quest_type"],
            category=q["category"],
            difficulty=difficulty,
            exp_reward=exp,
            stat_rewards=json.dumps(scaled_stat_rewards),
            status="pending",
        )
        db.add(dq)
        daily_quests.append(dq)
    
    await db.flush()
    await db.commit()  # Persist generated quests to PostgreSQL
    return daily_quests


async def refresh_daily_quests(db: AsyncSession, user: User, target_date: Optional[date] = None) -> List[DailyQuest]:
    today = target_date or date.today()
    
    existing = await db.execute(
        select(DailyQuest).where(
            and_(DailyQuest.user_id == user.id, DailyQuest.quest_date == today)
        )
    )
    existing_quests = existing.scalars().all()
    
    if not existing_quests:
        return await generate_daily_quests(db, user, today)
        
    any_pending = any(q.status == "pending" for q in existing_quests)
    if any_pending:
        return existing_quests
        
    character = await _get_character(db, user.id)
    level = character.level if character else 1
    
    completion_rate = await _get_7d_completion_rate(db, user.id, today)
    difficulty = min(50, int(existing_quests[0].difficulty * 1.1) + 1)
    
    completed_cats = [q.category for q in existing_quests if q.status == "completed"]
    dominant_cat = random.choice(completed_cats) if completed_cats else "wisdom"
    
    templates_pool = await _get_quest_templates(db)
    new_quest_data = []
    
    related_templates = templates_pool.get(dominant_cat, templates_pool.get("wisdom", []))
    if related_templates:
        selected_related = random.sample(related_templates, min(2, len(related_templates)))
        for template in selected_related:
            new_quest_data.append(_build_quest_from_template(template, difficulty, level, "side"))
        
    fitness_templates = templates_pool.get("fitness", [])
    if fitness_templates:
        template = random.choice(fitness_templates)
        new_quest_data.append(_build_quest_from_template(template, difficulty, level, "side"))
        
    new_entities = []
    streaks = await _get_streaks(db, user.id)
    overall_streak = _get_overall_streak(streaks)

    for q in new_quest_data:
        exp = calculate_quest_exp(difficulty, q["quest_type"], level, q.get("base_exp"))
        exp = int(exp * 1.2)
        
        stat_rewards = q.get("stat_rewards", {})
        scaled_stat_rewards = {}
        for stat_name, val in stat_rewards.items():
            base_gain = float(val)
            scaled_gain = calculate_stat_gain(base_gain, difficulty, overall_streak, level)
            scaled_stat_rewards[stat_name] = max(1, int(round(scaled_gain)))
        
        dq = DailyQuest(
            id=uuid.uuid4(),
            user_id=user.id,
            quest_date=today,
            title_vi=f"[Tăng cường] {q['title_vi']}",
            title_en=f"[Extra] {q['title_en']}",
            description_vi=q.get("desc_vi", ""),
            description_en=q.get("desc_en", ""),
            quest_type="special", 
            category=q["category"],
            difficulty=difficulty,
            exp_reward=exp,
            stat_rewards=json.dumps(scaled_stat_rewards),
            status="pending",
        )
        db.add(dq)
        new_entities.append(dq)
        
    await db.flush()
    await db.commit()  # Persist refreshed quests to PostgreSQL
    return existing_quests + new_entities


def _generate_main_quests(
    weak_stats: List[str], difficulty: int, level: int, profile, count: int, templates_pool: dict
) -> List[dict]:
    quests = []
    categories_used = set()
    
    for stat_name in weak_stats[:count]:
        cat = _stat_to_category(stat_name)
        if cat in categories_used:
            continue
        templates = templates_pool.get(cat, [])
        if not templates:
            continue
        
        template = random.choice(templates)
        quest = _build_quest_from_template(template, difficulty, level, "main")
        quests.append(quest)
        categories_used.add(cat)
    
    # Fill remaining
    pool_keys = list(templates_pool.keys())
    while len(quests) < count and pool_keys:
        cat = random.choice(pool_keys)
        if cat not in categories_used:
            templates = templates_pool.get(cat, [])
            if templates:
                template = random.choice(templates)
                quest = _build_quest_from_template(template, difficulty, level, "main")
                quests.append(quest)
                categories_used.add(cat)
        # Avoid infinite loop if not enough categories
        if len(categories_used) >= len(pool_keys):
            break
            
    return quests[:count]


def _generate_side_quests(
    stats: dict, difficulty: int, level: int, profile, count: int, templates_pool: dict
) -> List[dict]:
    quests = []
    cats = list(templates_pool.keys())
    random.shuffle(cats)
    
    for cat in cats[:count+2]: # add buffer just in case
        if len(quests) >= count:
            break
        templates = templates_pool.get(cat, [])
        if templates:
            template = random.choice(templates)
            quest = _build_quest_from_template(template, difficulty, level, "side")
            quests.append(quest)
    
    return quests[:count]


def _generate_habit_quests(
    difficulty: int, level: int, profile, count: int, templates_pool: dict
) -> List[dict]:
    # We can mix static habits with `discipline` tasks from the pool
    habit_templates = [
        {
            "title_vi": "Uống đủ 8 ly nước hôm nay",
            "title_en": "Drink 8 glasses of water today",
            "desc_vi": "Uống ít nhất 8 ly nước trong ngày để duy trì sức khỏe.",
            "desc_en": "Drink at least 8 glasses of water to stay healthy.",
            "category": "fitness",
            "stat_rewards": {"stamina": 1},
            "base_exp": 10,
        },
        {
            "title_vi": "Không dùng điện thoại 30 phút đầu tiên sau khi thức",
            "title_en": "No phone for 30 minutes after waking up",
            "desc_vi": "Tránh sử dụng điện thoại trong 30 phút đầu tiên để bắt đầu ngày tỉnh táo.",
            "desc_en": "Avoid using your phone for 30 minutes after waking to start your day clear.",
            "category": "discipline",
            "stat_rewards": {"discipline": 1, "focus": 1},
            "base_exp": 10,
        },
        {
            "title_vi": "Ghi lại 3 điều biết ơn hôm nay",
            "title_en": "Write 3 things you're grateful for today",
            "desc_vi": "Viết ra 3 điều bạn cảm thấy biết ơn ngày hôm nay.",
            "desc_en": "Write down 3 things you feel grateful for today.",
            "category": "focus",
            "stat_rewards": {"mental_resilience": 1},
            "base_exp": 10,
        },
    ]
    
    # Also fetch some basic routines from db if there any "habit" typed templates, but we query by category here
    habit_mix = habit_templates.copy()
    if "discipline" in templates_pool:
        habit_mix.extend(templates_pool["discipline"][:2])
    
    random.shuffle(habit_mix)
    quests = []
    for template in habit_mix[:count]:
        quest = _build_quest_from_template(template, difficulty, level, "habit")
        quests.append(quest)
    
    return quests[:count]


def _generate_penalty_quests(
    fail_count: int, difficulty: int, level: int, profile
) -> List[dict]:
    severity = "light" if fail_count <= 1 else ("moderate" if fail_count <= 3 else "heavy")
    matching = [p for p in PENALTY_TEMPLATES if p.get("severity", "light") in [severity, "light"]]
    if not matching:
        matching = PENALTY_TEMPLATES
    
    template = random.choice(matching)
    quest = _build_quest_from_template(template, max(1, difficulty - 1), level, "penalty")
    return [quest]


def _build_quest_from_template(
    template: dict, difficulty: int, level: int, quest_type: str
) -> dict:
    quest = {
        "quest_type": quest_type,
        "category": template["category"],
        "stat_rewards": template.get("stat_rewards", {}),
        "base_exp": template.get("base_exp", 15)
    }
    
    # Database tasks might not need replacing. 
    quest["title_vi"] = template.get("title_vi", "Nhiệm vụ ẩn")
    quest["title_en"] = template.get("title_en", "Hidden Quest")
    quest["desc_vi"] = template.get("desc_vi", "")
    quest["desc_en"] = template.get("desc_en", "")

    return quest


def _apply_chain_continuity(
    quests: List[dict], yesterday_quests: List, difficulty: int, level: int, templates_pool: dict
) -> List[dict]:
    if not yesterday_quests:
        return quests
    
    completed_categories = set()
    for yq in yesterday_quests:
        if yq.status == "completed":
            completed_categories.add(yq.category)
    
    current_categories = {q["category"] for q in quests}
    for cat in completed_categories:
        if cat not in current_categories and cat in templates_pool:
            templates = templates_pool[cat]
            if templates:
                template = random.choice(templates)
                quest = _build_quest_from_template(template, difficulty, level, "side")
                quests.append(quest)
                break
    
    return quests


def _stat_to_category(stat_name: str) -> str:
    mapping = {
        "wisdom": "wisdom",
        "knowledge": "wisdom",
        "confidence": "confidence",
        "social_courage": "confidence",
        "strength": "fitness",
        "stamina": "fitness",
        "discipline": "discipline",
        "consistency": "discipline",
        "focus": "focus",
        "mental_resilience": "focus",
    }
    return mapping.get(stat_name, "wisdom")


def _find_weak_stats(stats: dict, cap: int) -> List[str]:
    threshold = cap * 0.4
    weak = []
    for stat_name in CORE_STATS:
        val = stats.get(stat_name, 0)
        if val < threshold:
            weak.append(stat_name)
    random.shuffle(weak)
    if not weak:
        weak = list(CORE_STATS)
        random.shuffle(weak)
    return weak


def _find_strong_stats(stats: dict, cap: int) -> List[str]:
    threshold = cap * 0.8
    return [s for s in CORE_STATS if stats.get(s, 0) >= threshold]


async def _get_character(db: AsyncSession, user_id) -> Optional[Character]:
    result = await db.execute(select(Character).where(Character.user_id == user_id))
    return result.scalar_one_or_none()


async def _get_stats(db: AsyncSession, character_id) -> dict:
    if not character_id:
        return {}
    result = await db.execute(select(UserStat).where(UserStat.character_id == character_id))
    stats = result.scalars().all()
    return {s.stat_name: s.current_value for s in stats}


async def _get_stat_cap(db: AsyncSession, character_id) -> Optional[StatCap]:
    if not character_id:
        return None
    result = await db.execute(select(StatCap).where(StatCap.character_id == character_id))
    return result.scalar_one_or_none()


async def _get_streaks(db: AsyncSession, user_id) -> List[Streak]:
    result = await db.execute(select(Streak).where(Streak.user_id == user_id))
    return result.scalars().all()


def _get_overall_streak(streaks: List[Streak]) -> int:
    for s in streaks:
        if s.streak_type == "overall":
            return s.current_streak
    return 0


async def _get_yesterday_quests(db: AsyncSession, user_id, today: date) -> List[DailyQuest]:
    yesterday = today - timedelta(days=1)
    result = await db.execute(
        select(DailyQuest).where(
            and_(DailyQuest.user_id == user_id, DailyQuest.quest_date == yesterday)
        )
    )
    return result.scalars().all()


async def _get_profile(db: AsyncSession, user_id) -> Optional[UserProfile]:
    result = await db.execute(select(UserProfile).where(UserProfile.user_id == user_id))
    return result.scalar_one_or_none()


async def _get_recent_performance(db: AsyncSession, user_id) -> tuple:
    recent = await db.execute(
        select(QuestHistory)
        .where(QuestHistory.user_id == user_id)
        .order_by(QuestHistory.quest_date.desc())
        .limit(7)
    )
    histories = recent.scalars().all()
    
    consecutive_fails = 0
    consecutive_successes = 0
    
    for h in histories:
        if h.day_completed:
            if consecutive_fails == 0:
                consecutive_successes += 1
            else:
                break
        else:
            if consecutive_successes == 0:
                consecutive_fails += 1
            else:
                break
    
    return consecutive_fails, consecutive_successes


async def _get_7d_completion_rate(db: AsyncSession, user_id, today: date) -> float:
    week_ago = today - timedelta(days=7)
    result = await db.execute(
        select(QuestHistory)
        .where(and_(QuestHistory.user_id == user_id, QuestHistory.quest_date >= week_ago))
    )
    histories = result.scalars().all()
    
    if not histories:
        return 0.5
    
    total = sum(h.total_quests for h in histories)
    completed = sum(h.completed_quests for h in histories)
    
    return completed / total if total > 0 else 0.5


def get_daily_quote() -> dict:
    return random.choice(DAILY_QUOTES)


async def reroll_daily_quest(db: AsyncSession, user: User, quest_id: uuid.UUID) -> DailyQuest:
    result = await db.execute(
        select(DailyQuest).where(
            and_(DailyQuest.id == quest_id, DailyQuest.user_id == user.id)
        )
    )
    old_quest = result.scalar_one_or_none()
    if not old_quest:
        return None
    if old_quest.is_rerolled:
        return None
        
    character = await _get_character(db, user.id)
    level = character.level if character else 1
    
    today = date.today()
    existing_quests_result = await db.execute(
        select(DailyQuest).where(
            and_(DailyQuest.user_id == user.id, DailyQuest.quest_date == today)
        )
    )
    active_titles = {q.title_vi for q in existing_quests_result.scalars().all()}
    
    templates_pool = await _get_quest_templates(db)
    all_categories = list(templates_pool.keys())
    other_categories = [c for c in all_categories if c != old_quest.category]
    if not other_categories:
        other_categories = all_categories
        
    available_templates = []
    
    # Try different categories
    for cat in other_categories:
        for t in templates_pool.get(cat, []):
            if t["title_vi"].strip() not in active_titles:
                available_templates.append(t)
                
    # Fallback to old category
    if not available_templates:
        for t in templates_pool.get(old_quest.category, []):
            if t["title_vi"].strip() not in active_titles:
                available_templates.append(t)
                    
    if not available_templates:
        for cat in all_categories:
            available_templates.extend(templates_pool.get(cat, []))
            
    template = random.choice(available_templates)
    
    q = _build_quest_from_template(template, old_quest.difficulty, level, old_quest.quest_type)
    
    streaks = await _get_streaks(db, user.id)
    overall_streak = _get_overall_streak(streaks)
    
    # Update stats scalar
    stat_rewards = q.get("stat_rewards", {})
    scaled_stat_rewards = {}
    for stat_name, val in stat_rewards.items():
        base_gain = float(val)
        scaled_gain = calculate_stat_gain(base_gain, old_quest.difficulty, overall_streak, level)
        scaled_stat_rewards[stat_name] = max(1, int(round(scaled_gain)))
        
    old_quest.title_vi = q["title_vi"]
    old_quest.title_en = q["title_en"]
    old_quest.description_vi = q.get("desc_vi", "")
    old_quest.description_en = q.get("desc_en", "")
    old_quest.category = q["category"]
    old_quest.status = "pending"
    old_quest.completed_at = None
    old_quest.fail_reason = None
    old_quest.is_rerolled = True
    old_quest.stat_rewards = json.dumps(scaled_stat_rewards)
    
    # Re-calculate EXP dynamically
    exp = calculate_quest_exp(old_quest.difficulty, old_quest.quest_type, level, q.get("base_exp"))
    old_quest.exp_reward = exp
    
    await db.flush()
    return old_quest
