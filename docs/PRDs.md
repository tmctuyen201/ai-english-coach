# AI English Coach — Product Requirements Document (PRD)

> **Project Code:** AI20K-033
> **Version:** 1.0.0
> **Last Updated:** 2026-05-30
> **Status:** Brainstorming Phase

---

## 1. Executive Summary

### 1.1 Vision
Build an AI-powered English speaking and listening practice platform for Vietnamese K-12 students that provides real-time conversation practice, grammar correction, pronunciation feedback, and personalized learning paths — at 1/10th the cost of a native tutor.

### 1.2 Mission
Democratize English speaking practice for 20M+ Vietnamese students who currently get only 5 minutes of speaking time per week in class.

### 1.3 Key Metrics (KPIs)

| Metric | Target (Month 1) | Target (Month 6) | Target (Year 1) |
|--------|-------------------|-------------------|------------------|
| DAU (Daily Active Users) | 500 | 10,000 | 100,000 |
| MAU (Monthly Active Users) | 2,000 | 50,000 | 500,000 |
| Avg Session Duration | 8 min | 12 min | 15 min |
| Conversation Completion Rate | 60% | 75% | 85% |
| Subscription Conversion (Free→Paid) | 3% | 5% | 8% |
| Monthly Churn Rate | 15% | 10% | 7% |
| NPS Score | 30 | 45 | 60 |
| Pronunciation Improvement (TOEIC-like) | +5% | +15% | +25% |

### 1.4 Business Model

```
┌─────────────────────────────────────────────────────────┐
│                    REVENUE MODEL                         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Free Tier (Freemium)                                    │
│  ├── 3 conversations/day                                 │
│  ├── Basic grammar feedback                              │
│  ├── Limited topics (5 topics)                           │
│  └── No pronunciation scoring                            │
│                                                          │
│  Premium — 99,000 VND/month (~$4)                        │
│  ├── Unlimited conversations                             │
│  ├── Full grammar + pronunciation feedback               │
│  ├── All topics (50+ topics)                             │
│  ├── Progress tracking & analytics                       │
│  ├── Vocabulary builder with spaced repetition           │
│  └── Parent dashboard                                    │
│                                                          │
│  Premium+ — 199,000 VND/month (~$8)                      │
│  ├── Everything in Premium                               │
│  ├── AI video avatar conversation partner                │
│  ├── IELTS/TOEIC mock speaking tests                     │
│  ├── Homework help (photo → explanation)                 │
│  ├── Multi-language support (Chinese, Japanese)          │
│  └── Priority support                                    │
│                                                          │
│  School License — 50,000 VND/student/year                │
│  ├── Bulk pricing for schools                            │
│  ├── Teacher dashboard                                   │
│  ├── Curriculum alignment                                │
│  ├── Class management                                    │
│  └── Analytics & reporting                               │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### 1.5 Revenue Projections

| Timeline | Users | Paying Users | MRR (VND) | MRR (USD) |
|----------|-------|--------------|-----------|-----------|
| Month 3 | 5,000 | 150 (3%) | 14.8M | $600 |
| Month 6 | 50,000 | 2,500 (5%) | 247M | $10,000 |
| Month 12 | 500,000 | 40,000 (8%) | 3.96B | $160,000 |
| Month 24 | 2,000,000 | 200,000 (10%) | 19.8B | $800,000 |

---

## 2. Problem Statement

### 2.1 Market Pain Points

```
┌──────────────────────────────────────────────────────────────┐
│                    CURRENT STATE (Pain)                        │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Vietnamese K-12 English Education                            │
│  ├── 20M+ students learning English                           │
│  ├── Average class size: 35-40 students                       │
│  ├── Speaking practice per student: ~5 min/week               │
│  ├── 80% students afraid to speak English                     │
│  └── English proficiency rank: #65 globally (EF EPI 2025)    │
│                                                               │
│  Current Solutions (Expensive & Limited)                      │
│  ├── Native tutor: 500K-1M VND/hour                           │
│  ├── English center: 3-5M VND/month                           │
│  ├── Mobile apps (Duolingo, Elsa): limited speaking practice  │
│  └── YouTube/videos: no interaction, no feedback              │
│                                                               │
│  Gap in Market                                                │
│  ├── No affordable 24/7 speaking practice partner             │
│  ├── No real-time pronunciation feedback in Vietnamese market │
│  ├── No conversation practice adapted to VN curriculum        │
│  └── No parent visibility into speaking progress              │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

### 2.2 Market Size

| Segment | TAM | SAM | SOM (Year 1) |
|---------|-----|-----|---------------|
| K-12 Students VN | 20M students × 1.2M VND/yr = 24T VND | 5M urban students = 6T VND | 500K students × 1.2M = 600B VND |
| University Students VN | 2M students | 500K | 50K |
| Working Adults VN | 10M professionals | 2M | 100K |
| **Total** | **$1B+** | **$250M** | **$25M** |

### 2.3 Competitive Landscape

| Feature | Duolingo | Elsa Speak | **AI English Coach (Ours)** | Native Tutor |
|---------|----------|------------|----------------------------|--------------|
| Price/month | Free/$7 | Free/$12 | Free/$4/$8 | $200-400 |
| Speaking practice | Limited | Pronunciation only | **Full conversation** | Full conversation |
| Real-time feedback | Basic | Pronunciation | **Grammar + Pronunciation + Fluency** | Varies |
| Vietnamese support | Basic | Good | **Excellent (built for VN)** | Depends |
| 24/7 availability | ✅ | ✅ | ✅ | ❌ |
| Curriculum aligned (VN) | ❌ | ❌ | **✅ (GDPT 2018)** | Sometimes |
| Parent dashboard | ❌ | ❌ | **✅** | ❌ |
| Conversation topics | Limited | Limited | **50+ with VN context** | Unlimited |
| Adaptive difficulty | Basic | Medium | **Advanced (BKT + RL)** | Depends |
| Price affordability | ✅ | ⚠️ | **✅** | ❌ |

