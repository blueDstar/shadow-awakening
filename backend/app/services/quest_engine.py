"""
Quest Engine - Core quest generation system
Generates daily quests based on user profile, stats, streaks, and history.
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
    DailyQuest, QuestHistory, Streak, UserChallenge
)
from app.utils.exp_calculator import calculate_quest_exp, calculate_stat_gain
from app.utils.difficulty_scaler import (
    calculate_base_difficulty,
    apply_dynamic_adjustment,
    scale_quest_requirements,
)

# ============================================================
# QUEST TEMPLATES - organized by category
# ============================================================

QUEST_TEMPLATES = {
    "fitness": [
        {
            "title_vi": "Chống đẩy {n} cái",
            "title_en": "Do {n} push-ups",
            "desc_vi": "Hoàn thành {n} cái chống đẩy. Có thể chia thành nhiều set.",
            "desc_en": "Complete {n} push-ups. You can split into multiple sets.",
            "category": "fitness",
            "stat_rewards": {"strength": 2, "discipline": 1},
            "base_n": 10, "param": "n",
        },
        {
            "title_vi": "Squat {n} cái",
            "title_en": "Do {n} squats",
            "desc_vi": "Thực hiện {n} squat với tư thế đúng.",
            "desc_en": "Perform {n} squats with proper form.",
            "category": "fitness",
            "stat_rewards": {"strength": 2, "stamina": 1},
            "base_n": 15, "param": "n",
        },
        {
            "title_vi": "Plank {n} giây",
            "title_en": "Plank for {n} seconds",
            "desc_vi": "Giữ plank trong {n} giây. Tập trung vào core.",
            "desc_en": "Hold plank for {n} seconds. Focus on your core.",
            "category": "fitness",
            "stat_rewards": {"strength": 1, "discipline": 2, "stamina": 1},
            "base_n": 30, "param": "n",
        },
        {
            "title_vi": "Đi bộ nhanh {n} phút",
            "title_en": "Brisk walk for {n} minutes",
            "desc_vi": "Đi bộ nhanh ngoài trời hoặc trong nhà trong {n} phút.",
            "desc_en": "Take a brisk walk outdoors or indoors for {n} minutes.",
            "category": "fitness",
            "stat_rewards": {"stamina": 2, "discipline": 1},
            "base_n": 15, "param": "n",
        },
        {
            "title_vi": "Giãn cơ toàn thân {n} phút",
            "title_en": "Full body stretch for {n} minutes",
            "desc_vi": "Thực hiện các bài giãn cơ toàn thân trong {n} phút.",
            "desc_en": "Perform full body stretching exercises for {n} minutes.",
            "category": "fitness",
            "stat_rewards": {"stamina": 1, "strength": 1},
            "base_n": 10, "param": "n",
        },
    ],
    "wisdom": [
        {
            "title_vi": "Đọc {n} trang sách",
            "title_en": "Read {n} pages",
            "desc_vi": "Đọc {n} trang từ sách bạn đang đọc. Ghi chú 1-2 insight.",
            "desc_en": "Read {n} pages from your current book. Note 1-2 insights.",
            "category": "wisdom",
            "stat_rewards": {"wisdom": 2, "focus": 1},
            "base_n": 10, "param": "n",
        },
        {
            "title_vi": "Học {n} từ tiếng Anh mới",
            "title_en": "Learn {n} new English words",
            "desc_vi": "Học {n} từ vựng mới và viết ít nhất 2 câu ví dụ.",
            "desc_en": "Learn {n} new vocabulary words and write at least 2 example sentences.",
            "category": "wisdom",
            "stat_rewards": {"wisdom": 1, "confidence": 1, "knowledge": 1},
            "base_n": 10, "param": "n",
        },
        {
            "title_vi": "Ôn {n} từ tiếng Anh cũ",
            "title_en": "Review {n} old English words",
            "desc_vi": "Ôn lại {n} từ đã học và kiểm tra bản thân.",
            "desc_en": "Review {n} previously learned words and test yourself.",
            "category": "wisdom",
            "stat_rewards": {"wisdom": 1, "consistency": 1},
            "base_n": 15, "param": "n",
        },
        {
            "title_vi": "Đọc 1 bài nghiên cứu và ghi {n} insight",
            "title_en": "Read 1 research article and note {n} insights",
            "desc_vi": "Tìm và đọc 1 bài nghiên cứu khoa học. Ghi lại {n} insight quan trọng.",
            "desc_en": "Find and read 1 scientific article. Note {n} key insights.",
            "category": "wisdom",
            "stat_rewards": {"wisdom": 3, "knowledge": 2, "focus": 1},
            "base_n": 3, "param": "n",
        },
        {
            "title_vi": "Tìm hiểu 1 học bổng và ghi {n} ý chính",
            "title_en": "Research 1 scholarship and note {n} key points",
            "desc_vi": "Tìm hiểu chi tiết 1 chương trình học bổng. Ghi lại {n} ý quan trọng.",
            "desc_en": "Research 1 scholarship program in detail. Note {n} important points.",
            "category": "wisdom",
            "stat_rewards": {"wisdom": 2, "confidence": 1},
            "base_n": 3, "param": "n",
        },
    ],
    "discipline": [
        {
            "title_vi": "Dọn bàn học trong {n} phút",
            "title_en": "Clean study desk for {n} minutes",
            "desc_vi": "Dọn dẹp và sắp xếp lại không gian học tập trong {n} phút.",
            "desc_en": "Clean and organize your study space for {n} minutes.",
            "category": "discipline",
            "stat_rewards": {"discipline": 2},
            "base_n": 10, "param": "n",
        },
        {
            "title_vi": "Lên kế hoạch ngày mai chi tiết",
            "title_en": "Plan tomorrow in detail",
            "desc_vi": "Viết kế hoạch chi tiết cho ngày mai bao gồm time blocks.",
            "desc_en": "Write a detailed plan for tomorrow including time blocks.",
            "category": "discipline",
            "stat_rewards": {"discipline": 2, "focus": 1},
            "base_n": 0, "param": None,
        },
        {
            "title_vi": "Giới hạn mạng xã hội dưới {n} phút hôm nay",
            "title_en": "Limit social media to under {n} minutes today",
            "desc_vi": "Kiểm soát thời gian dùng mạng xã hội dưới {n} phút.",
            "desc_en": "Keep social media usage under {n} minutes.",
            "category": "discipline",
            "stat_rewards": {"discipline": 2, "focus": 1, "mental_resilience": 1},
            "base_n": 30, "param": "n",
        },
        {
            "title_vi": "Ngủ trước {time}",
            "title_en": "Sleep before {time}",
            "desc_vi": "Đi ngủ trước {time} để duy trì thói quen tốt.",
            "desc_en": "Go to bed before {time} to maintain a good routine.",
            "category": "discipline",
            "stat_rewards": {"discipline": 2, "stamina": 1},
            "base_n": 0, "param": "time",
        },
    ],
    "focus": [
        {
            "title_vi": "Deep work {n} Pomodoro ({m} phút)",
            "title_en": "Deep work {n} Pomodoro ({m} minutes)",
            "desc_vi": "Làm việc tập trung sâu {n} session Pomodoro, mỗi session {m} phút.",
            "desc_en": "Complete {n} deep work Pomodoro sessions, {m} minutes each.",
            "category": "focus",
            "stat_rewards": {"focus": 3, "discipline": 1},
            "base_n": 2, "param": "n",
        },
        {
            "title_vi": "Viết reflection {n} dòng",
            "title_en": "Write {n} lines of reflection",
            "desc_vi": "Viết ít nhất {n} dòng về những gì bạn đã học và cảm nhận hôm nay.",
            "desc_en": "Write at least {n} lines about what you learned and felt today.",
            "category": "focus",
            "stat_rewards": {"focus": 1, "discipline": 1, "mental_resilience": 1},
            "base_n": 5, "param": "n",
        },
        {
            "title_vi": "Thiền {n} phút",
            "title_en": "Meditate for {n} minutes",
            "desc_vi": "Thiền định trong {n} phút. Tập trung vào hơi thở.",
            "desc_en": "Meditate for {n} minutes. Focus on your breathing.",
            "category": "focus",
            "stat_rewards": {"focus": 2, "mental_resilience": 2},
            "base_n": 5, "param": "n",
        },
    ],
    "confidence": [
        {
            "title_vi": "Nói chuyện với {n} người mới",
            "title_en": "Talk to {n} new people",
            "desc_vi": "Bắt chuyện hoặc tương tác với {n} người mà bạn chưa quen.",
            "desc_en": "Start a conversation or interact with {n} people you don't know well.",
            "category": "confidence",
            "stat_rewards": {"confidence": 3, "social_courage": 2},
            "base_n": 1, "param": "n",
        },
        {
            "title_vi": "Trình bày ý kiến trước nhóm",
            "title_en": "Share your opinion in a group",
            "desc_vi": "Chia sẻ ý kiến cá nhân trong 1 nhóm hoặc cuộc họp.",
            "desc_en": "Share your personal opinion in a group or meeting.",
            "category": "confidence",
            "stat_rewards": {"confidence": 2, "social_courage": 2},
            "base_n": 0, "param": None,
        },
    ],
    "exploration": [
        {
            "title_vi": "Tìm hiểu 1 chủ đề mới: {topic}",
            "title_en": "Explore a new topic: {topic}",
            "desc_vi": "Dành {n} phút tìm hiểu về {topic}. Ghi lại 3 điều thú vị.",
            "desc_en": "Spend {n} minutes learning about {topic}. Note 3 interesting facts.",
            "category": "exploration",
            "stat_rewards": {"knowledge": 2, "wisdom": 1},
            "base_n": 20, "param": "n",
        },
    ],
}

EXPLORATION_TOPICS = [
    "tâm lý học", "triết học", "khoa học thần kinh", "vật lý thiên văn",
    "sinh học tiến hóa", "trí tuệ nhân tạo", "lịch sử cổ đại",
    "kinh tế học hành vi", "công nghệ blockchain", "thiết kế UX",
    "marketing số", "dinh dưỡng học", "ngôn ngữ học",
    "khoa học khí hậu", "robotics", "nhiếp ảnh",
]

PENALTY_TEMPLATES = [
    {
        "title_vi": "Phạt: Squat {n} cái",
        "title_en": "Penalty: {n} squats",
        "desc_vi": "Bạn chưa hoàn thành nhiệm vụ hôm qua. Hoàn thành {n} squat để chuộc lỗi.",
        "desc_en": "You didn't complete yesterday's quests. Do {n} squats as penalty.",
        "category": "fitness",
        "stat_rewards": {"strength": 1, "discipline": 2},
        "base_n": 15, "param": "n", "severity": "light",
    },
    {
        "title_vi": "Phạt: Plank {n} giây",
        "title_en": "Penalty: Plank {n} seconds",
        "desc_vi": "Giữ plank trong {n} giây để rèn luyện kỷ luật.",
        "desc_en": "Hold plank for {n} seconds to build discipline.",
        "category": "fitness",
        "stat_rewards": {"strength": 1, "discipline": 2},
        "base_n": 45, "param": "n", "severity": "light",
    },
    {
        "title_vi": "Phạt: Viết {n} dòng reflection vì sao thất bại",
        "title_en": "Penalty: Write {n} lines about why you failed",
        "desc_vi": "Viết ít nhất {n} dòng phân tích lý do thất bại và bài học rút ra.",
        "desc_en": "Write at least {n} lines analyzing your failure reasons and lessons learned.",
        "category": "discipline",
        "stat_rewards": {"discipline": 2, "mental_resilience": 1},
        "base_n": 5, "param": "n", "severity": "moderate",
    },
    {
        "title_vi": "Phạt: Block tập trung {n} phút không điện thoại",
        "title_en": "Penalty: {n} minutes focus block without phone",
        "desc_vi": "Tắt điện thoại hoặc để chế độ máy bay trong {n} phút và làm việc.",
        "desc_en": "Turn off phone or airplane mode for {n} minutes and focus on work.",
        "category": "focus",
        "stat_rewards": {"focus": 2, "discipline": 2},
        "base_n": 30, "param": "n", "severity": "moderate",
    },
    {
        "title_vi": "Phạt: Đi bộ nhanh {n} phút",
        "title_en": "Penalty: Brisk walk for {n} minutes",
        "desc_vi": "Đi bộ nhanh {n} phút để lấy lại năng lượng và kỷ luật.",
        "desc_en": "Take a {n}-minute brisk walk to regain energy and discipline.",
        "category": "fitness",
        "stat_rewards": {"stamina": 1, "discipline": 2},
        "base_n": 15, "param": "n", "severity": "light",
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


async def generate_daily_quests(db: AsyncSession, user: User) -> List[DailyQuest]:
    """Main quest generation function. Creates daily quests for a user."""
    today = date.today()
    
    # Check if quests already generated for today
    existing = await db.execute(
        select(DailyQuest).where(
            and_(DailyQuest.user_id == user.id, DailyQuest.quest_date == today)
        )
    )
    existing_quests = existing.scalars().all()
    if existing_quests:
        return existing_quests
    
    # Gather user data
    character = await _get_character(db, user.id)
    stats = await _get_stats(db, character.id if character else None)
    stat_cap = await _get_stat_cap(db, character.id if character else None)
    streaks = await _get_streaks(db, user.id)
    yesterday_quests = await _get_yesterday_quests(db, user.id)
    profile = await _get_profile(db, user.id)
    
    level = character.level if character else 1
    overall_streak = _get_overall_streak(streaks)
    
    # Calculate difficulty
    base_diff = calculate_base_difficulty(level, overall_streak)
    fails, successes = await _get_recent_performance(db, user.id)
    completion_rate = await _get_7d_completion_rate(db, user.id)
    difficulty = apply_dynamic_adjustment(base_diff, fails, successes, completion_rate)
    
    # Identify weak stats
    weak_stats = _find_weak_stats(stats, stat_cap.current_cap if stat_cap else 100)
    strong_stats = _find_strong_stats(stats, stat_cap.current_cap if stat_cap else 100)
    
    quests = []
    
    # 1. Main Quests (2-3)
    quests.extend(_generate_main_quests(weak_stats, difficulty, level, profile, 2))
    
    # 2. Side Quests (1-2)
    quests.extend(_generate_side_quests(stats, difficulty, level, profile, 1))
    
    # 3. Habit Quests (2-3)
    quests.extend(_generate_habit_quests(difficulty, level, profile, 2))
    
    # 4. Penalty Quests if yesterday had failures
    failed_yesterday = [q for q in yesterday_quests if q.status == "failed"]
    if failed_yesterday:
        quests.extend(_generate_penalty_quests(len(failed_yesterday), difficulty, level, profile))
    
    # 5. Apply chain continuity from yesterday
    quests = _apply_chain_continuity(quests, yesterday_quests, difficulty, level)
    
    # 6. Limit total quests (5-8 based on level)
    max_quests = min(5 + level // 5, 10)
    quests = quests[:max_quests]
    
    # 7. Save to database
    daily_quests = []
    for q in quests:
        exp = calculate_quest_exp(difficulty, q["quest_type"], level)
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
            stat_rewards=json.dumps(q.get("stat_rewards", {})),
            status="pending",
        )
        db.add(dq)
        daily_quests.append(dq)
    
    await db.flush()
    return daily_quests


def _generate_main_quests(
    weak_stats: List[str], difficulty: int, level: int, profile, count: int
) -> List[dict]:
    """Generate main quests targeting weak stats."""
    quests = []
    categories_used = set()
    
    for stat_name in weak_stats[:count]:
        cat = _stat_to_category(stat_name)
        if cat in categories_used:
            continue
        templates = QUEST_TEMPLATES.get(cat, [])
        if not templates:
            continue
        
        template = random.choice(templates)
        quest = _build_quest_from_template(template, difficulty, level, "main")
        quests.append(quest)
        categories_used.add(cat)
    
    # Fill remaining with random categories
    while len(quests) < count:
        cat = random.choice(list(QUEST_TEMPLATES.keys()))
        if cat not in categories_used:
            templates = QUEST_TEMPLATES[cat]
            template = random.choice(templates)
            quest = _build_quest_from_template(template, difficulty, level, "main")
            quests.append(quest)
            categories_used.add(cat)
    
    return quests[:count]


def _generate_side_quests(
    stats: dict, difficulty: int, level: int, profile, count: int
) -> List[dict]:
    """Generate side quests for balanced development."""
    quests = []
    cats = list(QUEST_TEMPLATES.keys())
    random.shuffle(cats)
    
    for cat in cats[:count]:
        templates = QUEST_TEMPLATES[cat]
        template = random.choice(templates)
        quest = _build_quest_from_template(template, difficulty, level, "side")
        quests.append(quest)
    
    return quests[:count]


def _generate_habit_quests(
    difficulty: int, level: int, profile, count: int
) -> List[dict]:
    """Generate habit quests for daily routines."""
    habit_templates = [
        {
            "title_vi": "Uống đủ {n} ly nước hôm nay",
            "title_en": "Drink {n} glasses of water today",
            "desc_vi": "Uống ít nhất {n} ly nước trong ngày để duy trì sức khỏe.",
            "desc_en": "Drink at least {n} glasses of water to stay healthy.",
            "category": "fitness",
            "stat_rewards": {"stamina": 1},
            "base_n": 8, "param": "n",
        },
        {
            "title_vi": "Không dùng điện thoại 30 phút đầu tiên sau khi thức",
            "title_en": "No phone for 30 minutes after waking up",
            "desc_vi": "Tránh sử dụng điện thoại trong 30 phút đầu tiên để bắt đầu ngày tỉnh táo.",
            "desc_en": "Avoid using your phone for 30 minutes after waking to start your day clear.",
            "category": "discipline",
            "stat_rewards": {"discipline": 1, "focus": 1},
            "base_n": 0, "param": None,
        },
        {
            "title_vi": "Ghi lại 3 điều biết ơn hôm nay",
            "title_en": "Write 3 things you're grateful for today",
            "desc_vi": "Viết ra 3 điều bạn cảm thấy biết ơn ngày hôm nay.",
            "desc_en": "Write down 3 things you feel grateful for today.",
            "category": "focus",
            "stat_rewards": {"mental_resilience": 1},
            "base_n": 0, "param": None,
        },
    ]
    
    random.shuffle(habit_templates)
    quests = []
    for template in habit_templates[:count]:
        quest = _build_quest_from_template(template, difficulty, level, "habit")
        quests.append(quest)
    
    return quests[:count]


def _generate_penalty_quests(
    fail_count: int, difficulty: int, level: int, profile
) -> List[dict]:
    """Generate penalty quests based on yesterday's failures."""
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
    """Build a concrete quest from a template."""
    quest = {
        "quest_type": quest_type,
        "category": template["category"],
        "stat_rewards": template.get("stat_rewards", {}),
    }
    
    base_n = template.get("base_n", 0)
    param = template.get("param")
    
    if param == "n" and base_n > 0:
        n = scale_quest_requirements(base_n, difficulty, level)
        quest["title_vi"] = template["title_vi"].replace("{n}", str(n))
        quest["title_en"] = template["title_en"].replace("{n}", str(n))
        quest["desc_vi"] = template.get("desc_vi", "").replace("{n}", str(n))
        quest["desc_en"] = template.get("desc_en", "").replace("{n}", str(n))
    elif param == "time":
        quest["title_vi"] = template["title_vi"].replace("{time}", "23:00")
        quest["title_en"] = template["title_en"].replace("{time}", "23:00")
        quest["desc_vi"] = template.get("desc_vi", "").replace("{time}", "23:00")
        quest["desc_en"] = template.get("desc_en", "").replace("{time}", "23:00")
    else:
        quest["title_vi"] = template["title_vi"]
        quest["title_en"] = template["title_en"]
        quest["desc_vi"] = template.get("desc_vi", "")
        quest["desc_en"] = template.get("desc_en", "")
    
    # Handle exploration topics
    if "{topic}" in quest.get("title_vi", ""):
        topic = random.choice(EXPLORATION_TOPICS)
        quest["title_vi"] = quest["title_vi"].replace("{topic}", topic)
        quest["title_en"] = quest["title_en"].replace("{topic}", topic)
        quest["desc_vi"] = quest["desc_vi"].replace("{topic}", topic)
        quest["desc_en"] = quest["desc_en"].replace("{topic}", topic)
    
    # Handle Pomodoro
    if "{m}" in quest.get("title_vi", ""):
        m = 25
        quest["title_vi"] = quest["title_vi"].replace("{m}", str(m))
        quest["title_en"] = quest["title_en"].replace("{m}", str(m))
        quest["desc_vi"] = quest["desc_vi"].replace("{m}", str(m))
        quest["desc_en"] = quest["desc_en"].replace("{m}", str(m))
    
    return quest


