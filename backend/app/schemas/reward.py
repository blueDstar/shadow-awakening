from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class RewardResponse(BaseModel):
    id: str
    name_vi: str
    name_en: str
    reward_type: str
    description_vi: str
    description_en: str
    icon: str
    rarity: str
    unlocked_at: Optional[datetime] = None
    is_equipped: bool = False

    class Config:
        from_attributes = True


class SkillResponse(BaseModel):
    id: str
    name_vi: str
    name_en: str
    description_vi: str
    description_en: str
    icon: str
    unlocked: bool = False
    unlock_condition: str = "{}"

    class Config:
        from_attributes = True
