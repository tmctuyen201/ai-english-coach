"""
AI English Coach — Voice Conversation Room Server
Real-time 1v1 voice conversation between student and AI teacher.
"""
import os
import json
import asyncio
import hashlib
from datetime import datetime
from typing import Dict, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
PORT = int(os.getenv("PORT", "8089"))

app = FastAPI(title="AI English Coach — Voice Room")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# ---------------------------------------------------------------------------
# Topic Definitions
# ---------------------------------------------------------------------------
TOPICS = {
    "free-chat": {
        "id": "free-chat",
        "title_en": "Free Chat",
        "title_vi": "Nói Chuyện Tự Do",
        "level": "A2",
        "icon": "💬",
        "system_prompt": """You are a friendly, patient English conversation partner for Vietnamese students.

RULES:
1. Keep responses SHORT (1-3 sentences max)
2. Speak naturally, like a real friend talking
3. If the student makes a grammar mistake, correct it NATURALLY by using the correct form in your next response — don't lecture or break the conversation flow
4. If the student seems stuck or says something very short, ask a follow-up question to keep them talking
5. Be warm and encouraging — celebrate small wins ("Great!", "Nice sentence!")
6. Use vocabulary appropriate for the student's level
7. If the student uses Vietnamese, gently guide them back to English
8. Ask ONE question at a time — don't overload with multiple questions
9. Be genuinely interested in what they say — react to their content"""
    },
    "ordering-food": {
        "id": "ordering-food",
        "title_en": "Ordering Food",
        "title_vi": "Gọi Món",
        "level": "A2",
        "icon": "🍜",
        "system_prompt": """You are a friendly waiter at a Vietnamese restaurant called "Pho 24".

SCENARIO: A customer (the student) is ordering food.

RULES:
1. Stay in character as the waiter
2. Keep responses SHORT (1-2 sentences)
3. Greet them warmly, ask what they'd like to order
4. If they make grammar mistakes, naturally use the correct form in your response
5. Recommend dishes, ask about preferences (beef/chicken, spicy/mild)
6. Be patient and helpful — guide them through ordering
7. Use simple vocabulary appropriate for A2 level
8. After they order, confirm the order and ask if they want anything else"""
    },
    "meeting-people": {
        "id": "meeting-people",
        "title_en": "Meeting New People",
        "title_vi": "Gặp Gỡ Người Mới",
        "level": "A1",
        "icon": "👋",
        "system_prompt": """You are a friendly new classmate meeting the student for the first time at a school event.

RULES:
1. Keep responses VERY SHORT (1-2 sentences) — this is A1 level
2. Use simple words and short sentences
3. Ask basic questions: name, age, hobbies, where they're from
4. Be warm and smiley (use friendly tone)
5. If they make mistakes, gently use the correct form in your response
6. Share a little about yourself too (make up a name, hobbies)
7. Be patient — this might be their first English conversation ever"""
    },
    "ielts-part1": {
        "id": "ielts-part1",
        "title_en": "IELTS Part 1",
        "title_vi": "IELTS Part 1",
        "level": "B1-B2",
        "icon": "🎯",
        "system_prompt": """You are an IELTS Speaking examiner conducting Part 1 of the test.

SCENARIO: You are asking the student personal questions about familiar topics (home, family, work, studies, hobbies).

RULES:
1. Be professional but friendly — like a real IELTS examiner
2. Ask ONE question at a time
3. Keep questions clear and appropriate for Part 1
4. After each answer, acknowledge briefly and move to next question
5. Cover 3-4 different topics in the session
6. Topics: hometown, family, studies/work, hobbies, daily routine, food, weather, travel
7. Don't correct grammar during the test — just listen and note
8. At the end, thank them and give a brief overall impression (not a band score)"""
    },
    "job-interview": {
        "id": "job-interview",
        "title_en": "Job Interview",
        "title_vi": "Phỏng Vấn Xin Việc",
        "level": "B1",
        "icon": "💼",
        "system_prompt": """You are an HR manager interviewing the student for a part-time position.

RULES:
1. Be professional but approachable
2. Ask common interview questions one at a time
3. Questions: Tell me about yourself, Why do you want this job?, What are your strengths/weaknesses?, Do you have any experience?, When can you start?
4. React to their answers naturally
5. If they make grammar mistakes, note them but don't interrupt — correct naturally in your responses
6. At the end, tell them you'll be in touch and give feedback on their English"""
    }
}

# ---------------------------------------------------------------------------
# Conversation sessions (in-memory)
# ---------------------------------------------------------------------------
sessions: Dict[str, dict] = {}

# ---------------------------------------------------------------------------
# LLM Call via OpenRouter
# ---------------------------------------------------------------------------
async def call_llm(messages: list) -> str:
    """Call LLM via OpenRouter API."""
    if not OPENROUTER_API_KEY:
        # Fallback responses if no API key
        fallbacks = [
            "That's interesting! Can you tell me more?",
            "Good try! I understand what you mean. What else?",
            "Nice! Let me ask you — what do you like to do in your free time?",
            "I see! That's a great answer. Keep going!",
            "Wonderful! Your English is getting better. What else would you like to talk about?",
        ]
        import random
        return random.choice(fallbacks)

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://aistudy.io.vn",
                    "X-Title": "AI English Coach"
                },
                json={
                    "model": OPENROUTER_MODEL,
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 150,
                }
            )
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"].strip()
            else:
                print(f"LLM error: {response.status_code} {response.text[:200]}")
                return "That's interesting! Can you tell me more?"
    except Exception as e:
        print(f"LLM exception: {e}")
        return "I'm thinking... Can you say that again?"

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/")
async def index():
    return FileResponse("landing.html")

