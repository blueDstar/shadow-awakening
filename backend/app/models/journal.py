import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, DateTime, Date, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base


class Reflection(Base):
    __tablename__ = "reflections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    reflection_date = Column(Date, nullable=False, default=date.today)
    content = Column(Text, default="")
    mood = Column(String(20), default="neutral")  # great/good/neutral/bad/terrible
    insights = Column(Text, default="")
    success_reasons = Column(Text, default="")
    fail_reasons = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="reflections")
