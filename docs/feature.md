# AI English Coach — Feature Specifications

> **Version:** 1.0.0
> **Last Updated:** 2026-05-30

---

## 1. Feature Overview

### 1.1 Feature Prioritization Matrix

```
┌─────────────────────────────────────────────────────────────────────┐
│                    FEATURE PRIORITIZATION                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Impact ▲                                                            │
│         │                                                            │
│    High │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│         │  │  F1: Voice   │  │  F5: Vocab   │  │  F7: Avatar  │      │
│         │  │  Conversation│  │  Builder     │  │  (Phase 3)   │      │
│         │  │  (MVP)       │  │  (Phase 2)   │  │              │      │
│         │  └─────────────┘  └─────────────┘  └─────────────┘      │
│         │                                                            │
│   Medium│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│         │  │  F2: Grammar │  │  F6: Parent  │  │  F8: IELTS   │      │
│         │  │  Checker     │  │  Dashboard   │  │  Mock Test   │      │
│         │  │  (MVP)       │  │  (Phase 2)   │  │  (Phase 3)   │      │
│         │  └─────────────┘  └─────────────┘  └─────────────┘      │
│         │                                                            │
│     Low │  ┌─────────────┐  ┌─────────────┐                       │
│         │  │  F3: Pronunc.│  │  F4: Topics  │                       │
│         │  │  Scoring     │  │  System      │                       │
│         │  │  (MVP)       │  │  (MVP)       │                       │
│         │  └─────────────┘  └─────────────┘                       │
│         │                                                            │
│         └───────────────────────────────────────────────────▶      │
│              Low              Medium            High                 │
│                                  Effort                               │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Phase 1 (MVP):    F1, F2, F3, F4                           │   │
│  │  Phase 2 (Growth): F5, F6, Payment, Mobile App              │   │
│  │  Phase 3 (Scale):  F7, F8, F9, School License               │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.2 Feature Dependencies

```
┌─────────────────────────────────────────────────────────────────────┐
│                    FEATURE DEPENDENCY GRAPH                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────┐                                                       │
│  │  Auth     │                                                       │
│  │  (Phone   │                                                       │
│  │   OTP)    │                                                       │
│  └────┬─────┘                                                       │
│       │                                                              │
│       ▼                                                              │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐                    │
│  │  F1:      │────▶│  F2:      │────▶│  F5:      │                    │
│  │  Voice    │     │  Grammar  │     │  Vocab    │                    │
│  │  Conv.    │     │  Checker  │     │  Builder  │                    │
│  └────┬─────┘     └────┬─────┘     └──────────┘                    │
│       │                │                                             │
│       ▼                ▼                                             │
│  ┌──────────┐     ┌──────────┐                                      │
│  │  F3:      │     │  F6:      │                                      │
│  │  Pronunc. │     │  Parent   │                                      │
│  │  Scoring  │     │  Dashboard│                                      │
│  └──────────┘     └──────────┘                                      │
│                                                                      │
│  ┌──────────┐                                                       │
│  │  F4:      │ (independent, can be built in parallel)              │
│  │  Topics   │                                                       │
│  └──────────┘                                                       │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. Feature F1: Voice Conversation Engine

### 2.1 Description

Real-time voice conversation with an AI English tutor that adapts to the student's level, provides natural dialogue, and gives immediate feedback on grammar and pronunciation.

### 2.2 User Stories

| ID | User Story | Priority | Acceptance Criteria |
|----|-----------|----------|---------------------|
| F1.1 | As a student, I want to start a conversation by selecting a topic | P0 | Topic list loads < 2s, selection starts conversation |
| F1.2 | As a student, I want to speak and have the AI understand me | P0 | ASR accuracy > 90% for VN-accented English |
| F1.3 | As a student, I want the AI to respond naturally like a real person | P0 | Response latency < 3s, natural dialogue flow |
| F1.4 | As a student, I want to see what I said (transcript) | P1 | Transcript appears within 1s of speech end |
| F1.5 | As a student, I want to type instead of speak (fallback) | P1 | Text input works same as voice |
| F1.6 | As a student, I want the AI to adjust difficulty to my level | P1 | AI adapts vocabulary/grammar to student's CEFR level |
| F1.7 | As a student, I want to pause and resume conversation | P2 | Conversation state preserved for 30 min |

