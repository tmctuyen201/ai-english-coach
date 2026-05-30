"""Shared fixtures for Playwright E2E tests."""
import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def base_url():
    return "http://localhost:8089"


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        br = p.chromium.launch(headless=True)
        yield br
        br.close()


@pytest.fixture()
def page(browser):
    ctx = browser.new_context()
    pg = ctx.new_page()
    yield pg
    pg.close()
    ctx.close()
