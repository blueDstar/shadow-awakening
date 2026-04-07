"""Auth Service - handles registration, login, token management."""
import uuid
import json
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from app.models import User, UserProfile, Character, StatCap, UserStat, Streak, UserSettings
from app.core.security import hash_password, verify_password, create_access_token
from app.services.quest_engine import CORE_STATS, EXTENDED_STATS, ALL_STATS

STREAK_TYPES = ["overall", "reading", "english", "fitness", "deep_work", "journal", "research"]


async def register_user(db: AsyncSession, username: str, email: str, password: str) -> dict:
    """Register a new user with default character, stats, streaks."""
    # Normalize
    username = username.strip().lower()
    email = email.strip().lower()
    
    # Check existing
    existing = await db.execute(select(User).where(or_(User.username == username, User.email == email)))
    if existing.scalar_one_or_none():
        raise ValueError("Username or Email already registered")
    
    # Create user
    user = User(
        id=uuid.uuid4(),
        username=username,
        email=email,
        password_hash=hash_password(password),
    )
    db.add(user)
    await db.flush()
    
    # Create profile
    profile = UserProfile(
        id=uuid.uuid4(),
        user_id=user.id,
    )
    db.add(profile)
    
    # Create character
    character = Character(
        id=uuid.uuid4(),
        user_id=user.id,
        name=username,
        title="Kẻ Thức Tỉnh",
        level=1,
        current_exp=0,
        total_exp=0,
    )
    db.add(character)
    await db.flush()
    
    # Create stat cap
    stat_cap = StatCap(
        id=uuid.uuid4(),
        character_id=character.id,
        current_cap=100,
        phase=1,
    )
    db.add(stat_cap)
    
    # Create initial stats
    for stat_name in ALL_STATS:
        stat = UserStat(
            id=uuid.uuid4(),
            character_id=character.id,
            stat_name=stat_name,
            current_value=0.0,
        )
        db.add(stat)
    
    # Create streaks
    for streak_type in STREAK_TYPES:
        streak = Streak(
            id=uuid.uuid4(),
            user_id=user.id,
            streak_type=streak_type,
            current_streak=0,
            best_streak=0,
        )
        db.add(streak)
    
    # Create settings
    settings = UserSettings(
        id=uuid.uuid4(),
        user_id=user.id,
        language="vi",
        timezone="Asia/Ho_Chi_Minh",
    )
    db.add(settings)
    
    await db.flush()
    
    # Generate token
    token = create_access_token({"sub": str(user.id)})
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": str(user.id),
    }


async def login_user(db: AsyncSession, identifier: str, password: str) -> dict:
    """Authenticate via username or email and return JWT token."""
    identifier = identifier.strip().lower()
    
    # Search by username OR email
    result = await db.execute(
        select(User).where(
            or_(
                User.username == identifier,
                User.email == identifier
            )
        )
    )
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(password, user.password_hash):
        raise ValueError("Invalid credentials")
    
    token = create_access_token({"sub": str(user.id)})
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": str(user.id),
    }


async def complete_onboarding(db: AsyncSession, user: User, data: dict) -> dict:
    """Complete user onboarding with profile and character data."""
    # Update profile
    result = await db.execute(select(UserProfile).where(UserProfile.user_id == user.id))
    profile = result.scalar_one_or_none()
    
    if profile:
        profile.long_term_goals = data.get("long_term_goals", "")
        profile.short_term_goals = data.get("short_term_goals", "")
        profile.development_areas = json.dumps(data.get("development_areas", []))
        profile.daily_free_time_minutes = str(data.get("daily_free_time_minutes", 120))
        profile.fitness_level = data.get("fitness_level", "beginner")
        profile.focus_capacity = data.get("focus_capacity", "moderate")
        profile.sleep_time = data.get("sleep_time", "23:00")
        profile.wake_time = data.get("wake_time", "07:00")
        profile.current_habits = json.dumps(data.get("current_habits", []))
        profile.exploration_interests = json.dumps(data.get("exploration_interests", []))
        profile.discipline_level = data.get("discipline_level", "moderate")
        profile.onboarding_completed = True
    
    # Update character name
    result = await db.execute(select(Character).where(Character.user_id == user.id))
    character = result.scalar_one_or_none()
    if character:
        character.name = data.get("character_name", user.username)
    
    # Update settings
    result = await db.execute(select(UserSettings).where(UserSettings.user_id == user.id))
    settings = result.scalar_one_or_none()
    if settings:
        settings.language = data.get("language", "vi")
        settings.timezone = data.get("timezone", "Asia/Ho_Chi_Minh")
    
    await db.flush()
    
    return {"status": "ok", "message": "Onboarding completed"}
