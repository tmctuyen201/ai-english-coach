import random
import string
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.models import User

router = APIRouter(prefix="/auth", tags=["auth"])

# In-memory OTP store
otp_store: dict[str, str] = {}


class OTPRequest(BaseModel):
    phone: str


class OTPVerify(BaseModel):
    phone: str
    otp: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/phone/send-otp")
async def send_otp(request: OTPRequest):
    otp = "".join(random.choices(string.digits, k=6))
    otp_store[request.phone] = otp
    return {"message": f"OTP sent to {request.phone}", "phone": request.phone}


@router.post("/phone/verify", response_model=TokenResponse)
async def verify_otp(request: OTPVerify, db: AsyncSession = Depends(get_db)):
    stored_otp = otp_store.get(request.phone)
    if not stored_otp or stored_otp != request.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    # Clean up OTP
    otp_store.pop(request.phone, None)

    # Find or create user
    result = await db.execute(select(User).where(User.phone == request.phone))
    user = result.scalar_one_or_none()
    if not user:
        user = User(phone=request.phone, name=f"User {request.phone[-4:]}")
        db.add(user)
        await db.flush()

    return {"access_token": f"fake-jwt-token-{user.id}"}
