"""Endpoint for generating LLM summaries of engagements."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.security import get_current_user
from app.database import get_db
from app.models.engagement import Engagement
from app.models.document import Document
from app.models.extractedfield import ExtractedField
from app.models.riskflag import RiskFlag
from app.models.workingpaper import WorkingPaper
from app.services import llm_service
from app.schemas.document import WorkingPaperOut
from app.models.user import User

router = APIRouter()


@router.post("/{engagement_id}/generate-summary", response_model=WorkingPaperOut)
async def generate_summary(
    engagement_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Gather data and risk flags then call the LLM service to generate a summary.

    Stores the result as a WorkingPaper record.
    """
    result = await db.execute(select(Engagement).where(Engagement.id == engagement_id))
    eng = result.scalar_one_or_none()
    if not eng or eng.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Engagement not found")

    # collect data
    docs = await db.execute(select(Document).where(Document.engagement_id == engagement_id))
    docs = docs.scalars().all()
    structured = []
    risk_flags = []
    for d in docs:
        fields = (await db.execute(select(ExtractedField).where(ExtractedField.document_id == d.id))).scalars().all()
        flags = (await db.execute(select(RiskFlag).where(RiskFlag.document_id == d.id))).scalars().all()
        structured.append({"document_id": d.id, "fields": {f.name: f.value for f in fields}})
        for f in flags:
            risk_flags.append({"rule": f.rule, "severity": f.severity, "message": f.message})

    # call LLM
    summary = llm_service.generate_working_paper({"docs": structured}, risk_flags)
    # store
    wp = WorkingPaper(content=summary, engagement_id=engagement_id)
    db.add(wp)
    await db.commit()
    await db.refresh(wp)
    return {"content": summary}
