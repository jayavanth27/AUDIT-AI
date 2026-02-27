"""Authentication routes (registration/login)."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserCreate, UserLogin, UserOut
from app.services import auth_service
from app.database import get_db

router = APIRouter()


@router.post("/register", response_model=UserOut)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user.

    Returns the created user record.
    """
    existing = await auth_service.authenticate_user(db, user_in.email, user_in.password)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = await auth_service.register_user(db, user_in)
    return user


@router.post("/login")
async def login(user_in: UserLogin, db: AsyncSession = Depends(get_db)):
    """Authenticate user and return JWT token."""
    user = await auth_service.authenticate_user(db, user_in.email, user_in.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = auth_service.create_token_for_user(user)
    return {"access_token": token, "token_type": "bearer"}
