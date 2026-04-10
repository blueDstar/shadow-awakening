from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime


class CharacterResponse(BaseModel):
    id: str
    name: str
    title: str
    level: int
    current_exp: int
    total_exp: int
    aura: str
    avatar_type: str
    exp_to_next_level: int = 0
    stats: List[dict] = []
    stat_cap: int = 100
    phase: int = 1
    avatar_url: Optional[str] = None
    cover_url: Optional[str] = None
    background_url: Optional[str] = None

    class Config:
        from_attributes = True


class CharacterUpdate(BaseModel):
    name: Optional[str] = None
    avatar_type: Optional[str] = None
    avatar_url: Optional[str] = None
    cover_url: Optional[str] = None
    background_url: Optional[str] = None
