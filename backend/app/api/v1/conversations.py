"""
AI English Coach — Conversations API
"""
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.conversation_service import ConversationService
from pydantic import BaseModel
from typing import Optional
from uuid import UUID

router = APIRouter()


class StartConversationRequest(BaseModel):
    topic_id: str
    voice: Optional[str] = "friendly_female"
    speed: Optional[float] = 0.9


class ConversationResponse(BaseModel):
    session_id: str
    topic_id: str
    ai_greeting: str
    ai_audio_url: Optional[str] = None


@router.post("/start", response_model=ConversationResponse)
async def start_conversation(
    request: StartConversationRequest,
    db: AsyncSession = Depends(get_db)
):
    """Start a new conversation session."""
    service = ConversationService(db)
    session = await service.start_session(
        topic_id=request.topic_id,
        voice=request.voice,
        speed=request.speed
    )
    return session


@router.websocket("/{session_id}")
async def conversation_websocket(
    websocket: WebSocket,
    session_id: str
):
    """Real-time voice conversation via WebSocket."""
    await websocket.accept()
    service = ConversationService()

    try:
        while True:
            data = await websocket.receive_json()

            if data.get("type") == "audio_end":
                # Process audio and generate response
                result = await service.process_turn(
                    session_id=session_id,
                    audio_data=data.get("audio_base64")
                )
                await websocket.send_json({
                    "type": "ai_response",
                    "text": result["ai_text"],
                    "audio_url": result["ai_audio_url"],
                    "feedback": result["feedback"]
                })

            elif data.get("type") == "text_message":
                result = await service.process_text_turn(
                    session_id=session_id,
                    text=data.get("text")
                )
                await websocket.send_json({
                    "type": "ai_response",
                    "text": result["ai_text"],
                    "audio_url": result["ai_audio_url"],
                    "feedback": result["feedback"]
                })

            elif data.get("type") == "session_end":
                summary = await service.end_session(session_id)
                await websocket.send_json({
                    "type": "session_summary",
                    **summary
                })
                break

    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_json({"type": "error", "message": str(e)})
    finally:
        await websocket.close()


@router.get("/{session_id}")
async def get_session(session_id: str, db: AsyncSession = Depends(get_db)):
    """Get conversation session details."""
    service = ConversationService(db)
    return await service.get_session(session_id)


@router.get("/{session_id}/feedback")
async def get_feedback(session_id: str, db: AsyncSession = Depends(get_db)):
    """Get detailed feedback for a session."""
    service = ConversationService(db)
    return await service.get_feedback(session_id)
