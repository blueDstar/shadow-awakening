from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import date, datetime


class QuestResponse(BaseModel):
    id: str
    title_vi: str
    title_en: str
    description_vi: str
    description_en: str
    quest_type: str
    category: str
    difficulty: int
    exp_reward: int
    stat_rewards: str
    status: str
    quest_date: date
    completed_at: Optional[datetime] = None
    fail_reason: Optional[str] = None

    class Config:
        from_attributes = True


class QuestCompleteRequest(BaseModel):
    quest_id: str


class QuestFailRequest(BaseModel):
    quest_id: str
    fail_reason: str = "forgot"  # forgot/overloaded/no_time/too_hard/skipped


class DailyQuestsResponse(BaseModel):
    quests: List[QuestResponse]
    total: int
    completed: int
    failed: int
    day_completed: bool
    quest_date: date
