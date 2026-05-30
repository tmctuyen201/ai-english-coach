# AI English Coach — Deployment Architecture

> **Version:** 2.0.0
> **Last Updated:** 2026-05-30
> **Status:** Deployable

---

## 1. Deployment Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DEPLOYMENT TOPOLOGY                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                    CLOUDFLARE CDN                             │    │
│  │  ├── Static assets (JS, CSS, images, audio cache)           │    │
│  │  ├── DDoS protection                                        │    │
│  │  └── SSL termination                                        │    │
│  └────────────────────────────┬────────────────────────────────┘    │
│                                │                                      │
│                                ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                    NGINX REVERSE PROXY                        │    │
│  │  ├── Port 80 → HTTPS redirect                               │    │
│  │  ├── Port 443 → SSL + routing                               │    │
│  │  ├── /api/* → Backend (rate limit: 30 req/s)               │    │
│  │  ├── /api/v1/auth/* → Backend (rate limit: 5 req/s)        │    │
│  │  ├── /ws/* → Backend WebSocket (upgrade)                    │    │
│  │  └── /* → Frontend (Next.js)                                │    │
│  └────────────────────────────┬────────────────────────────────┘    │
│                                │                                      │
│              ┌─────────────────┼─────────────────┐                  │
│              ▼                 ▼                 ▼                  │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐       │
│  │   FRONTEND       │ │   BACKEND        │ │   WORKERS        │       │
│  │   (Next.js)      │ │   (FastAPI)      │ │   (Celery)       │       │
│  │   Port 3000      │ │   Port 8000      │ │   Async tasks    │       │
│  │   1 instance     │ │   3 instances    │ │   4 workers      │       │
│  └─────────────────┘ └────────┬────────┘ └────────┬────────┘       │
│                                │                    │                  │
│              ┌─────────────────┼────────────────────┤                │
│              ▼                 ▼                    ▼                │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐       │
│  │   POSTGRESQL     │ │   REDIS           │ │   QDRANT         │       │
│  │   Port 5432      │ │   Port 6379       │ │   Port 6333      │       │
│  │   Primary DB     │ │   Cache + Sessions│ │   Vector DB      │       │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘       │
│                                                                      │
│  ┌─────────────────┐                                               │
│  │   MINIO           │                                               │
│  │   Port 9000       │                                               │
│  │   Audio Storage   │                                               │
│  └─────────────────┘                                               │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. Docker Services

### 2.1 Service Matrix

| Service | Image | Port | CPU | Memory | Health Check |
|---------|-------|------|-----|--------|--------------|
| postgres | postgres:16-alpine | 5432 | 1 core | 512MB | pg_isready |
| redis | redis:7-alpine | 6379 | 0.5 core | 256MB | redis-cli ping |
| qdrant | qdrant/qdrant:v1.8.0 | 6333 | 1 core | 512MB | curl /healthz |
| minio | minio/minio:latest | 9000 | 0.5 core | 256MB | curl /health/live |
| backend | custom (FastAPI) | 8000 | 2 cores | 1GB | curl /health |
| frontend | custom (Next.js) | 3000 | 1 core | 512MB | curl / |
| nginx | nginx:alpine | 80, 443 | 0.5 core | 128MB | - |
| celery_worker | custom | - | 2 cores | 1GB | - |
| celery_beat | custom | - | 0.5 core | 256MB | - |
| flower | custom | 5555 | 0.5 core | 256MB | - |

**Total:** ~10 CPU cores, ~4.5GB RAM minimum

### 2.2 Docker Compose Commands

```bash
# Development (hot-reload)
docker compose up -d

# Production
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# View logs
docker compose logs -f backend
docker compose logs -f frontend

# Scale backend
docker compose up -d --scale backend=3

# Database backup
docker compose exec postgres pg_dump -U postgres ai_english_coach > backup.sql

# Database restore
cat backup.sql | docker compose exec -T postgres psql -U postgres ai_english_coach

# Stop all
docker compose down

# Stop and remove volumes (CAREFUL: deletes data)
docker compose down -v
```

---

## 3. Backend Architecture

### 3.1 FastAPI Application Structure

```
backend/
├── Dockerfile                    # Multi-stage build
├── requirements.txt              # Python dependencies
├── alembic/
│   ├── init.sql                  # DB initialization
│   └── versions/                 # Migration files
├── app/
│   ├── main.py                   # FastAPI entry point
│   ├── core/
│   │   ├── config.py             # Pydantic settings
│   │   ├── database.py           # SQLAlchemy async engine
│   │   └── celery_app.py         # Celery configuration
│   ├── api/
│   │   └── v1/
│   │       ├── router.py         # API router aggregation
│   │       ├── auth.py           # OTP authentication
│   │       ├── conversations.py  # Conversation CRUD + WebSocket
│   │       ├── topics.py         # Topic management
│   │       ├── vocabulary.py     # Vocabulary + spaced repetition
│   │       ├── users.py          # User profile management
│   │       └── analytics.py      # Progress analytics
│   ├── models/
│   │   └── models.py             # SQLAlchemy ORM models
│   ├── schemas/
│   │   └── schemas.py            # Pydantic request/response models
│   ├── services/
│   │   ├── conversation_service.py  # ASR→LLM→TTS pipeline
│   │   ├── grammar_service.py       # Grammar checking
│   │   ├── pronunciation_service.py # Pronunciation scoring
│   │   ├── tts_service.py           # Text-to-speech
│   │   └── vocabulary_service.py    # Spaced repetition
│   └── utils/
│       ├── security.py           # JWT, password hashing
│       └── redis_client.py       # Redis connection
└── tests/
    ├── test_auth.py
    ├── test_conversations.py
    └── test_vocabulary.py
```

### 3.2 API Endpoints

```yaml
# Authentication
POST   /api/v1/auth/phone/send-otp      # Send OTP to phone
POST   /api/v1/auth/phone/verify         # Verify OTP → JWT
POST   /api/v1/auth/refresh              # Refresh access token

# Users
GET    /api/v1/users/me                  # Get current user
PUT    /api/v1/users/me                  # Update profile
GET    /api/v1/users/me/stats            # Get learning statistics

# Conversations
POST   /api/v1/conversations/start       # Start new session
WS     /ws/v1/conversations/{id}         # Real-time voice conversation
GET    /api/v1/conversations/{id}        # Get session details
POST   /api/v1/conversations/{id}/end    # End session → summary
GET    /api/v1/conversations/{id}/feedback # Detailed feedback

# Topics
GET    /api/v1/topics                    # List all topics
GET    /api/v1/topics/{id}              # Get topic details
GET    /api/v1/topics/recommended       # Personalized recommendations

# Vocabulary
GET    /api/v1/vocabulary                # User's vocabulary list
GET    /api/v1/vocabulary/due            # Words due for review
POST   /api/v1/vocabulary/review         # Submit review (SM-2)

# Analytics
GET    /api/v1/analytics/progress        # Progress over time
GET    /api/v1/analytics/report          # Generate report (PDF)

# Health
GET    /health                           # Health check
```

### 3.3 Database Schema

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    phone VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(255),
    name VARCHAR(100) NOT NULL,
    date_of_birth TIMESTAMP,
    grade INTEGER,
    school VARCHAR(200),
    city VARCHAR(100),
    cefr_level VARCHAR(5) DEFAULT 'A2',
    learning_goal VARCHAR(50) DEFAULT 'communication',
    daily_goal_minutes INTEGER DEFAULT 15,
    plan VARCHAR(20) DEFAULT 'free',
    plan_expires_at TIMESTAMP,
    total_practice_minutes INTEGER DEFAULT 0,
    total_conversations INTEGER DEFAULT 0,
    current_streak INTEGER DEFAULT 0,
    longest_streak INTEGER DEFAULT 0,
    total_words_learned INTEGER DEFAULT 0,
    preferred_voice VARCHAR(50) DEFAULT 'friendly_female',
    preferred_speed FLOAT DEFAULT 0.9,
    language_interface VARCHAR(5) DEFAULT 'vi',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_active_at TIMESTAMP
);

-- Conversation sessions
CREATE TABLE conversation_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    topic_id VARCHAR(100) NOT NULL,
    started_at TIMESTAMP DEFAULT NOW(),
    ended_at TIMESTAMP,
    duration_seconds INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'active',
    total_turns INTEGER DEFAULT 0,
    avg_grammar_score FLOAT DEFAULT 0,
    avg_pronunciation_score FLOAT DEFAULT 0,
    overall_score FLOAT DEFAULT 0,
    summary_feedback_vi TEXT,
    summary_feedback_en TEXT,
    strengths JSONB DEFAULT '[]',
    improvements JSONB DEFAULT '[]'
);

-- Conversation turns
CREATE TABLE conversation_turns (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID REFERENCES conversation_sessions(id) ON DELETE CASCADE,
    turn_number INTEGER NOT NULL,
    role VARCHAR(10) NOT NULL,  -- 'student' or 'ai'
    student_text TEXT,
    student_audio_url VARCHAR(500),
    ai_text TEXT,
    ai_audio_url VARCHAR(500),
    grammar_corrections JSONB DEFAULT '[]',
    pronunciation_score FLOAT,
    fluency_score FLOAT,
    speech_duration_ms INTEGER DEFAULT 0,
    response_latency_ms INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Vocabulary items (spaced repetition)
CREATE TABLE vocabulary_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    word VARCHAR(100) NOT NULL,
    phonetic VARCHAR(100),
    part_of_speech VARCHAR(20),
    meaning_en TEXT,
    meaning_vi TEXT,
    example_sentence TEXT,
    ease_factor FLOAT DEFAULT 2.5,
    interval INTEGER DEFAULT 0,
    repetitions INTEGER DEFAULT 0,
    next_review_at TIMESTAMP,
    source VARCHAR(50) DEFAULT 'conversation',
    topic_id VARCHAR(100),
    times_reviewed INTEGER DEFAULT 0,
    times_correct INTEGER DEFAULT 0,
    last_reviewed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_users_phone ON users(phone);
CREATE INDEX idx_sessions_user_id ON conversation_sessions(user_id);
CREATE INDEX idx_sessions_started_at ON conversation_sessions(started_at DESC);
CREATE INDEX idx_turns_session_id ON conversation_turns(session_id);
CREATE INDEX idx_vocabulary_user_review ON vocabulary_items(user_id, next_review_at);
```

---

## 4. Frontend Architecture

### 4.1 Next.js Application Structure

```
frontend/
├── Dockerfile
├── package.json
├── next.config.js
├── tailwind.config.ts
├── tsconfig.json
├── public/
│   ├── favicon.ico
│   └── assets/
└── src/
    ├── app/
    │   ├── layout.tsx              # Root layout
    │   ├── page.tsx                # Landing page
    │   ├── login/page.tsx          # Phone OTP login
    │   ├── dashboard/page.tsx      # Main dashboard
    │   ├── practice/
    │   │   ├── page.tsx            # Topic selection
    │   │   └── [topicId]/
    │   │       └── page.tsx        # Conversation page
    │   ├── vocabulary/page.tsx     # Vocabulary review
    │   ├── progress/page.tsx       # Progress charts
    │   └── parent/page.tsx         # Parent dashboard
    ├── components/
    │   ├── Conversation/
    │   │   ├── ChatBubble.tsx       # Message bubble
    │   │   ├── AudioRecorder.tsx    # Mic button + recording
    │   │   ├── GrammarFeedback.tsx  # Grammar corrections overlay
    │   │   ├── PronScore.tsx        # Pronunciation score display
    │   │   └── WaveformVisualizer.tsx # Audio waveform
    │   ├── Dashboard/
    │   │   ├── StatsCard.tsx        # Stats summary
    │   │   ├── ProgressChart.tsx    # Progress line chart
    │   │   └── StreakBadge.tsx      # Streak display
    │   ├── Vocabulary/
    │   │   ├── FlashCard.tsx        # Vocabulary flashcard
    │   │   └── ReviewSession.tsx    # Spaced repetition session
    │   └── UI/
    │       ├── Button.tsx
    │       ├── Card.tsx
    │       ├── Modal.tsx
    │       └── Loading.tsx
    ├── hooks/
    │   ├── useAudio.ts             # Audio recording hook
    │   ├── useWebSocket.ts         # WebSocket connection
    │   └── useConversation.ts      # Conversation state
    ├── lib/
    │   ├── api.ts                  # API client
    │   ├── auth.ts                 # Auth utilities
    │   └── constants.ts            # App constants
    ├── types/
    │   └── index.ts                # TypeScript types
    └── styles/
        └── globals.css             # Tailwind CSS
```

### 4.2 Key Pages

| Page | URL | Description |
|------|-----|-------------|
| Landing | `/` | Marketing page, app download |
| Login | `/login` | Phone OTP authentication |
| Dashboard | `/dashboard` | Overview, streaks, quick start |
| Topics | `/practice` | Browse and select conversation topics |
| Conversation | `/practice/[topicId]` | Real-time voice conversation |
| Vocabulary | `/vocabulary` | Spaced repetition flashcards |
| Progress | `/progress` | Charts, history, achievements |
| Parent | `/parent` | Parent dashboard with child's progress |

---

## 5. External API Integration

### 5.1 API Dependencies

```
┌─────────────────────────────────────────────────────────────────────┐
│                    EXTERNAL API INTEGRATION                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  OpenAI API                                                    │  │
│  │  ├── Whisper API → Speech-to-Text                              │  │
│  │  │   Endpoint: POST /v1/audio/transcriptions                   │  │
│  │  │   Model: whisper-1                                          │  │
│  │  │   Cost: $0.006/minute                                       │  │
│  │  │                                                              │  │
│  │  ├── GPT-4o-mini → Conversation + Grammar                      │  │
│  │  │   Endpoint: POST /v1/chat/completions                       │  │
│  │  │   Cost: $0.15/1M input, $0.60/1M output                    │  │
│  │  │                                                              │  │
│  │  ├── TTS API → Text-to-Speech                                  │  │
│  │  │   Endpoint: POST /v1/audio/speech                           │  │
│  │  │   Model: tts-1-hd                                           │  │
│  │  │   Cost: $0.030/1K characters                                │  │
│  │  │                                                              │  │
│  │  └── Embeddings → Semantic search                              │  │
│  │      Endpoint: POST /v1/embeddings                             │  │
│  │      Model: text-embedding-3-small                             │  │
│  │      Cost: $0.02/1M tokens                                     │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  Deepgram (Optional, Premium tier)                             │  │
│  │  ├── Nova-2 → Streaming ASR                                    │  │
│  │  │   WebSocket streaming                                       │  │
│  │  │   Cost: $0.0043/minute                                      │  │
│  │  └── Use for: Real-time transcription during conversation      │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  FPT.AI (Vietnamese TTS)                                       │  │
│  │  ├── Vietnamese voice synthesis                                 │  │
│  │  ├── Cost: 500K VND/month (unlimited)                          │  │
│  │  └── Use for: Vietnamese explanations in feedback               │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  Zalo OA API (Notifications)                                   │  │
│  │  ├── Weekly progress reports to parents                        │  │
│  │  ├── Streak reminders                                          │  │
│  │  └── Milestone celebrations                                    │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  VNPay / MoMo (Payments)                                       │  │
│  │  ├── Subscription payments                                     │  │
│  │  ├── QR code payment                                           │  │
│  │  └── Webhook for payment confirmation                          │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 5.2 API Cost Model (per 1000 active users/month)

| API | Usage/User/Month | Unit Cost | Cost/User | Cost/1000 Users |
|-----|-----------------|-----------|-----------|-----------------|
| Whisper ASR | 120 min | $0.006/min | $0.72 | $720 |
| GPT-4o-mini | 50K tokens | $0.15/1M | $0.008 | $8 |
| TTS (tts-1-hd) | 10K chars | $0.030/1K | $0.30 | $300 |
| Embeddings | 5K tokens | $0.02/1M | $0.0001 | $0.1 |
| Deepgram (optional) | 60 min | $0.0043/min | $0.26 | $260 |
| FPT.AI | flat | 500K VND/mo | - | $20 |
| **Total** | | | **$1.03** | **$1,028** |

---

## 6. Environment Variables

### 6.1 Complete Environment Configuration

```bash
# =============================================================================
# AI English Coach — Environment Variables
# =============================================================================

# ---- Application ----
APP_NAME=ai-english-coach
APP_ENV=development|staging|production
DEBUG=true|false
SECRET_KEY=<random-32-chars>
APP_PORT=8000

# ---- Database ----
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/dbname
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10

# ---- Redis ----
REDIS_URL=redis://host:6379/0

# ---- Qdrant ----
QDRANT_URL=http://host:6333
QDRANT_COLLECTION=english_coach

# ---- S3/MinIO ----
S3_ENDPOINT=http://host:9000
S3_ACCESS_KEY=<access-key>
S3_SECRET_KEY=<secret-key>
S3_BUCKET_AUDIO=audio-recordings

# ---- OpenAI ----
OPENAI_API_KEY=sk-...

# ---- Deepgram ----
DEEPGRAM_API_KEY=...

# ---- FPT.AI ----
FPT_API_KEY=...

# ---- Zalo OA ----
ZALO_OA_APP_ID=...
ZALO_OA_APP_SECRET=...

# ---- VNPay ----
VNPAY_TMN_CODE=...
VNPAY_HASH_SECRET=...
VNPAY_RETURN_URL=https://aistudy.io.vn/payment/return

# ---- MoMo ----
MOMO_PARTNER_CODE=...
MOMO_ACCESS_KEY=...
MOMO_SECRET_KEY=...

# ---- Frontend ----
NEXT_PUBLIC_API_URL=https://aistudy.io.vn/api
NEXT_PUBLIC_WS_URL=wss://aistudy.io.vn/ws
NEXT_PUBLIC_APP_NAME=AI English Coach

# ---- Monitoring ----
SENTRY_DSN=https://...@sentry.io/...
POSTHOG_KEY=phc_...
```

---

## 7. Deployment Commands

### 7.1 First-Time Setup

```bash
# 1. Clone repo
git clone https://github.com/tmctuyen201/ai-english-coach.git
cd ai-english-coach

# 2. Copy environment template
cp infra/docker/.env.template .env
# Edit .env with your API keys

# 3. Deploy
chmod +x infra/scripts/deploy.sh
./infra/scripts/deploy.sh

# 4. Verify
curl http://localhost:8000/health
# → {"status":"healthy","version":"1.0.0"}
```

### 7.2 Production Deployment

```bash
# Build production images
BUILD_TARGET=production docker compose build

# Deploy with production config
docker compose -f docker-compose.yml up -d

# Run migrations
docker compose exec backend alembic upgrade head

# Verify all services
docker compose ps
```

### 7.3 Monitoring

```bash
# View logs
docker compose logs -f backend --tail 100
docker compose logs -f frontend --tail 100

# Check resource usage
docker stats

# Celery monitoring
open http://localhost:5555  # Flower dashboard

# MinIO console
open http://localhost:9001  # MinIO dashboard
```

---

## 8. Scaling Strategy

### 8.1 Horizontal Scaling

```bash
# Scale backend instances
docker compose up -d --scale backend=5

# Scale celery workers
docker compose up -d --scale celery_worker=8
```

### 8.2 Vertical Scaling (Server Upgrade Path)

| Phase | Users | Server | Cost/Month |
|-------|-------|--------|------------|
| MVP | 0-1K | 4 CPU, 8GB RAM | $20 |
| Growth | 1K-10K | 8 CPU, 16GB RAM | $50 |
| Scale | 10K-100K | 16 CPU, 32GB RAM + read replicas | $200 |
| Scale+ | 100K+ | Multi-server, load balancer | $500+ |

### 8.3 CDN Strategy

```
Cloudflare (Free tier):
├── Cache static assets (JS, CSS, images) — TTL: 1 year
├── Cache TTS audio (common phrases) — TTL: 1 hour
├── DDoS protection
├── SSL certificate (free)
└── Page rules for /api/* (bypass cache)
```