### 2.4 Our Differentiators

1. **Built for Vietnamese students** — curriculum aligned with GDPT 2018, topics relevant to VN culture
2. **Full conversation practice** — not just pronunciation drills, real back-and-forth dialogue
3. **Multi-signal feedback** — grammar + pronunciation + fluency + vocabulary in one session
4. **10x cheaper** than human tutors with comparable quality
5. **Parent dashboard** — Vietnamese parents want visibility into their children's progress
6. **School integration** — B2B license for schools to use as supplementary tool

---

## 3. User Personas

### 3.1 Primary Persona: Minh (Student, 15 years old)

```
┌─────────────────────────────────────────────────┐
│  PERSONA: Minh Học Sinh                          │
├─────────────────────────────────────────────────┤
│  Age: 15 | Grade: 10 | Location: HCMC           │
│  English Level: A2 (Pre-Intermediate)            │
│  Device: Android phone (Samsung Galaxy A series) │
│  Internet: 4G/WiFi at home                       │
├─────────────────────────────────────────────────┤
│  Goals:                                          │
│  ├── Get good grades in English class            │
│  ├── Pass university entrance exam               │
│  ├── Be able to talk to foreigners               │
│  └── Watch English YouTube without subtitles     │
│                                                   │
│  Frustrations:                                    │
│  ├── Too shy to speak English in class           │
│  ├── Teacher can't give individual attention     │
│  ├── Grammar is boring when studied from books   │
│  ├── Pronunciation is never corrected properly   │
│  └── No one to practice with at home             │
│                                                   │
│  Behavior:                                        │
│  ├── Uses phone 3-4 hours/day                    │
│  ├── Watches TikTok/YouTube in Vietnamese        │
│  ├── Studies English 30 min before exams         │
│  ├── Plays mobile games                          │
│  └── Chat with friends on Zalo/Messenger         │
│                                                   │
│  Willingness to Pay: 50K-100K VND/month          │
│  (Asks parents, who decide based on grades)      │
│                                                   │
│  Success Metric: Can hold 5-min conversation     │
│  on familiar topic without freezing              │
└─────────────────────────────────────────────────┘
```

### 3.2 Secondary Persona: Lan (Parent, 42 years old)

```
┌─────────────────────────────────────────────────┐
│  PERSONA: Lan Phụ Huynh                          │
├─────────────────────────────────────────────────┤
│  Age: 42 | Occupation: Office worker             │
│  Children: 2 (ages 12, 15)                       │
│  Location: Hanoi                                 │
│  English Level: A1 (can't help kids)             │
├─────────────────────────────────────────────────┤
│  Goals:                                          │
│  ├── Children get good English grades            │
│  ├── Children have better future opportunities   │
│  ├── Affordable English learning solution        │
│  └── See measurable progress                     │
│                                                   │
│  Frustrations:                                    │
│  ├── Can't afford native tutor (1M/hour)         │
│  ├── English centers are expensive (3-5M/month)  │
│  ├── Can't verify if children are actually study │
│  ├── No visibility into what children learn      │
│  └── Children say "I studied" but no improvement │
│                                                   │
│  Decision Process:                                │
│  ├── Hears from other parents / teacher          │
│  ├── Checks if app is "educational" (not game)   │
│  ├── Wants to see progress reports               │
│  ├── Prefers paying monthly (not annual)         │
│  └── Will pay if sees grade improvement          │
│                                                   │
│  Willingness to Pay: 100K-200K VND/month         │
│  (for both children)                             │
│                                                   │
│  Success Metric: Children's English scores       │
│  improve by 1-2 points within 3 months           │
└─────────────────────────────────────────────────┘
```

### 3.3 Tertiary Persona: Thầy Trần (English Teacher, 35 years old)

```
┌─────────────────────────────────────────────────┐
│  PERSONA: Thầy Trần Giáo Viên                    │
├─────────────────────────────────────────────────┤
│  Age: 35 | Experience: 10 years                  │
│  School: Public high school, Hanoi               │
│  Students: 200+ across 5 classes                 │
│  English Level: C1 (Advanced)                    │
├─────────────────────────────────────────────────┤
│  Goals:                                          │
│  ├── Improve students' speaking skills           │
│  ├── Reduce time spent on repetitive Q&A         │
│  ├── Track student progress efficiently          │
│  └── Align with GDPT 2018 curriculum             │
│                                                   │
│  Frustrations:                                    │
│  ├── 40 students/class, can't practice with each │
│  ├── Students too shy to speak in class          │
│  ├── No tool to track speaking progress          │
│  ├── Homework grading takes too long             │
│  └── Parents ask "how is my child's English?"    │
│                                                   │
│  Needs from Platform:                             │
│  ├── Assign conversation topics as homework      │
│  ├── View class analytics (who practiced, scores)│
│  ├── Align topics with textbook chapters         │
│  ├── Export progress reports for parent meetings  │
│  └── Create custom conversation scenarios        │
│                                                   │
│  Influence: Can recommend to 200+ parents        │
│  (high-value channel for B2B school license)     │
└─────────────────────────────────────────────────┘
```

