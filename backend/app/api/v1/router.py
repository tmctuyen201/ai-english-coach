"""
AI English Coach — API v1 Router
"""
from fastapi import APIRouter
from app.api.v1 import auth, conversations, topics, vocabulary, users, analytics

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(conversations.router, prefix="/conversations", tags=["Conversations"])
api_router.include_router(topics.router, prefix="/topics", tags=["Topics"])
api_router.include_router(vocabulary.router, prefix="/vocabulary", tags=["Vocabulary"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
