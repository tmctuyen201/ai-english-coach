"""E2E tests for the AI English Coach conversation room UI."""
import re
import pytest
from playwright.sync_api import Page, expect


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def enter_room(page: Page, base_url: str):
    """Navigate, fill name, pick topic, click start → room visible."""
    page.goto(base_url)
    page.wait_for_selector("#lobby", state="visible")
    page.fill("#name-input", "TestUser")
    # Click the first non-selected topic btn (second one, since free-chat is pre-selected)
    btns = page.locator(".topic-btn")
    if btns.count() > 1:
        btns.nth(1).click()
    page.click("#start-btn")
    page.wait_for_selector("#room", state="visible", timeout=10000)


# ---------------------------------------------------------------------------
# Lobby tests
# ---------------------------------------------------------------------------

def test_lobby_loads(page: Page, base_url: str):
    page.goto(base_url)
    expect(page).to_have_title(re.compile(r"AI English Coach"))


def test_name_input_exists(page: Page, base_url: str):
    page.goto(base_url)
    expect(page.locator("input#name-input")).to_be_visible()


def test_topic_buttons_exist(page: Page, base_url: str):
    page.goto(base_url)
    page.wait_for_selector(".topic-btn", timeout=5000)
    btns = page.locator(".topic-btn")
    assert btns.count() >= 3, f"Expected >= 3 topic buttons, got {btns.count()}"


def test_select_topic(page: Page, base_url: str):
    page.goto(base_url)
    page.wait_for_selector(".topic-btn", timeout=5000)
    btns = page.locator(".topic-btn")
    # Click second button (first is already selected)
    btns.nth(1).click()
    expect(btns.nth(1)).to_have_class(re.compile(r"selected"))


def test_start_button_exists(page: Page, base_url: str):
    page.goto(base_url)
    expect(page.locator("#start-btn")).to_be_visible()


# ---------------------------------------------------------------------------
# Room tests — require entering the room first
# ---------------------------------------------------------------------------

def test_start_room(page: Page, base_url: str):
    enter_room(page, base_url)
    expect(page.locator("#room")).to_be_visible()


def test_room_has_chat(page: Page, base_url: str):
    enter_room(page, base_url)
    expect(page.locator("#chat")).to_be_visible()


def test_room_has_mic_button(page: Page, base_url: str):
    enter_room(page, base_url)
    expect(page.locator(".mic-btn")).to_be_visible()


def test_room_has_end_button(page: Page, base_url: str):
    enter_room(page, base_url)
    expect(page.locator(".end-btn")).to_be_visible()


def test_room_has_mode_toggle(page: Page, base_url: str):
    enter_room(page, base_url)
    expect(page.locator(".mode-toggle")).to_be_visible()
    expect(page.locator("#mode-voice")).to_be_visible()
    expect(page.locator("#mode-text")).to_be_visible()


# ---------------------------------------------------------------------------
# Mode switching
# ---------------------------------------------------------------------------

def test_switch_to_text_mode(page: Page, base_url: str):
    enter_room(page, base_url)
    page.click("#mode-text")
    # text-mode visible, voice-mode hidden
    expect(page.locator("#text-mode")).to_be_visible()
    expect(page.locator("#voice-mode")).to_be_hidden()


def test_switch_to_voice_mode(page: Page, base_url: str):
    enter_room(page, base_url)
    # First switch to text, then back to voice
    page.click("#mode-text")
    expect(page.locator("#voice-mode")).to_be_hidden()
    page.click("#mode-voice")
    expect(page.locator("#voice-mode")).to_be_visible()
    expect(page.locator("#text-mode")).to_be_hidden()


def test_text_input_exists_in_text_mode(page: Page, base_url: str):
    enter_room(page, base_url)
    page.click("#mode-text")
    expect(page.locator("#text-input")).to_be_visible()


def test_send_text_message(page: Page, base_url: str):
    enter_room(page, base_url)
    page.click("#mode-text")
    page.fill("#text-input", "Hello, how are you?")
    page.press("#text-input", "Enter")
    # The student message bubble should appear in #chat
    expect(page.locator("#chat .msg.student")).to_be_visible(timeout=5000)


# ---------------------------------------------------------------------------
# Summary / End session
# ---------------------------------------------------------------------------

def test_end_session_shows_summary(page: Page, base_url: str):
    enter_room(page, base_url)
    # Wait a moment for the WS greeting to arrive so WS is fully ready
    page.wait_for_selector("#chat .msg.ai", timeout=10000)
    page.click(".end-btn")
    # Summary modal should appear (server sends session_summary after "end")
    expect(page.locator("#summary-modal.show")).to_be_visible(timeout=15000)


def test_summary_has_feedback(page: Page, base_url: str):
    enter_room(page, base_url)
    page.wait_for_selector("#chat .msg.ai", timeout=10000)
    page.click(".end-btn")
    page.wait_for_selector("#summary-modal.show", timeout=15000)
    feedback = page.locator("#sum-feedback")
    expect(feedback).not_to_have_text("", timeout=5000)


def test_close_summary_returns_to_lobby(page: Page, base_url: str):
    enter_room(page, base_url)
    page.wait_for_selector("#chat .msg.ai", timeout=10000)
    page.click(".end-btn")
    page.wait_for_selector("#summary-modal.show", timeout=15000)
    page.click(".close-btn")
    expect(page.locator("#lobby")).to_be_visible()


def test_back_button_leaves_room(page: Page, base_url: str):
    enter_room(page, base_url)
    page.click(".back")
    expect(page.locator("#lobby")).to_be_visible()
