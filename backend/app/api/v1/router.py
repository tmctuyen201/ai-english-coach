from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.conversations import router as conversations_router
from app.api.v1.topics import router as topics_router
from app.api.v1.vocabulary import router as vocabulary_router
from app.api.v1.analytics import router as analytics_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(conversations_router)
api_router.include_router(topics_router)
api_router.include_router(vocabulary_router)
api_router.include_router(analytics_router)
