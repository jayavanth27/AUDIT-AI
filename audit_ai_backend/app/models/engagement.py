from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from . import Base


class Engagement(Base):
    """Audit engagement/project owned by a user."""

    __tablename__ = "engagements"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="engagements")

    documents = relationship("Document", back_populates="engagement")
    working_papers = relationship("WorkingPaper", back_populates="engagement")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
