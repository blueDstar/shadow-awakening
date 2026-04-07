from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
import uuid


class UserRegister(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str


class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserProfileCreate(BaseModel):
    long_term_goals: str = ""
    short_term_goals: str = ""
    development_areas: List[str] = []
    daily_free_time_minutes: int = 120
    fitness_level: str = "beginner"
    focus_capacity: str = "moderate"
    sleep_time: str = "23:00"
    wake_time: str = "07:00"
    current_habits: List[str] = []
    exploration_interests: List[str] = []
    discipline_level: str = "moderate"


class UserProfileResponse(BaseModel):
    id: str
    long_term_goals: str
    short_term_goals: str
    development_areas: str
    daily_free_time_minutes: str
    fitness_level: str
    focus_capacity: str
    sleep_time: str
    wake_time: str
    current_habits: str
    exploration_interests: str
    discipline_level: str
    onboarding_completed: bool

    class Config:
        from_attributes = True


class OnboardingData(BaseModel):
    character_name: str
    long_term_goals: str = ""
    short_term_goals: str = ""
    development_areas: List[str] = []
    daily_free_time_minutes: int = 120
    fitness_level: str = "beginner"
    focus_capacity: str = "moderate"
    sleep_time: str = "23:00"
    wake_time: str = "07:00"
    current_habits: List[str] = []
    exploration_interests: List[str] = []
    discipline_level: str = "moderate"
    language: str = "vi"
    timezone: str = "Asia/Ho_Chi_Minh"
