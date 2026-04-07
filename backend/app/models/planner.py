import uuid
from datetime import date
from sqlalchemy import Column, String, Date, ForeignKey, Boolean, Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base


class PlannerBlock(Base):
    __tablename__ = "planner_blocks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    block_date = Column(Date, nullable=False, default=date.today)
    start_time = Column(String(10), nullable=False)  # "08:00"
    end_time = Column(String(10), nullable=False)  # "09:30"
    activity = Column(String(255), nullable=False)
    category = Column(String(30), default="general")  # study/fitness/rest/work/explore
    completed = Column(Boolean, default=False)

    user = relationship("User", back_populates="planner_blocks")
