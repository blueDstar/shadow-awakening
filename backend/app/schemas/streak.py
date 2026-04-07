from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import date, datetime


class StreakResponse(BaseModel):
    streak_type: str
    current_streak: int
    best_streak: int
    last_active_date: Optional[date] = None

    class Config:
        from_attributes = True


class AllStreaksResponse(BaseModel):
    streaks: List[StreakResponse]
