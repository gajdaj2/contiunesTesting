import os
import pytest
from selenium.webdriver.common.by import By

from src.utils.config import BASE_URL
from src.utils.driver_factory import create_driver


@pytest.mark.ui
def test_homepage_title():
    browser = os.getenv("BROWSER", "chrome")
    headless = os.getenv("HEADLESS", "true").lower() == "true"

    driver = create_driver(browser, headless)
    try:
        driver.get(BASE_URL)  # kluczowy krok: punkt startowy testu
        title = driver.title

        # Stabilna asercja dla aplikacji demo
        assert "CT Demo App" in title
    finally:
        driver.quit()


@pytest.mark.ui
def test_more_information_link():
    browser = os.getenv("BROWSER", "chrome")
    headless = os.getenv("HEADLESS", "true").lower() == "true"

    driver = create_driver(browser, headless)
    try:
        driver.get(BASE_URL)
        link = driver.find_element(By.CSS_SELECTOR, "#info-link")

        # Weryfikujemy link do strony info
        assert link.get_attribute("href").endswith("/info")
        assert link.text.strip() == "More information"
    finally:
        driver.quit()


@pytest.mark.ui
def test_info_page():
    browser = os.getenv("BROWSER", "chrome")
    headless = os.getenv("HEADLESS", "true").lower() == "true"

    driver = create_driver(browser, headless)
    try:
        driver.get(f"{BASE_URL}/info")
        heading = driver.find_element(By.CSS_SELECTOR, "#info-title")

        # Kluczowa asercja: obecny naglowek strony info
        assert heading.text.strip() == "Info Page"
    finally:
        driver.quit()
