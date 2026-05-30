"""
Playwright E2E Tests — AI English Coach Conversation Room
Tests the room/conversation-room.html UI served by room/server.py
"""
import pytest
from playwright.sync_api import sync_playwright, expect

BASE_URL = "http://localhost:8089/room"


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    ctx = browser.new_context()
    page = ctx.new_page()
    page.goto(BASE_URL)
    page.wait_for_load_state("domcontentloaded")
    yield page
    ctx.close()


def _enter_room(page, name="TestUser"):
    page.fill("#name-input", name)
    page.locator(".topic-btn").first.click()
    page.click("#start-btn")
    page.wait_for_timeout(800)


# ── LOBBY ────────────────────────────────────────────────────

def test_page_loads(page):
    expect(page).to_have_title("AI English Coach — Voice Room")

def test_name_input_exists(page):
    expect(page.locator("#name-input")).to_be_visible()

def test_topic_buttons_exist(page):
    assert page.locator(".topic-btn").count() >= 3

def test_select_topic(page):
    btn = page.locator(".topic-btn").nth(1)
    btn.click()
    classes = btn.get_attribute("class") or ""
    assert "selected" in classes

def test_start_button_exists(page):
    expect(page.locator("#start-btn")).to_be_visible()


# ── ROOM ─────────────────────────────────────────────────────

def test_start_room_shows_room(page):
    _enter_room(page)
    expect(page.locator("#room")).to_be_visible()

def test_room_has_chat(page):
    _enter_room(page)
    expect(page.locator("#chat")).to_be_visible()

def test_room_has_mic_button(page):
    _enter_room(page)
    expect(page.locator(".mic")).to_be_visible()

def test_room_has_end_button(page):
    _enter_room(page)
    expect(page.locator(".topbar-end")).to_be_visible()

def test_room_has_mode_toggle(page):
    _enter_room(page)
    expect(page.locator("#mode-voice")).to_be_visible()
    expect(page.locator("#mode-text")).to_be_visible()


# ── MODE SWITCH ──────────────────────────────────────────────

def test_switch_to_text_mode(page):
    _enter_room(page)
    page.click("#mode-text")
    text_mode = page.locator("#text-mode")
    assert text_mode.is_visible()

def test_text_input_in_text_mode(page):
    _enter_room(page)
    page.click("#mode-text")
    expect(page.locator("#text-input")).to_be_visible()


# ── TEXT CONVERSATION ────────────────────────────────────────

def test_send_text_message(page):
    _enter_room(page)
    page.wait_for_timeout(1500)  # Wait for AI greeting
    page.click("#mode-text")
    page.fill("#text-input", "Hello, how are you?")
    page.press("#text-input", "Enter")
    page.wait_for_timeout(300)
    student_msgs = page.locator(".msg.student")
    assert student_msgs.count() >= 1

def test_ai_responds_to_text(page):
    _enter_room(page)
    page.wait_for_timeout(1500)
    page.click("#mode-text")
    page.fill("#text-input", "Hello!")
    page.press("#text-input", "Enter")
    page.wait_for_timeout(6000)  # Wait for AI response
    ai_msgs = page.locator(".msg.ai")
    assert ai_msgs.count() >= 2  # greeting + response


# ── END SESSION ──────────────────────────────────────────────

def test_end_shows_summary(page):
    _enter_room(page)
    page.wait_for_timeout(1500)
    page.click(".topbar-end")
    page.wait_for_timeout(4000)
    modal = page.locator("#summary-modal")
    classes = modal.get_attribute("class") or ""
    assert "show" in classes

def test_summary_has_feedback(page):
    _enter_room(page)
    page.wait_for_timeout(1500)
    page.click(".topbar-end")
    page.wait_for_timeout(4000)
    feedback = page.locator("#sum-feedback")
    assert len(feedback.text_content() or "") > 0

def test_close_summary_returns_to_lobby(page):
    _enter_room(page)
    page.wait_for_timeout(1500)
    page.click(".topbar-end")
    page.wait_for_timeout(4000)
    page.click(".close-btn")
    page.wait_for_timeout(500)
    expect(page.locator("#lobby")).to_be_visible()


# ── NAVIGATION ───────────────────────────────────────────────

def test_back_leaves_room(page):
    _enter_room(page)
    page.click(".topbar-back")
    page.wait_for_timeout(500)
    expect(page.locator("#lobby")).to_be_visible()


# ── RESPONSIVE ───────────────────────────────────────────────

def test_mobile_viewport(browser):
    ctx = browser.new_context(viewport={"width": 390, "height": 844})
    page = ctx.new_page()
    page.goto(BASE_URL)
    page.wait_for_load_state("domcontentloaded")
    expect(page.locator("#lobby")).to_be_visible()
    ctx.close()

def test_desktop_viewport(browser):
    ctx = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = ctx.new_page()
    page.goto(BASE_URL)
    page.wait_for_load_state("domcontentloaded")
    expect(page.locator("#lobby")).to_be_visible()
    ctx.close()
