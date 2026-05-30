"""
AI English Coach — Stub API modules (topics, vocabulary, users, analytics)
"""
from fastapi import APIRouter

router = APIRouter()


# ---- Topics ----
topics_router = APIRouter()

@topics_router.get("/")
async def list_topics():
    return {"topics": [], "message": "TODO: implement topics list"}

@topics_router.get("/recommended")
async def recommended_topics():
    return {"topics": [], "message": "TODO: implement recommendations"}

router = topics_router