### 2.3 Conversation Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│  CONVERSATION FLOW DIAGRAM                                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐                                                   │
│  │  SELECT       │                                                   │
│  │  TOPIC        │                                                   │
│  └──────┬───────┘                                                   │
│         │                                                            │
│         ▼                                                            │
│  ┌──────────────┐     ┌──────────────┐                              │
│  │  AI INTRO     │────▶│  LISTEN TO    │                              │
│  │  (TTS plays)  │     │  STUDENT      │                              │
│  └──────────────┘     └──────┬───────┘                              │
│                               │                                      │
│                               ▼                                      │
│                        ┌──────────────┐                              │
│                        │  PROCESS      │                              │
│                        │  (ASR + NLP)  │                              │
│                        └──────┬───────┘                              │
│                               │                                      │
│              ┌────────────────┼────────────────┐                    │
│              ▼                ▼                ▼                    │
│       ┌──────────┐    ┌──────────┐    ┌──────────┐                 │
│       │  Grammar  │    │  Generate │    │  Pronunc.│                 │
│       │  Check    │    │  Response │    │  Score   │                 │
│       └────┬─────┘    └────┬─────┘    └────┬─────┘                 │
│            │               │               │                        │
│            └───────────────┼───────────────┘                        │
│                            ▼                                         │
│                     ┌──────────────┐                                 │
│                     │  SHOW         │                                 │
│                     │  FEEDBACK     │                                 │
│                     │  + AI REPLY   │                                 │
│                     └──────┬───────┘                                 │
│                            │                                         │
│              ┌─────────────┼─────────────┐                          │
│              ▼                           ▼                          │
│       ┌──────────┐               ┌──────────┐                      │
│       │  Continue │               │  End     │                      │
│       │  (loop)   │               │  Session │                      │
│       └──────────┘               └──────┬───┘                      │
│                                         │                           │
│                                         ▼                           │
│                                  ┌──────────────┐                   │
│                                  │  SUMMARY      │                   │
│                                  │  REPORT       │                   │
│                                  └──────────────┘                   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.4 Technical Specifications

| Spec | Requirement | Measurement |
|------|-------------|-------------|
| Audio Input | 16kHz, mono, WebM/Opus | WebRTC |
| ASR Latency | < 500ms (partial), < 1.5s (final) | Deepgram/Whisper |
| LLM Response | < 1.5s text generation | GPT-4o-mini |
| TTS Output | < 800ms audio generation | OpenAI TTS |
| E2E Latency | < 3s from speech end to AI audio | End-to-end |
| Concurrent Sessions | 1,000+ per instance | Load test |
| Session Duration | 5-30 min (configurable) | Timer |
| Audio Quality | Clear, natural, appropriate speed | User feedback |

### 2.5 Voice Configuration

```python
VOICE_PRESETS = {
    "friendly_female": {
        "provider": "openai",
        "voice_id": "nova",           # Warm, friendly
        "speed": 0.9,                  # Slightly slower for learners
        "stability": 0.65,
        "description": "Giọng nữ thân thiện, phù hợp mọi lứa tuổi"
    },
    "friendly_male": {
        "provider": "openai",
        "voice_id": "echo",           # Clear, friendly
        "speed": 0.9,
        "stability": 0.65,
        "description": "Giọng nam thân thiện, rõ ràng"
    },
    "professional_female": {
        "provider": "openai",
        "voice_id": "shimmer",        # Professional
        "speed": 1.0,
        "stability": 0.70,
        "description": "Giọng nữ chuyên nghiệp, phù hợp luyện IELTS"
    },
    "young_energetic": {
        "provider": "openai",
        "voice_id": "alloy",          # Young, energetic
        "speed": 0.95,
        "stability": 0.60,
        "description": "Giọng trẻ trung, phù hợp học sinh cấp 2"
    }
}

# Speed options
SPEED_OPTIONS = {
    "slow": 0.75,       # Beginner (A1-A2)
    "normal": 0.9,      # Intermediate (B1)
    "natural": 1.0,     # Advanced (B2+)
}
```

### 2.6 Error Handling

| Error | Handling | User Message (Vietnamese) |
|-------|----------|--------------------------|
| ASR timeout | Retry once, then prompt text input | "Không nghe rõ, bạn có thể nói lại hoặc gõ text" |
| ASR low confidence | Show transcript, ask for confirmation | "Bạn có nói '...' không?" |
| LLM timeout | Retry with simpler prompt | "AI đang suy nghĩ, chờ một chút..." |
| LLM error | Fallback to pre-written response | "Có lỗi xảy ra, thử lại nhé" |
| TTS error | Show text only | (Silent, show text) |
| Network disconnect | Save state, offer reconnect | "Mất kết nối, bạn có muốn tiếp tục?" |
| Audio permission denied | Prompt to enable mic | "Cho phép microphone để luyện nói nhé" |

---

## 3. Feature F2: Grammar Correction Engine

### 3.1 Description

Real-time grammar checking that identifies errors, provides corrections, and explains mistakes in Vietnamese with level-appropriate detail.

### 3.2 Grammar Error Categories

