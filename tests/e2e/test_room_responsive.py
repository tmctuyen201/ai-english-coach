"""Responsive viewport E2E tests for the AI English Coach conversation room."""
import pytest
from playwright.sync_api import Page


VIEWPORTS = [
    ("mobile", 390, 844),
    ("tablet", 768, 1024),
    ("desktop", 1920, 1080),
]


@pytest.fixture(params=VIEWPORTS, ids=[v[0] for v in VIEWPORTS])
def sized_page(request, browser):
    """Create a page with a specific viewport size."""
    name, w, h = request.param
    ctx = browser.new_context(viewport={"width": w, "height": h})
    pg = ctx.new_page()
    yield pg
    pg.close()
    ctx.close()


# Override the default `page` fixture so tests below use the sized one.
@pytest.fixture()
def page(sized_page):
    return sized_page


def test_mobile_viewport(page: Page, base_url: str):
    page.goto(base_url)
    page.wait_for_selector("#lobby", state="visible")
    assert page.title() != ""
    assert page.locator("input#name-input").is_visible()


def test_tablet_viewport(page: Page, base_url: str):
    page.goto(base_url)
    page.wait_for_selector("#lobby", state="visible")
    assert page.title() != ""
    assert page.locator("input#name-input").is_visible()


def test_desktop_viewport(page: Page, base_url: str):
    page.goto(base_url)
    page.wait_for_selector("#lobby", state="visible")
    assert page.title() != ""
    assert page.locator("input#name-input").is_visible()
