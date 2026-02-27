from pydantic import BaseModel
from typing import Optional


class EngagementCreate(BaseModel):
    """Payload for creating a new engagement."""

    name: str
    description: Optional[str] = None


class EngagementOut(BaseModel):
    """Representation of an engagement returned to the client."""

    id: int
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True
