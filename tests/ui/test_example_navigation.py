import os
import pytest
from selenium.webdriver.common.by import By

from src.utils.config import BASE_URL
from src.utils.driver_factory import create_driver


@pytest.mark.ui
def test_click_info_link():
    browser = os.getenv("BROWSER", "chrome")
    headless = os.getenv("HEADLESS", "true").lower() == "true"

    driver = create_driver(browser, headless)
    try:
        driver.get(BASE_URL)
        driver.find_element(By.CSS_SELECTOR, "#info-link").click()

        # Sprawdzamy, czy nawigacja prowadzi do strony info.
        assert driver.current_url.endswith("/info")
    finally:
        driver.quit()


@pytest.mark.ui
def test_info_page_header():
    browser = os.getenv("BROWSER", "chrome")
    headless = os.getenv("HEADLESS", "true").lower() == "true"

    driver = create_driver(browser, headless)
    try:
        driver.get(f"{BASE_URL}/info")
        heading = driver.find_element(By.CSS_SELECTOR, "#info-title")

        assert heading.text.strip() == "Info Page"
    finally:
        driver.quit()
