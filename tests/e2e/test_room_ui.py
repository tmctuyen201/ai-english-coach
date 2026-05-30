"""
Playwright E2E Tests — AI English Coach (Redesigned UI)
Tests all pages: landing, auth, room, topics, vocabulary, progress
"""
import pytest
from playwright.sync_api import sync_playwright, expect

BASE = "http://localhost:8089"


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        yield b
        b.close()


@pytest.fixture
def page(browser):
    ctx = browser.new_context()
    pg = ctx.new_page()
    yield pg
    ctx.close()


# ═══════════════════════════════════════════
# LANDING PAGE
# ═══════════════════════════════════════════

class TestLanding:
    def test_loads(self, page):
        page.goto(BASE)
        page.wait_for_load_state("domcontentloaded")
        expect(page.locator("h1")).to_be_visible()

    def test_has_nav(self, page):
        page.goto(BASE)
        expect(page.locator(".nav")).to_be_visible()

    def test_has_hero(self, page):
        page.goto(BASE)
        expect(page.locator(".hero")).to_be_visible()

    def test_has_features(self, page):
        page.goto(BASE)
        page.locator("#features").scroll_into_view_if_needed()
        assert page.locator(".feature-card").count() >= 4

    def test_has_pricing(self, page):
        page.goto(BASE)
        page.locator("#pricing").scroll_into_view_if_needed()
        assert page.locator(".price-card").count() >= 2

    def test_get_started_links_to_auth(self, page):
        page.goto(BASE)
        link = page.locator('a[href="auth.html"]').first
        expect(link).to_be_visible()


# ═══════════════════════════════════════════
# AUTH PAGE
# ═══════════════════════════════════════════

class TestAuth:
    def test_loads(self, page):
        page.goto(f"{BASE}/auth")
        page.wait_for_load_state("domcontentloaded")
        expect(page.locator(".auth-container")).to_be_visible()

    def test_has_tabs(self, page):
        page.goto(f"{BASE}/auth")
        assert page.locator(".tab").count() == 2

    def test_has_phone_input(self, page):
        page.goto(f"{BASE}/auth")
        expect(page.locator("#phone-input")).to_be_visible()

    def test_has_send_otp_button(self, page):
        page.goto(f"{BASE}/auth")
        expect(page.locator("#send-otp-btn")).to_be_visible()

    def test_send_otp(self, page):
        page.goto(f"{BASE}/auth")
        page.fill("#phone-input", "0902123456")
        page.click("#send-otp-btn")
        page.wait_for_timeout(500)
        expect(page.locator("#step-otp")).to_be_visible()

    def test_otp_inputs_exist(self, page):
        page.goto(f"{BASE}/auth")
        page.fill("#phone-input", "0902123456")
        page.click("#send-otp-btn")
        page.wait_for_timeout(500)
        assert page.locator(".otp-inputs input").count() == 6


# ═══════════════════════════════════════════
# CONVERSATION ROOM
# ═══════════════════════════════════════════

def _enter_room(page):
    page.goto(f"{BASE}/room")
    page.wait_for_load_state("domcontentloaded")
    page.fill("#name-input", "TestUser")
    page.locator(".topic-card").first.click()
    page.click("#start-btn")
    page.wait_for_timeout(1000)


class TestRoom:
    def test_lobby_loads(self, page):
        page.goto(f"{BASE}/room")
        page.wait_for_load_state("domcontentloaded")
        expect(page.locator("#lobby")).to_be_visible()

    def test_name_input(self, page):
        page.goto(f"{BASE}/room")
        expect(page.locator("#name-input")).to_be_visible()

    def test_topic_cards(self, page):
        page.goto(f"{BASE}/room")
        assert page.locator(".topic-card").count() >= 3

    def test_start_opens_room(self, page):
        _enter_room(page)
        expect(page.locator("#room")).to_be_visible()

    def test_room_has_chat(self, page):
        _enter_room(page)
        expect(page.locator("#chat")).to_be_visible()

    def test_room_has_mic(self, page):
        _enter_room(page)
        expect(page.locator(".mic-btn, #mic-btn, .mic")).to_be_visible()

    def test_room_has_text_input(self, page):
        _enter_room(page)
        # Text input should be accessible
        expect(page.locator("#text-input, .text-input")).to_be_visible()