```python
GRAMMAR_CATEGORIES = {
    "tense": {
        "name_vi": "Thì",
        "examples": [
            {
                "original": "I go to school yesterday",
                "corrected": "I went to school yesterday",
                "explanation_vi": "Dùng thì Quá khứ đơn (went) vì có 'yesterday' chỉ thời gian quá khứ",
                "rule": "Past Simple: S + V2/V-ed + time marker (yesterday, last week, ago)"
            },
            {
                "original": "I am liking English",
                "corrected": "I like English",
                "explanation_vi": "'Like' là động từ trạng thái, không dùng ở thì Continous",
                "rule": "Stative verbs (like, love, know, want) don't use -ing"
            }
        ]
    },
    "article": {
        "name_vi": "Mạo từ",
        "examples": [
            {
                "original": "I want apple",
                "corrected": "I want an apple",
                "explanation_vi": "Cần mạo từ 'an' trước danh từ đếm được số ít bắt đầu bằng nguyên âm",
                "rule": "a + consonant sound, an + vowel sound"
            },
            {
                "original": "I like the music",
                "corrected": "I like music",
                "explanation_vi": "Không cần 'the' khi nói về music nói chung (general)",
                "rule": "No article for general/uncountable nouns"
            }
        ]
    },
    "preposition": {
        "name_vi": "Giới từ",
        "examples": [
            {
                "original": "I go to school by Monday",
                "corrected": "I go to school on Monday",
                "explanation_vi": "Dùng 'on' với ngày trong tuần, không phải 'by'",
                "rule": "on + days, in + months/seasons, at + times"
            }
        ]
    },
    "word_order": {
        "name_vi": "Trật tự từ",
        "examples": [
            {
                "original": "I very like English",
                "corrected": "I like English very much",
                "explanation_vi": "'Very' không đứng trước động từ. Dùng 'very much' sau động từ",
                "rule": "Adverbs of degree (very, really) modify adjectives, not verbs directly"
            }
        ]
    },
    "subject_verb_agreement": {
        "name_vi": "Sự hòa hợp chủ ngữ - động từ",
        "examples": [
            {
                "original": "He don't like it",
                "corrected": "He doesn't like it",
                "explanation_vi": "He/She/It đi với 'doesn't', không phải 'don't'",
                "rule": "He/She/It + doesn't + V原形"
            }
        ]
    },
    "vocabulary": {
        "name_vi": "Từ vựng",
        "examples": [
            {
                "original": "I want to eat pho please",
                "corrected": "I'd like to have pho, please",
                "explanation_vi": "Dùng 'I'd like' thay vì 'I want' cho lịch sự hơn",
                "rule": "Use 'I'd like' for polite requests"
            }
        ]
    },
    "pronunciation_spelling": {
        "name_vi": "Phát âm chính tả",
        "examples": [
            {
                "original": "I am very happpy",
                "corrected": "I am very happy",
                "explanation_vi": "'Happy' chỉ có 1 chữ p",
                "rule": "Common spelling: happy, happen, apple (1 p)"
            }
        ]
    }
}
```

### 3.3 Grammar Score Calculation

```python
def calculate_grammar_score(
    text: str,
    corrections: List[GrammarCorrection],
    student_level: str
) -> float:
    """
    Calculate grammar score from 0-100.
    
    Scoring logic:
    - Base score: 100
    - Deductions based on error severity and student level
    - Beginners get more lenient scoring
    - Critical errors (communication breakdown) deduct more
    """
    if not text.strip():
        return 0.0
    
    word_count = len(text.split())
    if word_count == 0:
        return 0.0
    
    base_score = 100.0
    
    # Level-based tolerance
    tolerance = {
        "A1": 0.5,   # Very lenient
        "A2": 0.4,
        "B1": 0.3,
        "B2": 0.2,
        "C1": 0.1,   # Strict
        "C2": 0.05
    }.get(student_level, 0.3)
    
    # Deductions per error
    for correction in corrections:
        severity_multiplier = {
            "minor": 2,      # "a" vs "an"
            "moderate": 5,    # tense error
            "major": 10       # communication breakdown
        }.get(correction.severity, 5)
        
        # Apply tolerance (beginners lose less)
        deduction = severity_multiplier * (1 - tolerance)
        base_score -= deduction
    
    # Bonus for longer utterances (more complex = harder)
    length_bonus = min(5, word_count / 10)
    base_score += length_bonus
    
    return max(0, min(100, base_score))
```

### 3.4 Feedback Presentation Rules

```python
FEEDBACK_RULES = {
    "max_corrections_per_turn": 3,      # Don't overwhelm
    "show_severity_order": "major_first", # Most important first
    "inline_highlighting": True,          # Highlight errors in transcript
    "vietnamese_explanation": True,       # Always explain in Vietnamese
    "positive_before_negative": True,     # "Good try! Here's how to improve..."
    "level_appropriate_detail": {
        "A1-A2": "Simple rule + example",
        "B1-B2": "Rule + exception + alternative",
        "C1-C2": "Nuanced explanation + register difference"
    }
}
```

---

## 4. Feature F3: Pronunciation Scoring

### 4.1 Description

Phoneme-level pronunciation assessment with word-by-word scoring and actionable tips for improvement.

### 4.2 Scoring Algorithm

