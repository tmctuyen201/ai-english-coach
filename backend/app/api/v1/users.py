"""
AI English Coach — Users API
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/me")
async def get_current_user():
    return {"user": {}, "message": "TODO: implement user profile"}

@router.put("/me")
async def update_profile():
    return {"message": "TODO: implement profile update"}

@router.get("/me/stats")
async def get_stats():
    return {"stats": {}, "message": "TODO: implement user stats"}
