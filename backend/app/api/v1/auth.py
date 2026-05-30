"""
AI English Coach — Auth API
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.config import settings
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import jwt
import random
import redis.asyncio as redis

router = APIRouter()
redis_client = redis.from_url(settings.REDIS_URL)


class OTPRequest(BaseModel):
    phone: str


class OTPVerify(BaseModel):
    phone: str
    otp: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


def create_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")


@router.post("/phone/send-otp", status_code=status.HTTP_200_OK)
async def send_otp(request: OTPRequest):
    """Send OTP to phone number."""
    otp = "".join([str(random.randint(0, 9)) for _ in range(6)])
    await redis_client.setex(
        f"otp:{request.phone}",
        settings.OTP_EXPIRE_MINUTES * 60,
        otp
    )
    # TODO: integrate SMS provider (Twilio/Viettel)
    return {"message": "OTP sent", "phone": request.phone}


@router.post("/phone/verify", response_model=TokenResponse)
async def verify_otp(request: OTPVerify, db: AsyncSession = Depends(get_db)):
    """Verify OTP and return JWT tokens."""
    stored_otp = await redis_client.get(f"otp:{request.phone}")
    if not stored_otp or stored_otp.decode() != request.otp:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    await redis_client.delete(f"otp:{request.phone}")

    # TODO: find or create user in database
    access_token = create_token(
        {"sub": request.phone, "type": "access"},
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_token(
        {"sub": request.phone, "type": "refresh"},
        timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )
