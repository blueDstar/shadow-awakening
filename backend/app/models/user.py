import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    character = relationship("Character", back_populates="user", uselist=False, cascade="all, delete-orphan")
    daily_quests = relationship("DailyQuest", back_populates="user", cascade="all, delete-orphan")
    quest_history = relationship("QuestHistory", back_populates="user", cascade="all, delete-orphan")
    streaks = relationship("Streak", back_populates="user", cascade="all, delete-orphan")
    user_rewards = relationship("UserReward", back_populates="user", cascade="all, delete-orphan")
    user_skills = relationship("UserSkill", back_populates="user", cascade="all, delete-orphan")
    user_challenges = relationship("UserChallenge", back_populates="user", cascade="all, delete-orphan")
    reflections = relationship("Reflection", back_populates="user", cascade="all, delete-orphan")
    planner_blocks = relationship("PlannerBlock", back_populates="user", cascade="all, delete-orphan")
    settings = relationship("UserSettings", back_populates="user", uselist=False, cascade="all, delete-orphan")
    experience_logs = relationship("ExperienceLog", back_populates="user", cascade="all, delete-orphan")
    breakthrough_trials = relationship("BreakthroughTrial", back_populates="user", cascade="all, delete-orphan")


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True)
    long_term_goals = Column(String, default="")
    short_term_goals = Column(String, default="")
    development_areas = Column(String, default="[]")  # JSON string
    daily_free_time_minutes = Column(String(10), default="120")
    fitness_level = Column(String(20), default="beginner")
    focus_capacity = Column(String(20), default="moderate")
    sleep_time = Column(String(10), default="23:00")
    wake_time = Column(String(10), default="07:00")
    current_habits = Column(String, default="[]")  # JSON string
    exploration_interests = Column(String, default="[]")  # JSON string
    discipline_level = Column(String(20), default="moderate")
    onboarding_completed = Column(Boolean, default=False)

    user = relationship("User", back_populates="profile")

    __table_args__ = (
        {"extend_existing": True},
    )
