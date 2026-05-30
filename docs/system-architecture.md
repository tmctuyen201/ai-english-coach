# AI English Coach — System Architecture (Detailed)

> **Version:** 2.0.0 | **Last Updated:** 2026-05-30

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [User Journey Flow](#2-user-journey-flow)
3. [Authentication System](#3-authentication-system)
4. [Conversation Engine (Core)](#4-conversation-engine-core)
5. [Speech-to-Text (ASR) Pipeline](#5-speech-to-text-asr-pipeline)
6. [LLM Agent System](#6-llm-agent-system)
7. [Text-to-Speech (TTS) Pipeline](#7-text-to-speech-tts-pipeline)
8. [Grammar Checking Engine](#8-grammar-checking-engine)
9. [Pronunciation Scoring Engine](#9-pronunciation-scoring-engine)
10. [Vocabulary & Spaced Repetition](#10-vocabulary--spaced-repetition)
11. [Database Design](#11-database-design)
12. [Real-Time WebSocket Protocol](#12-real-time-websocket-protocol)
13. [Caching Architecture](#13-caching-architecture)
14. [External API Integration](#14-external-api-integration)
15. [Error Handling & Recovery](#15-error-handling--recovery)
16. [Security Architecture](#16-security-architecture)
17. [Monitoring & Observability](#17-monitoring--observability)
18. [Deployment Architecture](#18-deployment-architecture)
19. [Scaling Strategy](#19-scaling-strategy)
20. [Cost Analysis](#20-cost-analysis)

---

## 1. System Overview

### 1.1 What The System Does

AI English Coach is a platform where Vietnamese students practice speaking English with an AI conversation partner. The system:

1. **Listens** to the student speak (Speech-to-Text)
2. **Analyzes** their grammar, pronunciation, and fluency
3. **Responds** with a natural conversation reply (LLM)
4. **Speaks** the response back (Text-to-Speech)
5. **Shows** real-time feedback (grammar corrections, pronunciation scores)
6. **Tracks** progress over time (analytics, spaced repetition)

### 1.2 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        SYSTEM ARCHITECTURE                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  STUDENT DEVICE                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Mobile App (React Native) / Web App (Next.js)                  │    │
│  │                                                                  │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │    │
│  │  │  Mic      │  │  Speaker  │  │  Screen   │  │  Camera   │       │    │
│  │  │  (Input)  │  │  (Output) │  │  (UI)     │  │  (Photo)  │       │    │
│  │  └────┬─────┘  └────▲─────┘  └────┬─────┘  └────┬─────┘       │    │
│  │       │              │              │              │              │    │
│  │       ▼              │              ▼              ▼              │    │
│  │  ┌──────────────────┐│  ┌──────────────────────────────┐        │    │
│  │  │  Audio Recorder   ││  │  UI Components               │        │    │
│  │  │  (WebRTC/Expo AV) ││  │  ├── Chat Bubbles            │        │    │
│  │  │  16kHz, mono      ││  │  ├── Grammar Highlights      │        │    │
│  │  └────────┬──────────┘│  │  ├── Pronunciation Scores    │        │    │
│  │           │            │  │  ├── Vocabulary Cards        │        │    │
│  │           ▼            │  │  └── Progress Charts         │        │    │
│  │  ┌────────────────────┘  └──────────────────────────────┘        │    │
│  │  │  WebSocket Client    ◀──── Real-time bidirectional ────▶      │    │
│  └──┴───────────────────────────────────────────────────────────────┘    │
│       │                                                                  │
│       │  WebSocket (wss://) / HTTPS                                      │
│       ▼                                                                  │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  NGINX REVERSE PROXY                                            │    │
│  │  ├── SSL termination (TLS 1.3)                                  │    │
│  │  ├── Rate limiting (30 req/s API, 5 req/s auth)                │    │
│  │  ├── WebSocket upgrade (/ws/*)                                  │    │
│  │  └── Route to backend or frontend                               │    │
│  └────────────────────────────┬────────────────────────────────────┘    │
│                                │                                         │
│       ┌────────────────────────┼────────────────────────┐               │
│       ▼                        ▼                        ▼               │
│  ┌──────────┐          ┌──────────────┐          ┌──────────┐          │
│  │ FRONTEND  │          │   BACKEND     │          │  WORKERS  │          │
│  │ Next.js   │          │   FastAPI     │          │  Celery   │          │
│  │ SSR/SSG   │          │   REST+WS     │          │  Async    │          │
│  └──────────┘          └──────┬───────┘          └──────────┘          │
│                                │                                         │
│  ┌─────────────────────────────┼───────────────────────────────────┐    │
│  │                    SERVICE LAYER                                  │    │
│  │                              │                                    │    │
│  │  ┌───────────────────────────┼──────────────────────────────┐   │    │
│  │  │                    CONVERSATION ENGINE                     │   │    │
│  │  │                           │                                │   │    │
│  │  │    ┌──────────────────────┼──────────────────────┐       │   │    │
│  │  │    │                      │                      │       │   │    │
│  │  │    ▼                      ▼                      ▼       │   │    │
│  │  │  ┌─────────┐      ┌─────────────┐      ┌─────────┐     │   │    │
│  │  │  │  ASR     │      │  LLM AGENT   │      │  TTS     │     │   │    │
│  │  │  │  Engine  │      │  (GPT-4o-    │      │  Engine  │     │   │    │
│  │  │  │          │      │   mini)       │      │          │     │   │    │
│  │  │  └────┬─────┘      └──────┬──────┘      └────┬─────┘     │   │    │
│  │  │       │                    │                    │          │   │    │
│  │  │       ▼                    ▼                    ▼          │   │    │
│  │  │  ┌─────────┐      ┌─────────────┐      ┌─────────┐     │   │    │
│  │  │  │ Grammar  │      │  Response    │      │  Audio   │     │   │    │
│  │  │  │ Checker  │      │  Generator   │      │  Cache   │     │   │    │
│  │  │  └─────────┘      └─────────────┘      └─────────┘     │   │    │
│  │  │                                                          │   │    │
│  │  │  ┌─────────┐      ┌─────────────┐                       │   │    │
│  │  │  │ Pronunc. │      │  Feedback    │                       │   │    │
│  │  │  │ Scorer   │      │  Generator   │                       │   │    │
│  │  │  └─────────┘      └─────────────┘                       │   │    │
│  │  └──────────────────────────────────────────────────────────┘   │    │
│  │                                                                  │    │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐   │    │
│  │  │  USER SERVICE   │  │  LEARNING       │  │  ANALYTICS      │   │    │
│  │  │  Auth, Profile  │  │  Topics, Vocab  │  │  Progress, Report│   │    │
│  │  └────────────────┘  └────────────────┘  └────────────────┘   │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                │                                         │
│  ┌─────────────────────────────┼───────────────────────────────────┐    │
│  │                    DATA LAYER                                    │    │
│  │                              │                                    │    │
│  │  ┌──────────┐  ┌──────────┐ │ ┌──────────┐  ┌──────────┐      │    │
│  │  │PostgreSQL │  │  Redis    │ │ │  Qdrant   │  │  MinIO    │      │    │
│  │  │           │  │           │ │ │           │  │           │      │    │
│  │  │ Users     │  │ Sessions  │ │ │ Vectors   │  │ Audio     │      │    │
│  │  │ Sessions  │  │ Cache     │ │ │ Knowledge │  │ Files     │      │    │
│  │  │ Turns     │  │ OTP       │ │ │ Base      │  │ Recordings│      │    │
│  │  │ Vocab     │  │ Rate Limit│ │ │ Embeddings│  │           │      │    │
│  │  └──────────┘  └──────────┘ └ └──────────┘  └──────────┘      │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  EXTERNAL APIs                                                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │  OpenAI   │  │ Deepgram  │  │  FPT.AI   │  │  Zalo OA  │              │
│  │  Whisper  │  │  Nova-2   │  │  VN TTS   │  │  Notify   │              │
│  │  GPT-4o   │  │  Stream   │  │           │  │           │              │
│  │  TTS      │  │  ASR      │  │           │  │           │              │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘              │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. User Journey Flow

### 2.1 Complete User Journey (First Time → Daily User)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    USER JOURNEY — FIRST TIME USER                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  STEP 1: DISCOVERY                                                       │
│  ├── User sees ad on TikTok / friend recommends                         │
│  ├── Opens link → Landing page (Next.js SSR)                            │
│  ├── Clicks "Thử Miễn Phí" (Try Free) button                           │
│  └── Redirects to /login                                                │
│                                                                          │
│  STEP 2: AUTHENTICATION                                                  │
│  ├── Enters phone number: 0902xxx                                       │
│  ├── Clicks "Gửi mã OTP" (Send OTP)                                    │
│  ├── Frontend POST /api/v1/auth/phone/send-otp                          │
│  │   ├── Backend generates 6-digit OTP                                  │
│  │   ├── Stores OTP in Redis (TTL: 5 minutes)                           │
│  │   ├── Sends SMS via Twilio/Viettel                                  │
│  │   └── Returns { message: "OTP sent" }                               │
│  ├── User enters OTP: 123456                                            │
│  ├── Frontend POST /api/v1/auth/phone/verify                            │
│  │   ├── Backend checks OTP against Redis                               │
│  │   ├── If match: create/find user in PostgreSQL                       │
│  │   ├── Generate JWT access_token (24h) + refresh_token (30d)         │
│  │   ├── Delete OTP from Redis                                          │
│  │   └── Returns { access_token, refresh_token }                       │
│  └── Frontend stores tokens in localStorage, redirects to /dashboard    │
│                                                                          │
│  STEP 3: ONBOARDING (First Visit)                                        │
│  ├── Dashboard shows welcome screen                                      │
│  ├── Quick setup:                                                       │
│  │   ├── "Bạn bao nhiêu tuổi?" → Select age                            │
│  │   ├── "Bạn học lớp mấy?" → Select grade                             │
│  │   ├── "Mục tiêu học tiếng Anh?" → Select goal                       │
│  │   │   ├── 🏫 Điểm cao trên lớp                                      │
│  │   │   ├── 🎯 Thi IELTS/TOEIC                                        │
│  │   │   ├── 💬 Giao tiếp tự nhiên                                     │
│  │   │   └── 🎮 Xem phim, chơi game không phụ đề                       │
│  │   └── "Bạn muốn luyện bao lâu mỗi ngày?" → Select 10/15/30 min     │
│  ├── System sets initial CEFR level based on answers                    │
│  └── Shows "Bắt đầu luyện tập!" (Start practicing!) CTA                │
│                                                                          │
│  STEP 4: FIRST CONVERSATION                                              │
│  ├── Redirects to /practice (topic selection)                           │
│  ├── Shows recommended topics based on level                            │
│  ├── User taps "Chào hỏi" (Greetings) topic                            │
│  ├── Frontend POST /api/v1/conversations/start                          │
│  │   ├── Backend creates session in PostgreSQL                          │
│  │   ├── Loads topic data (scenario, AI role, target vocabulary)       │
│  │   ├── Generates AI greeting via LLM                                 │
│  │   ├── Generates TTS audio for greeting                              │
│  │   └── Returns { session_id, greeting, audio_url }                   │
│  ├── Frontend opens WebSocket to /ws/v1/conversations/{session_id}     │
│  ├── AI greeting plays through speaker                                  │
│  ├── Student holds mic button and speaks                                │
│  │   ... (see Section 4 for full conversation flow)                     │
│  └── After 8-15 turns, session ends with summary                       │
│                                                                          │
│  STEP 5: POST-CONVERSATION                                               │
│  ├── Shows summary card:                                                │
│  │   ├── Overall score: 72/100                                          │
│  │   ├── Grammar: 78/100                                                │
│  │   ├── Pronunciation: 65/100                                          │
│  │   ├── New words learned: 3                                           │
│  │   └── Duration: 8 minutes                                            │
│  ├── Shows top 3 strengths + top 3 improvements                        │
│  ├── "Luyện tiếp" (Continue) or "Về trang chủ" (Home)                 │
│  └── XP earned: +50 points, streak: 1 day                              │
│                                                                          │
│  STEP 6: DAILY RETURN                                                    │
│  ├── Day 2: Push notification "Bạn đã luyện 1 ngày liên tiếp! 🔥"    │
│  ├── Opens app → Dashboard shows streak: 1                             │
│  ├── Quick start: "Tiếp tục luyện" (Continue practicing)              │
│  ├── After 7 days: Achievement unlocked "7 Ngày Liên Tiếp!" 🏆        │
│  └── After 14 days: Prompt "Nâng cấp Premium để luyện không giới hạn" │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Authentication System

### 3.1 Phone OTP Flow (Vietnamese Market)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    AUTHENTICATION FLOW                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  WHY PHONE + OTP (not email + password):                                │
│  ├── Vietnamese users prefer phone-based auth (Zalo, Grab pattern)     │
│  ├── No password to remember (lower friction)                           │
│  ├── SMS OTP is familiar (banking apps use it)                          │
│  └── Phone number = unique identifier (no duplicate accounts)          │
│                                                                          │
│  FLOW:                                                                   │
│                                                                          │
│  ┌──────────┐     POST /api/v1/auth/phone/send-otp                     │
│  │  Client   │ ────────────────────────────────────────▶ ┌──────────┐  │
│  │  enters   │     { phone: "0902xxx" }                   │  Backend  │  │
│  │  phone    │                                            │           │  │
│  └──────────┘                                            └─────┬────┘  │
│                                                                 │        │
│  Backend:                                                       │        │
│  ├── 1. Validate phone format (VN: 0xx-xxx-xxxx)               │        │
│  ├── 2. Rate limit: max 3 OTP/hour per phone                   │        │
│  ├── 3. Generate 6-digit OTP: random.randint(100000, 999999)   │        │
│  ├── 4. Store in Redis:                                          │        │
│  │      key: "otp:0902xxx"                                      │        │
│  │      value: "123456"                                         │        │
│  │      TTL: 300 seconds (5 minutes)                            │        │
│  ├── 5. Send SMS via provider:                                   │        │
│  │      "Ma xac nhan AI English Coach cua ban la: 123456"      │        │
│  └── 6. Return: { message: "OTP sent", phone: "0902xxx" }      │        │
│                                                                 │        │
│  ┌──────────┐     POST /api/v1/auth/phone/verify               │        │
│  │  Client   │ ────────────────────────────────────────▶ ┌─────┴────┐  │
│  │  enters   │     { phone: "0902xxx", otp: "123456" }   │  Backend  │  │
│  │  OTP      │                                            │           │  │
│  └──────────┘                                            └─────┬────┘  │
│                                                                 │        │
│  Backend:                                                       │        │
│  ├── 1. Get stored OTP from Redis: "otp:0902xxx"               │        │
│  ├── 2. Compare: stored_otp == submitted_otp?                  │        │
│  ├── 3. If mismatch: return 400 "Invalid or expired OTP"       │        │
│  ├── 4. If match:                                                │        │
│  │      a. Delete OTP from Redis (one-time use)                │        │
│  │      b. Find or create user in PostgreSQL:                  │        │
│  │         SELECT * FROM users WHERE phone = '0902xxx'        │        │
│  │         IF not found:                                        │        │
│  │           INSERT INTO users (phone, name) VALUES (...)      │        │
│  │      c. Generate JWT tokens:                                 │        │
│  │         access_token = jwt.encode(                           │        │
│  │           { "sub": user_id, "phone": "0902xxx",             │        │
│  │             "plan": "free", "exp": now + 24h },             │        │
│  │           secret_key, algorithm="HS256")                    │        │
│  │         refresh_token = jwt.encode(                          │        │
│  │           { "sub": user_id, "type": "refresh",              │        │
│  │             "exp": now + 30d },                              │        │
│  │           secret_key, algorithm="HS256")                    │        │
│  │      d. Update user.last_active_at                          │        │
│  │      e. Return: { access_token, refresh_token }             │        │
│  │                                                              │        │
│  ┌──────────┐                                                    │        │
│  │  Client   │ stores tokens in localStorage                    │        │
│  │  stores   │ redirects to /dashboard                          │        │
│  │  tokens   │ All future requests: Authorization: Bearer <JWT> │        │
│  └──────────┘                                                    │        │
│                                                                          │
│  TOKEN REFRESH FLOW:                                                     │
│  ├── access_token expires after 24 hours                                │
│  ├── Client detects 401 Unauthorized                                    │
│  ├── Client POST /api/v1/auth/refresh { refresh_token }                │
│  ├── Backend validates refresh_token                                    │
│  ├── If valid: issue new access_token                                   │
│  └── If expired: redirect to /login                                     │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Conversation Engine (Core)

### 4.1 End-to-End Conversation Flow

This is the **core of the entire system**. When a student speaks, here's exactly what happens:

```
┌─────────────────────────────────────────────────────────────────────────┐
│              CONVERSATION ENGINE — END-TO-END FLOW                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  TOTAL LATENCY TARGET: < 3 seconds from student finishing speech        │
│  to AI audio starting to play                                           │
│                                                                          │
│  ═══════════════════════════════════════════════════════════════════     │
│  PHASE 1: AUDIO CAPTURE (Student's Device)                              │
│  ═══════════════════════════════════════════════════════════════════     │
│                                                                          │
│  Student taps and holds mic button                                      │
│       │                                                                  │
│       ▼                                                                  │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  WebRTC Audio Capture                                            │    │
│  │  ├── Sample rate: 16,000 Hz                                      │    │
│  │  ├── Channels: Mono (1)                                          │    │
│  │  ├── Encoding: WebM/Opus (compressed, low bandwidth)            │    │
│  │  ├── Chunk size: 100ms per frame                                 │    │
│  │  └── Noise suppression: Browser built-in (RNNoise)              │    │
│  └──────────────────────────────┬──────────────────────────────────┘    │
│                                  │                                       │
│                                  ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Voice Activity Detection (VAD) — Client-side                    │    │
│  │  ├── Detect when student starts speaking                        │    │
│  │  ├── Detect when student stops speaking (silence > 1.5s)        │    │
│  │  ├── Auto-send "audio_end" when silence detected                │    │
│  │  └── Prevents sending empty audio to server                     │    │
│  └──────────────────────────────┬──────────────────────────────────┘    │
│                                  │                                       │
│                                  ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  WebSocket: Send audio chunks to server                          │    │
│  │  ├── Binary frames: raw audio data                              │    │
│  │  ├── Text frames: control messages (audio_start, audio_end)     │    │
│  │  └── Compression: WebSocket per-message deflate                 │    │
│  └──────────────────────────────┬──────────────────────────────────┘    │
│                                  │                                       │
│  ═══════════════════════════════════════════════════════════════════     │
│  PHASE 2: SPEECH-TO-TEXT (Server)                                       │
│  ═══════════════════════════════════════════════════════════════════     │
│                                  │                                       │
│                                  ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  ASR PIPELINE                                                    │    │
│  │                                                                  │    │
│  │  Option A: OpenAI Whisper API (Free/Basic tier)                 │    │
│  │  ├── Send complete audio file after student stops speaking      │    │
│  │  ├── Model: whisper-1                                           │    │
│  │  ├── Language: "en" (optimize for English)                      │    │
│  │  ├── Response: { text: "I want to eat pho please" }            │    │
│  │  ├── Latency: 1-2 seconds                                       │    │
│  │  └── Cost: $0.006 per minute of audio                          │    │
│  │                                                                  │    │
│  │  Option B: Deepgram Nova-2 (Premium tier)                       │    │
│  │  ├── Stream audio chunks in real-time                           │    │
│  │  ├── Receive partial transcripts as student speaks              │    │
│  │  ├── Model: nova-2                                              │    │
│  │  ├── Response: streaming partial → final transcript             │    │
│  │  ├── Latency: 200-500ms                                         │    │
│  │  └── Cost: $0.0043 per minute of audio                         │    │
│  │                                                                  │    │
│  │  Selection Logic:                                                │    │
│  │  ├── Free tier → Whisper (batch, cheaper)                       │    │
│  │  └── Premium tier → Deepgram (streaming, better UX)            │    │
│  └──────────────────────────────┬──────────────────────────────────┘    │
│                                  │                                       │
│                                  ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Transcript Post-Processing                                      │    │
│  │  ├── Capitalize first letter                                    │    │
│  │  ├── Fix common ASR errors (Vietnamese accent patterns)         │    │
│  │  ├── Confidence score check (if < 0.7, ask for confirmation)   │    │
│  │  └── Final transcript: "I want to eat pho please"              │    │
│  └──────────────────────────────┬──────────────────────────────────┘    │
│                                  │                                       │
│  ═══════════════════════════════════════════════════════════════════     │
│  PHASE 3: PARALLEL ANALYSIS (Server)                                    │
│  ═══════════════════════════════════════════════════════════════════     │
│                                  │                                       │
│                    ┌─────────────┼─────────────┐                        │
│                    ▼             ▼             ▼                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │
│  │  GRAMMAR      │  │  LLM AGENT    │  │  PRONUNCIATION│                 │
│  │  CHECKER      │  │  (Response)   │  │  SCORER       │                 │
│  │              │  │              │  │              │                 │
│  │  Input:      │  │  Input:      │  │  Input:      │                 │
│  │  "I want to  │  │  student text│  │  audio + text│                 │
│  │  eat pho     │  │  + conversation│  │              │                 │
│  │  please"     │  │  history     │  │  Process:    │                 │
│  │              │  │              │  │  1. Forced   │                 │
│  │  Process:    │  │  Process:    │  │  alignment  │                 │
│  │  1. Rule-based│  │  1. Build    │  │  2. Phoneme │                 │
│  │  patterns    │  │  context     │  │  comparison │                 │
│  │  2. Language │  │  2. Generate │  │  3. Score   │                 │
│  │  Tool API    │  │  response    │  │  each word  │                 │
│  │  3. LLM      │  │  3. Include  │  │              │                 │
│  │  grammar     │  │  corrections │  │  Output:    │                 │
│  │              │  │              │  │  overall: 72│                 │
│  │  Output:     │  │  Output:     │  │  words: [   │                 │
│  │  corrected   │  │  "Great      │  │    {word:   │                 │
│  │  text + score│  │  choice!     │  │    score}   │                 │
│  │              │  │  Would you   │  │  ]          │                 │
│  │  Latency:    │  │  like beef   │  │              │                 │
│  │  ~500ms      │  │  or chicken?"│  │  Latency:   │                 │
│  │              │  │              │  │  ~800ms     │                 │
│  │              │  │  Latency:    │  │              │                 │
│  │              │  │  ~1.5s       │  │              │                 │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘                 │
│         │                 │                 │                          │
│         └─────────────────┼─────────────────┘                          │
│                           ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  RESULT MERGER                                                   │    │
│  │  Combines all three results into single response:               │    │
│  │  {                                                               │    │
│  │    "ai_text": "Great choice! Would you like beef or chicken?",  │    │
│  │    "grammar": {                                                  │    │
│  │      "corrections": [{                                           │    │
│  │        "original": "I want to eat pho please",                  │    │
│  │        "corrected": "I'd like to have pho, please",            │    │
│  │        "explanation_vi": "Dùng 'I'd like' cho lịch sự hơn"    │    │
│  │      }],                                                         │    │
│  │      "score": 65                                                 │    │
│  │    },                                                            │    │
│  │    "pronunciation": {                                            │    │
│  │      "overall": 72,                                              │    │
│  │      "words": [                                                  │    │
│  │        {"word": "want", "score": 85},                           │    │
│  │        {"word": "pho", "score": 88},                            │    │
│  │        {"word": "please", "score": 58}                          │    │
│  │      ]                                                           │    │
│  │    }                                                             │    │
│  │  }                                                               │    │
│  └──────────────────────────────┬──────────────────────────────────┘    │
│                                  │                                       │
│  ═══════════════════════════════════════════════════════════════════     │
│  PHASE 4: TEXT-TO-SPEECH (Server)                                       │
│  ═══════════════════════════════════════════════════════════════════     │
│                                  │                                       │
│                                  ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  TTS PIPELINE                                                    │    │
│  │                                                                  │    │
│  │  Input: "Great choice! Would you like beef or chicken pho?"     │    │
│  │                                                                  │    │
│  │  1. Check cache: hash(text + voice + speed) → cached audio?     │    │
│  │     ├── Hit: return cached audio URL                            │    │
│  │     └── Miss: generate new audio                                │    │
│  │                                                                  │    │
│  │  2. Generate audio:                                              │    │
│  │     ├── OpenAI TTS API                                          │    │
│  │     ├── Model: tts-1-hd (high definition)                       │    │
│  │     ├── Voice: nova (mapped from user preference)               │    │
│  │     ├── Speed: 0.9 (slower for learners)                        │    │
│  │     ├── Output: MP3 binary                                      │    │
│  │     └── Latency: ~800ms                                         │    │
│  │                                                                  │    │
│  │  3. Store audio:                                                 │    │
│  │     ├── Upload to MinIO (S3-compatible)                         │    │
│  │     ├── Generate signed URL (expires in 1 hour)                 │    │
│  │     └── Cache URL in Redis (TTL: 1 hour)                        │    │
│  │                                                                  │    │
│  │  4. Return: audio_url = "https://minio.../audio/abc123.mp3"     │    │
│  └──────────────────────────────┬──────────────────────────────────┘    │
│                                  │                                       │
│  ═══════════════════════════════════════════════════════════════════     │
│  PHASE 5: RESPONSE DELIVERY (Server → Client)                           │
│  ═══════════════════════════════════════════════════════════════════     │
│                                  │                                       │
│                                  ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  WebSocket: Send response to client                              │    │
│  │                                                                  │    │
│  │  Message 1: Transcript (immediate)                               │    │
│  │  { type: "transcript_final", text: "I want to eat pho please" } │    │
│  │                                                                  │    │
│  │  Message 2: Feedback (after analysis)                            │    │
│  │  { type: "feedback", grammar: {...}, pronunciation: {...} }     │    │
│  │                                                                  │    │
│  │  Message 3: AI Response (after LLM + TTS)                       │    │
│  │  { type: "ai_response", text: "...", audio_url: "..." }        │    │
│  └──────────────────────────────┬──────────────────────────────────┘    │
│                                  │                                       │
│  ═══════════════════════════════════════════════════════════════════     │
│  PHASE 6: CLIENT RENDERING                                              │
│  ═══════════════════════════════════════════════════════════════════     │
│                                  │                                       │
│                                  ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Client receives messages and:                                   │    │
│  │                                                                  │    │
│  │  1. Show student's transcript in chat bubble                    │    │
│  │  2. Highlight grammar errors inline (red underline)             │    │
│  │  3. Show pronunciation score badge on each word                 │    │
│  │  4. Show grammar correction card (expandable)                   │    │
│  │  5. Play AI response audio through speaker                      │    │
│  │  6. Show AI response text in chat bubble                        │    │
│  │  7. Enable mic button for next turn                             │    │
│  │  8. Update turn counter and session timer                       │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  TOTAL LATENCY BREAKDOWN:                                                │
│  ├── Audio capture → ASR: 1.0-2.0s                                      │
│  ├── ASR → Analysis (parallel): 1.0-1.5s                                │
│  ├── Analysis → TTS: 0.8-1.0s                                           │
│  ├── TTS → Client receives: 0.2-0.5s                                    │
│  └── TOTAL: 3.0-5.0s (target: < 3s for premium)                        │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Conversation State Machine

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    CONVERSATION STATE MACHINE                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│                        ┌───────────┐                                     │
│                        │   IDLE     │                                     │
│                        └─────┬─────┘                                     │
│                              │ POST /conversations/start                 │
│                              ▼                                           │
│                        ┌───────────┐                                     │
│                        │  TOPIC     │                                     │
│                        │  INTRO     │ ← AI greets, plays TTS             │
│                        └─────┬─────┘                                     │
│                              │ Student speaks or types                    │
│                              ▼                                           │
│                   ┌─────────────────────┐                                │
│                   │     LISTENING        │                                │
│                   │  (audio streaming)   │                                │
│                   └──────────┬──────────┘                                │
│                              │ audio_end / turn_complete                 │
│                              ▼                                           │
│                   ┌─────────────────────┐                                │
│                   │     PROCESSING       │                                │
│                   │  ASR + Grammar +     │                                │
│                   │  LLM + TTS (parallel)│                                │
│                   └──────────┬──────────┘                                │
│                              │ all complete                              │
│                              ▼                                           │
│                   ┌─────────────────────┐                                │
│                   │     RESPONDING       │                                │
│                   │  Send feedback +     │                                │
│                   │  AI response + audio │                                │
│                   └──────────┬──────────┘                                │
│                              │                                           │
│              ┌───────────────┼───────────────┐                           │
│              ▼                               ▼                           │
│     ┌────────────────┐              ┌────────────────┐                   │
│     │  turn < max     │              │  turn >= max    │                   │
│     │  (continue)     │              │  (end session)  │                   │
│     └────────┬───────┘              └────────┬───────┘                   │
│              │                               │                           │
│              ▼                               ▼                           │
│     ┌────────────────┐              ┌────────────────┐                   │
│     │  NEXT TURN      │              │  WRAP UP        │                   │
│     │  (back to       │              │  Generate       │                   │
│     │   LISTENING)    │              │  summary report │                   │
│     └────────────────┘              └────────┬───────┘                   │
│                                              │                           │
│                                              ▼                           │
│                                      ┌────────────────┐                  │
│                                      │  COMPLETED       │                  │
│                                      │  Show results,  │                  │
│                                      │  save to DB     │                  │
│                                      └────────────────┘                  │
│                                                                          │
│  PAUSE/RESUME:                                                           │
│  ├── Student can pause at any time (saves state)                        │
│  ├── Session stays active for 30 minutes                                │
│  └── After 30 min idle → auto-abandoned                                 │
│                                                                          │
│  ERROR STATES:                                                           │
│  ├── ASR_TIMEOUT → Ask "Could you repeat that?" (text fallback)        │
│  ├── LLM_TIMEOUT → Use pre-written response                            │
│  ├── TTS_ERROR → Show text only (no audio)                             │
│  └── NETWORK_ERROR → Save state, offer reconnect                       │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Speech-to-Text (ASR) Pipeline

### 5.1 ASR Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    ASR PIPELINE — DETAILED                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  INPUT:                                                                  │
│  ├── Format: WebM with Opus codec                                       │
│  ├── Sample rate: 16,000 Hz                                             │
│  ├── Channels: Mono                                                     │
│  ├── Duration: 2-30 seconds per utterance                               │
│  └── Quality: Variable (phone mic, ambient noise)                       │
│                                                                          │
│  PROCESSING:                                                             │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Step 1: Audio Preprocessing                                     │    │
│  │  ├── Decode WebM → PCM (raw audio)                              │    │
│  │  ├── Normalize volume (peak normalization)                      │    │
│  │  ├── Remove silence from start/end (trim)                       │    │
│  │  └── Resample to 16kHz if needed                                │    │
│  └──────────────────────────────┬──────────────────────────────────┘    │
│                                  │                                       │
│                                  ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Step 2: ASR Model                                               │    │
│  │                                                                  │    │
│  │  Option A: OpenAI Whisper (Batch)                                │    │
│  │  ├── Send complete audio file                                   │    │
│  │  ├── Model: whisper-1 (large-v2 equivalent)                     │    │
│  │  ├── Parameters:                                                │    │
│  │  │   language: "en"                                              │    │
│  │  │   task: "transcribe" (not translate)                          │    │
│  │  │   temperature: 0.0 (deterministic)                           │    │
│  │  │   best_of: 1                                                  │    │
│  │  └── Response: { text: "I want to eat pho please" }            │    │
│  │                                                                  │    │
│  │  Option B: Deepgram Nova-2 (Streaming)                           │    │
│  │  ├── Stream audio chunks via WebSocket                          │    │
│  │  ├── Receive partial results:                                    │    │
│  │  │   Chunk 1: "I"                                               │    │
│  │  │   Chunk 2: "I want"                                          │    │
│  │  │   Chunk 3: "I want to eat"                                   │    │
│  │  │   Final: "I want to eat pho please"                          │    │
│  │  ├── Parameters:                                                │    │
│  │  │   model: "nova-2"                                             │    │
│  │  │   language: "en"                                              │    │
│  │  │   smart_format: true                                          │    │
│  │  │   interim_results: true                                       │    │
│  │  │   endpointing: 300 (ms of silence = end of utterance)       │    │
│  │  └── Response: streaming partials → final                       │    │
│  └──────────────────────────────┬──────────────────────────────────┘    │
│                                  │                                       │
│                                  ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Step 3: Post-Processing                                         │    │
│  │  ├── Capitalize first letter                                    │    │
│  │  ├── Fix Vietnamese accent patterns:                            │    │
│  │  │   "pho" → "pho" (keep as-is, it's a valid English word)    │    │
│  │  │   "xin chào" → remove (student switched to Vietnamese)      │    │
│  │  ├── Remove filler words if too many:                           │    │
│  │  │   "um um I want um pho" → "I want pho"                     │    │
│  │  ├── Confidence check:                                          │    │
│  │  │   if confidence < 0.7 → send partial to client for confirm  │    │
│  │  └── Return final transcript                                    │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  VIETNAMESE ACCENT HANDLING:                                             │
│  ├── /θ/ → often transcribed as /t/ or /s/ (think → "tink")           │
│  ├── /ð/ → often transcribed as /d/ (the → "de")                       │
│  ├── /v/ → often transcribed as /b/ (very → "bery")                    │
│  ├── /r/ and /l/ → confused (right → "light")                          │
│  ├── Final consonants → often dropped (good → "goo")                   │
│  └── ASR models handle these better than rule-based systems            │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 5.2 ASR Configuration

```python
# ASR Configuration for different tiers
ASR_CONFIG = {
    "free_tier": {
        "provider": "openai_whisper",
        "model": "whisper-1",
        "mode": "batch",                    # Send complete audio
        "language": "en",
        "temperature": 0.0,
        "cost_per_minute": 0.006,           # USD
        "latency_typical": "1.5s",
        "latency_p95": "3.0s",
        "max_audio_duration": 120,          # seconds
    },
    "premium_tier": {
        "provider": "deepgram",
        "model": "nova-2",
        "mode": "streaming",                # Real-time streaming
        "language": "en",
        "smart_format": True,
        "interim_results": True,
        "endpointing": 300,                 # ms silence = end
        "cost_per_minute": 0.0043,          # USD
        "latency_typical": "300ms",
        "latency_p95": "800ms",
        "max_audio_duration": 600,          # seconds
    }
}
```

---

## 6. LLM Agent System

### 6.1 Agent Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    LLM AGENT SYSTEM                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  SYSTEM PROMPT (Invisible to student)                            │    │
│  │                                                                  │    │
│  │  "You are a friendly English conversation partner for            │    │
│  │  Vietnamese students. You are playing the role of:               │    │
│  │  {ai_role} in this scenario: {scenario}.                        │    │
│  │                                                                  │    │
│  │  Rules:                                                          │    │
│  │  1. Keep responses SHORT (1-3 sentences)                        │    │
│  │  2. Use vocabulary appropriate for {cefr_level} level           │    │
│  │  3. If student makes grammar error, correct NATURALLY           │    │
│  │     by using correct form in your response (don't lecture)      │    │
│  │  4. If student seems stuck, give hint or simpler question       │    │
│  │  5. Introduce 1-2 new vocabulary words naturally                │    │
│  │  6. Ask follow-up questions to keep conversation flowing        │    │
│  │  7. Be encouraging, celebrate small wins                        │    │
│  │  8. When topic is covered, naturally wrap up                    │    │
│  │                                                                  │    │
│  │  Target vocabulary: {target_vocabulary}                         │    │
│  │  Target grammar: {target_grammar}                               │    │
│  │  Current turn: {turn_number}/{max_turns}"                       │    │
│  └──────────────────────────────┬──────────────────────────────────┘    │
│                                  │                                       │
│  ┌──────────────────────────────▼──────────────────────────────────┐    │
│  │  CONVERSATION CONTEXT (sliding window)                           │    │
│  │                                                                  │    │
│  │  [System Prompt]                                                 │    │
│  │  [Turn 1] AI: "Welcome! Today we'll practice ordering food..."  │    │
│  │  [Turn 2] Student: "I want to eat pho please"                   │    │
│  │  [Turn 3] AI: "Great choice! Would you like beef or chicken?"   │    │
│  │  [Turn 4] Student: "I like beef"                                │    │
│  │  [Turn 5] AI: "Excellent! Beef pho is very popular..."          │    │
│  │  ...                                                             │    │
│  │  [Current] Student: "How much is it?"                           │    │
│  │                                                                  │    │
│  │  Context window: Last 10 turns (to stay within token limit)     │    │
│  │  Token budget: ~2000 tokens system + ~1000 tokens history       │    │
│  └──────────────────────────────┬──────────────────────────────────┘    │
│                                  │                                       │
│  ┌──────────────────────────────▼──────────────────────────────────┐    │
│  │  RESPONSE GENERATION                                             │    │
│  │                                                                  │    │
│  │  Model: GPT-4o-mini                                              │    │
│  │  Temperature: 0.7 (creative but consistent)                     │    │
│  │  Max tokens: 150 (keep responses short)                         │    │
│  │  Top-p: 0.9                                                      │    │
│  │                                                                  │    │
│  │  Response: "The beef pho is 45,000 dong. Very reasonable!       │    │
│  │  Would you like to add anything else? Maybe some spring rolls?" │    │
│  │                                                                  │    │
│  │  Post-processing:                                                │    │
│  │  ├── Remove any markdown formatting                             │    │
│  │  ├── Ensure response is 1-3 sentences                           │    │
│  │  ├── Check for inappropriate content                            │    │
│  │  └── Add to conversation history                                │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  MODEL SELECTION LOGIC:                                                  │
│  ├── Primary: GPT-4o-mini ($0.15/1M input, $0.60/1M output)           │
│  ├── Fallback: Claude 3.5 Haiku ($0.25/1M input, $1.25/1M output)     │
│  ├── Grammar check: Claude 3.5 Haiku (more accurate for grammar)      │
│  └── If primary fails → auto-switch to fallback                        │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 6.2 Conversation Topics (50+ Topics)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    TOPIC SYSTEM                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Each topic defines:                                                     │
│  ├── id: "ordering-food"                                                │
│  ├── title_en: "Ordering Food at a Restaurant"                          │
│  ├── title_vi: "Gọi Món tại Nhà Hàng"                                 │
│  ├── level: A2                                                          │
│  ├── scenario: "You're at a Vietnamese restaurant with a foreign friend"│
│  ├── ai_role: "Friendly waiter"                                         │
│  ├── target_vocabulary: ["order", "recommend", "bill", "tip"]          │
│  ├── target_grammar: ["I'd like...", "Could I have...?", "How much?"]  │
│  ├── max_turns: 12                                                      │
│  ├── estimated_duration: 8-10 minutes                                   │
│  └── curriculum_alignment: "Grade 10, Unit 5"                          │
│                                                                          │
│  TOPIC CATEGORIES:                                                       │
│                                                                          │
│  A1-A2 (Beginner):                                                       │
│  ├── Greetings & Introductions                                          │
│  ├── Talking About Family                                               │
│  ├── Hobbies & Free Time                                                │
│  ├── Daily Routine                                                      │
│  ├── Food & Drinks                                                      │
│  ├── Weather & Seasons                                                  │
│  ├── Shopping & Prices                                                  │
│  └── Directions & Places                                                │
│                                                                          │
│  B1 (Intermediate):                                                      │
│  ├── School Life & Subjects                                             │
│  ├── Health & Doctor Visit                                              │
│  ├── Travel & Hotels                                                    │
│  ├── Job Interview                                                      │
│  ├── Making Plans with Friends                                          │
│  ├── Describing Experiences                                             │
│  └── Current Events                                                     │
│                                                                          │
│  B2 (Upper Intermediate):                                                │
│  ├── IELTS Part 1 (Personal Questions)                                  │
│  ├── IELTS Part 2 (Cue Card)                                           │
│  ├── IELTS Part 3 (Discussion)                                         │
│  ├── Business Meetings                                                  │
│  ├── Presentations                                                      │
│  └── Debating Opinions                                                  │
│                                                                          │
│  Vietnamese Culture:                                                     │
│  ├── Explaining Tet to a Foreigner                                      │
│  ├── Vietnamese Food Culture                                            │
│  ├── Vietnamese Festivals                                               │
│  ├── Tourist Attractions                                                │
│  └── Vietnamese History                                                 │
│                                                                          │
│  CURRICULUM ALIGNED (GDPT 2018):                                        │
│  ├── Grade 6: Units 1-12                                                │
│  ├── Grade 7: Units 1-12                                                │
│  ├── Grade 8: Units 1-12                                                │
│  ├── Grade 9: Units 1-12                                                │
│  ├── Grade 10: Units 1-12                                               │
│  ├── Grade 11: Units 1-12                                               │
│  └── Grade 12: Units 1-12                                               │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Text-to-Speech (TTS) Pipeline

### 7.1 TTS Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    TTS PIPELINE                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  INPUT: AI response text                                                 │
│  "Great choice! Would you like beef or chicken pho?"                    │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Step 1: Cache Check                                             │    │
│  │                                                                  │    │
│  │  cache_key = hash(text + voice_id + speed)                      │    │
│  │  cached = redis.get(f"tts:{cache_key}")                         │    │
│  │                                                                  │    │
│  │  If cached:                                                      │    │
│  │  ├── Return cached audio URL immediately                        │    │
│  │  └── Latency: ~5ms                                              │    │
│  │                                                                  │    │
│  │  If not cached:                                                  │    │
│  │  └── Continue to Step 2                                         │    │
│  └──────────────────────────────┬──────────────────────────────────┘    │
│                                  │                                       │
│  ┌──────────────────────────────▼──────────────────────────────────┐    │
│  │  Step 2: Voice Selection                                         │    │
│  │                                                                  │    │
│  │  User preference → OpenAI voice mapping:                        │    │
│  │  ├── "friendly_female"     → "nova"     (warm, friendly)        │    │
│  │  ├── "friendly_male"       → "echo"     (clear, friendly)       │    │
│  │  ├── "professional_female" → "shimmer"  (professional)          │    │
│  │  └── "young_energetic"     → "alloy"    (young, energetic)      │    │
│  │                                                                  │    │
│  │  Speed adjustment:                                               │    │
│  │  ├── A1-A2 students: 0.75x (slow, clear)                       │    │
│  │  ├── B1 students: 0.9x (slightly slower than natural)          │    │
│  │  └── B2+ students: 1.0x (natural speed)                        │    │
│  └──────────────────────────────┬──────────────────────────────────┘    │
│                                  │                                       │
│  ┌──────────────────────────────▼──────────────────────────────────┐    │
│  │  Step 3: Audio Generation                                        │    │
│  │                                                                  │    │
│  │  OpenAI TTS API:                                                │    │
│  │  ├── Endpoint: POST https://api.openai.com/v1/audio/speech     │    │
│  │  ├── Model: tts-1-hd (high definition, natural sounding)        │    │
│  │  ├── Input: "Great choice! Would you like beef or chicken pho?" │    │
│  │  ├── Voice: "nova"                                              │    │
│  │  ├── Speed: 0.9                                                 │    │
│  │  ├── Response format: mp3                                       │    │
│  │  └── Latency: ~800ms                                            │    │
│  │                                                                  │    │
│  │  Output: MP3 binary data (~50KB for 5 seconds of speech)        │    │
│  └──────────────────────────────┬──────────────────────────────────┘    │
│                                  │                                       │
│  ┌──────────────────────────────▼──────────────────────────────────┐    │
│  │  Step 4: Storage & Caching                                       │    │
│  │                                                                  │    │
│  │  1. Upload MP3 to MinIO:                                        │    │
│  │     bucket: "audio-recordings"                                  │    │
│  │     key: "tts/{hash}.mp3"                                       │    │
│  │     content_type: "audio/mpeg"                                  │    │
│  │                                                                  │    │
│  │  2. Generate signed URL (expires in 1 hour):                    │    │
│  │     url = minio.presigned_get_object(                           │    │
│  │         bucket="audio-recordings",                              │    │
│  │         object_name=f"tts/{hash}.mp3",                         │    │
│  │         expires=timedelta(hours=1)                              │    │
│  │     )                                                           │    │
│  │                                                                  │    │
│  │  3. Cache URL in Redis:                                         │    │
│  │     redis.setex(f"tts:{cache_key}", 3600, url)                 │    │
│  │                                                                  │    │
│  │  4. Return URL to client                                        │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  TTS COST OPTIMIZATION:                                                  │
│  ├── Cache hit rate: ~30% (common phrases like "Great!", "Good job!")   │
│  ├── Pre-generate topic introductions (50 topics × 1 voice = 50 calls) │
│  ├── Use tts-1 (cheaper) for non-critical audio                        │
│  └── Estimated savings: 40% vs no caching                              │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 8. Grammar Checking Engine

### 8.1 Multi-Layer Grammar Pipeline

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    GRAMMAR CHECKING ENGINE                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  INPUT: Student transcript                                               │
│  "I want to eat pho please"                                             │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  LAYER 1: Rule-Based Patterns (Fast, < 10ms)                    │    │
│  │                                                                  │    │
│  │  Pattern matching for common Vietnamese learner errors:         │    │
│  │                                                                  │    │
│  │  ├── Subject-Verb Agreement:                                    │    │
│  │  │   "He don't" → "He doesn't"                                 │    │
│  │  │   "She have" → "She has"                                     │    │
│  │  │                                                              │    │
│  │  ├── Article Errors:                                            │    │
│  │  │   "I want apple" → "I want an apple"                        │    │
│  │  │   "I like the music" → "I like music" (general)             │    │
│  │  │                                                              │    │
│  │  ├── Tense Markers:                                             │    │
│  │  │   "yesterday" + present tense → suggest past tense           │    │
│  │  │   "tomorrow" + past tense → suggest future tense             │    │
│  │  │                                                              │    │
│  │  ├── Preposition Patterns:                                      │    │
│  │  │   "go to school by Monday" → "go to school on Monday"       │    │
│  │  │   "in the morning" ✓ (correct)                               │    │
│  │  │                                                              │    │
│  │  └── Common VN Learner Errors:                                  │    │
│  │      "I very like" → "I like ... very much"                    │    │
│  │      "I am agree" → "I agree"                                  │    │
│  │      "more better" → "better"                                  │    │
│  └──────────────────────────────┬──────────────────────────────────┘    │
│                                  │                                       │
│  ┌──────────────────────────────▼──────────────────────────────────┐    │
│  │  LAYER 2: Language Tool API (Comprehensive, < 200ms)            │    │
│  │                                                                  │    │
│  │  language_tool_python library (offline, no API cost):           │    │
│  │  ├── Catches: spelling, grammar, punctuation, style             │    │
│  │  ├── Supports: English (US/UK)                                  │    │
│  │  ├── Categories: TYPOS, GRAMMAR, CASING, PUNCTUATION           │    │
│  │  └── Returns: list of matches with offset, length, message      │    │
│  │                                                                  │    │
│  │  Example output:                                                │    │
│  │  [{                                                              │    │
│  │    "rule": "MORFOLOGIK_RULE_EN_US",                             │    │
│  │    "message": "Possible spelling mistake found",                │    │
│  │    "offset": 15,                                                 │    │
│  │    "length": 3,                                                  │    │
│  │    "replacements": ["phase", "phrase"]                          │    │
│  │  }]                                                              │    │
│  └──────────────────────────────┬──────────────────────────────────┘    │
│                                  │                                       │
│  ┌──────────────────────────────▼──────────────────────────────────┐    │
│  │  LAYER 3: LLM Grammar Check (Context-aware, < 1s)              │    │
│  │                                                                  │    │
│  │  Used only when:                                                │    │
│  │  ├── Sentence is complex (> 10 words)                           │    │
│  │  ├── Layer 1+2 found no errors (might be false negative)       │    │
│  │  └── Student level is B2+ (more nuanced errors)                │    │
│  │                                                                  │    │
│  │  Prompt:                                                        │    │
│  │  "Check grammar of: '{text}'                                    │    │
│  │   Student level: {cefr_level}                                   │    │
│  │   Context: {conversation_context}                               │    │
│  │   Return JSON: { corrections: [...], score: 0-100 }"           │    │
│  │                                                                  │    │
│  │  Model: Claude 3.5 Haiku (fast, accurate for grammar)          │    │
│  │  Temperature: 0.1 (deterministic)                               │    │
│  │  Response format: JSON                                          │    │
│  └──────────────────────────────┬──────────────────────────────────┘    │
│                                  │                                       │
│  ┌──────────────────────────────▼──────────────────────────────────┐    │
│  │  RESULT MERGER                                                   │    │
│  │                                                                  │    │
│  │  1. Collect corrections from all layers                         │    │
│  │  2. Deduplicate (same error caught by multiple layers)          │    │
│  │  3. Prioritize by severity:                                     │    │
│  │     ├── Major: communication breakdown (score -10)              │    │
│  │     ├── Moderate: grammar error (score -5)                      │    │
│  │     └── Minor: style suggestion (score -2)                      │    │
│  │  4. Limit to top 3 corrections per turn (don't overwhelm)      │    │
│  │  5. Generate Vietnamese explanations:                           │    │
│  │     ├── Rule in simple Vietnamese                               │    │
│  │     ├── Example with correction                                 │    │
│  │     └── Similar practice sentence                               │    │
│  │                                                                  │    │
│  │  FINAL OUTPUT:                                                   │    │
│  │  {                                                               │    │
│  │    "original": "I want to eat pho please",                      │    │
│  │    "corrected": "I'd like to have pho, please",                │    │
│  │    "corrections": [{                                             │    │
│  │      "original_segment": "I want to eat pho please",           │    │
│  │      "corrected_segment": "I'd like to have pho, please",     │    │
│  │      "error_type": "vocabulary",                                │    │
│  │      "severity": "moderate",                                    │    │
│  │      "explanation_en": "Use 'I'd like' for polite requests",   │    │
│  │      "explanation_vi": "Dùng 'I'd like' thay vì 'I want' cho  │    │
│  │                          lịch sự hơn khi gọi món"              │    │
│  │    }],                                                           │    │
│  │    "overall_score": 65,                                          │    │
│  │    "encouragement_vi": "Cố gắng tốt! Tiếp tục luyện nhé! 💪" │    │
│  │  }                                                               │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 9. Pronunciation Scoring Engine

### 9.1 Scoring Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    PRONUNCIATION SCORING ENGINE                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  INPUT:                                                                  │
│  ├── Audio: raw PCM audio from student                                  │
│  ├── Reference text: "I want to eat pho please"                        │
│  └── Student level: A2                                                  │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  STEP 1: Forced Alignment                                        │    │
│  │                                                                  │    │
│  │  Align audio to reference text at phoneme level:                │    │
│  │                                                                  │    │
│  │  Audio waveform:                                                 │    │
│  │  ┌────────────────────────────────────────────────────────┐     │    │
│  │  │  ╱╲   ╱╲  ╱╲    ╱╲   ╱╲   ╱╲                        │     │    │
│  │  │ ╱  ╲ ╱  ╲╱  ╲  ╱  ╲ ╱  ╲ ╱  ╲                       │     │    │
│  │  │╱    ╲    ╲    ╲╱    ╲    ╲    ╲                      │     │    │
│  │  │ I   want   to   eat   pho  please                     │     │    │
│  │  └────────────────────────────────────────────────────────┘     │    │
│  │  ↑    ↑    ↑    ↑    ↑    ↑                                    │    │
│  │  0ms 300ms 500ms 700ms 900ms 1100ms                           │    │
│  │                                                                  │    │
│  │  Each word aligned to time range in audio:                      │    │
│  │  ├── "I"      → 0-200ms                                        │    │
│  │  ├── "want"   → 200-450ms                                      │    │
│  │  ├── "to"     → 450-550ms                                      │    │
│  │  ├── "eat"    → 550-750ms                                      │    │
│  │  ├── "pho"    → 750-900ms                                      │    │
│  │  └── "please" → 900-1200ms                                     │    │
│  └──────────────────────────────┬──────────────────────────────────┘    │
│                                  │                                       │
│  ┌──────────────────────────────▼──────────────────────────────────┐    │
│  │  STEP 2: Phoneme-Level Comparison                                │    │
│  │                                                                  │    │
│  │  For each word, compare student's phonemes to reference:        │    │
│  │                                                                  │    │
│  │  "want" → /wɒnt/                                               │    │
│  │  ├── Student said: /wʌn/ (dropped final /t/)                   │    │
│  │  ├── Phoneme accuracy: 75% (3/4 phonemes correct)              │    │
│  │  └── Issue: Final consonant dropped (common VN error)          │    │
│  │                                                                  │    │
│  │  "please" → /pliːz/                                            │    │
│  │  ├── Student said: /pliːs/ (devoiced final /z/)                │    │
│  │  ├── Phoneme accuracy: 80% (4/5 phonemes correct)              │    │
│  │  └── Issue: /z/ → /s/ (VN speakers often devoice)             │    │
│  │                                                                  │    │
│  │  "pho" → /fə/                                                   │    │
│  │  ├── Student said: /fə/ (correct!)                              │    │
│  │  ├── Phoneme accuracy: 100%                                     │    │
│  │  └── No issues                                                  │    │
│  └──────────────────────────────┬──────────────────────────────────┘    │
│                                  │                                       │
│  ┌──────────────────────────────▼──────────────────────────────────┐    │
│  │  STEP 3: Multi-Dimensional Scoring                               │    │
│  │                                                                  │    │
│  │  Dimension 1: ACCURACY (40% weight)                              │    │
│  │  ├── Phoneme-level correctness                                  │    │
│  │  ├── Calculation: correct_phonemes / total_phonemes             │    │
│  │  ├── "I": 100%, "want": 75%, "to": 100%,                       │    │
│  │  │   "eat": 90%, "pho": 100%, "please": 80%                    │    │
│  │  └── Average: 90.8% → Score: 78/100                            │    │
│  │                                                                  │    │
│  │  Dimension 2: FLUENCY (25% weight)                               │    │
│  │  ├── Speech rate: words per minute                              │    │
│  │  ├── Pause detection: long pauses (> 2s) indicate struggle     │    │
│  │  ├── Hesitation markers: "um", "uh", repeated words            │    │
│  │  ├── Calculation:                                                │    │
│  │  │   speech_rate_score = min(100, wpm / target_wpm * 100)     │    │
│  │  │   pause_penalty = long_pauses * 5                            │    │
│  │  │   fluency = speech_rate_score - pause_penalty               │    │
│  │  └── Score: 72/100                                              │    │
│  │                                                                  │    │
│  │  Dimension 3: COMPLETENESS (20% weight)                          │    │
│  │  ├── Did student say all words?                                 │    │
│  │  ├── Calculation: spoken_words / expected_words                 │    │
│  │  ├── Student said 6/6 words                                     │    │
│  │  └── Score: 100/100                                             │    │
│  │                                                                  │    │
│  │  Dimension 4: PROSODY (15% weight)                               │    │
│  │  ├── Stress patterns: correct syllable stress                   │    │
│  │  ├── Intonation: rising for questions, falling for statements  │    │
│  │  ├── Rhythm: natural English rhythm (stress-timed)             │    │
│  │  └── Score: 65/100                                              │    │
│  │                                                                  │    │
│  │  OVERALL SCORE:                                                  │    │
│  │  = 78 × 0.40 + 72 × 0.25 + 100 × 0.20 + 65 × 0.15            │    │
│  │  = 31.2 + 18.0 + 20.0 + 9.75                                   │    │
│  │  = 78.95 → Round to 79/100                                     │    │
│  └──────────────────────────────┬──────────────────────────────────┘    │
│                                  │                                       │
│  ┌──────────────────────────────▼──────────────────────────────────┐    │
│  │  STEP 4: Generate Tips (Vietnamese)                              │    │
│  │                                                                  │    │
│  │  For each low-scoring word (< 70):                              │    │
│  │                                                                  │    │
│  │  Word: "please" (score: 58)                                     │    │
│  │  ├── Issue: Final /z/ devoiced to /s/                           │    │
│  │  ├── Tip_vi: "Âm /z/ cuối từ cần rung dây thanh.              │    │
│  │  │   Đặt tay lên cổ họng, nói 'zzz' để cảm nhận rung."      │    │
│  │  ├── Practice: "please, dogs, bags, cars" (all end in /z/)     │    │
│  │  └── Audio example: [link to correct pronunciation]             │    │
│  │                                                                  │    │
│  │  Word: "want" (score: 75)                                       │    │
│  │  ├── Issue: Final /t/ dropped                                   │    │
│  │  ├── Tip_vi: "Phát âm rõ âm /t/ cuối từ.                      │    │
│  │  │   Lưỡi chạm vòm miệng phía trên rồi nhả ra."              │    │
│  │  ├── Practice: "want, what, went, eat, meet" (all end in /t/)  │    │
│  │  └── Audio example: [link to correct pronunciation]              │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Vocabulary & Spaced Repetition

### 10.1 SM-2 Algorithm

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    SPACED REPETITION (SM-2)                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  WHAT IT DOES:                                                           │
│  Schedules vocabulary reviews at optimal intervals to maximize           │
│  long-term retention with minimum review time.                          │
│                                                                          │
│  ALGORITHM:                                                              │
│                                                                          │
│  For each vocabulary item, track:                                       │
│  ├── ease_factor (EF): starts at 2.5, adjusts based on performance    │
│  ├── interval: days until next review                                  │
│  └── repetitions: consecutive correct reviews                          │
│                                                                          │
│  When student reviews a word and rates difficulty (1-5):                │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  if quality >= 3 (correct):                                      │    │
│  │      if repetitions == 0: interval = 1                          │    │
│  │      elif repetitions == 1: interval = 6                        │    │
│  │      else: interval = interval * ease_factor                    │    │
│  │      repetitions += 1                                            │    │
│  │                                                                  │    │
│  │  if quality < 3 (incorrect):                                     │    │
│  │      interval = 1                                                │    │
│  │      repetitions = 0                                             │    │
│  │                                                                  │    │
│  │  ease_factor += 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)│ │
│  │  ease_factor = max(1.3, ease_factor)                            │    │
│  │                                                                  │    │
│  │  next_review_at = now + interval * days                          │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  EXAMPLE SCHEDULE:                                                       │
│                                                                          │
│  Word: "recommend"                                                       │
│  Day 1: Learn (interval=1, EF=2.5)                                      │
│  Day 2: Review → rated "Good" (4) → interval=6, EF=2.5                 │
│  Day 8: Review → rated "Easy" (5) → interval=15, EF=2.6                │
│  Day 23: Review → rated "Good" (4) → interval=39, EF=2.6               │
│  Day 62: Review → rated "Hard" (2) → interval=1, EF=2.36               │
│  Day 63: Review → rated "Good" (4) → interval=6, EF=2.36               │
│  ...                                                                     │
│                                                                          │
│  REVIEW QUEUE:                                                           │
│  ├── Every day, system checks: which words have next_review_at <= now? │
│  ├── Returns up to 20 words for review                                 │
│  ├── Prioritizes: overdue words first, then new words                  │
│  └── Limits: max 10 new words per day (don't overwhelm)                │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 11. Database Design

### 11.1 Complete Schema

```sql
-- =============================================================================
-- AI English Coach — Complete Database Schema
-- =============================================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ---- Users ----
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    phone VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(255),
    name VARCHAR(100) NOT NULL,
    date_of_birth TIMESTAMP,
    grade INTEGER CHECK (grade >= 1 AND grade <= 12),
    school VARCHAR(200),
    city VARCHAR(100),

    -- Learning Profile
    cefr_level VARCHAR(5) DEFAULT 'A2' CHECK (cefr_level IN ('A1','A2','B1','B2','C1','C2')),
    learning_goal VARCHAR(50) DEFAULT 'communication',
    daily_goal_minutes INTEGER DEFAULT 15 CHECK (daily_goal_minutes > 0),

    -- Subscription
    plan VARCHAR(20) DEFAULT 'free' CHECK (plan IN ('free','premium','premium_plus','school')),
    plan_expires_at TIMESTAMP,

    -- Stats
    total_practice_minutes INTEGER DEFAULT 0,
    total_conversations INTEGER DEFAULT 0,
    current_streak INTEGER DEFAULT 0,
    longest_streak INTEGER DEFAULT 0,
    total_words_learned INTEGER DEFAULT 0,

    -- Preferences
    preferred_voice VARCHAR(50) DEFAULT 'friendly_female',
    preferred_speed FLOAT DEFAULT 0.9 CHECK (preferred_speed > 0 AND preferred_speed <= 2.0),
    language_interface VARCHAR(5) DEFAULT 'vi',

    -- XP & Level
    xp INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1,

    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_active_at TIMESTAMP
);

-- ---- Conversation Sessions ----
CREATE TABLE conversation_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    topic_id VARCHAR(100) NOT NULL,

    -- Timing
    started_at TIMESTAMP DEFAULT NOW(),
    ended_at TIMESTAMP,
    duration_seconds INTEGER DEFAULT 0,

    -- Status
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active','completed','abandoned')),

    -- Scores
    total_turns INTEGER DEFAULT 0,
    avg_grammar_score FLOAT DEFAULT 0,
    avg_pronunciation_score FLOAT DEFAULT 0,
    avg_fluency_score FLOAT DEFAULT 0,
    overall_score FLOAT DEFAULT 0,

    -- Feedback
    summary_feedback_vi TEXT,
    summary_feedback_en TEXT,
    strengths JSONB DEFAULT '[]',
    improvements JSONB DEFAULT '[]',
    new_vocabulary JSONB DEFAULT '[]',

    -- Metadata
    voice_used VARCHAR(50),
    speed_used FLOAT
);

-- ---- Conversation Turns ----
CREATE TABLE conversation_turns (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES conversation_sessions(id) ON DELETE CASCADE,
    turn_number INTEGER NOT NULL,
    role VARCHAR(10) NOT NULL CHECK (role IN ('student','ai')),

    -- Student turn
    student_text TEXT,
    student_audio_url VARCHAR(500),

    -- AI turn
    ai_text TEXT,
    ai_audio_url VARCHAR(500),

    -- Analysis results
    grammar_corrections JSONB DEFAULT '[]',
    grammar_score FLOAT,
    pronunciation_score FLOAT,
    pronunciation_details JSONB,
    fluency_score FLOAT,

    -- Timing
    speech_duration_ms INTEGER DEFAULT 0,
    pause_before_ms INTEGER DEFAULT 0,
    response_latency_ms INTEGER DEFAULT 0,

    created_at TIMESTAMP DEFAULT NOW()
);

-- ---- Vocabulary Items (Spaced Repetition) ----
CREATE TABLE vocabulary_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    word VARCHAR(100) NOT NULL,

    -- Word details
    phonetic VARCHAR(100),
    part_of_speech VARCHAR(20),
    meaning_en TEXT,
    meaning_vi TEXT,
    example_sentence TEXT,

    -- SM-2 Spaced Repetition
    ease_factor FLOAT DEFAULT 2.5 CHECK (ease_factor >= 1.3),
    interval INTEGER DEFAULT 0 CHECK (interval >= 0),
    repetitions INTEGER DEFAULT 0 CHECK (repetitions >= 0),
    next_review_at TIMESTAMP,

    -- Source
    source VARCHAR(50) DEFAULT 'conversation',
    topic_id VARCHAR(100),

    -- Stats
    times_reviewed INTEGER DEFAULT 0,
    times_correct INTEGER DEFAULT 0,
    last_reviewed_at TIMESTAMP,

    created_at TIMESTAMP DEFAULT NOW(),

    -- Unique constraint: one entry per user per word
    UNIQUE(user_id, word)
);

-- ---- Achievements ----
CREATE TABLE achievements (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    achievement_id VARCHAR(50) NOT NULL,
    unlocked_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, achievement_id)
);

-- ---- Indexes for Performance ----
CREATE INDEX idx_users_phone ON users(phone);
CREATE INDEX idx_users_plan ON users(plan);
CREATE INDEX idx_sessions_user_id ON conversation_sessions(user_id);
CREATE INDEX idx_sessions_status ON conversation_sessions(status);
CREATE INDEX idx_sessions_started_at ON conversation_sessions(started_at DESC);
CREATE INDEX idx_turns_session_id ON conversation_turns(session_id);
CREATE INDEX idx_turns_role ON conversation_turns(role);
CREATE INDEX idx_vocabulary_user_id ON vocabulary_items(user_id);
CREATE INDEX idx_vocabulary_next_review ON vocabulary_items(user_id, next_review_at);
CREATE INDEX idx_vocabulary_word ON vocabulary_items(word);
CREATE INDEX idx_achievements_user ON achievements(user_id);
```

---

## 12. Real-Time WebSocket Protocol

### 12.1 Message Types

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    WEBSOCKET PROTOCOL                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  CONNECTION: wss://api.aistudy.io.vn/ws/v1/conversations/{session_id}  │
│                                                                          │
│  ═══════════════════════════════════════════════════════════════════     │
│  CLIENT → SERVER MESSAGES                                                │
│  ═══════════════════════════════════════════════════════════════════     │
│                                                                          │
│  1. Audio Start                                                          │
│  {                                                                       │
│    "type": "audio_start",                                                │
│    "config": {                                                           │
│      "sample_rate": 16000,                                               │
│      "encoding": "webm-opus"                                             │
│    }                                                                     │
│  }                                                                       │
│                                                                          │
│  2. Audio Chunk (binary frame)                                           │
│  <raw audio bytes>                                                       │
│                                                                          │
│  3. Audio End                                                            │
│  {                                                                       │
│    "type": "audio_end"                                                   │
│  }                                                                       │
│                                                                          │
│  4. Text Message (fallback)                                              │
│  {                                                                       │
│    "type": "text_message",                                               │
│    "text": "I want to order pho"                                         │
│  }                                                                       │
│                                                                          │
│  5. Turn Complete (manual signal)                                        │
│  {                                                                       │
│    "type": "turn_complete"                                               │
│  }                                                                       │
│                                                                          │
│  6. Session End                                                          │
│  {                                                                       │
│    "type": "session_end"                                                 │
│  }                                                                       │
│                                                                          │
│  ═══════════════════════════════════════════════════════════════════     │
│  SERVER → CLIENT MESSAGES                                                │
│  ═══════════════════════════════════════════════════════════════════     │
│                                                                          │
│  1. Transcript Partial (streaming ASR)                                   │
│  {                                                                       │
│    "type": "transcript_partial",                                         │
│    "text": "I want to eat..."                                            │
│  }                                                                       │
│                                                                          │
│  2. Transcript Final                                                     │
│  {                                                                       │
│    "type": "transcript_final",                                           │
│    "text": "I want to eat pho please"                                    │
│  }                                                                       │
│                                                                          │
│  3. AI Typing Indicator                                                  │
│  {                                                                       │
│    "type": "ai_typing"                                                   │
│  }                                                                       │
│                                                                          │
│  4. Feedback (grammar + pronunciation)                                    │
│  {                                                                       │
│    "type": "feedback",                                                   │
│    "grammar": {                                                          │
│      "corrections": [{                                                   │
│        "original": "I want to eat pho please",                          │
│        "corrected": "I'd like to have pho, please",                     │
│        "error_type": "vocabulary",                                       │
│        "explanation_vi": "Dùng 'I'd like' cho lịch sự hơn"              │
│      }],                                                                 │
│      "score": 65                                                         │
│    },                                                                    │
│    "pronunciation": {                                                    │
│      "overall": 72,                                                      │
│      "words": [                                                          │
│        {"word": "want", "score": 85, "tip_vi": null},                   │
│        {"word": "pho", "score": 88, "tip_vi": null},                    │
│        {"word": "please", "score": 58, "tip_vi": "Âm /z/ cuối..."}     │
│      ]                                                                   │
│    }                                                                     │
│  }                                                                       │
│                                                                          │
│  5. AI Response                                                          │
│  {                                                                       │
│    "type": "ai_response",                                                │
│    "text": "Great choice! Would you like beef or chicken?",              │
│    "audio_url": "https://minio.../tts/abc123.mp3",                      │
│    "turn_number": 3                                                      │
│  }                                                                       │
│                                                                          │
│  6. Session Summary                                                      │
│  {                                                                       │
│    "type": "session_summary",                                            │
│    "duration_seconds": 480,                                              │
│    "total_turns": 10,                                                    │
│    "overall_score": 74,                                                  │
│    "grammar_score": 78,                                                  │
│    "pronunciation_score": 68,                                            │
│    "fluency_score": 72,                                                  │
│    "new_words_learned": 5,                                               │
│    "summary_vi": "Bạn đã làm tốt! Điểm ngữ pháp cải thiện.",           │
│    "strengths": ["Vocabulary", "Confidence"],                            │
│    "improvements": ["Past tense", "Final consonants"],                   │
│    "xp_earned": 50                                                       │
│  }                                                                       │
│                                                                          │
│  7. Error                                                                │
│  {                                                                       │
│    "type": "error",                                                      │
│    "code": "ASR_TIMEOUT",                                                │
│    "message_vi": "Không nghe rõ, bạn nói lại nhé?",                     │
│    "recoverable": true                                                   │
│  }                                                                       │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 13. Caching Architecture

### 13.1 Cache Layers

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    CACHING ARCHITECTURE                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  LAYER 1: CDN (Cloudflare) — Edge Cache                                 │
│  ├── Static assets (JS, CSS, images): TTL 1 year                       │
│  ├── TTS audio (common phrases): TTL 1 hour                             │
│  └── Hit rate target: 90%+                                              │
│                                                                          │
│  LAYER 2: Application Cache (Redis)                                      │
│  ├── User session: key="session:{user_id}", TTL 24h                    │
│  ├── Conversation context: key="conv:{session_id}", TTL 1h             │
│  ├── TTS audio URL: key="tts:{hash}", TTL 1h                          │
│  ├── Grammar result: key="grammar:{text_hash}", TTL 30min              │
│  ├── Topic list: key="topics:{level}", TTL 24h                         │
│  ├── OTP: key="otp:{phone}", TTL 5min                                  │
│  └── Rate limit: key="ratelimit:{user_id}:{endpoint}", TTL 1min        │
│                                                                          │
│  LAYER 3: Database Query Cache (PostgreSQL)                              │
│  ├── Connection pooling: PgBouncer (max 100 connections)                │
│  ├── Prepared statements for frequent queries                           │
│  └── Materialized views for analytics                                   │
│                                                                          │
│  LAYER 4: Client Cache                                                   │
│  ├── Service Worker: offline fallback page                              │
│  ├── LocalStorage: user preferences, auth tokens                        │
│  ├── IndexedDB: vocabulary cache for offline review                     │
│  └── Memory: conversation history (current session)                     │
│                                                                          │
│  CACHE KEY PATTERNS:                                                     │
│  ├── user:profile:{user_id}           → User profile JSON              │
│  ├── user:session:{user_id}           → Active session JSON            │
│  ├── conv:context:{session_id}        → Last 10 turns                  │
│  ├── tts:audio:{text_hash}:{voice}    → Signed audio URL              │
│  ├── grammar:{text_hash}:{level}      → Grammar check result          │
│  ├── topics:list:{level}:{category}   → Topic list JSON               │
│  ├── otp:{phone}                      → 6-digit OTP                    │
│  └── ratelimit:{user_id}:{endpoint}   → Request counter               │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 14. External API Integration

### 14.1 OpenAI API Integration

```python
# OpenAI API Usage Summary
OPENAI_ENDPOINTS = {
    "whisper": {
        "url": "POST https://api.openai.com/v1/audio/transcriptions",
        "model": "whisper-1",
        "input": "audio file (WebM, MP3, WAV, etc.)",
        "output": '{ "text": "transcribed text" }',
        "cost": "$0.006 per minute",
        "latency": "1-2 seconds",
        "use_case": "Speech-to-text for student audio"
    },
    "gpt4o_mini": {
        "url": "POST https://api.openai.com/v1/chat/completions",
        "model": "gpt-4o-mini",
        "input": "messages array with system prompt + conversation history",
        "output": '{ "choices": [{ "message": { "content": "response" } }] }',
        "cost": "$0.15/1M input, $0.60/1M output",
        "latency": "1-2 seconds",
        "use_case": "Conversation response generation"
    },
    "tts": {
        "url": "POST https://api.openai.com/v1/audio/speech",
        "model": "tts-1-hd",
        "input": '{ "model": "tts-1-hd", "input": "text", "voice": "nova" }',
        "output": "MP3 binary audio",
        "cost": "$0.030 per 1K characters",
        "latency": "800ms",
        "use_case": "Text-to-speech for AI responses"
    },
    "embeddings": {
        "url": "POST https://api.openai.com/v1/embeddings",
        "model": "text-embedding-3-small",
        "input": "text string",
        "output": '{ "data": [{ "embedding": [0.1, -0.2, ...] }] }',
        "cost": "$0.02 per 1M tokens",
        "latency": "100ms",
        "use_case": "Semantic search for knowledge base"
    }
}
```

---

## 15. Error Handling & Recovery

### 15.1 Error Scenarios

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    ERROR HANDLING MATRIX                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ERROR                  │ HANDLING                    │ USER MESSAGE (VI)│
│  ───────────────────────┼─────────────────────────────┼─────────────────│
│  ASR timeout            │ Retry once, fallback text   │ "Không nghe rõ, │
│                         │                             │  nói lại hoặc   │
│                         │                             │  gõ text nhé"   │
│  ───────────────────────┼─────────────────────────────┼─────────────────│
│  ASR low confidence     │ Show transcript, ask confirm│ "Bạn có nói     │
│  (< 0.7)               │                             │  '...' không?"   │
│  ───────────────────────┼─────────────────────────────┼─────────────────│
│  LLM timeout            │ Retry with simpler prompt   │ "AI đang suy     │
│                         │                             │  nghĩ, chờ chút"│
│  ───────────────────────┼─────────────────────────────┼─────────────────│
│  LLM error (5xx)        │ Switch to fallback model    │ (transparent)    │
│  ───────────────────────┼─────────────────────────────┼─────────────────│
│  LLM rate limited       │ Queue request, show loading │ "Đang có nhiều   │
│                         │                             │  bạn đang học"   │
│  ───────────────────────┼─────────────────────────────┼─────────────────│
│  TTS error              │ Show text only (no audio)   │ (silent, show    │
│                         │                             │  text)           │
│  ───────────────────────┼─────────────────────────────┼─────────────────│
│  WebSocket disconnect   │ Auto-reconnect (3 attempts) │ "Đang kết nối   │
│                         │                             │  lại..."         │
│  ───────────────────────┼─────────────────────────────┼─────────────────│
│  Audio permission denied│ Show mic permission prompt  │ "Cho phép micro  │
│                         │                             │  để luyện nói"   │
│  ───────────────────────┼─────────────────────────────┼─────────────────│
│  Network offline        │ Queue messages, sync later  │ "Mạng yếu, đang │
│                         │                             │  lưu kết quả"    │
│  ───────────────────────┼─────────────────────────────┼─────────────────│
│  Database unavailable   │ Serve from cache, retry     │ "Hệ thống đang   │
│                         │                             │  bận, thử lại"   │
│  ───────────────────────┼─────────────────────────────┼─────────────────│
│  Redis unavailable      │ Skip cache, direct DB       │ (transparent)    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 16. Security Architecture

### 16.1 Security Layers

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    SECURITY ARCHITECTURE                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  LAYER 1: Network Security                                               │
│  ├── Cloudflare DDoS protection                                         │
│  ├── SSL/TLS 1.3 (all traffic encrypted)                               │
│  ├── HSTS headers (force HTTPS)                                         │
│  └── IP rate limiting (nginx)                                           │
│                                                                          │
│  LAYER 2: API Security                                                   │
│  ├── JWT authentication (HS256, 24h expiry)                            │
│  ├── Rate limiting per user (60 req/min API, 5 req/min auth)          │
│  ├── Input validation (Pydantic models)                                │
│  ├── CORS (whitelist origins only)                                      │
│  └── Request size limit (50MB for audio)                               │
│                                                                          │
│  LAYER 3: Data Security                                                  │
│  ├── User PII encrypted at rest (AES-256)                              │
│  ├── Audio recordings encrypted, auto-deleted after 30 days            │
│  ├── Database connections encrypted (SSL)                               │
│  ├── API keys stored in environment variables (not code)               │
│  └── No logging of sensitive data (OTP, tokens)                        │
│                                                                          │
│  LAYER 4: Content Safety                                                 │
│  ├── AI responses filtered for inappropriate content                   │
│  ├── Age-appropriate topics only                                        │
│  ├── No political/religious/controversial content                      │
│  └── Bullying/harassment detection in student input                    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 17. Monitoring & Observability

### 17.1 Key Metrics

```python
METRICS = {
    # Business Metrics
    "users.registered": "Counter — new registrations",
    "users.active_daily": "Gauge — DAU",
    "users.active_monthly": "Gauge — MAU",
    "conversations.started": "Counter — sessions started",
    "conversations.completed": "Counter — sessions completed",
    "conversations.abandoned": "Counter — sessions abandoned",
    "subscriptions.converted": "Counter — free → paid",
    "subscriptions.churned": "Counter — cancelled",
    "revenue.mrr": "Gauge — monthly recurring revenue (VND)",

    # Performance Metrics
    "asr.latency_ms": "Histogram — speech-to-text latency",
    "llm.latency_ms": "Histogram — LLM response latency",
    "tts.latency_ms": "Histogram — text-to-speech latency",
    "e2e.latency_ms": "Histogram — full turn latency",
    "websocket.connections": "Gauge — active WebSocket connections",
    "websocket.messages_per_sec": "Counter — messages/second",

    # Quality Metrics
    "grammar.score_avg": "Gauge — average grammar score",
    "pronunciation.score_avg": "Gauge — average pronunciation score",
    "session.score_avg": "Gauge — average session score",
    "session.duration_avg": "Gauge — average session duration (seconds)",
    "session.completion_rate": "Gauge — % sessions completed",

    # Error Metrics
    "asr.error_rate": "Gauge — % ASR failures",
    "llm.error_rate": "Gauge — % LLM failures",
    "tts.error_rate": "Gauge — % TTS failures",
    "websocket.error_rate": "Gauge — % WebSocket errors",
}
```

---

## 18. Deployment Architecture

See [deployment-architecture.md](deployment-architecture.md) for complete deployment details.

---

## 19. Scaling Strategy

| Phase | Users | Architecture | Server | Cost/Month |
|-------|-------|--------------|--------|------------|
| MVP | 0-1K | Single server, all-in-one | 4 CPU, 8GB | $20 |
| Growth | 1K-10K | Dedicated DB, 3 app instances | 8 CPU, 16GB | $50 |
| Scale | 10K-100K | Read replicas, auto-scaling | 16 CPU, 32GB | $200 |
| Scale+ | 100K+ | Multi-region, sharded | Multi-server | $500+ |

---

## 20. Cost Analysis

### 20.1 Per-User Monthly Cost

| Component | Usage/User/Month | Unit Cost | Cost/User |
|-----------|-----------------|-----------|-----------|
| Whisper ASR | 120 min | $0.006/min | $0.72 |
| GPT-4o-mini | 50K tokens | $0.15/1M | $0.008 |
| TTS (tts-1-hd) | 10K chars | $0.030/1K | $0.30 |
| Deepgram (optional) | 60 min | $0.0043/min | $0.26 |
| **Total API** | | | **$1.03** |
| Infrastructure (shared) | | | **$0.20** |
| **Total Cost/User** | | | **$1.23** |

### 20.2 Unit Economics

| Metric | Value |
|--------|-------|
| ARPU (Premium) | $4.00/month |
| Cost per user | $1.23/month |
| Gross margin | **69%** |
| LTV (12-month retention) | $48 |
| CAC (estimated) | $5 |
| LTV/CAC ratio | **9.6x** |
