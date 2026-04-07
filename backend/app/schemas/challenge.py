from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ChallengeResponse(BaseModel):
    id: str
    name_vi: str
    name_en: str
    description_vi: str
    description_en: str
    challenge_type: str
    duration_days: int
    category: str
    status: Optional[str] = None
    days_completed: int = 0
    started_at: Optional[datetime] = None

    class Config:
        from_attributes = True