@app.get("/auth")
async def auth_page():
    return FileResponse("auth.html")

@app.get("/room")
async def room_page():
    return FileResponse("conversation-room.html")

@app.get("/conversation-room.html")
async def room_page_alias():
    return FileResponse("conversation-room.html")

@app.get("/landing.html")
async def landing_alias():
    return FileResponse("landing.html")

@app.get("/auth.html")
async def auth_alias():
    return FileResponse("auth.html")

@app.get("/health")
async def health():
    return {"status": "healthy", "active_sessions": len(sessions)}

# ---------------------------------------------------------------------------
# Auth API (for login page)
# ---------------------------------------------------------------------------
otp_store: Dict[str, str] = {}

@app.post("/api/v1/auth/phone/send-otp")
async def send_otp(body: dict):
    phone = body.get("phone", "")
    if not phone:
        return {"detail": "Phone required"}
    otp = "123456"  # Demo: always use 123456
    otp_store[phone] = otp
    return {"message": "OTP sent", "phone": phone}

@app.post("/api/v1/auth/phone/verify")
async def verify_otp(body: dict):
    phone = body.get("phone", "")
    otp = body.get("otp", "")
    stored = otp_store.get(phone)
    if not stored or stored != otp:
        return {"detail": "Invalid OTP"}
    del otp_store[phone]
    return {"access_token": f"demo-token-{phone}"}

# ---------------------------------------------------------------------------
# WebSocket — Conversation Room
# ---------------------------------------------------------------------------
@app.websocket("/ws/room/{session_id}")
async def conversation_room(websocket: WebSocket, session_id: str):
    await websocket.accept()
    print(f"[Room {session_id}] Connected")

    # Initialize session
    if session_id not in sessions:
        sessions[session_id] = {
            "messages": [],
            "topic": "free-chat",
            "turn_count": 0,
            "created_at": datetime.now().isoformat()
        }

    session = sessions[session_id]

    try:
        while True:
            raw = await websocket.receive_text()
            data = json.loads(raw)
            msg_type = data.get("type")

            # ---- Start conversation ----
            if msg_type == "start":
                topic_id = data.get("topic", "free-chat")
                student_name = data.get("name", "Student")
                session["topic"] = topic_id
                session["student_name"] = student_name
                topic = TOPICS.get(topic_id, TOPICS["free-chat"])

                # System prompt
                session["messages"] = [
                    {"role": "system", "content": topic["system_prompt"]},
                    {"role": "system", "content": f"The student's name is {student_name}. Start the conversation with a warm greeting appropriate for the topic '{topic['title_en']}'. Keep it SHORT (1-2 sentences)."}
                ]

                # Generate greeting
                greeting = await call_llm(session["messages"])
                session["messages"].append({"role": "assistant", "content": greeting})
                session["turn_count"] = 0

                await websocket.send_json({
                    "type": "ai_greeting",
                    "text": greeting,
                    "topic": topic["title_en"],
                    "topic_vi": topic["title_vi"]
                })
                print(f"[Room {session_id}] Started topic: {topic_id}")

            # ---- Student speaks ----
            elif msg_type == "student_speech":
                text = data.get("text", "").strip()
                if not text:
                    await websocket.send_json({"type": "error", "message": "I didn't catch that. Could you try again?"})
                    continue

                session["turn_count"] += 1
                print(f"[Room {session_id}] Turn {session['turn_count']}: Student said: {text}")

                # Add student message to history
                session["messages"].append({"role": "user", "content": text})

                # Keep conversation history manageable (last 20 messages)
                if len(session["messages"]) > 22:
                    session["messages"] = [session["messages"][0]] + session["messages"][-20:]

                # Send "thinking" indicator
                await websocket.send_json({"type": "ai_thinking"})

                # Generate AI response
                ai_response = await call_llm(session["messages"])
                session["messages"].append({"role": "assistant", "content": ai_response})

                # Send response
                await websocket.send_json({
                    "type": "ai_response",
                    "text": ai_response,
                    "turn": session["turn_count"]
                })
                print(f"[Room {session_id}] AI: {ai_response}")

            # ---- End session ----
            elif msg_type == "end":
                # Generate summary
                summary_prompt = [
                    {"role": "system", "content": "You are a helpful English teacher. Summarize this conversation in 2-3 sentences. Mention what the student did well and one area to improve. Be encouraging. Respond in English."},
                ] + session["messages"][-10:] + [
                    {"role": "user", "content": "Please give me a brief summary of our conversation and feedback on my English."}
                ]
                summary = await call_llm(summary_prompt)

                await websocket.send_json({
                    "type": "session_summary",
                    "turns": session["turn_count"],
                    "summary": summary
                })

                # Clean up
                del sessions[session_id]
                print(f"[Room {session_id}] Ended. {session['turn_count']} turns.")
                break

            # ---- Ping ----
            elif msg_type == "ping":
                await websocket.send_json({"type": "pong"})

    except WebSocketDisconnect:
        print(f"[Room {session_id}] Disconnected")
        if session_id in sessions:
            del sessions[session_id]
    except Exception as e:
        print(f"[Room {session_id}] Error: {e}")
        try:
            await websocket.send_json({"type": "error", "message": str(e)})
        except:
            pass

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    print(f"🚀 AI English Coach — Voice Room starting on port {PORT}")
    print(f"📡 OpenRouter: {'✅ configured' if OPENROUTER_API_KEY else '❌ not set (using fallback)'}")
    print(f"🌐 Open http://localhost:{PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
