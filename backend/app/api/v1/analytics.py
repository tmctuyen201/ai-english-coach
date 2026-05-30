from fastapi import APIRouter

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/progress")
async def get_progress():
    return {
        "total_conversations": 12,
        "total_xp": 150,
        "current_level": 3,
        "current_streak": 5,
        "avg_grammar_score": 78.5,
        "avg_pronunciation_score": 72.3,
        "weekly_activity": [
            {"day": "Mon", "conversations": 2},
            {"day": "Tue", "conversations": 1},
            {"day": "Wed", "conversations": 3},
            {"day": "Thu", "conversations": 0},
            {"day": "Fri", "conversations": 2},
            {"day": "Sat", "conversations": 4},
            {"day": "Sun", "conversations": 0},
        ],
        "vocabulary_mastered": 45,
        "vocabulary_learning": 23,
    }
