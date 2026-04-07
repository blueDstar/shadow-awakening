import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base


class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name_vi = Column(String(100), nullable=False)
    name_en = Column(String(100), nullable=False)
    description_vi = Column(Text, default="")
    description_en = Column(Text, default="")
    challenge_type = Column(String(30), nullable=False)  # weekly/monthly/chain/stat_based/milestone
    duration_days = Column(Integer, default=7)
    requirements = Column(Text, default="{}")  # JSON
    rewards = Column(Text, default="{}")  # JSON
    min_level = Column(Integer, default=1)
    category = Column(String(30), default="general")
    created_at = Column(DateTime, default=datetime.utcnow)


class UserChallenge(Base):
    __tablename__ = "user_challenges"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    challenge_id = Column(UUID(as_uuid=True), ForeignKey("challenges.id"), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow)
    progress = Column(Text, default="{}")  # JSON
    days_completed = Column(Integer, default=0)
    status = Column(String(20), default="active")  # active/completed/failed/paused
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="user_challenges")
    challenge = relationship("Challenge")
