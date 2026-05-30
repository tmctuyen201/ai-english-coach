from datetime import datetime, timedelta
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/vocabulary", tags=["vocabulary"])

# Mock vocabulary data
VOCABULARY = [
    {
        "id": "vocab-001",
        "word": "hello",
        "phonetic": "/həˈloʊ/",
        "meaning_vi": "xin chào",
        "meaning_en": "a greeting",
        "ease_factor": 2.5,
        "interval": 1,
        "repetitions": 3,
        "next_review_at": (datetime.utcnow() + timedelta(days=1)).isoformat(),
    },
    {
        "id": "vocab-002",
        "word": "practice",
        "phonetic": "/ˈpræktɪs/",
        "meaning_vi": "luyện tập",
        "meaning_en": "to do something regularly to improve",
        "ease_factor": 2.5,
        "interval": 0,
        "repetitions": 0,
        "next_review_at": datetime.utcnow().isoformat(),
    },
    {
        "id": "vocab-003",
        "word": "conversation",
        "phonetic": "/ˌkɑːnvərˈseɪʃn/",
        "meaning_vi": "cuộc trò chuyện",
        "meaning_en": "a talk between two or more people",
        "ease_factor": 2.0,
        "interval": 3,
        "repetitions": 5,
        "next_review_at": (datetime.utcnow() + timedelta(days=3)).isoformat(),
    },
]


class ReviewRequest(BaseModel):
    word_id: str
    quality: int  # 0-5 rating


@router.get("")
async def list_vocabulary():
    return VOCABULARY


@router.get("/due")
async def due_vocabulary():
    now = datetime.utcnow()
    due = [v for v in VOCABULARY if v["next_review_at"] and v["next_review_at"] <= now.isoformat()]
    # If none are actually due (mock data timestamps), return at least the ones with interval=0
    if not due:
        due = [v for v in VOCABULARY if v["interval"] == 0]
    return due


@router.post("/review")
async def review_word(review: ReviewRequest):
    return {"message": "Review recorded successfully", "word_id": review.word_id}
