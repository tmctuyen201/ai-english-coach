# 🗣️ AI English Coach

> AI-powered English speaking practice platform for Vietnamese students

## 📋 Project Info

- **Project Code:** AI20K-033
- **Domain:** K-12 Education
- **Tech Stack:** FastAPI, Next.js, React Native, PostgreSQL, Redis, Qdrant
- **Target Market:** Vietnamese K-12 students (20M+ potential users)
- **Business Model:** Freemium SaaS (Free / 99K VND / 199K VND per month)

## 📁 Project Structure

```
ai-english-coach/
├── docs/
│   ├── PRDs.md                    # Product Requirements Document (64KB)
│   ├── system-architecture.md     # System Architecture (59KB)
│   ├── persona.md                 # User Personas (48KB)
│   └── feature.md                 # Feature Specifications (55KB)
├── src/                           # Source code (to be implemented)
├── tests/                         # Test files
├── scripts/                       # Utility scripts
├── assets/                        # Static assets
├── config/                        # Configuration files
└── README.md                      # This file
```

## 🎯 Core Features

### Phase 1 (MVP)
1. **Voice Conversation Engine** — Real-time voice chat with AI English tutor
2. **Grammar Correction** — Real-time grammar feedback with Vietnamese explanations
3. **Pronunciation Scoring** — Phoneme-level pronunciation assessment
4. **Topic System** — 50+ conversation topics aligned with GDPT 2018 curriculum

### Phase 2 (Growth)
5. **Vocabulary Builder** — Spaced repetition (SM-2) for long-term retention
6. **Parent Dashboard** — Progress monitoring for parents
7. **Payment Integration** — VNPay, MoMo, ZaloPay
8. **Mobile App** — React Native (iOS + Android)

### Phase 3 (Scale)
9. **AI Video Avatar** — Real-time lip-sync conversation partner
10. **IELTS/TOEIC Mock Tests** — Band score prediction
11. **Homework Help** — Photo → AI explanation
12. **School License** — Teacher dashboard, class management

## 💰 Revenue Model

| Plan | Price | Features |
|------|-------|----------|
| Free | 0 VND | 3 conversations/day, 5 topics |
| Premium | 99K VND/month | Unlimited conversations, all topics, progress tracking |
| Premium+ | 199K VND/month | + Avatar, IELTS prep, homework help |
| School | 50K VND/student/year | Bulk pricing, teacher dashboard |

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend Web | Next.js 14 |
| Frontend Mobile | React Native / Expo |
| Backend | FastAPI (Python) |
| Database | PostgreSQL 16 |
| Cache | Redis 7 |
| Vector DB | Qdrant |
| ASR | OpenAI Whisper + Deepgram |
| LLM | GPT-4o-mini + Claude Haiku |
| TTS | OpenAI TTS + FPT.AI |
| Hosting | Railway + Vercel |
| CDN | Cloudflare |

## 📊 Key Metrics (Targets)

| Metric | Month 1 | Month 6 | Year 1 |
|--------|---------|---------|--------|
| DAU | 500 | 10,000 | 100,000 |
| MAU | 2,000 | 50,000 | 500,000 |
| Conversion Rate | 3% | 5% | 8% |
| MRR | $600 | $10,000 | $160,000 |

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/tmctuyen201/ai-english-coach.git
cd ai-english-coach

# Backend
cd src
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## 📚 Documentation

- [PRDs.md](docs/PRDs.md) — Full Product Requirements Document
- [system-architecture.md](docs/system-architecture.md) — Technical Architecture
- [persona.md](docs/persona.md) — User Personas
- [feature.md](docs/feature.md) — Feature Specifications

## 📅 Roadmap

| Phase | Timeline | Focus |
|-------|----------|-------|
| Phase 1 (MVP) | Weeks 1-6 | Core conversation engine, web app |
| Phase 2 (Growth) | Weeks 7-12 | Mobile app, payment, parent dashboard |
| Phase 3 (Scale) | Weeks 13-24 | Avatar, IELTS, school license |

---

*Part of the AI Agent Builder Training Program (AI20K-033)*
