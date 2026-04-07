import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, Integer, DateTime, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base


class Streak(Base):
    __tablename__ = "streaks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    streak_type = Column(String(30), nullable=False)  # overall/reading/english/fitness/deep_work/journal/research
    current_streak = Column(Integer, default=0)
    best_streak = Column(Integer, default=0)
    last_active_date = Column(Date, nullable=True)
    started_at = Column(Date, default=date.today)

    user = relationship("User", back_populates="streaks")

    __table_args__ = (
        {"extend_existing": True},
    )


class StreakLog(Base):
    __tablename__ = "streak_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    streak_type = Column(String(30), nullable=False)
    log_date = Column(Date, nullable=False)
    streak_value = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
