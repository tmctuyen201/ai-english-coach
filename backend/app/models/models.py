"""
AI English Coach — Database Models
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Text, JSON, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class PlanType(str, enum.Enum):
    FREE = "free"
    PREMIUM = "premium"
    PREMIUM_PLUS = "premium_plus"
    SCHOOL = "school"


class CEFRLevel(str, enum.Enum):
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"
    C2 = "C2"


class SessionStatus(str, enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone = Column(String(20), unique=True, index=True, nullable=False)
    email = Column(String(255), nullable=True)
    name = Column(String(100), nullable=False)
    date_of_birth = Column(DateTime, nullable=True)
    grade = Column(Integer, nullable=True)
    school = Column(String(200), nullable=True)
    city = Column(String(100), nullable=True)

    # Learning Profile
    cefr_level = Column(SQLEnum(CEFRLevel), default=CEFRLevel.A2)
    learning_goal = Column(String(50), default="communication")
    daily_goal_minutes = Column(Integer, default=15)

    # Subscription
    plan = Column(SQLEnum(PlanType), default=PlanType.FREE)
    plan_expires_at = Column(DateTime, nullable=True)

    # Stats
    total_practice_minutes = Column(Integer, default=0)
    total_conversations = Column(Integer, default=0)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    total_words_learned = Column(Integer, default=0)

    # Preferences
    preferred_voice = Column(String(50), default="friendly_female")
    preferred_speed = Column(Float, default=0.9)
    language_interface = Column(String(5), default="vi")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_active_at = Column(DateTime, nullable=True)

    # Relationships
    sessions = relationship("ConversationSession", back_populates="user")
    vocabulary = relationship("VocabularyItem", back_populates="user")


class ConversationSession(Base):
    __tablename__ = "conversation_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    topic_id = Column(String(100), nullable=False)

    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    duration_seconds = Column(Integer, default=0)
    status = Column(SQLEnum(SessionStatus), default=SessionStatus.ACTIVE)

    total_turns = Column(Integer, default=0)
    avg_grammar_score = Column(Float, default=0.0)
    avg_pronunciation_score = Column(Float, default=0.0)
    overall_score = Column(Float, default=0.0)

    summary_feedback_vi = Column(Text, nullable=True)
    summary_feedback_en = Column(Text, nullable=True)
    strengths = Column(JSON, default=list)
    improvements = Column(JSON, default=list)

    # Relationships
    user = relationship("User", back_populates="sessions")
    turns = relationship("ConversationTurn", back_populates="session", order_by="ConversationTurn.turn_number")


class ConversationTurn(Base):
    __tablename__ = "conversation_turns"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("conversation_sessions.id"), nullable=False, index=True)
    turn_number = Column(Integer, nullable=False)
    role = Column(String(10), nullable=False)  # "student" or "ai"

    student_text = Column(Text, nullable=True)
    student_audio_url = Column(String(500), nullable=True)
    ai_text = Column(Text, nullable=True)
    ai_audio_url = Column(String(500), nullable=True)

    grammar_corrections = Column(JSON, default=list)
    pronunciation_score = Column(Float, nullable=True)
    fluency_score = Column(Float, nullable=True)

    speech_duration_ms = Column(Integer, default=0)
    response_latency_ms = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    session = relationship("ConversationSession", back_populates="turns")


class VocabularyItem(Base):
    __tablename__ = "vocabulary_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    word = Column(String(100), nullable=False)
    phonetic = Column(String(100), nullable=True)
    part_of_speech = Column(String(20), nullable=True)
    meaning_en = Column(Text, nullable=True)
    meaning_vi = Column(Text, nullable=True)
    example_sentence = Column(Text, nullable=True)

    # Spaced Repetition (SM-2)
    ease_factor = Column(Float, default=2.5)
    interval = Column(Integer, default=0)
    repetitions = Column(Integer, default=0)
    next_review_at = Column(DateTime, nullable=True)

    source = Column(String(50), default="conversation")
    topic_id = Column(String(100), nullable=True)

    times_reviewed = Column(Integer, default=0)
    times_correct = Column(Integer, default=0)
    last_reviewed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="vocabulary")