---

## 4. System Architecture

### 4.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │  Mobile App   │  │  Web App      │  │  Mini App     │              │
│  │  (React Native│  │  (Next.js)    │  │  (Zalo OA)    │              │
│  │   / Flutter)  │  │               │  │               │              │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
│         │                  │                  │                       │
│         └──────────────────┼──────────────────┘                       │
│                            │                                          │
└────────────────────────────┼──────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      API GATEWAY (Kong/Nginx)                        │
│  ├── Rate Limiting                                                   │
│  ├── Authentication (JWT)                                            │
│  ├── Request Routing                                                 │
│  └── SSL Termination                                                 │
└────────────────────────────┬──────────────────────────────────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  CONVERSATION    │ │  LEARNING        │ │  ANALYTICS       │
│  SERVICE          │ │  SERVICE          │ │  SERVICE          │
│                   │ │                   │ │                   │
│  ├── Voice I/O    │ │  ├── User Profile │ │  ├── Progress     │
│  ├── ASR Engine   │ │  ├── Curriculum   │ │  ├── Engagement   │
│  ├── LLM Agent    │ │  ├── Quiz Engine  │ │  ├── Predictions  │
│  ├── TTS Engine   │ │  ├── Vocab Builder│ │  └── Reports      │
│  └── Feedback Gen │ │  └── Study Plan   │ │                   │
└────────┬─────────┘ └────────┬─────────┘ └────────┬─────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        DATA LAYER                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │PostgreSQL │  │  Redis    │  │  Qdrant   │  │  S3/MinIO │           │
│  │(Users,    │  │  (Cache,  │  │  (Vector  │  │  (Audio   │           │
│  │ Progress, │  │  Sessions,│  │  Embeds,  │  │  Files,   │           │
│  │ Curriculum│  │  Rate     │  │  Knowledge│  │  Recordings│          │
│  │ )         │  │  Limits)  │  │  Base)    │  │  )        │           │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘           │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 4.2 Conversation Flow Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CONVERSATION ENGINE FLOW                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Student speaks                                                       │
│       │                                                              │
│       ▼                                                              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐             │
│  │  Audio       │───▶│  Whisper     │───▶│  Text        │             │
│  │  Capture     │    │  ASR         │    │  (Transcript)│             │
│  │  (WebRTC)    │    │  Streaming   │    │              │             │
│  └─────────────┘    └─────────────┘    └──────┬──────┘             │
│                                                │                     │
│                          ┌─────────────────────┼──────────────┐     │
│                          ▼                     ▼              ▼     │
│                   ┌─────────────┐    ┌─────────────┐  ┌─────────┐ │
│                   │  Grammar     │    │  LLM Agent   │  │Pronunc. │ │
│                   │  Checker     │    │  (GPT-4o/    │  │Scorer   │ │
│                   │  (Language   │    │   Claude)    │  │(Custom) │ │
│                   │   Tool)      │    │              │  │         │ │
│                   └──────┬──────┘    └──────┬──────┘  └────┬────┘ │
│                          │                  │              │       │
│                          ▼                  ▼              ▼       │
│                   ┌──────────────────────────────────────────────┐ │
│                   │           FEEDBACK GENERATOR                  │ │
│                   │  ├── Grammar corrections (inline)            │ │
│                   │  ├── Pronunciation score (0-100)             │ │
│                   │  ├── Fluency score (0-100)                   │ │
│                   │  ├── Vocabulary suggestions                  │ │
│                   │  └── Encouragement message                   │ │
│                   └──────────────────┬───────────────────────────┘ │
│                                      │                              │
│                                      ▼                              │
│                   ┌──────────────────────────────────────────────┐ │
│                   │           RESPONSE GENERATOR                  │ │
│                   │  ├── AI response text (conversation)         │ │
│                   │  ├── TTS audio (Vietnamese-accented English) │ │
│                   │  ├── Visual feedback (highlights, scores)    │ │
│                   │  └── Next question/prompt                    │ │
│                   └──────────────────────────────────────────────┘ │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 4.3 Tech Stack

| Layer | Technology | Version | Purpose | Cost/Month |
|-------|-----------|---------|---------|------------|
| **Frontend - Web** | Next.js 14 | 14.2.x | Web app, SSR, SEO | Free (OSS) |
| **Frontend - Mobile** | React Native / Expo | 50.x | iOS + Android | Free (OSS) |
| **Frontend - Mini App** | Zalo Mini App SDK | Latest | Zalo integration | Free |
| **Backend API** | FastAPI | 0.110+ | REST + WebSocket | Free (OSS) |
| **ASR (Speech-to-Text)** | OpenAI Whisper API | large-v3 | Speech recognition | $0.006/min |
| **ASR (Streaming)** | Deepgram Nova-2 | Latest | Real-time streaming | $0.0043/min |
| **LLM (Conversation)** | GPT-4o-mini | Latest | Dialogue generation | $0.15/1M input |
| **LLM (Grammar)** | Claude 3.5 Haiku | Latest | Grammar checking | $0.25/1M input |
| **TTS (Text-to-Speech)** | OpenAI TTS | tts-1-hd | Voice output | $0.030/1K chars |
| **TTS (Vietnamese)** | FPT.AI TTS | Latest | Vietnamese voice | 500K VND/month |
| **Vector DB** | Qdrant | Latest | Knowledge base, embeddings | Free (self-host) |
| **Database** | PostgreSQL | 16.x | Primary data store | Free (self-host) |
| **Cache** | Redis | 7.x | Sessions, rate limits | Free (self-host) |
| **Object Storage** | MinIO / S3 | Latest | Audio recordings | Free (self-host) |
| **Embeddings** | OpenAI text-embedding-3-small | Latest | Semantic search | $0.02/1M tokens |
| **Pronunciation Scoring** | Custom model (fine-tuned) | v1 | Phoneme-level scoring | Self-hosted |
| **Deployment** | Railway / Vercel | - | Hosting | $20-100/month |
| **CDN** | Cloudflare | Free tier | Static assets | Free |
| **Monitoring** | Sentry + PostHog | Free tier | Errors + analytics | Free |

