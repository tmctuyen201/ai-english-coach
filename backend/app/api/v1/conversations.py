import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/conversations", tags=["conversations"])

# In-memory session store for development
sessions: dict[str, dict] = {}


class StartConversationRequest(BaseModel):
    topic_id: str
    name: str


class SessionResponse(BaseModel):
    session_id: str
    ai_greeting: str


@router.post("/start", response_model=SessionResponse)
async def start_conversation(request: StartConversationRequest):
    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        "session_id": session_id,
        "topic_id": request.topic_id,
        "name": request.name,
        "status": "active",
        "total_turns": 0,
        "avg_grammar_score": None,
        "avg_pronunciation_score": None,
        "overall_score": None,
        "started_at": datetime.utcnow().isoformat(),
        "ended_at": None,
    }
    return SessionResponse(
        session_id=session_id,
        ai_greeting=f"Hello {request.name}! Let's practice English with the topic: {request.topic_id}. How are you today?",
    )


@router.get("/{session_id}")
async def get_conversation(session_id: str):
    session = sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.post("/{session_id}/end")
async def end_conversation(session_id: str):
    session = sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    session["status"] = "completed"
    session["ended_at"] = datetime.utcnow().isoformat()
    session["overall_score"] = 75.5

    return {
        "session_id": session_id,
        "status": "completed",
        "total_turns": session["total_turns"],
        "overall_score": session["overall_score"],
        "summary": "Great conversation! Keep practicing to improve your skills.",
    }