class TestRoomModes:
    def test_voice_mode_default(self, page):
        _enter_room(page)
        voice = page.locator("#voice-area, .voice-area")
        assert voice.is_visible()

    def test_text_fallback_exists(self, page):
        _enter_room(page)
        text = page.locator("#text-fallback, #text-input, .text-input")
        assert text.count() >= 1


class TestRoomConversation:
    def test_send_text(self, page):
        _enter_room(page)
        page.wait_for_timeout(1500)
        inp = page.locator("#text-input, .text-input")
        inp.fill("Hello!")
        inp.press("Enter")
        page.wait_for_timeout(300)
        student = page.locator(".msg.student, .msg-you, .msg-student")
        assert student.count() >= 1

    def test_ai_responds(self, page):
        _enter_room(page)
        page.wait_for_timeout(1500)
        inp = page.locator("#text-input, .text-input")
        inp.fill("Hello!")
        inp.press("Enter")
        page.wait_for_timeout(6000)
        ai = page.locator(".msg.ai, .msg-ai, .msg-teacher")
        assert ai.count() >= 2


class TestRoomEndSession:
    def test_end_shows_summary(self, page):
        _enter_room(page)
        page.wait_for_timeout(1500)
        page.click(".topbar-end, .end-btn, #end-btn")
        page.wait_for_timeout(4000)
        modal = page.locator("#summary-modal, .overlay.show, .modal-overlay.show")
        assert modal.is_visible()


# ═══════════════════════════════════════════
# TOPICS PAGE
# ═══════════════════════════════════════════

class TestTopics:
    def test_loads(self, page):
        page.goto(f"{BASE}/topics")
        page.wait_for_load_state("domcontentloaded")
        # Should have topic cards
        cards = page.locator(".topic-card, .card")
        assert cards.count() >= 5

    def test_has_search(self, page):
        page.goto(f"{BASE}/topics")
        search = page.locator("input[type='text'], input[placeholder*='earch']")
        assert search.count() >= 1

    def test_has_filter_pills(self, page):
        page.goto(f"{BASE}/topics")
        pills = page.locator(".pill, .filter-btn, .tag")
        assert pills.count() >= 3


# ═══════════════════════════════════════════
# VOCABULARY PAGE
# ═══════════════════════════════════════════

class TestVocabulary:
    def test_loads(self, page):
        page.goto(f"{BASE}/vocabulary")
        page.wait_for_load_state("domcontentloaded")
        expect(page.locator("body")).to_be_visible()

    def test_has_flashcard(self, page):
        page.goto(f"{BASE}/vocabulary")
        card = page.locator(".flashcard-area, .card-container, .flashcard, .card")
        assert card.count() >= 1


# ═══════════════════════════════════════════
# PROGRESS PAGE
# ═══════════════════════════════════════════

class TestProgress:
    def test_loads(self, page):
        page.goto(f"{BASE}/progress")
        page.wait_for_load_state("domcontentloaded")
        expect(page.locator("body")).to_be_visible()

    def test_has_stats(self, page):
        page.goto(f"{BASE}/progress")
        stats = page.locator(".stat-card, .stat, .metric")
        assert stats.count() >= 3


# ═══════════════════════════════════════════
# RESPONSIVE
# ═══════════════════════════════════════════

class TestResponsive:
    def test_mobile_landing(self, browser):
        ctx = browser.new_context(viewport={"width": 390, "height": 844})
        pg = ctx.new_page()
        pg.goto(BASE)
        pg.wait_for_load_state("domcontentloaded")
        expect(pg.locator("h1")).to_be_visible()
        ctx.close()

    def test_mobile_room(self, browser):
        ctx = browser.new_context(viewport={"width": 390, "height": 844})
        pg = ctx.new_page()
        pg.goto(f"{BASE}/room")
        pg.wait_for_load_state("domcontentloaded")
        expect(pg.locator("#lobby")).to_be_visible()
        ctx.close()

    def test_desktop_landing(self, browser):
        ctx = browser.new_context(viewport={"width": 1920, "height": 1080})
        pg = ctx.new_page()
        pg.goto(BASE)
        pg.wait_for_load_state("domcontentloaded")
        expect(pg.locator("h1")).to_be_visible()
        ctx.close()