### 4.4 Infrastructure Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    DEPLOYMENT ARCHITECTURE                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    Cloudflare CDN                         │    │
│  │  ├── Static assets (JS, CSS, images)                     │    │
│  │  ├── DDoS protection                                      │    │
│  │  └── SSL termination                                      │    │
│  └────────────────────────┬────────────────────────────────┘    │
│                            │                                      │
│                            ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    Railway (Backend)                       │    │
│  │                                                           │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐              │    │
│  │  │ FastAPI   │  │ FastAPI   │  │ FastAPI   │              │    │
│  │  │ Instance  │  │ Instance  │  │ Instance  │  (Auto-scale)│    │
│  │  │ #1        │  │ #2        │  │ #3        │              │    │
│  │  └──────────┘  └──────────┘  └──────────┘              │    │
│  │                                                           │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐              │    │
│  │  │PostgreSQL │  │  Redis    │  │  Qdrant   │              │    │
│  │  │ Primary   │  │  Cluster  │  │  Cluster  │              │    │
│  │  └──────────┘  └──────────┘  └──────────┘              │    │
│  │                                                           │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    Vercel (Frontend)                       │    │
│  │  ├── Next.js web app                                      │    │
│  │  ├── Edge functions                                       │    │
│  │  └── Image optimization                                   │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                   │
│  External APIs:                                                    │
│  ├── OpenAI (Whisper, GPT-4o-mini, TTS, Embeddings)             │
│  ├── Deepgram (Streaming ASR)                                    │
│  ├── FPT.AI (Vietnamese TTS)                                     │
│  └── Zalo OA API (notifications, mini app)                       │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. Feature Specifications

### 5.1 Core Features (MVP — Phase 1)

#### F1: Voice Conversation Engine

**Description:** Real-time voice conversation with AI English tutor

```
┌─────────────────────────────────────────────────────────┐
│  CONVERSATION UI MOCKUP                                  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Topic: Ordering Food at a Restaurant              │  │
│  │  Level: A2 (Pre-Intermediate)                      │  │
│  │  Duration: 3:45  │  Score: 78/100                  │  │
│  └───────────────────────────────────────────────────┘  │
│                                                          │
│  ┌───────────────────────────────────────────────────┐  │
│  │                                                    │  │
│  │  🤖 AI: Welcome! Today we'll practice ordering    │  │
│  │  food at a restaurant. I'll be your waiter.       │  │
│  │  Ready? Let's start!                              │  │
│  │                                                    │  │
│  │  🤖 AI: Good evening! Welcome to Pho 24.         │  │
│  │  Have you decided what you'd like to order?       │  │
│  │                                                    │  │
│  │  👤 You: [🎤 speaking...]                         │  │
│  │                                                    │  │
│  │  "I want to eat pho please"                       │  │
│  │                                                    │  │
│  │  ┌─ Grammar Feedback ─────────────────────────┐   │  │
│  │  │ ✏️ "I want to eat pho please"               │   │  │
│  │  │ → "I'd like to have pho, please"            │   │  │
│  │  │                                              │   │  │
│  │  │ 💡 Tip: Use "I'd like" instead of "I want"  │   │  │
│  │  │    for polite requests                      │   │  │
│  │  │                                              │   │  │
│  │  │ 🔊 Pronunciation: 72/100                    │   │  │
│  │  │    "pho" → /fə/ ✓ correct                   │   │  │
│  │  │    "please" → /pliːz/ ✓ good                │   │  │
│  │  └──────────────────────────────────────────────┘   │  │
│  │                                                    │  │
│  └───────────────────────────────────────────────────┘  │
│                                                          │
│  ┌───────────────────────────────────────────────────┐  │
│  │  [🎤 Hold to Speak]  [⌨️ Type]  [⏸️ Pause]        │  │
│  └───────────────────────────────────────────────────┘  │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

**Technical Requirements:**

| Requirement | Specification |
|-------------|---------------|
| Audio Input | WebRTC, 16kHz sample rate, mono channel |
| ASR Latency | < 500ms for first partial result |
| ASR Accuracy | > 92% WER for Vietnamese-accented English |
| LLM Response Time | < 1.5s for text response |
| TTS Latency | < 800ms for audio generation |
| End-to-end Latency | < 3s from speech end to AI audio start |
| Session Duration | 5-30 minutes (configurable) |
| Concurrent Users | 1,000+ per instance |
| Audio Format | WebM/Opus (recording), MP3 (TTS output) |

**Conversation State Machine:**

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  START   │───▶│  TOPIC   │───▶│  CHAT    │───▶│  WRAP    │
│          │    │  INTRO   │    │  (loop)  │    │  UP      │
└─────────┘    └─────────┘    └────┬────┘    └─────────┘
                                    │              │
                                    │              ▼
                                    │         ┌─────────┐
                                    └─────────│ FEEDBACK │
                                              │  REPORT  │
                                              └─────────┘
```

#### F2: Grammar Correction Engine