```python
class PronunciationScorer:
    """
    Multi-dimensional pronunciation scoring.
    
    Dimensions:
    1. Accuracy (40%): Phoneme-level correctness
    2. Fluency (25%): Speech rate, pauses, hesitations
    3. Completeness (20%): All words spoken
    4. Prosody (15%): Stress, rhythm, intonation
    """
    
    def score(self, audio: bytes, reference_text: str, student_level: str) -> PronunciationResult:
        # 1. Get phoneme alignment
        alignment = self.aligner.align(audio, reference_text)
        
        # 2. Score each dimension
        accuracy = self.score_accuracy(alignment)
        fluency = self.score_fluency(audio, reference_text)
        completeness = self.score_completeness(alignment, reference_text)
        prosody = self.score_prosody(audio, reference_text)
        
        # 3. Weighted overall score
        overall = (
            accuracy * 0.40 +
            fluency * 0.25 +
            completeness * 0.20 +
            prosody * 0.15
        )
        
        # 4. Word-level scores
        word_scores = []
        for word_alignment in alignment.words:
            word_score = self.score_word(word_alignment)
            word_scores.append(word_score)
        
        # 5. Generate tips for low-scoring words
        tips = []
        for ws in word_scores:
            if ws.score < 70:
                tip = self.generate_tip(ws, student_level)
                tips.append(tip)
        
        return PronunciationResult(
            overall=overall,
            accuracy=accuracy,
            fluency=fluency,
            completeness=completeness,
            prosody=prosody,
            word_scores=word_scores,
            tips=tips
        )
```

### 4.3 Common Pronunciation Errors for Vietnamese Speakers

```python
VN_PRONUNCIATION_ERRORS = {
    "/θ/ (th)": {
        "common_mistake": "/t/ or /s/",
        "examples": ["think → /tɪŋk/", "three → /triː/"],
        "tip_vi": "Đặt lưỡi giữa răng trên và dưới, thổi hơi ra. Gió thổi qua lưỡi.",
        "practice_words": ["think", "three", "thank", "thick", "thin"]
    },
    "/ð/ (th voiced)": {
        "common_mistake": "/d/ or /z/",
        "examples": ["the → /də/", "this → /dɪs/"],
        "tip_vi": "Giống /θ/ nhưng có rung dây thanh. Tay đặt cổ họng thấy rung.",
        "practice_words": ["the", "this", "that", "these", "those"]
    },
    "/r/ vs /l/": {
        "common_mistake": "Confused or merged",
        "examples": ["right → /laɪt/", "light → /raɪt/"],
        "tip_vi": "/r/: Cuộn lưỡi lên, không chạm vòm miệng. /l/: Lưỡi chạm vòm miệng phía sau răng.",
        "practice_words": ["right/light", "road/load", "red/led"]
    },
    "/ɪ/ vs /iː/": {
        "common_mistake": "Both pronounced as /iː/",
        "examples": ["ship → /ʃiːp/", "sit → /siːt/"],
        "tip_vi": "/ɪ/: Miệng mở rộng, ngắn. /iː/: Miệng kéo dài, cười.",
        "practice_words": ["ship/sheep", "sit/seat", "bit/beat"]
    },
    "/æ/": {
        "common_mistake": "/ɛ/ or /a/",
        "examples": ["cat → /kɛt/", "bad → /bɑːd/"],
        "tip_vi": "Miệng mở rộng ngang, hạ hàm dưới. Giống nói 'e' nhưng mở miệng hơn.",
        "practice_words": ["cat", "bad", "man", "hand", "stand"]
    },
    "/v/": {
        "common_mistake": "/b/ (Vietnamese doesn't have /v/)",
        "examples": ["very → /ˈbɛri/", "video → /ˈbɪdioʊ/"],
        "tip_vi": "Răng trên cắn nhẹ môi dưới, thổi hơi ra. Khác /b/ (môi chạm nhau).",
        "practice_words": ["very", "video", "vine", "view", "voice"]
    },
    "Final consonants": {
        "common_mistake": "Dropped or unreleased",
        "examples": ["good → /gʊ/", "like → /laɪ/"],
        "tip_vi": "Tiếng Việt không có phụ âm cuối mạnh. Phải phát âm rõ: /d/, /k/, /t/ cuối từ.",
        "practice_words": ["good", "like", "want", "help", "speak"]
    },
    "Word stress": {
        "common_mistake": "Equal stress on all syllables",
        "examples": ["PHO-toGRAPH vs pho-TO-gra-pher"],
        "tip_vi": "Nhấn mạnh 1 âm tiết, các âm còn lại nhẹ hơn. VD: pho-TO-gra-pher",
        "practice_words": ["photograph", "photographer", "interesting", "comfortable"]
    }
}
```

### 4.4 Pronunciation Feedback UI Spec

