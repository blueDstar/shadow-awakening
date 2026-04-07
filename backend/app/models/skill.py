import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base


class Skill(Base):
    __tablename__ = "skills"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name_vi = Column(String(100), nullable=False)
    name_en = Column(String(100), nullable=False)
    description_vi = Column(Text, default="")
    description_en = Column(Text, default="")
    unlock_condition = Column(Text, default="{}")  # JSON: {level: 10, streak: 7, stat: {focus: 50}}
    icon = Column(String(50), default="⚡")
    effect = Column(Text, default="{}")  # JSON
    created_at = Column(DateTime, default=datetime.utcnow)


class UserSkill(Base):
    __tablename__ = "user_skills"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skills.id"), nullable=False)
    unlocked_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="user_skills")
    skill = relationship("Skill")
