import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base


class BreakthroughTrial(Base):
    __tablename__ = "breakthrough_trials"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    phase = Column(Integer, nullable=False)  # 1, 2, 3, ...
    from_cap = Column(Integer, nullable=False)  # 100, 200, 300, ...
    to_cap = Column(Integer, nullable=False)  # 200, 300, 400, ...
    requirements = Column(Text, default="{}")  # JSON
    status = Column(String(20), default="available")  # available/in_progress/completed
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="breakthrough_trials")


class ExperienceLog(Base):
    __tablename__ = "experience_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    source = Column(String(50), nullable=False)  # quest/challenge/breakthrough/bonus
    source_id = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="experience_logs")


class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True)
    language = Column(String(5), default="vi")
    timezone = Column(String(50), default="Asia/Ho_Chi_Minh")
    difficulty_preference = Column(String(20), default="moderate")
    notification_enabled = Column(Boolean, default=True)
    daily_reset_hour = Column(Integer, default=0)

    user = relationship("User", back_populates="settings")