```
┌─────────────────────────────────────────────────────────────────────┐
│  PRONUNCIATION FEEDBACK UI SPECIFICATION                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Layout:                                                             │
│  ├── Header: Sentence text + overall score                          │
│  ├── Word grid: Each word with color-coded score                    │
│  ├── Detail panel: Selected word breakdown                          │
│  ├── Tips section: Vietnamese explanation + practice words          │
│  └── Action buttons: Listen / Try Again                             │
│                                                                      │
│  Color coding:                                                       │
│  ├── 90-100: Green (#22C55E) — Excellent                            │
│  ├── 70-89:  Blue (#3B82F6) — Good                                  │
│  ├── 50-69:  Orange (#F59E0B) — Needs improvement                   │
│  └── 0-49:   Red (#EF4444) — Practice more                          │
│                                                                      │
│  Interactions:                                                       │
│  ├── Tap word → Show phoneme breakdown + tips                       │
│  ├── Tap speaker icon → Play correct pronunciation                  │
│  ├── Tap mic icon → Re-practice that specific word                  │
│  └── Swipe left/right → Navigate between words                      │
│                                                                      │
│  Mobile responsive:                                                  │
│  ├── Phone: 2 words per row                                         │
│  ├── Tablet: 4 words per row                                        │
│  └── Desktop: Full width, side-by-side with conversation            │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 5. Feature F4: Topic-Based Conversations

### 5.1 Topic Database

```python
TOPICS = {
    # === A1-A2 Level (Beginner) ===
    "daily-life": {
        "greetings": {
            "title_en": "Meeting New People",
            "title_vi": "Gặp Gỡ Người Mới",
            "level": "A1",
            "scenario": "You're at a school event and meeting new classmates",
            "ai_role": "Friendly new classmate",
            "turns": 8,
            "target_vocabulary": ["hello", "nice to meet you", "name", "from", "like"],
            "target_grammar": ["My name is...", "I'm from...", "I like..."],
            "curriculum": "Grade 6, Unit 1"
        },
        "family": {
            "title_en": "Talking About Family",
            "title_vi": "Nói Về Gia Đình",
            "level": "A1",
            "scenario": "Your new friend asks about your family",
            "ai_role": "Curious classmate",
            "turns": 10,
            "target_vocabulary": ["mother", "father", "sister", "brother", "older", "younger"],
            "target_grammar": ["I have...", "She/He is...", "How many...?"],
            "curriculum": "Grade 6, Unit 3"
        },
        "hobbies": {
            "title_en": "What Do You Like?",
            "title_vi": "Bạn Thích Gì?",
            "level": "A1",
            "scenario": "Chatting with a friend about hobbies and free time",
            "ai_role": "Curious friend",
            "turns": 10,
            "target_vocabulary": ["play", "watch", "listen", "read", "favorite"],
            "target_grammar": ["I like + V-ing", "Do you like...?", "My favorite..."],
            "curriculum": "Grade 6, Unit 5"
        },
        "food": {
            "title_en": "At the Restaurant",
            "title_vi": "Tại Nhà Hàng",
            "level": "A2",
            "scenario": "You're ordering food at a Vietnamese restaurant with a foreign friend",
            "ai_role": "Friendly waiter",
            "turns": 12,
            "target_vocabulary": ["order", "recommend", "bill", "delicious", "spicy"],
            "target_grammar": ["I'd like...", "Could I have...?", "How much...?"],
            "curriculum": "Grade 7, Unit 4"
        },
        "weather": {
            "title_en": "Weather and Seasons",
            "title_vi": "Thời Tiết và Mùa",
            "level": "A2",
            "scenario": "Talking about weather with a foreign friend visiting Vietnam",
            "ai_role": "Foreign friend visiting Vietnam",
            "turns": 10,
            "target_vocabulary": ["hot", "cold", "rainy", "sunny", "season"],
            "target_grammar": ["It's + adjective", "What's the weather like?", "In Vietnam..."],
            "curriculum": "Grade 7, Unit 6"
        }
    },
    
    # === B1 Level (Intermediate) ===
    "school": {
        "subjects": {
            "title_en": "Favorite Subjects",
            "title_vi": "Môn Học Yêu Thích",
            "level": "B1",
            "scenario": "Discussing school subjects with an exchange student",
            "ai_role": "Exchange student from the US",
            "turns": 12,
            "target_vocabulary": ["mathematics", "literature", "difficult", "interesting", "prefer"],
            "target_grammar": ["I prefer... because...", "Comparatives", "Superlatives"],
            "curriculum": "Grade 9, Unit 1"
        },
        "exams": {
            "title_en": "Preparing for Exams",
            "title_vi": "Chuẩn Bị Thi",
            "level": "B1",
            "scenario": "Talking to a classmate about exam preparation strategies",
            "ai_role": "Studious classmate",
            "turns": 12,
            "target_vocabulary": ["review", "concentrate", "schedule", "nervous", "confident"],
            "target_grammar": ["Should/shouldn't", "If I..., I will...", "Present Perfect"],
            "curriculum": "Grade 10, Unit 2"
        }
    },
    
    # === B1-B2 Level (Upper Intermediate) ===
    "travel": {
        "airport": {
            "title_en": "At the Airport",
            "title_vi": "Tại Sân Bay",
            "level": "B1",
            "scenario": "You're at Tan Son Nhat airport, checking in for a flight",
            "ai_role": "Airport staff",
            "turns": 15,
            "target_vocabulary": ["boarding pass", "luggage", "departure", "gate", "delay"],
            "target_grammar": ["Passive voice", "Will for predictions", "Conditionals"],
            "curriculum": "Grade 11, Unit 5"
        },
        "hotel": {
            "title_en": "Booking a Hotel",
            "title_vi": "Đặt Phòng Khách Sạn",
            "level": "B1",
            "scenario": "Calling a hotel to book a room for your family vacation",
            "ai_role": "Hotel receptionist",
            "turns": 12,
            "target_vocabulary": ["reservation", "available", "check-in", "check-out", "amenities"],
            "target_grammar": ["Would like to", "How much does... cost?", "Conditionals"],
            "curriculum": "Grade 11, Unit 6"
        }
    },
    
    # === IELTS Preparation ===
    "ielts": {
        "part1_personal": {
            "title_en": "IELTS Part 1: Personal Questions",
            "title_vi": "IELTS Part 1: Câu Hỏi Cá Nhân",
            "level": "B1-B2",
            "scenario": "IELTS speaking examiner asking personal questions",
            "ai_role": "IELTS examiner",
            "turns": 15,
            "target_vocabulary": ["fluency markers", "discourse markers"],
            "target_grammar": ["Tense variety", "Complex sentences"],
            "time_per_response": "30-45 seconds"
        },
        "part2_cuecard": {
            "title_en": "IELTS Part 2: Cue Card",
            "title_vi": "IELTS Part 2: Thẻ Chủ Đề",
            "level": "B2",
            "scenario": "Describe a place you would like to visit",
            "ai_role": "IELTS examiner",
            "turns": 3,
            "prep_time": "1 minute",
            "speak_time": "2 minutes",
            "target_vocabulary": ["Descriptive language", "Sequencing words"],
            "target_grammar": ["Future forms", "Hypothetical language"]
        }
    },
    
    # === Vietnamese Culture Topics ===
    "culture": {
        "tet": {
            "title_en": "Explaining Tet to a Foreigner",
            "title_vi": "Giải Thích Tết Cho Người Nước Ngoài",
            "level": "B1",
            "scenario": "A foreign friend asks you about Vietnamese New Year",
            "ai_role": "Curious foreign friend",
            "turns": 12,
            "target_vocabulary": ["lunar new year", "tradition", "celebration", "lucky money", "ancestor"],
            "target_grammar": ["Used to", "Present Perfect for experiences", "Cultural explanations"]
        },
        "pho": {
            "title_en": "Vietnamese Food Culture",
            "title_vi": "Văn Hóa Ẩm Thực Việt",
            "level": "A2-B1",
            "scenario": "Teaching a foreigner about Vietnamese food",
            "ai_role": "Foreign food blogger visiting Vietnam",
            "turns": 12,
            "target_vocabulary": ["ingredients", "recipe", "traditional", "popular", "recommend"],
            "target_grammar": ["Imperatives for instructions", "Passive voice", "Comparatives"]
        }
    }
}
```

---

## 6. Feature F5: Vocabulary Builder

### 6.1 Description

Automated vocabulary extraction from conversations + spaced repetition system for long-term retention.

### 6.2 Vocabulary Extraction from Conversations

```python
class VocabularyExtractor:
    """Extract new vocabulary from conversation turns."""
    
    def extract(self, conversation_turn: ConversationTurn, user_vocab: Set[str]) -> List[NewVocabulary]:
        """
        Extract vocabulary from a conversation turn.
        
        Criteria for extraction:
        1. Word is not in user's known vocabulary
        2. Word is above user's current level (not too easy)
        3. Word appeared in meaningful context
        4. Word is a content word (noun, verb, adj, adv) — not function words
        """
        words = self.tokenize(conversation_turn.ai_text)
        
        new_vocab = []
        for word in words:
            if self.is_content_word(word) and word.lower() not in user_vocab:
                entry = self.lookup_word(word)
                if entry.level >= self.user_level_threshold(conversation_turn.user_level):
                    new_vocab.append(NewVocabulary(
                        word=word,
                        phonetic=entry.phonetic,
                        part_of_speech=entry.pos,
                        meaning_en=entry.definition,
                        meaning_vi=entry.definition_vi,
                        example_from_conversation=self.extract_context(word, conversation_turn),
                        source="conversation"
                    ))
        
        return new_vocab[:3]  # Max 3 new words per turn (don't overwhelm)
