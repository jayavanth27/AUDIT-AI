from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """Request model for registering a new user."""

    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """Request model for logging in an existing user."""

    email: EmailStr
    password: str


class UserOut(BaseModel):
    """Response model representing a user record."""

    id: int
    email: EmailStr

    class Config:
        orm_mode = True
