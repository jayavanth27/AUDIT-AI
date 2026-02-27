from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship

from . import Base


class ExtractedField(Base):
    """Field/value pairs parsed from a document."""

    __tablename__ = "extracted_fields"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    value = Column(String, nullable=True)
    raw = Column(JSON, nullable=True)

    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    document = relationship("Document", back_populates="extracted_fields")
