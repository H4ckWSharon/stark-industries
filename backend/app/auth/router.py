"""
STARK INDUSTRIES SQL — Auth Router
Open registration: users sign up with their own username/email and password.
Admin accounts are protected by the ADMIN_INVITE_CODE env variable.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime, timezone

from app.database import get_db
from app.auth.models import User
from app.auth.jwt import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_token,
)
from app.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


# ─── Schemas ──────────────────────────────────────────────────────────────────

class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict


class UserRegister(BaseModel):
    username: str
    email: Optional[str] = None
    password: str
    admin_invite_code: Optional[str] = None  # optional — only needed for admin accounts

    @field_validator("username")
    @classmethod
    def username_valid(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters")
        if len(v) > 50:
            raise ValueError("Username must be under 50 characters")
        if not v.replace("_", "").replace("-", "").isalnum():
            raise ValueError("Username can only contain letters, numbers, hyphens and underscores")
        return v

    @field_validator("password")
    @classmethod
    def password_valid(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v


class UserLogin(BaseModel):
    username: str   # username or email
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: Optional[str]
    is_admin: bool
    xp: int
    level: int
    rank: str

    class Config:
        from_attributes = True


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _user_payload(user: User) -> dict:
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_admin": user.is_admin,
        "xp": user.xp,
        "level": user.level,
        "rank": user.rank,
    }


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user


async def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


# ─── Routes ───────────────────────────────────────────────────────────────────

@router.post("/register", response_model=Token, summary="Register a new account")
async def register(
    body: UserRegister,
    db: AsyncSession = Depends(get_db),
):
    """
    Open registration — any user can sign up with their own username and password.
    Optionally provide an email address.
    To register as admin, supply the correct admin_invite_code.
    """
    # Check username not taken
    result = await db.execute(select(User).where(User.username == body.username))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username already taken. Please choose another.")

    # Check email not taken (if provided)
    if body.email:
        result = await db.execute(select(User).where(User.email == body.email))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email address already registered.")

    # Determine admin status via invite code
    is_admin = False
    if body.admin_invite_code:
        correct_code = getattr(settings, "admin_invite_code", settings.admin_password)
        if body.admin_invite_code != correct_code:
            raise HTTPException(status_code=403, detail="Invalid admin invite code.")
        is_admin = True

    user = User(
        username=body.username,
        email=body.email or None,
        hashed_password=get_password_hash(body.password),
        is_admin=is_admin,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    token = create_access_token({"sub": user.username, "admin": user.is_admin})
    return {"access_token": token, "token_type": "bearer", "user": _user_payload(user)}


@router.post("/token", response_model=Token, summary="Login with username/email + password")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """
    Login with username OR email and password.
    Works for any registered user account.
    """
    # Find user by username or email
    result = await db.execute(
        select(User).where(
            or_(User.username == form_data.username, User.email == form_data.username)
        )
    )
    user = result.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user.last_login = datetime.now(timezone.utc)
    await db.commit()

    token = create_access_token({"sub": user.username, "admin": user.is_admin})
    return {"access_token": token, "token_type": "bearer", "user": _user_payload(user)}


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
