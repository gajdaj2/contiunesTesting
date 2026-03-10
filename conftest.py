import pytest
from playwright.sync_api import sync_playwright, expect


@pytest.fixture
def page():
    """Fixture - przeglądarką dostępną w każdym teście"""
    with sync_playwright() as p:
        browser = p.chromium.launch()  # headless=False żeby widzieć
        page = browser.new_page()
        yield page
        browser.close()

@pytest.fixture
def browser_context():
    """Fixture z pełnym contextem"""
    with sync_playwright() as p:
        browser = p.firefox.launch()
        context = browser.new_context()
        yield context
        context.close()
        browser.close()
