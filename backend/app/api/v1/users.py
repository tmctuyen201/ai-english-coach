from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/users", tags=["users"])

# Mock user for development
MOCK_USER = {
    "id": "mock-user-001",
    "phone": "+84901234567",
    "name": "Nguyen Van A",
    "cefr_level": "A2",
    "plan": "free",
    "xp": 150,
    "level": 3,
    "current_streak": 5,
    "total_conversations": 12,
}


class UserUpdate(BaseModel):
    name: Optional[str] = None
    cefr_level: Optional[str] = None


@router.get("/me")
async def get_current_user():
    return MOCK_USER


@router.put("/me")
async def update_current_user(update: UserUpdate):
    if update.name is not None:
        MOCK_USER["name"] = update.name
    if update.cefr_level is not None:
        MOCK_USER["cefr_level"] = update.cefr_level
    return MOCK_USER
