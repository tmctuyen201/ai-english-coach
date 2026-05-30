"""
AI English Coach — Vocabulary API
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_vocabulary():
    return {"vocabulary": [], "message": "TODO: implement vocabulary list"}

@router.get("/due")
async def due_vocabulary():
    return {"vocabulary": [], "message": "TODO: implement due reviews"}

@router.post("/review")
async def submit_review():
    return {"message": "TODO: implement review submission"}
