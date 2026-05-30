from fastapi import APIRouter

router = APIRouter(prefix="/topics", tags=["topics"])

TOPICS = [
    {
        "id": "daily-routine",
        "title_en": "Daily Routine",
        "title_vi": "Hoạt động hàng ngày",
        "level": "A2",
        "icon": "🌅",
    },
    {
        "id": "food-ordering",
        "title_en": "Ordering Food",
        "title_vi": "Gọi đồ ăn",
        "level": "A2",
        "icon": "🍔",
    },
    {
        "id": "travel-directions",
        "title_en": "Asking for Directions",
        "title_vi": "Hỏi đường",
        "level": "B1",
        "icon": "🗺️",
    },
    {
        "id": "shopping",
        "title_en": "Shopping",
        "title_vi": "Mua sắm",
        "level": "A2",
        "icon": "🛍️",
    },
    {
        "id": "job-interview",
        "title_en": "Job Interview",
        "title_vi": "Phỏng vấn xin việc",
        "level": "B2",
        "icon": "💼",
    },
]


@router.get("")
async def list_topics():
    return TOPICS
