from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.user import UserRegister, UserLogin, TokenResponse, OnboardingData
from app.services.auth_service import register_user, login_user, complete_onboarding
from app.core.deps import get_current_user
from app.models import User

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
async def register(data: UserRegister, db: AsyncSession = Depends(get_db)):
    try:
        result = await register_user(db, data.username, data.email, data.password)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    try:
        result = await login_user(db, data.username, data.password)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.get("/me")
async def get_me(user: User = Depends(get_current_user)):
    return {
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
        "is_active": user.is_active,
    }


@router.post("/onboarding")
async def onboarding(
    data: OnboardingData,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await complete_onboarding(db, user, data.dict())
    return result
