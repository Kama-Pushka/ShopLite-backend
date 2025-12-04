from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserCreate, UserLogin, Token, UserOut, RefreshToken
from app.database import get_db
from app.services.auth_service import AuthService
from app.schemas.user import EmailSchema, ResetPassword
from app.database import User

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=Token)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = await AuthService.register_user(user.email, user.password, user.name, db)
    access_token, refresh_token = await AuthService.authenticate(user.email, user.password, db)
    return Token(access_token=access_token, refresh_token=refresh_token)

@router.post("/login", response_model=Token)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    access_token, refresh_token = await AuthService.authenticate(user.email, user.password, db)
    return Token(access_token=access_token, refresh_token=refresh_token)

@router.post("/refresh", response_model=Token)
async def refresh_tokens(data: RefreshToken, db: AsyncSession = Depends(get_db)):
    access_token, refresh_token = await AuthService.refresh_tokens(data.refresh_token, db)
    return Token(access_token=access_token, refresh_token=refresh_token)

@router.get("/me", response_model=UserOut)
async def get_me(current_user: User = Depends(AuthService.get_current_user)):
    return current_user

@router.post("/forgot")
async def forgot(email: EmailSchema, db: AsyncSession = Depends(get_db)):
    await AuthService.forgot_password(email.email, db)
    return {"message": "If this email exists, reset link was sent"}

@router.post("/reset")
async def reset_password(data: ResetPassword, db: AsyncSession = Depends(get_db)):
    await AuthService.reset_password(data.token, data.new_password, db)
    return {"message": "Password successfully updated"}
