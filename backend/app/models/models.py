import uuid
from datetime import datetime
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    phone: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    cefr_level: Mapped[str] = mapped_column(String(10), default="A2")
    plan: Mapped[str] = mapped_column(String(20), default="free")
    xp: Mapped[int] = mapped_column(Integer, default=0)
    level: Mapped[int] = mapped_column(Integer, default=1)
    current_streak: Mapped[int] = mapped_column(Integer, default=0)
    total_conversations: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    sessions: Mapped[list["ConversationSession"]] = relationship(back_populates="user")
    vocabulary: Mapped[list["VocabularyItem"]] = relationship(back_populates="user")


class ConversationSession(Base):
    __tablename__ = "conversation_sessions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    topic_id: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="active")
    total_turns: Mapped[int] = mapped_column(Integer, default=0)
    avg_grammar_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    avg_pronunciation_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    overall_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    user: Mapped["User"] = relationship(back_populates="sessions")
    turns: Mapped[list["ConversationTurn"]] = relationship(back_populates="session")


class ConversationTurn(Base):
    __tablename__ = "conversation_turns"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("conversation_sessions.id"), nullable=False)
    turn_number: Mapped[int] = mapped_column(Integer, nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    student_text: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    ai_text: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    grammar_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    pronunciation_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    session: Mapped["ConversationSession"] = relationship(back_populates="turns")


class VocabularyItem(Base):
    __tablename__ = "vocabulary_items"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    word: Mapped[str] = mapped_column(String(100), nullable=False)
    phonetic: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    meaning_vi: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    meaning_en: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    ease_factor: Mapped[float] = mapped_column(Float, default=2.5)
    interval: Mapped[int] = mapped_column(Integer, default=0)
    repetitions: Mapped[int] = mapped_column(Integer, default=0)
    next_review_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="vocabulary")
