import time

import pytest
from playwright.sync_api import sync_playwright
from e2e.pom.pages.inputs_page import InputsPage
from e2e.pom.pages.main_page import MainPage

import logging
import sys

@pytest.fixture
def browser_page():
    """Fixture do inicjalizacji przeglądarki"""
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    yield page
    browser.close()
    playwright.stop()




def test_inputs_page(browser_page,rp_logger):
    """Test: nawigacja do inputs i wpisanie tekstu"""
    # Inicjalizacja POM

    main_page = MainPage(browser_page)
    main_page.navigate()
    inputs_page = main_page.click_inputs_link()

    # Wpisanie liczby (input[type=number] nie akceptuje tekstu)
    test_text = "12345"
    inputs_page.type_text(test_text)

    time.sleep(5)

    # Asercja - sprawdzenie czy tekst się pojawił
    assert inputs_page.get_input_value() == test_text
