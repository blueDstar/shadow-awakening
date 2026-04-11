import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, BigInteger, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base


class Character(Base):
    __tablename__ = "characters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    title = Column(String(100), default="Kẻ Thức Tỉnh")
    level = Column(Integer, default=1)
    current_exp = Column(BigInteger, default=0)
    total_exp = Column(BigInteger, default=0)
    aura = Column(String(50), default="shadow_basic")
    avatar_type = Column(String(50), default="default")
    avatar_url = Column(String, nullable=True)
    cover_url = Column(String, nullable=True)
    background_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="character")
    stats = relationship("UserStat", back_populates="character", cascade="all, delete-orphan")
    stat_cap = relationship("StatCap", back_populates="character", uselist=False, cascade="all, delete-orphan")


class StatCap(Base):
    __tablename__ = "stat_caps"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    character_id = Column(UUID(as_uuid=True), ForeignKey("characters.id"), nullable=False, unique=True)
    current_cap = Column(Integer, default=100)
    phase = Column(Integer, default=0)
    breakthrough_available = Column(Boolean, default=False)

    character = relationship("Character", back_populates="stat_cap")


class UserStat(Base):
    __tablename__ = "user_stats"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    character_id = Column(UUID(as_uuid=True), ForeignKey("characters.id"), nullable=False)
    stat_name = Column(String(50), nullable=False)
    current_value = Column(Float, default=0.0)

    character = relationship("Character", back_populates="stats")

    __table_args__ = (
        {"extend_existing": True},
    )