**Description:** Real-time grammar checking with explanations in Vietnamese

**Correction Categories:**

| Category | Example Input | Correction | Explanation (Vietnamese) |
|----------|--------------|------------|--------------------------|
| Tense | "I go yesterday" | "I went yesterday" | "Dùng thì Quá khứ đơn (went) vì có 'yesterday'" |
| Article | "I want apple" | "I want an apple" | "Cần mạo từ 'an' trước danh từ đếm được số ít" |
| Preposition | "I go to school by Monday" | "I go to school on Monday" | "Dùng 'on' với ngày trong tuần" |
| Word Order | "I very like English" | "I like English very much" | "'Very' không đứng trước động từ, dùng 'very much' sau động từ" |
| Vocabulary | "I want to eat pho please" | "I'd like to have pho, please" | "Dùng 'I'd like' thay vì 'I want' cho lịch sự" |
| Subject-Verb | "He don't like it" | "He doesn't like it" | "He/She/It đi với 'doesn't', không phải 'don't'" |

**Grammar Check Pipeline:**

```python
# Grammar checking pipeline (pseudocode)
async def check_grammar(text: str, student_level: str) -> GrammarFeedback:
    """
    Multi-layer grammar checking pipeline.
    
    Layer 1: Rule-based (fast, common errors)
    Layer 2: Language Tool API (comprehensive)
    Layer 3: LLM-based (context-aware, nuanced)
    """
    corrections = []
    
    # Layer 1: Rule-based patterns (fast, < 10ms)
    rule_corrections = apply_grammar_rules(text, student_level)
    corrections.extend(rule_corrections)
    
    # Layer 2: Language Tool (medium speed, < 200ms)
    lt_corrections = await language_tool.check(text)
    corrections.extend(lt_corrections)
    
    # Layer 3: LLM for context-aware corrections (slower, < 1s)
    if needs_llm_check(text, student_level):
        llm_corrections = await llm_grammar_check(text, student_level)
        corrections.extend(llm_corrections)
    
    # Deduplicate and prioritize
    corrections = deduplicate(corrections)
    corrections = prioritize_by_level(corrections, student_level)
    
    # Generate Vietnamese explanations
    for correction in corrections:
        correction.explanation_vi = generate_explanation_vi(correction)
    
    return GrammarFeedback(
        original=text,
        corrected=apply_corrections(text, corrections),
        corrections=corrections,
        score=calculate_grammar_score(text, corrections)
    )
```

#### F3: Pronunciation Scoring

**Description:** Phoneme-level pronunciation assessment

**Scoring Dimensions:**

| Dimension | Weight | Description | How Measured |
|-----------|--------|-------------|--------------|
| Accuracy | 40% | Correct phonemes | Phoneme alignment vs reference |
| Fluency | 25% | Smooth speech, no long pauses | Pause detection, speech rate |
| Completeness | 20% | All words spoken | Word coverage vs expected |
| Prosody | 15% | Stress, rhythm, intonation | Pitch analysis, stress patterns |

**Pronunciation Feedback UI:**

```
┌─────────────────────────────────────────────────────────┐
│  PRONUNCIATION ANALYSIS                                  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Sentence: "I'd like to have pho, please"               │
│                                                          │
│  Overall Score: 78/100 ████████████████░░░░ 78%         │
│                                                          │
│  Word-by-word breakdown:                                │
│  ┌────────────────────────────────────────────────────┐ │
│  │  I'd    → /aɪd/      ████████████ 95% ✅          │ │
│  │  like   → /laɪk/     ██████████░░ 82% ✅          │ │
│  │  to     → /tuː/      ████████████ 90% ✅          │ │
│  │  have   → /hæv/      ████████░░░░ 65% ⚠️          │ │
│  │  pho    → /fə/       ███████████░ 88% ✅          │ │
│  │  please → /pliːz/    ███████░░░░░ 58% ❌          │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  Tips:                                                   │
│  ├── "have": Try /hæv/ not /hɑːv/. Open mouth less.    │ │
│  └── "please": The /z/ sound at the end is important.   │ │
│       Practice: "pleeeze" with buzzing sound at end.    │ │
│                                                          │
│  [🔊 Listen to correct]  [🎤 Try again]                 │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

#### F4: Topic-Based Conversations

**Description:** 50+ conversation topics organized by level and curriculum alignment

**Topic Categories:**

| Category | Topics | Level | Curriculum Alignment |
|----------|--------|-------|---------------------|
| Daily Life | Greetings, Family, Hobbies, Weather, Food | A1-A2 | Grade 6-9 |
| School | Subjects, Homework, Exams, Friends, Teachers | A2-B1 | Grade 9-12 |
| Travel | Airport, Hotel, Directions, Shopping, Restaurant | A2-B1 | Grade 10-12 |
| Work | Job Interview, Meeting, Email, Phone Call | B1-B2 | University |
| Culture | Vietnamese Holidays, Food, Tourism, History | A2-B1 | All levels |
| IELTS | Part 1 (Personal), Part 2 (Cue Card), Part 3 (Discussion) | B1-C1 | IELTS prep |
| TOEIC | Workplace scenarios, Phone calls, Presentations | B1-B2 | TOEIC prep |

**Topic Data Model:**

```python
class Topic(BaseModel):
    id: str                          # "ordering-food"
    title_en: str                    # "Ordering Food at a Restaurant"
    title_vi: str                    # "Gọi Món tại Nhà Hàng"
    category: str                    # "daily-life"
    level: CEFRLevel                 # A2
    curriculum_grade: Optional[int]  # 10 (GDPT 2018 alignment)
    chapter: Optional[str]           # "Unit 5: Food and Drink"
    
    # Conversation structure
    scenario: str                    # "You are at a Vietnamese restaurant..."
    ai_role: str                     # "Friendly waiter"
    student_role: str                # "Customer"
    
    # Learning objectives
    target_vocabulary: List[str]     # ["order", "recommend", "bill", "tip"]
    target_grammar: List[str]        # ["I'd like...", "Could I have..."]
    target_pronunciation: List[str]  # ["/fə/", "/pliːz/"]
    
    # Conversation flow
    turns: List[ConversationTurn]    # 8-15 turns per conversation
    difficulty_score: float          # 0.0-1.0
    estimated_duration: int          # minutes
    
    # Metadata
    popularity_score: float          # Based on user completions
    avg_rating: float                # User ratings
    completion_rate: float           # % who finish
