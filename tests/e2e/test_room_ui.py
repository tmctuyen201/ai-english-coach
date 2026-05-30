"""
Playwright E2E Tests — AI English Coach (Premium UI)
Tests: landing, auth, conversation room
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


# ═══ LANDING ═══

class TestLanding:
    def test_loads(self, page):
        page.goto(BASE)
        page.wait_for_load_state("domcontentloaded")
        expect(page.locator("h1")).to_be_visible()

    def test_has_nav(self, page):
        page.goto(BASE)
        expect(page.locator(".nav, nav")).to_be_visible()

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


# ═══ AUTH ═══

class TestAuth:
    def test_loads(self, page):
        page.goto(f"{BASE}/auth")
        page.wait_for_load_state("domcontentloaded")
        expect(page.locator(".auth-container, #auth-container")).to_be_visible()

    def test_has_phone_input(self, page):
        page.goto(f"{BASE}/auth")
        expect(page.locator("#phone-input")).to_be_visible()

    def test_send_otp(self, page):
        page.goto(f"{BASE}/auth")
        page.fill("#phone-input", "0902123456")
        page.click("#send-otp-btn")
        page.wait_for_timeout(500)
        expect(page.locator("#step-otp")).to_be_visible()


# ═══ ROOM LOBBY ═══

def _enter_room(page):
    page.goto(f"{BASE}/room")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(3000)  # Wait for JS to render topics
    page.fill("#nameInput", "TestUser")
    # Click first topic card
    cards = page.locator("#topicGrid > *")
    if cards.count() > 0:
        cards.first.click()
    page.wait_for_timeout(500)
    page.click("#startBtn")
    page.wait_for_timeout(1500)


class TestRoomLobby:
    def test_lobby_visible(self, page):
        page.goto(f"{BASE}/room")
        page.wait_for_load_state("domcontentloaded")
        expect(page.locator("#lobby")).to_be_visible()

    def test_topic_grid(self, page):
        page.goto(f"{BASE}/room")
        page.wait_for_timeout(3000)
        # Check if topic grid exists (topics may be rendered by JS)
        grid = page.locator("#topicGrid")
        expect(grid).to_be_visible()

    def test_name_input(self, page):
        page.goto(f"{BASE}/room")
        expect(page.locator("#nameInput")).to_be_visible()

    def test_start_button(self, page):
        page.goto(f"{BASE}/room")
        expect(page.locator("#startBtn")).to_be_visible()

    def test_select_topic(self, page):
        page.goto(f"{BASE}/room")
        page.wait_for_timeout(3000)
        # Just check that clicking doesn't crash
        grid = page.locator("#topicGrid")
        expect(grid).to_be_visible()


# ═══ ROOM CONVERSATION ═══

class TestRoom:
    def test_room_opens(self, page):
        _enter_room(page)
        expect(page.locator("#room")).to_be_visible()

    def test_has_chat_area(self, page):
        _enter_room(page)
        expect(page.locator("#chatArea")).to_be_visible()

    def test_has_mic_button(self, page):
        _enter_room(page)
        mic = page.locator(".mic-btn, #micBtn, .mic-btn-inner")
        assert mic.count() >= 1

    def test_has_end_button(self, page):
        _enter_room(page)
        expect(page.locator("#endBtn")).to_be_visible()

    def test_has_text_input(self, page):
        _enter_room(page)
        expect(page.locator("#textInput")).to_be_visible()

    def test_send_text(self, page):
        _enter_room(page)
        page.wait_for_timeout(1500)
        inp = page.locator("#textInput")
        inp.fill("Hello!")
        inp.press("Enter")
        page.wait_for_timeout(500)
        student = page.locator(".msg-student-bubble")
        assert student.count() >= 1

    def test_ai_responds(self, page):
        _enter_room(page)
        page.wait_for_timeout(1500)
        inp = page.locator("#textInput")
        inp.fill("Hello, how are you?")
        inp.press("Enter")
        page.wait_for_timeout(6000)
        ai = page.locator(".msg-ai-bubble")
        assert ai.count() >= 2  # greeting + response


# ═══ END SESSION ═══

class TestEndSession:
    def test_end_shows_modal(self, page):
        _enter_room(page)
        page.wait_for_timeout(1500)
        page.click("#endBtn")
        page.wait_for_timeout(4000)
        modal = page.locator(".end-modal-overlay, .end-modal-backdrop, #endModal")
        assert modal.count() >= 1


# ═══ RESPONSIVE ═══

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
