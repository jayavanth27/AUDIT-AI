from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from . import Base


class User(Base):
    """Represents a registered user of the system."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    engagements = relationship("Engagement", back_populates="owner")
