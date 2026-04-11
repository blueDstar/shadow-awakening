import asyncio
import json
from uuid import UUID
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import delete

# Import models
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.core.config import settings
from app.models import BreakthroughRitual

RITUALS_DATA = [
  {
    "id": "d6d5cd7d-bc2e-4504-83ad-85ed25d1d2ee",
    "phase": 1,
    "title_vi": "Nghi thức Thức Tỉnh",
    "title_en": "Awakening Ritual",
    "aura_name": "blue_glow",
    "foundation_req": {"type": "streak", "target": 7},
    "mandatory_reqs": [{"type": "habit_count", "target": 10}, {"type": "confidence_count", "target": 1}, {"type": "reflection_count", "target": 1}],
    "optional_paths": [{"id": "opt1", "req": {"type": "wisdom_count", "target": 5}, "tag": "wisdom", "label_en": "Wisdom", "label_vi": "Trí Tuệ"}, {"id": "opt2", "req": {"type": "fitness_count", "target": 5}, "tag": "fitness", "label_en": "Fitness", "label_vi": "Thể Lực"}, {"id": "opt3", "req": {"type": "deep_work_hours", "target": 2}, "tag": "focus", "label_en": "Focus", "label_vi": "Tập Trung"}],
    "min_reflection_words": 300
  },
  {
    "id": "88e27a64-9226-4b4d-843d-85d08d24cd83",
    "phase": 2,
    "title_vi": "Phá Xiềng Trì Hoãn",
    "title_en": "Breaking Procrastination",
    "aura_name": "dark_fire",
    "foundation_req": {"type": "streak", "target": 7},
    "mandatory_reqs": [{"type": "deep_work_hours", "target": 7}, {"type": "delayed_tasks_resolved", "target": 3}, {"type": "early_wake_days", "target": 5}],
    "optional_paths": [{"id": "opt1", "req": {"type": "no_social_morning", "target": 5}, "tag": "discipline", "label_en": "Morning Discipline", "label_vi": "Kỷ Luật Sáng"}, {"id": "opt2", "req": {"type": "stamina_count", "target": 10}, "tag": "fitness", "label_en": "Endurance", "label_vi": "Bền Bỉ"}, {"id": "opt3", "req": {"type": "wisdom_count", "target": 5}, "tag": "wisdom", "label_en": "Clarity", "label_vi": "Sáng Suốt"}],
    "min_reflection_words": 300
  },
  {
    "id": "4bd0d005-75b3-49a2-924d-77ec8eefc2d6",
    "phase": 3,
    "title_vi": "Thử Lửa Can Đảm",
    "title_en": "Social Courage Trial",
    "aura_name": "golden_aura",
    "foundation_req": {"type": "streak", "target": 7},
    "mandatory_reqs": [{"type": "new_conversations", "target": 10}, {"type": "public_questions", "target": 3}, {"type": "direct_feedback_requests", "target": 2}],
    "optional_paths": [{"id": "opt1", "req": {"type": "coffee_invitation", "target": 1}, "tag": "social", "label_en": "Connection", "label_vi": "Kết Nối"}, {"id": "opt2", "req": {"type": "sincere_compliments", "target": 5}, "tag": "confidence", "label_en": "Influence", "label_vi": "Lan Tỏa"}, {"id": "opt3", "req": {"type": "group_discussion", "target": 1}, "tag": "wisdom", "label_en": "Leadership", "label_vi": "Dẫn Dắt"}],
    "min_reflection_words": 300
  },
  {
    "id": "29a74a85-cf93-4cb4-8c49-a105aa0e5f00",
    "phase": 4,
    "title_vi": "Bách Luyện Trí Tuệ",
    "title_en": "Wisdom Refinement",
    "aura_name": "purple_mystic",
    "foundation_req": {"type": "streak", "target": 7},
    "mandatory_reqs": [{"type": "book_completed", "target": 1}, {"type": "skill_module_completed", "target": 1}, {"type": "wisdom_focus_count", "target": 10}],
    "optional_paths": [{"id": "opt1", "req": {"type": "knowledge_note_500w", "target": 1}, "tag": "wisdom", "label_en": "Synthesis", "label_vi": "Tổng Hợp"}, {"id": "opt2", "req": {"type": "new_vocab_count", "target": 200}, "tag": "wisdom", "label_en": "Language", "label_vi": "Ngôn Ngữ"}, {"id": "opt3", "req": {"type": "productivity_system_setup", "target": 1}, "tag": "discipline", "label_en": "Application", "label_vi": "Ứng Dụng"}],
    "min_reflection_words": 500
  },
  {
    "id": "af0ee017-6f1f-46ae-97e6-4b2de75b95e3",
    "phase": 5,
    "title_vi": "Luyện Thân - Luyện Tâm",
    "title_en": "Body and Mind Tempering",
    "aura_name": "green_vitality",
    "foundation_req": {"type": "streak", "target": 7},
    "mandatory_reqs": [{"type": "workout_sessions", "target": 12}, {"type": "meditation_minutes", "target": 120}, {"type": "no_skip_workout_2d", "target": 1}],
    "optional_paths": [{"id": "opt1", "req": {"type": "pushups_daily_100", "target": 1}, "tag": "fitness", "label_en": "Strength", "label_vi": "Sức Mạnh"}, {"id": "opt2", "req": {"type": "walking_15km_week", "target": 1}, "tag": "fitness", "label_en": "Endurance", "label_vi": "Bền Bỉ"}, {"id": "opt3", "req": {"type": "squats_daily_300", "target": 1}, "tag": "fitness", "label_en": "Mobility", "label_vi": "Linh Hoạt"}],
    "min_reflection_words": 400
  },
  {
    "id": "99bea6ad-25c5-45be-9787-1efdced0be2d",
    "phase": 6,
    "title_vi": "Vực Sâu Tập Trung",
    "title_en": "Focus Abyss",
    "aura_name": "cyan_crystal",
    "foundation_req": {"type": "streak", "target": 10},
    "mandatory_reqs": [{"type": "deep_work_hours", "target": 20}, {"type": "hard_task_3d_duration", "target": 1}, {"type": "no_fail_focus_7d", "target": 1}],
    "optional_paths": [{"id": "opt1", "req": {"type": "distraction_report", "target": 1}, "tag": "wisdom", "label_en": "Analysis", "label_vi": "Phân Tích"}, {"id": "opt2", "req": {"type": "creative_sprint_10h", "target": 1}, "tag": "focus", "label_en": "Creative Sprint", "label_vi": "Sáng Tạo"}, {"id": "opt3", "req": {"type": "silence_challenge_2h", "target": 1}, "tag": "focus", "label_en": "Silence", "label_vi": "Trầm Tĩnh"}],
    "min_reflection_words": 500
  },
  {
    "id": "613dfcde-ab21-4ae9-a148-71bedcba287c",
    "phase": 7,
    "title_vi": "Vòng Tròn Ảnh Hưởng",
    "title_en": "Circle of Influence",
    "aura_name": "orange_flare",
    "foundation_req": {"type": "streak", "target": 10},
    "mandatory_reqs": [{"type": "group_learning_lead", "target": 1}, {"type": "help_others_count", "target": 3}, {"type": "goal_oriented_convos", "target": 5}],
    "optional_paths": [{"id": "opt1", "req": {"type": "positive_feedback_count", "target": 3}, "tag": "social", "label_en": "Feedback", "label_vi": "Phản Hồi"}, {"id": "opt2", "req": {"type": "public_resource_share", "target": 1}, "tag": "wisdom", "label_en": "Sharing", "label_vi": "Chia Sẻ"}, {"id": "opt3", "req": {"type": "one_on_one_mentoring", "target": 1}, "tag": "social", "label_en": "Deep Connection", "label_vi": "Kết Nối Sâu"}],
    "min_reflection_words": 400
  },
  {
    "id": "e03641cd-e1ab-4f85-a39a-6f445f7a24f9",
    "phase": 8,
    "title_vi": "Nghi thức Dẫn Đường",
    "title_en": "Pathfinder Ritual",
    "aura_name": "white_radiance",
    "foundation_req": {"type": "streak", "target": 14},
    "mandatory_reqs": [{"type": "mentoring_sessions", "target": 3}, {"type": "useful_resource_created", "target": 1}, {"type": "social_courage_challenge", "target": 1}],
    "optional_paths": [{"id": "opt1", "req": {"type": "useful_template_creation", "target": 1}, "tag": "wisdom", "label_en": "Template", "label_vi": "Template"}, {"id": "opt2", "req": {"type": "tutorial_video_short", "target": 1}, "tag": "wisdom", "label_en": "Tutorial", "label_vi": "Hướng Dẫn"}, {"id": "opt3", "req": {"type": "comprehensive_checklist", "target": 1}, "tag": "wisdom", "label_en": "Checklist", "label_vi": "Văn Bản"}],
    "min_reflection_words": 500
  },
  {
    "id": "c6e4e8f6-739a-4dab-b634-18d5860e3284",
    "phase": 9,
    "title_vi": "Kiến Trúc Sư Kỷ Luật",
    "title_en": "Discipline Architect",
    "aura_name": "red_obsidian",
    "foundation_req": {"type": "streak", "target": 21},
    "mandatory_reqs": [{"type": "self_system_design_30d", "target": 1}, {"type": "weekly_review_streak", "target": 4}, {"type": "core_habit_no_fail_21d", "target": 1}],
    "optional_paths": [{"id": "opt1", "req": {"type": "progress_in_4_groups", "target": 1}, "tag": "discipline", "label_en": "Holistic", "label_vi": "Toàn Diện"}, {"id": "opt2", "req": {"type": "deep_work_30h_month", "target": 1}, "tag": "focus", "label_en": "Challenge", "label_vi": "Thử Thách"}, {"id": "opt3", "req": {"type": "bad_habit_elimination", "target": 1}, "tag": "discipline", "label_en": "Minimalism", "label_vi": "Tối Giản"}],
    "min_reflection_words": 500
  },
  {
    "id": "fa18cbf8-74ae-4c34-b6c3-4aed9c788cb1",
    "phase": 10,
    "title_vi": "Lãnh Đạo Bản Thân",
    "title_en": "Self Leadership",
    "aura_name": "silver_knight",
    "foundation_req": {"type": "streak", "target": 30},
    "mandatory_reqs": [{"type": "deep_work_hours", "target": 30}, {"type": "major_goal_completed", "target": 1}, {"type": "public_presentation", "target": 1}],
    "optional_paths": [{"id": "opt1", "req": {"type": "major_bad_habit_cut", "target": 1}, "tag": "discipline", "label_en": "Renunciation", "label_vi": "Từ Bỏ"}, {"id": "opt2", "req": {"type": "lead_public_project", "target": 1}, "tag": "confidence", "label_en": "Pioneer", "label_vi": "Tiên Phong"}, {"id": "opt3", "req": {"type": "personal_philosophy_essay", "target": 1}, "tag": "wisdom", "label_en": "Wisdom", "label_vi": "Trí Tuệ"}],
    "min_reflection_words": 600
  },
  {
    "id": "5f98f6c3-cc7b-45b0-bfc2-6af386ad4160",
    "phase": 11,
    "title_vi": "Hành Trình Quân Vương",
    "title_en": "Sovereign Path",
    "aura_name": "rainbow_divine",
    "foundation_req": {"type": "streak", "target": 45},
    "mandatory_reqs": [{"type": "major_knowledge_achievements", "target": 2}, {"type": "physical_milestone_major", "target": 1}, {"type": "valuable_public_contribution", "target": 1}],
    "optional_paths": [{"id": "opt1", "req": {"type": "deep_reflection_5_essays", "target": 1}, "tag": "focus", "label_en": "Inner Depth", "label_vi": "Nội Tâm"}, {"id": "opt2", "req": {"type": "study_2_books_and_project", "target": 1}, "tag": "wisdom", "label_en": "Scholarship", "label_vi": "Trí Tuệ"}, {"id": "opt3", "req": {"type": "community_support_action", "target": 1}, "tag": "social", "label_en": "Contribution", "label_vi": "Cống Hiến"}],
    "min_reflection_words": 800
  },
  {
    "id": "d64d1109-ee7a-43c1-b170-bd0b182103fc",
    "phase": 12,
    "title_vi": "Nghi thức Siêu Việt",
    "title_en": "Transcendence Ritual",
    "aura_name": "cosmic_void",
    "foundation_req": {"type": "streak", "target": 60},
    "mandatory_reqs": [{"type": "deep_work_hours", "target": 50}, {"type": "personal_project_result", "target": 1}, {"type": "clear_social_impact", "target": 1}],
    "optional_paths": [{"id": "opt1", "req": {"type": "teach_group_community", "target": 1}, "tag": "social", "label_en": "Ignite Others", "label_vi": "Truyền Lửa"}, {"id": "opt2", "req": {"type": "self_dev_manifesto_v2", "target": 1}, "tag": "wisdom", "label_en": "Manifesto", "label_vi": "Tuyên Ngôn"}, {"id": "opt3", "req": {"type": "no_system_failure_60d", "target": 1}, "tag": "discipline", "label_en": "Unbroken System", "label_vi": "Vô Biến"}],
    "min_reflection_words": 1000
  }
]

async def seed():
    from app.db.database import init_db
    await init_db()
    engine = create_async_engine(settings.DATABASE_URL)
    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with AsyncSessionLocal() as db:
        # Clear existing rituals to avoid conflicts
        await db.execute(delete(BreakthroughRitual))
        
        for ritual_data in RITUALS_DATA:
            ritual = BreakthroughRitual(
                id=UUID(ritual_data["id"]),
                phase=ritual_data["phase"],
                title_vi=ritual_data["title_vi"],
                title_en=ritual_data["title_en"],
                aura_name=ritual_data["aura_name"],
                foundation_req=json.dumps(ritual_data["foundation_req"]),
                mandatory_reqs=json.dumps(ritual_data["mandatory_reqs"]),
                optional_paths=json.dumps(ritual_data["optional_paths"]),
                min_reflection_words=ritual_data["min_reflection_words"]
            )
            db.add(ritual)
        
        await db.commit()
        print(f"Successfully seeded {len(RITUALS_DATA)} rituals.")

if __name__ == "__main__":
    asyncio.run(seed())
