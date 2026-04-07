import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base


class Reward(Base):
    __tablename__ = "rewards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name_vi = Column(String(100), nullable=False)
    name_en = Column(String(100), nullable=False)
    reward_type = Column(String(30), nullable=False)  # badge/title/aura/theme/skill
    description_vi = Column(Text, default="")
    description_en = Column(Text, default="")
    unlock_condition = Column(Text, default="{}")  # JSON
    icon = Column(String(50), default="🏆")
    rarity = Column(String(20), default="common")  # common/rare/epic/legendary
    created_at = Column(DateTime, default=datetime.utcnow)


class UserReward(Base):
    __tablename__ = "user_rewards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    reward_id = Column(UUID(as_uuid=True), ForeignKey("rewards.id"), nullable=False)
    unlocked_at = Column(DateTime, default=datetime.utcnow)
    is_equipped = Column(Boolean, default=False)

    user = relationship("User", back_populates="user_rewards")
    reward = relationship("Reward")
