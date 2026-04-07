from pydantic import BaseModel
from typing import Optional
from datetime import date


class PlannerBlockCreate(BaseModel):
    block_date: date
    start_time: str
    end_time: str
    activity: str
    category: str = "general"


class PlannerBlockUpdate(BaseModel):
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    activity: Optional[str] = None
    category: Optional[str] = None
    completed: Optional[bool] = None


class PlannerBlockResponse(BaseModel):
    id: str
    block_date: date
    start_time: str
    end_time: str
    activity: str
    category: str
    completed: bool

    class Config:
        from_attributes = True
