from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, JSON
from sqlalchemy.orm import relationship

from . import Base


class Document(Base):
    """Represents an uploaded file associated with an engagement."""

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    s3_key = Column(String, nullable=False, unique=True)
    content_type = Column(String, nullable=False)
    metadata = Column(JSON, nullable=True)

    engagement_id = Column(Integer, ForeignKey("engagements.id"), nullable=False)
    engagement = relationship("Engagement", back_populates="documents")

    extracted_fields = relationship("ExtractedField", back_populates="document")
    risk_flags = relationship("RiskFlag", back_populates="document")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