```

### 5.2 Enhanced Features (Phase 2)

#### F5: Vocabulary Builder with Spaced Repetition

```
┌─────────────────────────────────────────────────────────┐
│  VOCABULARY REVIEW                                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Today's Review: 12 words                                │
│  Streak: 🔥 7 days                                       │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │                                                      │ │
│  │          "recommend"                                 │ │
│  │          /ˌrekəˈmend/                                │ │
│  │                                                      │ │
│  │  Meaning: suggest something as good/useful           │ │
│  │  Vietnamese: giới thiệu, khuyên                      │ │
│  │                                                      │ │
│  │  Example: "I recommend the pho bo."                  │ │
│  │                                                      │ │
│  │  [🔊 Listen]  [🎤 Practice]                          │ │
│  │                                                      │ │
│  │  How well do you know this word?                     │ │
│  │  [1] [2] [3] [4] [5]                                │ │
│  │  Again  Hard  Good  Easy  Perfect                    │ │
│  │                                                      │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  Progress: ████████████████░░░░ 80% mastered today      │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

**Spaced Repetition Algorithm (SM-2):**

```python
class SpacedRepetition:
    """SM-2 Algorithm for vocabulary review scheduling."""
    
    def calculate_next_review(
        self,
        quality: int,          # 1-5 rating
        repetitions: int,      # Number of successful reviews
        ease_factor: float,    # Current ease factor (>= 1.3)
        interval: int          # Current interval in days
    ) -> tuple[int, float, int]:
        """
        Calculate next review parameters.
        
        Returns: (new_interval, new_ease_factor, new_repetitions)
        """
        if quality >= 3:  # Successful recall
            if repetitions == 0:
                new_interval = 1
            elif repetitions == 1:
                new_interval = 6
            else:
                new_interval = int(interval * ease_factor)
            new_repetitions = repetitions + 1
        else:  # Failed recall
            new_interval = 1
            new_repetitions = 0
        
        # Update ease factor
        new_ease_factor = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        new_ease_factor = max(1.3, new_ease_factor)
        
        return new_interval, new_ease_factor, new_repetitions
```

#### F6: Parent Dashboard

```
┌─────────────────────────────────────────────────────────┐
│  PARENT DASHBOARD — Minh's Progress                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  This Week                                               │
│  ├── Practice time: 45 min (↑ 15% from last week)       │
│  ├── Conversations completed: 8                          │
│  ├── New words learned: 23                               │
│  └── Avg pronunciation score: 72/100 (↑ 5 points)       │
│                                                          │
│  Monthly Trend                                           │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Speaking Score                                      │ │
│  │  80│                                    ╭──         │ │
│  │  70│                         ╭────╮    │            │ │
│  │  60│              ╭────╮    │    │    │            │ │
│  │  50│  ╭────╮     │    │    │    │    │            │ │
│  │  40│  │    │     │    │    │    │    │            │ │
│  │     └──┴────┴─────┴────┴────┴────┴────┴──          │ │
│  │     Wk1   Wk2   Wk3   Wk4   Wk5   Wk6            │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  Strengths:                                              │
│  ├── Good at greetings and introductions                 │
│  ├── Vocabulary improving steadily                       │
│  └── More confident in daily life topics                 │
│                                                          │
│  Areas to Improve:                                       │
│  ├── Grammar: Past tense still confused                  │
│  ├── Pronunciation: /θ/ and /ð/ sounds                  │
│  └── Fluency: Too many pauses in longer sentences        │
│                                                          │
│  Teacher's Note: "Minh has improved a lot this month!    │
│  Keep encouraging daily practice."                       │
│                                                          │
│  [📧 Send Report]  [📊 Full History]  [⚙️ Settings]      │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### 5.3 Advanced Features (Phase 3)

#### F7: AI Video Avatar Conversation Partner
- Real-time lip-sync with TTS output
- Facial expressions matching conversation tone
- Multiple avatar personalities (friendly, professional, casual)
- Camera-based student engagement detection

#### F8: IELTS/TOEIC Mock Speaking Tests
- Part 1, 2, 3 simulation for IELTS
- Timed responses with countdown
- Band score prediction (IELTS 1-9)
- Detailed feedback per criterion (fluency, coherence, grammar, vocabulary)

#### F9: Homework Help (Photo → Explanation)
- Snap photo of English homework
- OCR + AI explanation in Vietnamese
- Step-by-step problem solving
- Similar practice problems generated

---

## 6. Data Models

### 6.1 User Model

```python
class User(BaseModel):
    id: UUID
    email: Optional[str]
    phone: str                           # Primary auth (VN market)
    name: str
    date_of_birth: Optional[date]
    grade: Optional[int]                 # 6-12
    school: Optional[str]
    city: Optional[str]
    
    # Learning Profile
    cefr_level: CEFRLevel               # A1, A2, B1, B2, C1, C2
    target_score: Optional[float]        # IELTS target, if any
    learning_goal: str                   # "school", "ielts", "communication"
    daily_goal_minutes: int              # 10, 15, 30, 60
    
    # Subscription
    plan: PlanType                       # FREE, PREMIUM, PREMIUM_PLUS
    plan_expires_at: Optional[datetime]
    
    # Stats
    total_practice_minutes: int
    total_conversations: int
    current_streak: int
    longest_streak: int
    total_words_learned: int
    
    # Preferences
    preferred_voice: str                 # "female_warm", "male_friendly"
    preferred_speed: float               # 0.75, 1.0, 1.25
    show_grammar_hints: bool
    show_pronunciation_hints: bool
    language_interface: str              # "vi", "en"
    
    created_at: datetime
    updated_at: datetime
    last_active_at: Optional[datetime]