```

### 6.3 Review UI Specification

```
┌─────────────────────────────────────────────────────────────────────┐
│  VOCABULARY REVIEW UI                                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  State 1: Show word                                                  │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                              │   │
│  │                    "recommend"                                │   │
│  │                    /ˌrekəˈmend/                               │   │
│  │                    [verb]                                     │   │
│  │                                                              │   │
│  │  Meaning: ?                                                  │   │
│  │                                                              │   │
│  │  [🔊 Listen]  [Show Answer]                                  │   │
│  │                                                              │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  State 2: Reveal answer                                              │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                              │   │
│  │                    "recommend"                                │   │
│  │                    /ˌrekəˈmend/                               │   │
│  │                    [verb]                                     │   │
│  │                                                              │   │
│  │  Meaning: giới thiệu, khuyên dùng                            │   │
│  │  "I recommend the pho bo."                                   │   │
│  │                                                              │   │
│  │  How well did you know this?                                 │   │
│  │  [1 Again] [2 Hard] [3 Good] [4 Easy] [5 Perfect]           │   │
│  │                                                              │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  Rating → Next Review Interval:                                      │
│  ├── 1 (Again): 1 minute                                            │
│  ├── 2 (Hard): 1 day                                                │
│  ├── 3 (Good): 3 days                                               │
│  ├── 4 (Easy): 7 days                                               │
│  └── 5 (Perfect): 14 days                                           │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 7. Feature F6: Parent Dashboard

