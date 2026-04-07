from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import date


class DashboardSummary(BaseModel):
    character_name: str
    title: str
    level: int
    current_exp: int
    exp_to_next_level: int
    aura: str
    stats: List[dict]
    stat_cap: int
    phase: int
    breakthrough_available: bool
    today_quests_total: int
    today_quests_completed: int
    today_quests_failed: int
    day_completed: bool
    overall_streak: int
    best_streak: int
    streaks: List[dict]
    reset_countdown_seconds: int
    quote_vi: str = ""
    quote_en: str = ""
