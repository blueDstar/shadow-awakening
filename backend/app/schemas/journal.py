from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class ReflectionCreate(BaseModel):
    content: str
    mood: str = "neutral"
    insights: str = ""
    success_reasons: str = ""
    fail_reasons: str = ""


class ReflectionResponse(BaseModel):
    id: str
    reflection_date: date
    content: str
    mood: str
    insights: str
    success_reasons: str
    fail_reasons: str
    created_at: datetime

    class Config:
        from_attributes = True
