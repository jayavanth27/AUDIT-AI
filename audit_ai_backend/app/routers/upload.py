"""Document upload and processing endpoints."""

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.security import get_current_user
from app.database import get_db
from app.models.engagement import Engagement
from app.models.document import Document
from app.models.extractedfield import ExtractedField
from app.models.riskflag import RiskFlag
from app.services import s3_service, extraction_service, risk_engine
from app.schemas.document import DocumentOut
from app.models.user import User

router = APIRouter()


@router.post("/{engagement_id}/upload", response_model=DocumentOut)
async def upload_document(
    engagement_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Handle file upload, store in S3, extract fields, and flag risks."""
    # verify engagement
    result = await db.execute(select(Engagement).where(Engagement.id == engagement_id))
    eng = result.scalar_one_or_none()
    if not eng or eng.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Engagement not found")

    # upload to s3
    contents = await file.read()
    from io import BytesIO

    key = s3_service.upload_fileobj(BytesIO(contents), file.content_type)
    doc = Document(
        filename=file.filename,
        s3_key=key,
        content_type=file.content_type,
        engagement_id=engagement_id,
    )
    db.add(doc)
    await db.commit()
    await db.refresh(doc)

    # extraction
    from io import BytesIO

    extracted = extraction_service.extract_document(BytesIO(contents), file.filename, file.content_type)
    # save fields
    for name, value in extracted.get("fields", {}).items():
        fld = ExtractedField(name=name, value=str(value), raw=None, document_id=doc.id)
        db.add(fld)
    await db.commit()

    # risk flags
    flags = risk_engine.evaluate(doc, extracted)
    for f in flags:
        rf = RiskFlag(rule=f["rule"], severity=f["severity"], message=f["message"], details=f.get("details"), document_id=doc.id)
        db.add(rf)
    await db.commit()

    return {
        "id": doc.id,
        "filename": doc.filename,
        "s3_key": doc.s3_key,
        "content_type": doc.content_type,
        "metadata": doc.metadata,
        "extraction": {"document_type": extracted.get("document_type"), "fields": extracted.get("fields")},
        "risk_flags": flags,
    }
