import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, Integer, DateTime, Date, ForeignKey, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base


class Quest(Base):
    """Quest templates - predefined quests that can be generated"""
    __tablename__ = "quests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title_vi = Column(String(255), nullable=False)
    title_en = Column(String(255), nullable=False)
    description_vi = Column(Text, default="")
    description_en = Column(Text, default="")
    quest_type = Column(String(30), nullable=False)  # main/side/habit/challenge/penalty/special/breakthrough
    category = Column(String(30), nullable=False)  # fitness/wisdom/discipline/focus/confidence/exploration
    difficulty_min_level = Column(Integer, default=1)
    difficulty_max_level = Column(Integer, default=100)
    exp_reward = Column(Integer, default=10)
    stat_rewards = Column(Text, default="{}")  # JSON: {"strength": 2, "discipline": 1}
    base_requirements = Column(Text, default="{}")  # JSON
    is_template = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class DailyQuest(Base):
    """Actual quests assigned to users each day"""
    __tablename__ = "daily_quests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    quest_template_id = Column(UUID(as_uuid=True), ForeignKey("quests.id"), nullable=True)
    quest_date = Column(Date, nullable=False, default=date.today)
    title_vi = Column(String(255), nullable=False)
    title_en = Column(String(255), nullable=False)
    description_vi = Column(Text, default="")
    description_en = Column(Text, default="")
    quest_type = Column(String(30), nullable=False)
    category = Column(String(30), nullable=False)
    difficulty = Column(Integer, default=1)
    exp_reward = Column(Integer, default=10)
    stat_rewards = Column(Text, default="{}")  # JSON
    status = Column(String(20), default="pending")  # pending/completed/failed/skipped
    completed_at = Column(DateTime, nullable=True)
    chain_parent_id = Column(UUID(as_uuid=True), ForeignKey("daily_quests.id"), nullable=True)
    fail_reason = Column(String(50), nullable=True)
    # is_rerolled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="daily_quests")
    quest_template = relationship("Quest")
    chain_parent = relationship("DailyQuest", remote_side="DailyQuest.id")


class QuestHistory(Base):
    """Daily summary of quest completion"""
    __tablename__ = "quest_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    quest_date = Column(Date, nullable=False)
    total_quests = Column(Integer, default=0)
    completed_quests = Column(Integer, default=0)
    failed_quests = Column(Integer, default=0)
    exp_earned = Column(Integer, default=0)
    stats_gained = Column(Text, default="{}")  # JSON
    day_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="quest_history")
