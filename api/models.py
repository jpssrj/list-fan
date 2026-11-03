from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from api.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    is_completed = Column(Boolean, default=False, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
