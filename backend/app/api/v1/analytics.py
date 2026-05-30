"""
AI English Coach — Analytics API
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/progress")
async def get_progress():
    return {"progress": {}, "message": "TODO: implement progress analytics"}

@router.get("/report")
async def generate_report():
    return {"report": {}, "message": "TODO: implement report generation"}