```

### 6.2 Conversation Session Model

```python
class ConversationSession(BaseModel):
    id: UUID
    user_id: UUID
    topic_id: str
    
    # Session metadata
    started_at: datetime
    ended_at: Optional[datetime]
    duration_seconds: int
    status: SessionStatus               # ACTIVE, COMPLETED, ABANDONED
    
    # Performance
    total_turns: int
    avg_grammar_score: float
    avg_pronunciation_score: float
    avg_fluency_score: float
    overall_score: float
    
    # Conversation history
    turns: List[ConversationTurn]
    
    # Audio recordings
    audio_urls: List[str]               # S3 URLs for each turn
    
    # Feedback
    summary_feedback_vi: str             # Vietnamese summary
    summary_feedback_en: str             # English summary
    strengths: List[str]
    improvements: List[str]
    new_vocabulary: List[str]

class ConversationTurn(BaseModel):
    turn_number: int
    role: str                            # "student" or "ai"
    
    # Student turn data
    student_text: str                    # ASR transcript
    student_audio_url: Optional[str]
    
    # AI turn data
    ai_text: str
    ai_audio_url: Optional[str]
    
    # Feedback
    grammar_corrections: List[GrammarCorrection]
    pronunciation_score: Optional[float]
    pronunciation_details: Optional[PronunciationDetail]
    fluency_score: Optional[float]
    
    # Timing
    speech_duration_ms: int
    pause_before_ms: int
    response_latency_ms: int
```

### 6.3 Vocabulary Model

```python
class VocabularyItem(BaseModel):
    id: UUID
    user_id: UUID
    word: str
    phonetic: str                        # "/fə/"
    part_of_speech: str                  # "noun", "verb"
    meaning_en: str
    meaning_vi: str
    example_sentence: str
    
    # Spaced Repetition
    ease_factor: float                   # SM-2 ease factor
    interval: int                        # Days until next review
    repetitions: int                     # Successful reviews
    next_review_at: datetime
    
    # Source
    source: str                          # "conversation", "manual", "curriculum"
    topic_id: Optional[str]
    
    # Stats
    times_reviewed: int
    times_correct: int
    last_reviewed_at: Optional[datetime]
    
    created_at: datetime
```

---

## 7. API Design

### 7.1 Core API Endpoints

```yaml
# Conversation APIs
POST   /api/v1/conversations/start          # Start new conversation session
POST   /api/v1/conversations/{id}/audio     # Upload audio chunk (streaming)
POST   /api/v1/conversations/{id}/text      # Send text message
GET    /api/v1/conversations/{id}           # Get session details
POST   /api/v1/conversations/{id}/end       # End session, get feedback
GET    /api/v1/conversations/{id}/feedback  # Get detailed feedback

# WebSocket for real-time conversation
WS     /ws/v1/conversations/{id}            # Real-time voice conversation

# User APIs
POST   /api/v1/auth/phone/send-otp         # Send OTP to phone
POST   /api/v1/auth/phone/verify           # Verify OTP, get JWT
GET    /api/v1/users/me                     # Get current user profile
PUT    /api/v1/users/me                     # Update profile
GET    /api/v1/users/me/stats              # Get learning statistics
GET    /api/v1/users/me/progress           # Get progress over time

# Learning APIs
GET    /api/v1/topics                       # List all topics
GET    /api/v1/topics/{id}                 # Get topic details
GET    /api/v1/topics/recommended          # Get recommended topics
GET    /api/v1/vocabulary                   # Get user's vocabulary list
POST   /api/v1/vocabulary/review           # Submit vocabulary review
GET    /api/v1/vocabulary/due              # Get words due for review

# Parent APIs
GET    /api/v1/parent/children             # List linked children
GET    /api/v1/parent/children/{id}/stats  # Get child's stats
GET    /api/v1/parent/children/{id}/report # Generate report

# School APIs
GET    /api/v1/school/classes              # List classes
GET    /api/v1/school/classes/{id}/analytics # Class analytics
POST   /api/v1/school/assignments          # Create assignment
GET    /api/v1/school/assignments/{id}/results # Get results
```

### 7.2 WebSocket Protocol

```json
// Client → Server: Start streaming
{
  "type": "audio_start",
  "topic_id": "ordering-food",
  "audio_config": {
    "sample_rate": 16000,
    "encoding": "webm-opus"
  }
}

// Client → Server: Audio chunk (binary)
// (raw audio bytes)

// Client → Server: End of speech
{
  "type": "audio_end"
}