def _apply_chain_continuity(
    quests: List[dict], yesterday_quests: List, difficulty: int, level: int
) -> List[dict]:
    """Apply quest chain continuity from yesterday's completed quests."""
    if not yesterday_quests:
        return quests
    
    completed_categories = set()
    for yq in yesterday_quests:
        if yq.status == "completed":
            completed_categories.add(yq.category)
    
    # Ensure at least one quest continues from yesterday's categories
    current_categories = {q["category"] for q in quests}
    for cat in completed_categories:
        if cat not in current_categories and cat in QUEST_TEMPLATES:
            templates = QUEST_TEMPLATES[cat]
            template = random.choice(templates)
            quest = _build_quest_from_template(template, difficulty, level, "side")
            quests.append(quest)
            break
    
    return quests


def _stat_to_category(stat_name: str) -> str:
    """Map stat name to quest category."""
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
    """Find stats below 40% of cap."""
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
    """Find stats above 80% of cap."""
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


async def _get_yesterday_quests(db: AsyncSession, user_id) -> List[DailyQuest]:
    yesterday = date.today() - timedelta(days=1)
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
    """Get consecutive fails and successes."""
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


async def _get_7d_completion_rate(db: AsyncSession, user_id) -> float:
    """Get 7-day quest completion rate."""
    week_ago = date.today() - timedelta(days=7)
    result = await db.execute(
        select(QuestHistory)
        .where(and_(QuestHistory.user_id == user_id, QuestHistory.quest_date >= week_ago))
    )
    histories = result.scalars().all()
    
    if not histories:
        return 0.5  # Default to moderate
    
    total = sum(h.total_quests for h in histories)
    completed = sum(h.completed_quests for h in histories)
    
    return completed / total if total > 0 else 0.5


def get_daily_quote() -> dict:
    """Get a random daily motivational quote."""
    return random.choice(DAILY_QUOTES)