### 7.1 Description

Separate web/app interface for parents to monitor their children's learning progress.

### 7.2 Dashboard Sections

```
┌─────────────────────────────────────────────────────────────────────┐
│  PARENT DASHBOARD SPECIFICATION                                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Section 1: Overview Card                                            │
│  ├── Child name + photo                                             │
│  ├── Current level (CEFR)                                           │
│  ├── Weekly practice time (vs goal)                                 │
│  ├── Current streak (days)                                          │
│  └── Overall score trend (↑↓→)                                     │
│                                                                      │
│  Section 2: Weekly Activity                                          │
│  ├── Bar chart: practice minutes per day (7 days)                   │
│  ├── Conversations completed this week                              │
│  ├── New words learned                                              │
│  └── Compared to last week (% change)                               │
│                                                                      │
│  Section 3: Progress Chart                                           │
│  ├── Line chart: overall score over 4 weeks                         │
│  ├── Grammar score trend                                            │
│  ├── Pronunciation score trend                                      │
│  └── Fluency score trend                                            │
│                                                                      │
│  Section 4: Strengths & Improvements                                 │
│  ├── Top 3 strengths (with examples)                                │
│  ├── Top 3 areas to improve (with tips)                             │
│  └── Teacher's note (if school license)                             │
│                                                                      │
│  Section 5: Recent Activity                                          │
│  ├── List of recent conversations                                   │
│  ├── Topic + score + duration                                       │
│  └── Expandable: turn-by-turn transcript                            │
│                                                                      │
│  Section 6: Actions                                                  │
│  ├── [📧 Send weekly report to Zalo]                                │
│  ├── [📊 Download full report (PDF)]                                │
│  ├── [⚙️ Settings (goals, notifications)]                           │
│  └── [👨‍👩‍👧 Add another child]                                        │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 7.3 Notification System

```python
NOTIFICATION_CONFIG = {
    "weekly_report": {
        "channel": "zalo",          # Primary channel for VN parents
        "frequency": "weekly",      # Every Sunday 8 PM
        "content": {
            "practice_minutes": "int",
            "conversations_completed": "int",
            "new_words_learned": "int",
            "score_change": "float",
            "strengths": "List[str]",
            "areas_to_improve": "List[str]",
            "link_to_dashboard": "str"
        }
    },
    "milestone_alert": {
        "trigger": "streak == 7 or streak == 30 or streak == 100",
        "channel": "zalo",
        "content": "🎉 Minh đã luyện tập {streak} ngày liên tiếp!"
    },
    "grade_improvement": {
        "trigger": "score increased > 10% in 2 weeks",
        "channel": "zalo",
        "content": "📈 Điểm phát âm của Minh đã tăng {improvement}%!"
    },
    "inactivity_alert": {
        "trigger": "no practice for 3 days",
        "channel": "zalo",
        "content": "⏰ Minh chưa luyện tập 3 ngày. Nhắc con luyện tập nhé!"
    }
}
```

---

## 8. Feature F7: AI Video Avatar (Phase 3)

### 8.1 Description

Real-time AI video avatar that serves as conversation partner with lip-sync, facial expressions, and personality.

### 8.2 Avatar Specifications

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
            "voice": "friendly_female"
        },
        "friendly_teacher_male": {
            "appearance": "Young Vietnamese man, casual",
            "personality": "Enthusiastic, clear, supportive",
            "voice": "friendly_male"
        },
        "international_female": {
            "appearance": "Western woman, professional",
            "personality": "Professional, clear pronunciation",
            "voice": "professional_female"
        }
    }
}
```

---

## 9. Feature F8: IELTS Mock Speaking Test (Phase 3)

### 9.1 Description

Simulated IELTS Speaking test with band score prediction and detailed feedback.

### 9.2 IELTS Scoring Rubric

