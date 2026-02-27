"""Routes for managing audit engagements."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.schemas.engagement import EngagementCreate, EngagementOut
from app.models.engagement import Engagement
from app.core.security import get_current_user
from app.database import get_db
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=EngagementOut)
async def create_engagement(
    data: EngagementCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new engagement owned by the current user."""
    eng = Engagement(name=data.name, description=data.description, owner_id=current_user.id)
    db.add(eng)
    await db.commit()
    await db.refresh(eng)
    return eng


@router.get("/", response_model=list[EngagementOut])
async def list_engagements(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return all engagements belonging to the authenticated user."""
    result = await db.execute(select(Engagement).where(Engagement.owner_id == current_user.id))
    return result.scalars().all()


@router.get("/{engagement_id}", response_model=EngagementOut)
async def get_engagement(
    engagement_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Fetch a single engagement by id if owned by current user."""
    result = await db.execute(select(Engagement).where(Engagement.id == engagement_id))
    eng = result.scalar_one_or_none()
    if not eng or eng.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Engagement not found")
    return eng
