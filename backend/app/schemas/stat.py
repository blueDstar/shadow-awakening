from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import datetime


class StatResponse(BaseModel):
    stat_name: str
    current_value: float
    cap: int = 100

    class Config:
        from_attributes = True


class AllStatsResponse(BaseModel):
    stats: List[StatResponse]
    current_cap: int
    phase: int
    breakthrough_available: bool


class StatCapResponse(BaseModel):
    current_cap: int
    phase: int
    breakthrough_available: bool