// Server → Client: Partial transcript
{
  "type": "transcript_partial",
  "text": "I want to eat..."
}

// Server → Server: Final transcript + analysis
{
  "type": "transcript_final",
  "text": "I want to eat pho please",
  "grammar_corrections": [...],
  "pronunciation_score": 72
}

// Server → Client: AI response
{
  "type": "ai_response",
  "text": "Great choice! Would you like beef pho or chicken pho?",
  "audio_url": "https://...",
  "turn_number": 3
}

// Server → Client: Feedback overlay
{
  "type": "feedback",
  "grammar": {
    "corrections": [
      {
        "original": "I want to eat pho please",
        "corrected": "I'd like to have pho, please",
        "explanation_vi": "Dùng 'I'd like' thay vì 'I want' cho lịch sự"
      }
    ],
    "score": 65
  },
  "pronunciation": {
    "overall": 72,
    "words": [
      {"word": "pho", "score": 88, "phonemes": "/fə/"},
      {"word": "please", "score": 58, "tip_vi": "Âm /z/ cuối cần rung dây thanh"}
    ]
  }
}
```

---

## 8. Milestones & Roadmap

### Phase 1: MVP (Weeks 1-6)

| Week | Deliverable | Description |
|------|------------|-------------|
| 1 | Project setup + Auth | FastAPI scaffold, PostgreSQL, phone OTP auth |
| 2 | Conversation engine (text) | LLM agent, topic system, text-based chat |
| 3 | Voice integration | Whisper ASR, TTS, WebSocket streaming |
| 4 | Grammar + Pronunciation | Grammar checker, pronunciation scoring |
| 5 | Frontend (web) | Next.js web app, conversation UI |
| 6 | MVP launch | Deploy, beta testing with 50 students |

### Phase 2: Growth (Weeks 7-12)

| Week | Deliverable | Description |
|------|------------|-------------|
| 7-8 | Mobile app (React Native) | iOS + Android app |
| 9 | Vocabulary builder | Spaced repetition, word extraction |
| 10 | Parent dashboard | Progress tracking, reports |
| 11 | Payment integration | VNPay, MoMo subscription |
| 12 | Public launch | Marketing, 1000 users target |

### Phase 3: Scale (Weeks 13-24)

| Week | Deliverable | Description |
|------|------------|-------------|
| 13-14 | School license | Teacher dashboard, class management |
| 15-16 | IELTS/TOEIC prep | Mock tests, band prediction |
| 17-18 | Zalo Mini App | In-Zalo experience |
| 19-20 | AI Avatar | Video avatar conversation partner |
| 21-24 | Optimization | Performance, cost reduction, scaling |

---

## 9. Legal & Ethics

### 9.1 Data Privacy
- Comply with Vietnam's Cybersecurity Law (2018)
- Parental consent required for users under 16
- Audio recordings stored encrypted, auto-deleted after 30 days
- No selling of user data to third parties
- GDPR-compliant data export and deletion

### 9.2 Content Safety
- AI responses filtered for inappropriate content
- Age-appropriate conversation topics
- No political, religious, or controversial content
- Bullying/harassment detection in student interactions

### 9.3 AI Transparency
- Clear indication that conversation partner is AI
- No deception about AI capabilities
- Feedback marked as AI-generated, not teacher-graded
- Parents informed about AI usage

---

## 10. Cost Analysis

### 10.1 Per-User Monthly Cost (Active User)

| Component | Usage/User/Month | Unit Cost | Cost/User |
|-----------|-----------------|-----------|-----------|
| Whisper ASR | 120 min | $0.006/min | $0.72 |
| GPT-4o-mini | 50K tokens | $0.15/1M | $0.008 |
| Claude Haiku (grammar) | 30K tokens | $0.25/1M | $0.008 |
| OpenAI TTS | 10K chars | $0.030/1K | $0.30 |
| Embeddings | 5K tokens | $0.02/1M | $0.0001 |
| **Total API Cost** | | | **$1.04** |
| Infrastructure (shared) | | | **$0.20** |
| **Total Cost/User** | | | **$1.24** |

### 10.2 Unit Economics

| Metric | Value |
|--------|-------|
| ARPU (Premium) | $4.00/month |
| Cost per user | $1.24/month |
| Gross margin | **69%** |
| LTV (12-month retention) | $48 |
| CAC (estimated) | $5 |
| LTV/CAC ratio | **9.6x** |

---

## Appendix A: Glossary

| Term | Definition |
|------|-----------|
| ASR | Automatic Speech Recognition (Speech-to-Text) |
| TTS | Text-to-Speech |
| CEFR | Common European Framework of Reference for Languages |
| WER | Word Error Rate |
| SM-2 | SuperMemo 2 spaced repetition algorithm |
| BKT | Bayesian Knowledge Tracing |
| GDPT 2018 | Chương trình Giáo dục Phổ thông 2018 (VN national curriculum) |
| IELTS | International English Language Testing System |
| TOEIC | Test of English for International Communication |
| ARPU | Average Revenue Per User |
| LTV | Lifetime Value |
| CAC | Customer Acquisition Cost |
| DAU | Daily Active Users |
| MAU | Monthly Active Users |

---

## Appendix B: Reference Documents

- [ ] system-architecture.md — Detailed system architecture
- [ ] persona.md — Detailed user personas
- [ ] feature.md — Feature specifications
- [ ] api-spec.yaml — OpenAPI specification
- [ ] database-schema.sql — Database schema
- [ ] deployment-guide.md — Deployment instructions
