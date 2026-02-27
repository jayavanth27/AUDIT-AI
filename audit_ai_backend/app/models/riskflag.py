from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship

from . import Base


class RiskFlag(Base):
    """A flag raised by the risk engine for a document."""

    __tablename__ = "risk_flags"

    id = Column(Integer, primary_key=True, index=True)
    rule = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    message = Column(String, nullable=False)
    details = Column(JSON, nullable=True)

    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    document = relationship("Document", back_populates="risk_flags")
