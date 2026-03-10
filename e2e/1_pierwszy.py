from playwright.sync_api import expect
import pytest


def test_example(page):
    # Otworz stronę
    page.goto("https://example.com")

    # Sprawdź tytuł
    expect(page).to_have_title("Example Domain")