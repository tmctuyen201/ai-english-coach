"""
AI English Coach — Conversation Service (Core Business Logic)
"""
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional, Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
import httpx
import json


class ConversationService:
    """Manages conversation sessions: ASR → LLM → TTS pipeline."""

    def __init__(self, db: AsyncSession = None):
        self.db = db
        self.openai_key = settings.OPENAI_API_KEY

    async def start_session(
        self,
        topic_id: str,
        user_id: UUID = None,
        voice: str = "friendly_female",
        speed: float = 0.9
    ) -> Dict[str, Any]:
        """Start a new conversation session."""
        session_id = str(uuid4())

        # Get topic details
        topic = self._get_topic(topic_id)

        # Generate AI greeting
        greeting = await self._generate_greeting(topic)

        # Generate TTS for greeting
        audio_url = await self._text_to_speech(greeting, voice, speed)

        # TODO: Save session to database

        return {
            "session_id": session_id,
            "topic_id": topic_id,
            "ai_greeting": greeting,
            "ai_audio_url": audio_url
        }

    async def process_turn(
        self,
        session_id: str,
        audio_data: str = None,
        text: str = None
    ) -> Dict[str, Any]:
        """Process a student turn: ASR → Grammar Check → LLM → TTS."""
        # Step 1: Speech-to-Text (if audio)
        if audio_data and not text:
            text = await self._speech_to_text(audio_data)

        if not text:
            return {"ai_text": "I didn't catch that. Could you try again?",
                    "ai_audio_url": None, "feedback": {}}

        # Step 2: Grammar check (parallel with LLM)
        grammar_result = await self._check_grammar(text)

        # Step 3: Generate AI response
        ai_response = await self._generate_response(text, session_id)

        # Step 4: Generate TTS
        audio_url = await self._text_to_speech(ai_response["text"])

        # Step 5: Pronunciation scoring (if audio)
        pron_score = None
        if audio_data:
            pron_score = await self._score_pronunciation(audio_data, text)

        return {
            "ai_text": ai_response["text"],
            "ai_audio_url": audio_url,
            "feedback": {
                "grammar": grammar_result,
                "pronunciation": pron_score
            }
        }

    async def process_text_turn(self, session_id: str, text: str) -> Dict[str, Any]:
        """Process a text-based turn (no ASR needed)."""
        return await self.process_turn(session_id, text=text)

    async def end_session(self, session_id: str) -> Dict[str, Any]:
        """End session and generate summary."""
        # TODO: Calculate session stats from DB
        return {
            "duration_seconds": 300,
            "total_turns": 8,
            "avg_grammar_score": 72.5,
            "avg_pronunciation_score": 68.0,
            "overall_score": 70.2,
            "summary_vi": "Bạn đã làm tốt! Tiếp tục luyện tập nhé.",
            "summary_en": "Great job! Keep practicing.",
            "strengths": ["Vocabulary", "Confidence"],
            "improvements": ["Past tense", "Pronunciation /θ/"]
        }

    async def get_session(self, session_id: str) -> Dict[str, Any]:
        """Get session details."""
        # TODO: fetch from DB
        return {"session_id": session_id, "status": "active"}

    async def get_feedback(self, session_id: str) -> Dict[str, Any]:
        """Get detailed feedback."""
        # TODO: fetch from DB
        return {"feedback": {}}

    # ---- Private: External API Calls ----

    async def _speech_to_text(self, audio_base64: str) -> str:
        """Convert speech to text using OpenAI Whisper."""
        try:
            async with httpx.AsyncClient() as client:
                # Decode base64 audio and send to Whisper
                response = await client.post(
                    "https://api.openai.com/v1/audio/transcriptions",
                    headers={"Authorization": f"Bearer {self.openai_key}"},
                    files={"file": ("audio.webm", audio_base64.encode(), "audio/webm")},
                    data={"model": "whisper-1", "language": "en"},
                    timeout=10.0
                )
                if response.status_code == 200:
                    return response.json().get("text", "")
        except Exception as e:
            print(f"ASR error: {e}")
        return ""

    async def _text_to_speech(self, text: str, voice: str = "nova", speed: float = 0.9) -> Optional[str]:
        """Convert text to speech using OpenAI TTS."""
        try:
            voice_map = {
                "friendly_female": "nova",
                "friendly_male": "echo",
                "professional_female": "shimmer",
                "young_energetic": "alloy"
            }
            openai_voice = voice_map.get(voice, "nova")

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.openai.com/v1/audio/speech",
                    headers={"Authorization": f"Bearer {self.openai_key}"},
                    json={"model": "tts-1-hd", "input": text, "voice": openai_voice, "speed": speed},
                    timeout=15.0
                )
                if response.status_code == 200:
                    # Save audio and return URL
                    # TODO: upload to S3/MinIO
                    return None
        except Exception as e:
            print(f"TTS error: {e}")
        return None

    async def _check_grammar(self, text: str) -> Dict[str, Any]:
        """Check grammar using LLM."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {self.openai_key}"},
                    json={
                        "model": "gpt-4o-mini",
                        "messages": [
                            {"role": "system", "content": "You are an English grammar checker. Return JSON with corrections."},
                            {"role": "user", "content": f"Check grammar: \"{text}\""}
                        ],
                        "response_format": {"type": "json_object"},
                        "temperature": 0.1
                    },
                    timeout=5.0
                )
                if response.status_code == 200:
                    return json.loads(response.json()["choices"][0]["message"]["content"])
        except Exception as e:
            print(f"Grammar check error: {e}")
        return {"has_errors": False, "corrections": [], "overall_score": 100}

    async def _generate_response(self, student_text: str, session_id: str) -> Dict[str, Any]:
        """Generate AI conversation response."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {self.openai_key}"},
                    json={
                        "model": "gpt-4o-mini",
                        "messages": [
                            {"role": "system", "content": "You are a friendly English conversation partner for Vietnamese students. Keep responses SHORT (1-3 sentences). Be encouraging."},
                            {"role": "user", "content": student_text}
                        ],
                        "temperature": 0.7,
                        "max_tokens": 150
                    },
                    timeout=5.0
                )
                if response.status_code == 200:
                    text = response.json()["choices"][0]["message"]["content"]
                    return {"text": text}
        except Exception as e:
            print(f"LLM error: {e}")
        return {"text": "That's interesting! Can you tell me more?"}

    async def _generate_greeting(self, topic: Dict) -> str:
        """Generate AI greeting for topic."""
        return f"Hi! Welcome! Today we'll practice {topic.get('title', 'English conversation')}. Are you ready? Let's start!"

    async def _score_pronunciation(self, audio_base64: str, reference_text: str) -> Dict[str, Any]:
        """Score pronunciation."""
        # TODO: implement pronunciation scoring
        return {"overall": 75, "accuracy": 78, "fluency": 72, "completeness": 80, "prosody": 70}

    def _get_topic(self, topic_id: str) -> Dict:
        """Get topic details from static data."""
        topics = {
            "greetings": {"title": "Meeting New People", "level": "A1"},
            "food": {"title": "Ordering Food", "level": "A2"},
            "school": {"title": "School Life", "level": "B1"},
        }
        return topics.get(topic_id, {"title": "General Conversation", "level": "A2"})
