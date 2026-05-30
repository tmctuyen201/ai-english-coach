# AI English Coach — Feature Specifications (Detailed)

> **Version:** 2.0.0 | **Last Updated:** 2026-05-30 | **Status:** Voice Room MVP Live

---

## Table of Contents

1. [Feature Overview](#1-feature-overview)
2. [F1: Voice Conversation Engine](#2-f1-voice-conversation-engine)
3. [F2: Grammar Correction Engine](#3-f2-grammar-correction-engine)
4. [F3: Pronunciation Scoring](#4-f3-pronunciation-scoring)
5. [F4: Topic-Based Conversations](#5-f4-topic-based-conversations)
6. [F5: Vocabulary Builder (Spaced Repetition)](#6-f5-vocabulary-builder-spaced-repetition)
7. [F6: Parent Dashboard](#7-f6-parent-dashboard)
8. [F7: Gamification System](#8-f7-gamification-system)
9. [F8: AI Video Avatar (Phase 3)](#9-f8-ai-video-avatar-phase-3)
10. [F9: IELTS Mock Speaking Test (Phase 3)](#10-f9-ielts-mock-speaking-test-phase-3)
11. [F10: Homework Help (Phase 3)](#11-f10-homework-help-phase-3)
12. [Screen-by-Screen Specifications](#12-screen-by-screen-specifications)
13. [API Specifications](#13-api-specifications)
14. [Error Handling](#14-error-handling)
15. [Edge Cases](#15-edge-cases)

---

## 1. Feature Overview

### 1.1 Feature Priority Matrix

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    FEATURE PRIORITY MATRIX                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  PHASE 1 — MVP (Weeks 1-6):                                             │
│  ├── F1: Voice Conversation Engine      ← CORE, must have              │
│  ├── F2: Grammar Correction Engine      ← CORE, must have              │
│  ├── F3: Pronunciation Scoring          ← CORE, must have              │
│  └── F4: Topic-Based Conversations      ← CORE, must have              │
│                                                                          │
│  PHASE 2 — Growth (Weeks 7-12):                                         │
│  ├── F5: Vocabulary Builder              ← HIGH value, drives retention │
│  ├── F6: Parent Dashboard               ← HIGH value, drives revenue   │
│  ├── F7: Gamification System            ← MEDIUM value, drives engagement│
│  └── Payment Integration (VNPay/MoMo)   ← REQUIRED for revenue         │
│                                                                          │
│  PHASE 3 — Scale (Weeks 13-24):                                         │
│  ├── F8: AI Video Avatar                ← HIGH value, premium feature  │
│  ├── F9: IELTS Mock Speaking Test       ← HIGH value, premium feature  │
│  ├── F10: Homework Help                 ← MEDIUM value, engagement     │
│  └── School License                     ← HIGH value, B2B revenue      │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Live Voice Room — 1v1 Conversation ✅ IMPLEMENTED

> **Status:** MVP Live — `room/server.py` + `room/conversation-room.html`
> **Port:** 8089 | **URL:** http://213.199.53.171:8089

The **Live Voice Room** is the core product experience. A student enters a room and has a real-time voice conversation with an AI teacher — like a private English tutoring session.

### User Flow

```
LOBBY                          VOICE ROOM                       SUMMARY
┌─────────────┐               ┌─────────────────┐              ┌─────────────┐
│ Enter name  │               │ AI: "Hello!     │              │ Turns: 10   │
│ Pick topic  │ ──────────▶   │ Welcome to..."  │ ──────────▶  │ Feedback:   │
│ Click Start │               │                 │              │ "Great job!"│
└─────────────┘               │ 🎤 [Hold to     │              │             │
                              │     speak]      │              │ [Back to    │
                              │                 │              │  Lobby]     │
                              │ Student: "I     │              └─────────────┘
                              │ want pho..."    │
                              │                 │
                              │ AI: "Would you  │
                              │ like beef or    │
                              │ chicken?"       │
                              └─────────────────┘
```

### Key Design Decisions

| Decision | Why | Impact |
|----------|-----|--------|
| ASR in browser (Web Speech API) | Zero latency, no server cost | Instant transcript |
| TTS in browser (Speech Synthesis) | Zero latency, no API cost | Instant AI speech |
| Only 1 network call per turn (LLM) | Minimize latency | ~1-2s total per turn |
| WebSocket connection | Persistent, no HTTP overhead | Smooth conversation |
| Hold-to-talk button | Natural turn-taking UX | Like a walkie-talkie |
| AI speaks first | Sets tone, student responds | Reduces anxiety |

### Conversation Topics (MVP)

| Topic | Level | Scenario | AI Role |
|-------|-------|----------|---------|
| 💬 Free Chat | A2 | Open conversation | Friendly partner |
| 🍜 Ordering Food | A2 | Restaurant | Waiter at Pho 24 |
| 👋 Meeting People | A1 | School event | New classmate |
| 🎯 IELTS Part 1 | B1-B2 | IELTS exam | Examiner |
| 💼 Job Interview | B1 | Interview | HR manager |

### Server API

```
WebSocket: ws://host:8089/ws/room/{session_id}

Client → Server:
  { type: "start", topic: "ordering-food", name: "Minh" }
  { type: "student_speech", text: "I want to eat pho" }
  { type: "end" }

Server → Client:
  { type: "ai_greeting", text: "Welcome! ..." }
  { type: "ai_thinking" }
  { type: "ai_response", text: "Would you like beef?", turn: 3 }
  { type: "session_summary", turns: 10, summary: "..." }
```

### Files

| File | Lines | Purpose |
|------|-------|---------|
| `room/server.py` | ~250 | FastAPI + WebSocket + OpenRouter LLM |
| `room/conversation-room.html` | ~500 | Lobby + Voice Room + Summary UI |

---

## 3. F1: Voice Conversation Engine

### 2.1 What It Does

The voice conversation engine is the **core feature** of the entire app. It allows students to have a natural English conversation with an AI tutor that:
- Listens to the student speak
- Understands what they said (speech-to-text)
- Responds naturally like a real person
- Speaks the response back (text-to-speech)
- Gives real-time feedback on grammar and pronunciation

### 2.2 Screen: Conversation Page

```
┌─────────────────────────────────────────────────────────────────────────┐
│  CONVERSATION PAGE — Mobile View (390 × 844)                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  HEADER BAR                                                      │    │
│  │  ┌───┐                                        ┌───┐ ┌───┐      │    │
│  │  │ ← │  Ordering Food at a Restaurant         │ ⏸️ │ │ ✕ │      │    │
│  │  └───┘  Level: A2  │  Turn 5/12  │  3:45      └───┘ └───┘      │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  CHAT AREA (scrollable)                                          │    │
│  │                                                                  │    │
│  │  ┌─────────────────────────────────────────────────────────┐    │    │
│  │  │  🤖 AI (Waiter)                                          │    │    │
│  │  │  "Good evening! Welcome to Pho 24. Have you decided     │    │    │
│  │  │  what you'd like to order?"                              │    │    │
│  │  │                                          🔊 [Play]       │    │    │
│  │  └─────────────────────────────────────────────────────────┘    │    │
│  │                                                                  │    │
│  │  ┌─────────────────────────────────────────────────────────┐    │    │
│  │  │  👤 You                                                  │    │    │
│  │  │  "I want to eat pho please"                              │    │    │
│  │  │                                                          │    │    │
│  │  │  ┌─ Grammar ────────────────────────────────────────┐   │    │    │
│  │  │  │  ✏️ "I want to eat pho please"                    │   │    │    │
│  │  │  │  → "I'd like to have pho, please"                │   │    │    │
│  │  │  │  💡 Dùng "I'd like" cho lịch sự hơn              │   │    │    │
│  │  │  │  Score: 65/100                                    │   │    │    │
│  │  │  └──────────────────────────────────────────────────┘   │    │    │
│  │  │                                                          │    │    │
│  │  │  ┌─ Pronunciation ──────────────────────────────────┐   │    │    │
│  │  │  │  I    want   to   eat   pho   please              │   │    │    │
│  │  │  │  95%  85%   90%  90%  88%  58%                   │   │    │    │
│  │  │  │  ✅   ✅    ✅   ✅   ✅   ⚠️                     │   │    │    │
│  │  │  │                                                  │   │    │    │
│  │  │  │  Tip: "please" — Âm /z/ cuối cần rung dây thanh │   │    │    │
│  │  │  └──────────────────────────────────────────────────┘   │    │    │
│  │  └─────────────────────────────────────────────────────────┘    │    │
│  │                                                                  │    │
│  │  ┌─────────────────────────────────────────────────────────┐    │    │
│  │  │  🤖 AI (Waiter)                                          │    │    │
│  │  │  "Great choice! Would you like beef pho or chicken?"     │    │    │
│  │  │                                          🔊 [Play]       │    │    │
│  │  └─────────────────────────────────────────────────────────┘    │    │
│  │                                                                  │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  INPUT BAR (fixed at bottom)                                     │    │
│  │                                                                  │    │
│  │  ┌─────────────────────────────────────────┐  ┌────┐ ┌────┐   │    │
│  │  │  [Type a message...]                    │  │ 🎤 │ │ ⌨️ │   │    │
│  │  └─────────────────────────────────────────┘  └────┘ └────┘   │    │
│  │                                                                  │    │
│  │  [When holding mic button:]                                      │    │
│  │  ┌─────────────────────────────────────────────────────────┐    │    │
│  │  │        🔴 Recording... (waveform animation)              │    │    │
│  │  │        ╱╲ ╱╲ ╱╲ ╱╲ ╱╲ ╱╲ ╱╲ ╱╲                        │    │    │
│  │  │  [Release to send]                    [Slide to cancel]  │    │    │
│  │  └─────────────────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  PROGRESS BAR (bottom)                                           │    │
│  │  ████████████░░░░░░░░ 5/12 turns                                 │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.3 Voice Recording Interaction

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    VOICE RECORDING INTERACTION                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  STATE 1: IDLE                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                                                                  │    │
│  │  ┌─────────────────────────────────────────────────────────┐    │    │
│  │  │                                                          │    │    │
│  │  │                    ┌─────────┐                           │    │    │
│  │  │                    │   🎤    │  ← Large mic button       │    │    │
│  │  │                    │  Hold   │     (80px, centered)      │    │    │
│  │  │                    │ to Talk │                           │    │    │
│  │  │                    └─────────┘                           │    │    │
│  │  │                                                          │    │    │
│  │  └─────────────────────────────────────────────────────────┘    │    │
│  │                                                                  │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  STATE 2: RECORDING (user holds button)                                 │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                                                                  │    │
│  │  ┌─────────────────────────────────────────────────────────┐    │    │
│  │  │  ┌─────────────────────────────────────────────────┐    │    │    │
│  │  │  │              🔴 Recording...                      │    │    │    │
│  │  │  │              ╱╲ ╱╲ ╱╲ ╱╲ ╱╲ ╱╲                  │    │    │    │
│  │  │  │             ╱  ╲╱  ╲╱  ╲╱  ╲╱  ╲                 │    │    │    │
│  │  │  │            (waveform animation)                   │    │    │    │
│  │  │  └─────────────────────────────────────────────────┘    │    │    │
│  │  │                                                          │    │    │
│  │  │  ┌─────────┐                                             │    │    │
│  │  │  │   🔴    │  ← Button turns red, pulses                │    │    │
│  │  │  │Release  │                                             │    │    │
│  │  │  │to Send  │                                             │    │    │
│  │  │  └─────────┘                                             │    │    │
│  │  │                                                          │    │    │
│  │  │  ← Slide left to cancel →                               │    │    │
│  │  └─────────────────────────────────────────────────────────┘    │    │
│  │                                                                  │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  STATE 3: PROCESSING (after release)                                    │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                                                                  │    │
│  │  ┌─────────────────────────────────────────────────────────┐    │    │
│  │  │                                                          │    │    │
│  │  │                    ┌─────────┐                           │    │    │
│  │  │                    │   ⏳    │  ← Loading spinner        │    │    │
│  │  │                    │Listening│                           │    │    │
│  │  │                    └─────────┘                           │    │    │
│  │  │                                                          │    │    │
│  │  └─────────────────────────────────────────────────────────┘    │    │
│  │                                                                  │    │
│  │  Shows partial transcript as ASR processes:                     │    │
│  │  "I want to eat..."                                              │    │
│  │                                                                  │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  STATE 4: AI RESPONDING                                                 │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                                                                  │    │
│  │  ┌─────────────────────────────────────────────────────────┐    │    │
│  │  │  🤖 AI is typing...                                       │    │    │
│  │  │  ┌─────────────────────────────────────────────────┐    │    │    │
│  │  │  │  ● ● ●  (typing indicator dots)                 │    │    │    │
│  │  │  └─────────────────────────────────────────────────┘    │    │    │
│  │  └─────────────────────────────────────────────────────────┘    │    │
│  │                                                                  │    │
│  │  AI audio plays automatically through speaker                    │    │
│  │  Student can tap 🔊 to replay                                   │    │
│  │                                                                  │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.4 Conversation Flow Logic

```python
# Conversation flow pseudocode
async def handle_conversation_turn(session_id: str, audio_data: bytes):
    """
    Complete flow for one conversation turn.
    Called when student finishes speaking.
    """

    # STEP 1: Speech-to-Text
    transcript = await asr_service.transcribe(audio_data)
    # → "I want to eat pho please"

    # Send partial transcript to client immediately
    await ws.send({"type": "transcript_partial", "text": transcript})

    # STEP 2: Parallel processing (all three run simultaneously)
    grammar_task = asyncio.create_task(grammar_service.check(transcript))
    llm_task = asyncio.create_task(llm_service.generate_response(transcript, session_id))
    pron_task = asyncio.create_task(pron_service.score(audio_data, transcript))

    # Wait for all three to complete
    grammar_result, llm_result, pron_result = await asyncio.gather(
        grammar_task, llm_task, pron_task
    )

    # STEP 3: Generate TTS for AI response
    audio_url = await tts_service.synthesize(llm_result.text)

    # STEP 4: Send all results to client
    await ws.send({"type": "transcript_final", "text": transcript})
    await ws.send({"type": "feedback", "grammar": grammar_result, "pronunciation": pron_result})
    await ws.send({"type": "ai_response", "text": llm_result.text, "audio_url": audio_url})

    # STEP 5: Save to database
    await db.save_turn(session_id, transcript, llm_result.text, grammar_result, pron_result)

    # STEP 6: Extract new vocabulary
    new_words = await vocab_service.extract(transcript, llm_result.text, user_id)
    if new_words:
        await ws.send({"type": "new_vocabulary", "words": new_words})
```

---

## 3. F2: Grammar Correction Engine

### 3.1 What It Does

Checks every student utterance for grammar errors and provides:
1. The corrected version of their sentence
2. Specific error highlighting (which word/phrase is wrong)
3. Vietnamese explanation of the grammar rule
4. An overall grammar score (0-100)

### 3.2 Grammar Error Categories (Vietnamese Learners)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    GRAMMAR ERROR CATEGORIES                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  CATEGORY 1: TENSE ERRORS (Most common for VN learners)                │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Example: "I go to school yesterday"                            │    │
│  │  Correction: "I went to school yesterday"                       │    │
│  │  Error: Present tense used instead of Past tense                │    │
│  │  Explanation_vi: "Dùng thì Quá khứ đơn (went) vì có            │    │
│  │  'yesterday' chỉ thời gian quá khứ.                            │    │
│  │  Quy tắc: S + V2/V-ed + time marker (yesterday, last week)"   │    │
│  │  Rule: Past Simple for completed actions in the past            │    │
│  │  Practice: "I _____ (eat) pho yesterday" → "ate"               │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  CATEGORY 2: ARTICLE ERRORS                                              │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Example: "I want apple"                                        │    │
│  │  Correction: "I want an apple"                                  │    │
│  │  Error: Missing article before countable noun                   │    │
│  │  Explanation_vi: "Cần mạo từ 'an' trước danh từ đếm được       │    │
│  │  số ít bắt đầu bằng nguyên âm (a, e, i, o, u).                 │    │
│  │  'apple' bắt đầu bằng /æ/ (nguyên âm) → dùng 'an'."          │    │
│  │  Rule: a + consonant sound, an + vowel sound                   │    │
│  │  Practice: "I want _____ orange" → "an"                        │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  CATEGORY 3: WORD ORDER                                                  │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Example: "I very like English"                                 │    │
│  │  Correction: "I like English very much"                         │    │
│  │  Error: Adverb placed before verb (Vietnamese word order)       │    │
│  │  Explanation_vi: "'Very' không đứng trước động từ trong         │    │
│  │  tiếng Anh. Dùng 'very much' SAU động từ.                      │    │
│  │  Tiếng Việt: 'Tôi rất thích' → Anh: 'I like ... very much'." │    │
│  │  Rule: Subject + Verb + Object + Adverb of degree              │    │
│  │  Practice: "She _____ English _____" → "likes ... very much"   │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  CATEGORY 4: SUBJECT-VERB AGREEMENT                                      │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Example: "He don't like it"                                    │    │
│  │  Correction: "He doesn't like it"                               │    │
│  │  Error: Wrong auxiliary verb for 3rd person singular            │    │
│  │  Explanation_vi: "He/She/It đi với 'doesn't', không phải       │    │
│  │  'don't'. 'Don't' chỉ dùng với I/You/We/They.                 │    │
│  │  Quy tắc: He/She/It + doesn't + V nguyên thể."               │    │
│  │  Rule: 3rd person singular requires "doesn't"                  │    │
│  │  Practice: "She _____ (not, like) coffee" → "doesn't like"     │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  CATEGORY 5: PREPOSITION ERRORS                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Example: "I go to school by Monday"                            │    │
│  │  Correction: "I go to school on Monday"                         │    │
│  │  Error: Wrong preposition for days                              │    │
│  │  Explanation_vi: "Dùng 'on' với ngày trong tuần (Monday,       │    │
│  │  Tuesday...), không phải 'by'.                                  │    │
│  │  Quy tắc: on + ngày, in + tháng/mùa, at + giờ."              │    │
│  │  Rule: on + days, in + months/seasons, at + times              │    │
│  │  Practice: "I wake up _____ 7 AM" → "at"                       │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  CATEGORY 6: VOCABULARY/REGISTER                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Example: "I want to eat pho please"                            │    │
│  │  Correction: "I'd like to have pho, please"                    │    │
│  │  Error: Too direct/impolite for ordering food                   │    │
│  │  Explanation_vi: "Dùng 'I'd like' thay vì 'I want' khi         │    │
│  │  gọi món hoặc yêu cầu — lịch sự hơn.                          │    │
│  │  Tương tự: 'Could I have...' cũng rất lịch sự."               │    │
│  │  Rule: Use "I'd like" for polite requests                      │    │
│  │  Practice: "_____ you help me?" → "Could"                      │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  CATEGORY 7: MISSING FINAL CONSONANTS (VN-specific)                     │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Example: "I wan to ea pho"                                     │    │
│  │  Correction: "I want to eat pho"                                │    │
│  │  Error: Final /t/ and /t/ dropped                               │    │
│  │  Explanation_vi: "Tiếng Việt không có phụ âm cuối mạnh,         │    │
│  │  nên người Việt hay bỏ âm cuối. Phải phát âm rõ:              │    │
│  │  'wanT', 'eaT' — lưỡi chạm vòm miệng rồi nhả ra."            │    │
│  │  Rule: English requires final consonants                        │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.3 Grammar Score Calculation

```python
def calculate_grammar_score(text: str, corrections: list, level: str) -> float:
    """
    Calculate grammar score from 0-100.

    Scoring logic:
    - Start at 100
    - Deduct points per error based on severity
    - Beginners get more lenient scoring (smaller deductions)
    - Longer sentences get a small bonus (more complex = harder)

    Example:
    - Text: "I want to eat pho please" (6 words)
    - Corrections: 1 moderate error (vocabulary/register)
    - Level: A2
    - Score: 100 - (5 * 0.6) + 0.6 = 97.6 → 78 (scaled)
    """

    # Level-based tolerance (how much to forgive)
    TOLERANCE = {
        "A1": 0.5,   # Very lenient — beginners make lots of mistakes
        "A2": 0.4,
        "B1": 0.3,
        "B2": 0.2,
        "C1": 0.1,   # Strict — advanced learners should be accurate
        "C2": 0.05
    }

    # Severity point deductions
    SEVERITY = {
        "minor": 3,       # "a" vs "an" — small mistake
        "moderate": 7,     # Tense error — affects meaning
        "major": 15        # Communication breakdown — listener confused
    }

    word_count = len(text.split())
    tolerance = TOLERANCE.get(level, 0.3)

    # Calculate deductions
    total_deduction = 0
    for correction in corrections:
        base_deduction = SEVERITY.get(correction["severity"], 7)
        # Apply tolerance (beginners lose fewer points)
        adjusted_deduction = base_deduction * (1 - tolerance)
        total_deduction += adjusted_deduction

    # Length bonus (reward longer utterances)
    length_bonus = min(5, word_count / 5)

    # Calculate final score
    score = 100 - total_deduction + length_bonus
    return max(0, min(100, round(score, 1)))


# Examples:
# "Hello" (1 word, 0 errors, A1) → 100 + 0.2 = 100
# "I want apple" (3 words, 1 minor, A2) → 100 - 1.8 + 0.6 = 98.8
# "I go yesterday" (3 words, 1 moderate, A2) → 100 - 4.2 + 0.6 = 96.4
# "He don't like go school yesterday" (6 words, 2 errors, A2) → 100 - 8.4 + 1.2 = 92.8
```

### 3.4 Feedback Display Rules

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    FEEDBACK DISPLAY RULES                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  RULE 1: Maximum 3 corrections per turn                                 │
│  ├── Don't overwhelm the student                                        │
│  ├── Show the most important errors first                               │
│  └── Minor errors can be skipped                                        │
│                                                                          │
│  RULE 2: Positive before negative                                       │
│  ├── Start with what they did well                                      │
│  ├── "Good try! Here's how to improve..."                              │
│  └── Never just show errors without encouragement                       │
│                                                                          │
│  RULE 3: Vietnamese explanations always                                 │
│  ├── All grammar explanations in Vietnamese                             │
│  ├── Include the grammar rule in simple terms                           │
│  └── Include a practice sentence                                        │
│                                                                          │
│  RULE 4: Inline highlighting                                            │
│  ├── Errors highlighted in the transcript                               │
│  ├── Red underline for errors                                           │
│  ├── Tap to see correction + explanation                                │
│  └── Green checkmark for correct parts                                  │
│                                                                          │
│  RULE 5: Level-appropriate detail                                       │
│  ├── A1-A2: Simple rule + example                                       │
│  ├── B1-B2: Rule + exception + alternative                              │
│  └── C1-C2: Nuanced explanation + register difference                   │
│                                                                          │
│  RULE 6: Don't interrupt flow                                           │
│  ├── Show feedback AFTER student finishes speaking                      │
│  ├── Don't stop conversation for minor errors                           │
│  ├── AI response naturally uses correct form                            │
│  └── Student learns by hearing the correct version                      │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 4. F3: Pronunciation Scoring

### 4.1 What It Does

Analyzes the student's spoken audio and provides:
1. Overall pronunciation score (0-100)
2. Word-by-word breakdown with color coding
3. Specific tips for low-scoring words (in Vietnamese)
4. Comparison with correct pronunciation (play correct version)

### 4.2 Pronunciation Error Patterns (Vietnamese Speakers)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    COMMON PRONUNCIATION ERRORS (VN Speakers)             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ERROR 1: /θ/ (voiceless "th")                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Common mistake: /t/ or /s/                                      │    │
│  │  Examples: "think" → /tɪŋk/, "three" → /triː/                  │    │
│  │  Tip_vi: "Đặt lưỡi giữa răng trên và dưới, thổi hơi ra.       │    │
│  │  Gió thổi qua lưỡi. Không phải /t/ (lưỡi chạm vòm)."          │    │
│  │  Practice words: "think, three, thank, thick, thin, month"      │    │
│  │  Practice sentences: "I think three things are important"       │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  ERROR 2: /ð/ (voiced "th")                                             │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Common mistake: /d/ or /z/                                      │    │
│  │  Examples: "the" → /də/, "this" → /dɪs/                        │    │
│  │  Tip_vi: "Giống /θ/ nhưng có rung dây thanh.                    │    │
│  │  Đặt tay lên cổ họng, nói 'thhhh' — tay phải rung."          │    │
│  │  Practice words: "the, this, that, these, those, father"        │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  ERROR 3: /r/ vs /l/ confusion                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Common mistake: /r/ and /l/ mixed or merged                    │    │
│  │  Examples: "right" → /laɪt/, "light" → /raɪt/                  │    │
│  │  Tip_vi: "/r/: Cuộn lưỡi lên, không chạm vòm miệng.            │    │
│  │  /l/: Lưỡi chạm vòm miệng phía sau răng trên."                │    │
│  │  Practice pairs: "right/light, road/load, red/led, fly/cry"     │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  ERROR 4: /ɪ/ vs /iː/ (short vs long "i")                              │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Common mistake: Both pronounced as /iː/                        │    │
│  │  Examples: "ship" → /ʃiːp/, "sit" → /siːt/                    │    │
│  │  Tip_vi: "/ɪ/: Miệng mở rộng, ngắn, thả lỏng.                 │    │
│  │  /iː/: Miệng kéo dài, cười, căng cơ."                        │    │
│  │  Practice pairs: "ship/sheep, sit/seat, bit/beat, live/leave"   │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  ERROR 5: /æ/ (the "a" in "cat")                                       │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Common mistake: /ɛ/ or /a/                                      │    │
│  │  Examples: "cat" → /kɛt/, "bad" → /bɑːd/                      │    │
│  │  Tip_vi: "Miệng mở rộng ngang, hạ hàm dưới.                    │    │
│  │  Giống nói 'e' nhưng mở miệng hơn. Nói 'ae' nhanh."          │    │
│  │  Practice words: "cat, bad, man, hand, stand, happy"            │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  ERROR 6: /v/ (Vietnamese doesn't have /v/)                             │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Common mistake: /b/                                             │    │
│  │  Examples: "very" → /ˈbɛri/, "video" → /ˈbɪdioʊ/              │    │
│  │  Tip_vi: "Răng trên cắn nhẹ môi dưới, thổi hơi ra.             │    │
│  │  Khác /b/ (môi chạm nhau). Nói 'vvvv' rung môi."             │    │
│  │  Practice words: "very, video, vine, view, voice, love"         │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  ERROR 7: Final consonant deletion (BIGGEST issue)                      │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Common mistake: Drop final consonant entirely                  │    │
│  │  Examples: "good" → /gʊ/, "like" → /laɪ/, "want" → /wɒn/     │    │
│  │  Tip_vi: "Tiếng Việt không có phụ âm cuối mạnh.                │    │
│  │  Phải phát âm rõ phụ âm cuối:                                   │    │
│  │  - /t/: Lưỡi chạm vòm rồi nhả ra (want, eat, what)           │    │
│  │  - /d/: Giống /t/ nhưng rung dây thanh (good, and)            │    │
│  │  - /k/: Cuống lưỡi chạm vòm (like, make, speak)               │    │
│  │  - /s/: Thổi hơi qua kẽ răng (this, yes, books)               │    │
│  │  Practice: "I want to eat good food and drink milk"             │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  ERROR 8: Word stress                                                    │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Common mistake: Equal stress on all syllables                  │    │
│  │  Examples: "PHO-to-GRAPH" vs "pho-TO-gra-pher"                 │    │
│  │  Tip_vi: "Nhấn mạnh 1 âm tiết, các âm còn lại nhẹ hơn.        │    │
│  │  Quy tắc: Danh từ nhấn âm 1, động từ nhấn âm cuối.           │    │
│  │  Practice: "PHOtograph, phoTOGrapher, inTEResting, COMfortable"│    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 5. F4: Topic-Based Conversations

### 5.1 Complete Topic Database (50+ Topics)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    TOPIC DATABASE                                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ═══════════════════════════════════════════════════════════════════     │
│  A1 LEVEL (Beginner) — Grade 6-7                                        │
│  ═══════════════════════════════════════════════════════════════════     │
│                                                                          │
│  Topic 1: Meeting New People                                            │
│  ├── id: "meeting-people"                                               │
│  ├── title_vi: "Gặp Gỡ Người Mới"                                     │
│  ├── scenario: "You're at a school event meeting new classmates"        │
│  ├── ai_role: "Friendly new classmate from another school"              │
│  ├── max_turns: 8                                                       │
│  ├── target_vocabulary: ["hello", "nice to meet you", "name",           │
│  │                       "from", "like", "favorite"]                    │
│  ├── target_grammar: ["My name is...", "I'm from...", "I like..."]     │
│  ├── curriculum: "Grade 6, Unit 1: Getting to Know You"                │
│  └── duration: 5-8 minutes                                              │
│                                                                          │
│  Topic 2: My Family                                                     │
│  ├── id: "family"                                                       │
│  ├── title_vi: "Gia Đình Của Tôi"                                      │
│  ├── scenario: "Your friend asks about your family"                     │
│  ├── ai_role: "Curious classmate"                                       │
│  ├── max_turns: 10                                                      │
│  ├── target_vocabulary: ["mother", "father", "sister", "brother",       │
│  │                       "older", "younger", "family"]                  │
│  ├── target_grammar: ["I have...", "She/He is...", "How many...?"]     │
│  ├── curriculum: "Grade 6, Unit 3: My Family"                          │
│  └── duration: 5-8 minutes                                              │
│                                                                          │
│  Topic 3: Hobbies & Free Time                                           │
│  ├── id: "hobbies"                                                      │
│  ├── title_vi: "Sở Thích & Thời Gian Rảnh"                            │
│  ├── scenario: "Chatting with a friend about what you do for fun"       │
│  ├── ai_role: "Curious friend"                                          │
│  ├── max_turns: 10                                                      │
│  ├── target_vocabulary: ["play", "watch", "listen", "read",             │
│  │                       "favorite", "hobby", "free time"]              │
│  ├── target_grammar: ["I like + V-ing", "Do you like...?",             │
│  │                     "My favorite... is..."]                          │
│  ├── curriculum: "Grade 6, Unit 5: Hobbies"                            │
│  └── duration: 5-8 minutes                                              │
│                                                                          │
│  ═══════════════════════════════════════════════════════════════════     │
│  A2 LEVEL (Pre-Intermediate) — Grade 8-9                                │
│  ═══════════════════════════════════════════════════════════════════     │
│                                                                          │
│  Topic 4: Ordering Food                                                 │
│  ├── id: "ordering-food"                                                │
│  ├── title_vi: "Gọi Món Tại Nhà Hàng"                                 │
│  ├── scenario: "You're ordering food at a Vietnamese restaurant"        │
│  ├── ai_role: "Friendly waiter"                                         │
│  ├── max_turns: 12                                                      │
│  ├── target_vocabulary: ["order", "recommend", "bill", "delicious",     │
│  │                       "spicy", "menu", "drink"]                      │
│  ├── target_grammar: ["I'd like...", "Could I have...?",               │
│  │                     "How much is...?", "Can I get...?"]             │
│  ├── curriculum: "Grade 8, Unit 4: Food and Drinks"                    │
│  └── duration: 8-12 minutes                                             │
│                                                                          │
│  Topic 5: Asking for Directions                                         │
│  ├── id: "directions"                                                   │
│  ├── title_vi: "Hỏi Đường"                                              │
│  ├── scenario: "You're lost in Hanoi and need directions"               │
│  ├── ai_role: "Helpful local person"                                    │
│  ├── max_turns: 12                                                      │
│  ├── target_vocabulary: ["turn left", "turn right", "straight",         │
│  │                       "next to", "opposite", "near", "far"]         │
│  ├── target_grammar: ["Where is...?", "How do I get to...?",           │
│  │                     "Go straight, then turn..."]                     │
│  ├── curriculum: "Grade 8, Unit 6: Places"                             │
│  └── duration: 8-12 minutes                                             │
│                                                                          │
│  ═══════════════════════════════════════════════════════════════════     │
│  B1 LEVEL (Intermediate) — Grade 10-11                                  │
│  ═══════════════════════════════════════════════════════════════════     │
│                                                                          │
│  Topic 6: Job Interview                                                 │
│  ├── id: "job-interview"                                                │
│  ├── title_vi: "Phỏng Vấn Xin Việc"                                   │
│  ├── scenario: "You're interviewing for a part-time job"                │
│  ├── ai_role: "HR manager"                                              │
│  ├── max_turns: 15                                                      │
│  ├── target_vocabulary: ["experience", "skills", "strengths",           │
│  │                       "weaknesses", "salary", "schedule"]            │
│  ├── target_grammar: ["I have experience in...", "I'm good at...",     │
│  │                     "Could you tell me about...?"]                   │
│  ├── curriculum: "Grade 11, Unit 4: Careers"                           │
│  └── duration: 10-15 minutes                                            │
│                                                                          │
│  ═══════════════════════════════════════════════════════════════════     │
│  B2 LEVEL (Upper Intermediate) — IELTS Prep                             │
│  ═══════════════════════════════════════════════════════════════════     │
│                                                                          │
│  Topic 7: IELTS Part 1 — Personal Questions                            │
│  ├── id: "ielts-part1"                                                  │
│  ├── title_vi: "IELTS Part 1: Câu Hỏi Cá Nhân"                        │
│  ├── scenario: "IELTS examiner asking about your life"                  │
│  ├── ai_role: "IELTS examiner"                                          │
│  ├── max_turns: 15                                                      │
│  ├── target_vocabulary: ["discourse markers", "fluency fillers"]       │
│  ├── target_grammar: ["Tense variety", "Complex sentences"]            │
│  ├── time_per_response: "30-45 seconds"                                 │
│  └── duration: 10-15 minutes                                            │
│                                                                          │
│  ═══════════════════════════════════════════════════════════════════     │
│  VIETNAMESE CULTURE TOPICS                                              │
│  ═══════════════════════════════════════════════════════════════════     │
│                                                                          │
│  Topic 8: Explaining Tet                                                │
│  ├── id: "tet"                                                          │
│  ├── title_vi: "Giải Thích Tết Cho Người Nước Ngoài"                  │
│  ├── scenario: "A foreign friend asks about Vietnamese New Year"        │
│  ├── ai_role: "Curious foreign friend"                                  │
│  ├── max_turns: 12                                                      │
│  ├── target_vocabulary: ["lunar new year", "tradition", "celebration",  │
│  │                       "lucky money", "ancestor", "fireworks"]        │
│  ├── target_grammar: ["We usually...", "It's tradition to...",         │
│  │                     "The reason is..."]                              │
│  └── duration: 8-12 minutes                                             │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 6. F5: Vocabulary Builder (Spaced Repetition)

### 6.1 How Vocabulary Is Extracted

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    VOCABULARY EXTRACTION FLOW                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  During conversation, the system automatically extracts new words:      │
│                                                                          │
│  Student says: "I want to order the beef pho with spring rolls"         │
│  AI responds: "Great choice! The spring rolls are very crispy today"    │
│                                                                          │
│  Extraction process:                                                     │
│  1. Parse both sentences for content words (nouns, verbs, adj, adv)    │
│  2. Check against user's known vocabulary list                          │
│  3. Filter: only words above user's current level                      │
│  4. Limit: max 3 new words per turn (don't overwhelm)                  │
│                                                                          │
│  Extracted words:                                                       │
│  ├── "order" — student already knows (in vocab list) → SKIP            │
│  ├── "beef" — student already knows → SKIP                             │
│  ├── "pho" — student already knows → SKIP                              │
│  ├── "spring rolls" — NEW → EXTRACT                                    │
│  │   ├── phonetic: /sprɪŋ roʊlz/                                       │
│  │   ├── meaning_vi: "chả cuốn"                                        │
│  │   └── example: "The spring rolls are very crispy"                   │
│  ├── "crispy" — NEW → EXTRACT                                          │
│  │   ├── phonetic: /ˈkrɪspi/                                           │
│  │   ├── meaning_vi: "giòn"                                            │
│  │   └── example: "The spring rolls are very crispy today"             │
│  └── "choice" — student already knows → SKIP                           │
│                                                                          │
│  After conversation ends:                                               │
│  ├── New words added to vocabulary list                                │
│  ├── Next review scheduled (1 day from now)                            │
│  └── Notification: "Bạn đã học 2 từ mới hôm nay! 📚"                 │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 6.2 Review UI (Flashcard)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    VOCABULARY REVIEW UI                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  HEADER                                                          │    │
│  │  Today's Review: 12 words  │  Streak: 🔥 7 days                  │    │
│  │  Progress: ████████████░░░░ 8/12                                  │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  STATE 1: Show word (student tries to recall meaning)                   │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                                                                  │    │
│  │                    ┌─────────────────────┐                       │    │
│  │                    │                     │                       │    │
│  │                    │    "recommend"       │                       │    │
│  │                    │    /ˌrekəˈmend/      │                       │    │
│  │                    │    [verb]            │                       │    │
│  │                    │                     │                       │    │
│  │                    │    Meaning: ?        │                       │    │
│  │                    │                     │                       │    │
│  │                    └─────────────────────┘                       │    │
│  │                                                                  │    │
│  │  [🔊 Listen]     [Show Answer]                                  │    │
│  │                                                                  │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  STATE 2: Reveal answer (student rates difficulty)                      │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                                                                  │    │
│  │                    ┌─────────────────────┐                       │    │
│  │                    │                     │                       │    │
│  │                    │    "recommend"       │                       │    │
│  │                    │    /ˌrekəˈmend/      │                       │    │
│  │                    │    [verb]            │                       │    │
│  │                    │                     │                       │    │
│  │                    │    Meaning:          │                       │    │
│  │                    │    giới thiệu, khuyên│                       │    │
│  │                    │                     │                       │    │
│  │                    │    Example:          │                       │    │
│  │                    │    "I recommend the  │                       │    │
│  │                    │     pho bo."         │                       │    │
│  │                    │                     │                       │    │
│  │                    └─────────────────────┘                       │    │
│  │                                                                  │    │
│  │  [🔊 Listen]  [🎤 Practice]                                     │    │
│  │                                                                  │    │
│  │  How well did you know this?                                     │    │
│  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐                 │    │
│  │  │  1   │ │  2   │ │  3   │ │  4   │ │  5   │                 │    │
│  │  │Again │ │ Hard │ │ Good │ │ Easy │ │Perfect│                 │    │
│  │  │ 1d   │ │ 3d   │ │ 7d   │ │ 14d  │ │ 30d  │                 │    │
│  │  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘                 │    │
│  │                                                                  │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  Rating → Next Review:                                                  │
│  ├── 1 (Again): Show again in 1 minute (within same session)           │
│  ├── 2 (Hard): Next review in 1 day                                    │
│  ├── 3 (Good): Next review in 3 days                                   │
│  ├── 4 (Easy): Next review in 7 days                                   │
│  └── 5 (Perfect): Next review in 14 days                               │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 7. F6: Parent Dashboard

### 7.1 Parent Dashboard Screens

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    PARENT DASHBOARD                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  HEADER                                                          │    │
│  │  👨‍👩‍👧 Phụ Huynh — Con: Minh Nguyễn                                │    │
│  │  Lớp 10, Trường THPT Lê Quý Đôn                                 │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  THIS WEEK OVERVIEW                                              │    │
│  │                                                                  │    │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │    │
│  │  │ 45 min   │ │  8       │ │  23      │ │  72/100  │          │    │
│  │  │ Practice │ │ Convos   │ │ New Words│ │ Score    │          │    │
│  │  │ ↑15% ↑   │ │ ↑3 ↑     │ │ ↑5 ↑     │ │ ↑5 ↑     │          │    │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘          │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  SCORE TREND (Line chart — 4 weeks)                              │    │
│  │                                                                  │    │
│  │  80│                                          ╭──               │    │
│  │  70│                         ╭──╮            │                  │    │
│  │  60│              ╭──╮      │  │            │                  │    │
│  │  50│  ╭──╮       │  │      │  │            │                  │    │
│  │  40│  │  │       │  │      │  │            │                  │    │
│  │     └──┴──┴───────┴──┴──────┴──┴────────────┴──                │    │
│  │     Wk1  Wk2    Wk3  Wk4   Wk5  Wk6      Wk7                 │    │
│  │                                                                  │    │
│  │  Legend: ── Grammar  ── Pronunciation  ── Overall               │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  STRENGTHS & IMPROVEMENTS                                        │    │
│  │                                                                  │    │
│  │  ✅ Điểm mạnh:                                                  │    │
│  │  ├── Tốt khi chào hỏi và giới thiệu bản thân                   │    │
│  │  ├── Từ vựng cải thiện đều qua từng tuần                      │    │
│  │  └── Tự tin hơn khi nói về sở thích                            │    │
│  │                                                                  │    │
│  │  ⚠️ Cần cải thiện:                                              │    │
│  │  ├── Ngữ pháp: Thì quá khứ vẫn hay nhầm                        │    │
│  │  ├── Phát âm: Âm /θ/ và /ð/ (th) chưa đúng                    │    │
│  │  └── Độ trôi chảy: Còn nhiều khoảng dừng khi nói dài           │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  ACTIONS                                                         │    │
│  │                                                                  │    │
│  │  [📧 Gửi báo cáo qua Zalo]  [📊 Tải PDF]  [⚙️ Cài đặt]       │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 8. F7: Gamification System

### 8.1 XP & Leveling

```python
XP_REWARDS = {
    "complete_conversation": 50,        # Finish a conversation session
    "perfect_grammar_turn": 10,         # Grammar score 100 on a turn
    "new_vocabulary_learned": 5,        # Learn a new word
    "daily_streak_bonus": 20,           # Per day of streak (day 1=20, day 2=40...)
    "weekly_goal_met": 100,             # Practice enough days in a week
    "pronunciation_improvement": 15,    # Score improved vs last time
    "topic_completed_first_time": 25,   # First time completing a new topic
}

LEVELS = [
    {"level": 1, "xp": 0, "title": "Seed", "title_vi": "Hạt Giống", "emoji": "🌱"},
    {"level": 2, "xp": 100, "title": "Sprout", "title_vi": "Mầm Non", "emoji": "🌿"},
    {"level": 3, "xp": 300, "title": "Sapling", "title_vi": "Cây Non", "emoji": "🌲"},
    {"level": 4, "xp": 600, "title": "Tree", "title_vi": "Cây Trưởng Thành", "emoji": "🌳"},
    {"level": 5, "xp": 1000, "title": "Forest", "title_vi": "Khu Rừng", "emoji": "🏔️"},
    {"level": 6, "xp": 1500, "title": "Mountain", "title_vi": "Ngọn Núi", "emoji": "⛰️"},
    {"level": 7, "xp": 2500, "title": "Sky", "title_vi": "Bầu Trời", "emoji": "☁️"},
    {"level": 8, "xp": 4000, "title": "Star", "title_vi": "Ngôi Sao", "emoji": "⭐"},
    {"level": 9, "xp": 6000, "title": "Galaxy", "title_vi": "Thiên Hà", "emoji": "🌌"},
    {"level": 10, "xp": 10000, "title": "Universe", "title_vi": "Vũ Trụ", "emoji": "🚀"},
]
```

### 8.2 Achievements

```python
ACHIEVEMENTS = [
    {"id": "first_step", "name_vi": "Bước Đầu Tiên", "emoji": "👶",
     "condition": "Complete 1 conversation", "xp": 10},
    {"id": "week_warrior", "name_vi": "7 Ngày Liên Tiếp", "emoji": "🔥",
     "condition": "7-day practice streak", "xp": 50},
    {"id": "month_master", "name_vi": "30 Ngày Kiên Trì", "emoji": "💎",
     "condition": "30-day practice streak", "xp": 200},
    {"id": "century_club", "name_vi": "Trăm Trận", "emoji": "💯",
     "condition": "Complete 100 conversations", "xp": 100},
    {"id": "grammar_guru", "name_vi": "Bậc Thầy Ngữ Pháp", "emoji": "📝",
     "condition": "Grammar score > 90 for 10 consecutive sessions", "xp": 75},
    {"id": "pron_pro", "name_vi": "Phát Âm Chuẩn", "emoji": "🎤",
     "condition": "Pronunciation score > 85 for 10 consecutive sessions", "xp": 75},
    {"id": "word_collector", "name_vi": "Sưu Tập Từ Vựng", "emoji": "📚",
     "condition": "Learn 500 vocabulary words", "xp": 100},
    {"id": "topic_explorer", "name_vi": "Khám Phá Chủ Đề", "emoji": "🗺️",
     "condition": "Try 20 different topics", "xp": 50},
    {"id": "night_owl", "name_vi": "Cú Đêm", "emoji": "🦉",
     "condition": "Practice after 10 PM on 10 different days", "xp": 25},
    {"id": "early_bird", "name_vi": "Chim Sớm", "emoji": "🐦",
     "condition": "Practice before 7 AM on 10 different days", "xp": 25},
    {"id": "perfectionist", "name_vi": "Người Hoàn Hảo", "emoji": "✨",
     "condition": "Get grammar score 100 on 5 turns in one session", "xp": 50},
    {"id": "social_butterfly", "name_vi": "Bướm Xã Hội", "emoji": "🦋",
     "condition": "Complete all 'Daily Life' topics", "xp": 75},
]
```

---

## 9. F8: AI Video Avatar (Phase 3)

### 9.1 What It Does

An AI video avatar that appears as a face on screen while talking to the student. The avatar:
- Lip-syncs with the TTS audio output
- Shows facial expressions matching the conversation tone
- Has multiple personality options (friendly, professional, casual)
- Creates a more engaging, "human-like" experience

### 9.2 Avatar Specifications

```python
AVATAR_CONFIG = {
    "providers": {
        "heygen": {
            "type": "streaming",
            "latency": "500-800ms",
            "quality": "high",
            "cost": "$0.10/min",
            "lip_sync": "excellent",
            "best_for": "Premium+ users"
        },
        "did": {
            "type": "streaming",
            "latency": "800-1200ms",
            "quality": "medium",
            "cost": "$0.05/min",
            "lip_sync": "good",
            "best_for": "Fallback"
        }
    },
    "avatars": {
        "friendly_teacher_female": {
            "appearance": "Young Vietnamese woman, professional casual",
            "personality": "Warm, encouraging, patient",
            "voice": "friendly_female",
            "best_for": "All ages"
        },
        "friendly_teacher_male": {
            "appearance": "Young Vietnamese man, casual",
            "personality": "Enthusiastic, clear, supportive",
            "voice": "friendly_male",
            "best_for": "High school students"
        },
        "international_female": {
            "appearance": "Western woman, professional",
            "personality": "Professional, clear pronunciation",
            "voice": "professional_female",
            "best_for": "IELTS/TOEIC prep"
        }
    }
}
```

---

## 10. F9: IELTS Mock Speaking Test (Phase 3)

### 10.1 IELTS Speaking Test Simulation

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    IELTS SPEAKING TEST SIMULATION                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  PART 1: Introduction & Interview (4-5 minutes)                         │
│  ├── Examiner asks familiar questions                                   │
│  ├── Topics: home, family, work, studies, interests                     │
│  ├── Response length: 2-3 sentences per question                       │
│  └── Focus: Fluency, natural responses                                  │
│                                                                          │
│  PART 2: Individual Long Turn (3-4 minutes)                             │
│  ├── Examiner gives cue card with topic                                 │
│  ├── Student has 1 minute to prepare (notes allowed)                   │
│  ├── Student speaks for 1-2 minutes                                     │
│  ├── Timer shown on screen                                              │
│  └── Focus: Extended speaking, organization, vocabulary                 │
│                                                                          │
│  PART 3: Two-Way Discussion (4-5 minutes)                               │
│  ├── Examiner asks abstract questions related to Part 2 topic          │
│  ├── Requires deeper analysis and opinion                               │
│  ├── Response length: 3-5 sentences per question                       │
│  └── Focus: Complex language, critical thinking                         │
│                                                                          │
│  SCORING (after test):                                                   │
│  ├── Fluency & Coherence: Band 1-9                                     │
│  ├── Lexical Resource: Band 1-9                                        │
│  ├── Grammatical Range & Accuracy: Band 1-9                            │
│  ├── Pronunciation: Band 1-9                                            │
│  └── Overall Band: Average of 4 criteria                               │
│                                                                          │
│  FEEDBACK:                                                               │
│  ├── Band score prediction (e.g., 6.0)                                  │
│  ├── Detailed feedback per criterion                                    │
│  ├── Specific examples from student's responses                        │
│  ├── Improvement suggestions                                            │
│  └── Practice recommendations                                           │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 11. F10: Homework Help (Phase 3)

### 11.1 How It Works

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    HOMEWORK HELP FLOW                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  STEP 1: Student takes photo of homework                                │
│  ├── Uses phone camera within app                                       │
│  ├── Auto-crop and enhance image                                        │
│  └── Support: handwritten or printed text                               │
│                                                                          │
│  STEP 2: OCR + AI Vision                                                │
│  ├── Extract text from image (Vietnamese OCR)                           │
│  ├── Identify question type:                                            │
│  │   ├── Fill-in-the-blank                                              │
│  │   ├── Multiple choice                                                │
│  │   ├── Short answer                                                   │
│  │   ├── Essay / paragraph                                              │
│  │   └── Grammar exercise                                               │
│  ├── Parse exercise structure                                           │
│  └── Identify the specific question being asked                        │
│                                                                          │
│  STEP 3: AI generates explanation                                       │
│  ├── Step-by-step solution (in Vietnamese)                              │
│  ├── Grammar rule explanation                                           │
│  ├── Why this answer is correct                                         │
│  ├── Similar examples                                                   │
│  └── Practice problems (generated by AI)                               │
│                                                                          │
│  STEP 4: Interactive follow-up                                          │
│  ├── Student can ask: "Tại sao dùng 'went' mà không phải 'goed'?"     │
│  ├── AI explains in Vietnamese with examples                           │
│  └── Student can practice similar problems                             │
│                                                                          │
│  IMPORTANT: The AI explains HOW to solve, not just the answer           │
│  ├── "Đây là bài về thì quá khứ đơn..."                              │
│  ├── "Quy tắc: động từ 'go' → quá khứ là 'went' (bất quy tắc)"      │
│  └── KHÔNG chỉ cho đáp án mà hướng dẫn cách tư duy                   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 12. Screen-by-Screen Specifications

### 12.1 Landing Page (/)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  LANDING PAGE                                                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Section 1: Hero                                                        │
│  ├── Headline: "Luyện nói tiếng Anh với AI — mọi lúc, mọi nơi"        │
│  ├── Subtitle: "80% học sinh Việt Nam sợ nói tiếng Anh.               │
│  │              Chúng tôi thay đổi điều đó."                           │
│  ├── CTA: "Thử Miễn Phí" (large green button)                         │
│  └── Hero image: Student talking to phone with AI avatar               │
│                                                                          │
│  Section 2: How It Works                                                │
│  ├── Step 1: "Chọn chủ đề" (icon: 📱)                                 │
│  ├── Step 2: "Nói với AI" (icon: 🎤)                                  │
│  ├── Step 3: "Nhận phản hồi" (icon: 📊)                               │
│  └── Step 4: "Cải thiện mỗi ngày" (icon: 📈)                          │
│                                                                          │
│  Section 3: Features                                                    │
│  ├── "Luyện nói 24/7" — AI luôn sẵn sàng                               │
│  ├── "Sửa ngữ pháp tức thì" — Phản hồi ngay khi bạn nói              │
│  ├── "Chấm phát âm chi tiết" — Từng từ một                            │
│  └── "50+ chủ đề" — Từ chào hỏi đến IELTS                            │
│                                                                          │
│  Section 4: Social Proof                                                │
│  ├── "10,000+ học sinh đang sử dụng"                                   │
│  ├── Parent testimonials                                                │
│  └── Teacher endorsements                                               │
│                                                                          │
│  Section 5: Pricing                                                     │
│  ├── Free: "Miễn phí" — 3 cuộc hội thoại/ngày                         │
│  ├── Premium: "99,000đ/tháng" — Không giới hạn                         │
│  └── Premium+: "199,000đ/tháng" — Avatar + IELTS                      │
│                                                                          │
│  Section 6: CTA                                                         │
│  └── "Bắt đầu luyện tập miễn phí ngay!" (large button)               │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 12.2 Login Page (/login)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  LOGIN PAGE                                                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                                                                  │    │
│  │                    🗣️ AI English Coach                           │    │
│  │                                                                  │    │
│  │                    ┌─────────────────────┐                       │    │
│  │                    │ 🇻🇳 +84              │                       │    │
│  │                    │ 0902 xxx xxx        │                       │    │
│  │                    └─────────────────────┘                       │    │
│  │                                                                  │    │
│  │                    [Gửi mã OTP]                                  │    │
│  │                                                                  │    │
│  │                    ─── hoặc ───                                  │    │
│  │                                                                  │    │
│  │                    [📱 Tiếp tục với Zalo]                        │    │
│  │                                                                  │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  After OTP sent:                                                        │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                                                                  │    │
│  │                    Nhập mã OTP đã gửi đến                       │    │
│  │                    0902 xxx xxx                                  │    │
│  │                                                                  │    │
│  │                    ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐        │    │
│  │                    │ 1 │ │ 2 │ │ 3 │ │ 4 │ │ 5 │ │ 6 │        │    │
│  │                    └───┘ └───┘ └───┘ └───┘ └───┘ └───┘        │    │
│  │                                                                  │    │
│  │                    [Xác nhận]                                    │    │
│  │                                                                  │    │
│  │                    Gửi lại mã (00:45)                            │    │
│  │                                                                  │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 12.3 Dashboard (/dashboard)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  DASHBOARD                                                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  HEADER                                                          │    │
│  │  Xin chào, Minh! 👋                              [🔔] [⚙️]     │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  STREAK & LEVEL                                                  │    │
│  │                                                                  │    │
│  │  🔥 7 ngày liên tiếp    │    🌲 Level 3 — Cây Non              │    │
│  │  ████████████░░░ 300 XP │    ████████████░░░ 600 XP             │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  QUICK START                                                     │    │
│  │                                                                  │    │
│  │  ┌─────────────────────────────────────────────────────────┐    │    │
│  │  │  🎯 Tiếp tục luyện                                      │    │    │
│  │  │  Ordering Food — Turn 5/12                               │    │    │
│  │  │  [Tiếp tục ▶]                                            │    │    │
│  │  └─────────────────────────────────────────────────────────┘    │    │
│  │                                                                  │    │
│  │  Hoặc chọn chủ đề mới:                                          │    │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐                  │    │
│  │  │ 🍜     │ │ 🏫     │ │ ✈️     │ │ 💼     │                  │    │
│  │  │ Đồ ăn │ │ Trường │ │ Du lịch│ │ Phỏng │                  │    │
│  │  │ học    │ │        │ │        │ │ vấn   │                  │    │
│  │  └────────┘ └────────┘ └────────┘ └────────┘                  │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  TODAY'S STATS                                                   │    │
│  │                                                                  │    │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │    │
│  │  │ 15 min   │ │  2       │ │  5       │ │  72/100  │          │    │
│  │  │ Luyện tập│ │ Hội thoại│ │ Từ mới   │ │ Điểm TB  │          │    │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘          │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  REVIEW TODAY                                                    │    │
│  │                                                                  │    │
│  │  📚 12 từ cần ôn hôm nay                              [Ôn ▶]  │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  BOTTOM NAV                                                      │    │
│  │  [🏠 Home]  [📝 Practice]  [📚 Vocab]  [📊 Progress]  [👤]     │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 13. API Specifications

### 13.1 Authentication API

```yaml
POST /api/v1/auth/phone/send-otp:
  Request:
    { "phone": "0902123456" }
  Response (200):
    { "message": "OTP sent", "phone": "0902xxx", "expires_in": 300 }
  Response (429):
    { "detail": "Too many OTP requests. Try again in 5 minutes." }

POST /api/v1/auth/phone/verify:
  Request:
    { "phone": "0902123456", "otp": "123456" }
  Response (200):
    { "access_token": "eyJ...", "refresh_token": "eyJ...", "token_type": "bearer" }
  Response (400):
    { "detail": "Invalid or expired OTP" }

POST /api/v1/auth/refresh:
  Request:
    { "refresh_token": "eyJ..." }
  Response (200):
    { "access_token": "eyJ...", "token_type": "bearer" }
```

### 13.2 Conversation API

```yaml
POST /api/v1/conversations/start:
  Headers: { Authorization: "Bearer <token>" }
  Request:
    { "topic_id": "ordering-food", "voice": "friendly_female", "speed": 0.9 }
  Response (200):
    {
      "session_id": "uuid",
      "topic_id": "ordering-food",
      "ai_greeting": "Good evening! Welcome to Pho 24...",
      "ai_audio_url": "https://minio.../greeting.mp3"
    }

WS /ws/v1/conversations/{session_id}:
  See WebSocket Protocol section above.

GET /api/v1/conversations/{session_id}:
  Headers: { Authorization: "Bearer <token>" }
  Response (200):
    {
      "id": "uuid",
      "topic_id": "ordering-food",
      "status": "completed",
      "started_at": "2026-05-30T10:00:00Z",
      "ended_at": "2026-05-30T10:12:00Z",
      "duration_seconds": 720,
      "total_turns": 10,
      "avg_grammar_score": 72.5,
      "avg_pronunciation_score": 68.0,
      "overall_score": 70.2,
      "turns": [...]
    }

GET /api/v1/conversations/{session_id}/feedback:
  Response (200):
    {
      "overall_score": 70.2,
      "grammar": { "score": 72.5, "top_errors": [...] },
      "pronunciation": { "score": 68.0, "problem_sounds": [...] },
      "vocabulary": { "new_words": 5, "words": [...] },
      "summary_vi": "Bạn đã làm tốt! Tiếp tục luyện tập nhé.",
      "strengths": ["Vocabulary", "Confidence"],
      "improvements": ["Past tense", "Final consonants"]
    }
```

---

## 14. Error Handling

See [system-architecture.md](system-architecture.md) Section 15 for complete error handling matrix.

---

## 15. Edge Cases

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    EDGE CASES                                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  AUDIO EDGE CASES:                                                      │
│  ├── Student speaks Vietnamese instead of English                       │
│  │   → ASR detects language, respond: "Let's try in English!"          │
│  ├── Student speaks too quietly                                         │
│  │   → ASR low confidence, ask to repeat                               │
│  ├── Background noise (TV, traffic)                                     │
│  │   → Noise suppression + lower confidence threshold                  │
│  ├── Student coughs or makes non-speech sounds                         │
│  │   → VAD filters out non-speech, don't process                      │
│  ├── Student plays music while practicing                              │
│  │   → Background audio affects ASR, prompt to find quiet place        │
│  └── Very long silence (student thinking)                              │
│      → After 10s, gentle prompt: "Take your time!"                     │
│      → After 30s, offer: "Would you like a hint?"                     │
│                                                                          │
│  CONVERSATION EDGE CASES:                                               │
│  ├── Student gives very short answers ("yes", "no")                    │
│  │   → AI asks follow-up to encourage longer responses                │
│  ├── Student repeats same answer                                        │
│  │   → AI acknowledges, gently introduces new topic                   │
│  ├── Student asks question in Vietnamese                                │
│  │   → AI responds in English, acknowledges they can use VN if stuck  │
│  ├── Student goes off-topic                                             │
│  │   → AI acknowledges, gently steers back to topic                   │
│  ├── Student asks about non-English topics (math, science)             │
│  │   → AI: "Interesting! Let's practice talking about that in English" │
│  └── Student is rude or uses inappropriate language                    │
│      → AI responds politely, doesn't engage with rudeness              │
│                                                                          │
│  TECHNICAL EDGE CASES:                                                  │
│  ├── Internet connection drops mid-conversation                        │
│  │   → Auto-reconnect (3 attempts), preserve conversation state       │
│  ├── Browser tab becomes inactive                                       │
│  │   → Pause audio recording, resume when tab active again            │
│  ├── Multiple devices logged in same account                           │
│  │   → Allow, but only 1 active conversation at a time                │
│  ├── Student changes phone orientation mid-conversation                │
│  │   → Responsive layout adapts, conversation continues               │
│  └── Battery dies mid-conversation                                     │
│      → Conversation state saved server-side, resume on next login      │
│                                                                          │
│  PAYMENT EDGE CASES:                                                    │
│  ├── Payment succeeds but webhook delayed                              │
│  │   → Poll payment status every 5s for 2 min                        │
│  ├── Subscription expires mid-conversation                             │
│  │   → Allow current session to complete, limit next session          │
│  └── Student tries to use premium features on free plan                │
│      → Show upgrade prompt with clear pricing                          │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```