```python
IELTS_CRITERIA = {
    "fluency_and_coherence": {
        "weight": 0.25,
        "bands": {
            "9": "Speaks fluently with only rare repetition or self-correction",
            "7": "Speaks at length without noticeable effort or loss of coherence",
            "5": "Usually maintains flow but uses repetition, self-correction and/or slow speech",
            "3": "Cannot respond without noticeable pauses; may repeat words"
        }
    },
    "lexical_resource": {
        "weight": 0.25,
        "bands": {
            "9": "Uses vocabulary with full flexibility and precision",
            "7": "Uses vocabulary resourcefully to discuss a variety of topics",
            "5": "Manages to talk about familiar topics but vocabulary limited",
            "3": "Only uses isolated words or memorized phrases"
        }
    },
    "grammatical_range_and_accuracy": {
        "weight": 0.25,
        "bands": {
            "9": "Uses a full range of structures naturally and appropriately",
            "7": "Uses a range of complex structures with flexibility",
            "5": "Uses a limited range of complex structures but with limited flexibility",
            "3": "Cannot use basic sentence forms"
        }
    },
    "pronunciation": {
        "weight": 0.25,
        "bands": {
            "9": "Uses a full range of pronunciation features with precision",
            "7": "Shows all positive features; uses some less common features",
            "5": "Shows some effective use of features but control is limited",
            "3": "Speech is often unintelligible"
        }
    }
}
```

---

## 10. Feature F9: Homework Help (Phase 3)

### 10.1 Description

Photo-based homework help where students snap a photo of their English homework and get AI explanations.

### 10.2 Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│  HOMEWORK HELP FLOW                                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  1. Student takes photo of homework                                  │
│       │                                                              │
│       ▼                                                              │
│  2. OCR + AI Vision processes image                                  │
│       ├── Extract text (Vietnamese handwriting OCR)                 │
│       ├── Identify question type (grammar, vocab, reading, etc.)    │
│       └── Parse exercise format (fill-in, multiple choice, essay)   │
│       │                                                              │
│       ▼                                                              │
│  3. AI generates explanation                                         │
│       ├── Step-by-step solution (in Vietnamese)                     │
│       ├── Grammar rule explanation                                  │
│       ├── Similar examples                                          │
│       └── Practice problems                                         │
│       │                                                              │
│       ▼                                                              │
│  4. Student can ask follow-up questions                              │
│       └── "Tại sao dùng 'went' mà không phải 'goed'?"             │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 11. Gamification System

### 11.1 XP & Leveling

```python
XP_REWARDS = {
    "complete_conversation": 50,
    "perfect_grammar_turn": 10,
    "new_vocabulary_learned": 5,
    "daily_streak_bonus": 20,          # Per day of streak
    "weekly_goal_met": 100,
    "pronunciation_improvement": 15,    # Score improved vs last time
}

LEVELS = [
    {"level": 1, "xp_required": 0, "title": "Seed", "title_vi": "Hạt Giống"},
    {"level": 2, "xp_required": 100, "title": "Sprout", "title_vi": "Mầm Non"},
    {"level": 3, "xp_required": 300, "title": "Sapling", "title_vi": "Cây Non"},
    {"level": 4, "xp_required": 600, "title": "Tree", "title_vi": "Cây Trưởng Thành"},
    {"level": 5, "xp_required": 1000, "title": "Forest", "title_vi": "Khu Rừng"},
    {"level": 6, "xp_required": 1500, "title": "Mountain", "title_vi": "Ngọn Núi"},
    {"level": 7, "xp_required": 2500, "title": "Sky", "title_vi": "Bầu Trời"},
    {"level": 8, "xp_required": 4000, "title": "Star", "title_vi": "Ngôi Sao"},
    {"level": 9, "xp_required": 6000, "title": "Galaxy", "title_vi": "Thiên Hà"},
    {"level": 10, "xp_required": 10000, "title": "Universe", "title_vi": "Vũ Trụ"}
]
```

### 11.2 Achievements

```python
ACHIEVEMENTS = [
    {"id": "first_conversation", "name_vi": "Bước Đầu Tiên", "condition": "Complete 1 conversation"},
    {"id": "week_streak", "name_vi": "7 Ngày Liên Tiếp", "condition": "7-day practice streak"},
    {"id": "month_streak", "name_vi": "30 Ngày Kiên Trì", "condition": "30-day practice streak"},
    {"id": "100_conversations", "name_vi": "Trăm Trận", "condition": "Complete 100 conversations"},
    {"id": "grammar_master", "name_vi": "Bậc Thầy Ngữ Pháp", "condition": "Grammar score > 90 for 10 sessions"},
    {"id": "pronunciation_pro", "name_vi": "Phát Âm Chuẩn", "condition": "Pronunciation score > 85 for 10 sessions"},
    {"id": "vocab_collector", "name_vi": "Sưu Tập Từ Vựng", "condition": "Learn 500 words"},
    {"id": "topic_explorer", "name_vi": "Khám Phá Chủ Đề", "condition": "Try 20 different topics"},
    {"id": "night_owl", "name_vi": "Cú Đêm", "condition": "Practice after 10 PM 10 times"},
    {"id": "early_bird", "name_vi": "Chim Sớm", "condition": "Practice before 7 AM 10 times"}
]
```
