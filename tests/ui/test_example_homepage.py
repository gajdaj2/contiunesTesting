import os
import pytest
from selenium.webdriver.common.by import By

from src.utils.config import BASE_URL
from src.utils.driver_factory import create_driver


@pytest.mark.ui
def test_homepage_title_and_intro():
    browser = os.getenv("BROWSER", "chrome")
    headless = os.getenv("HEADLESS", "true").lower() == "true"

    driver = create_driver(browser, headless)
    try:
        driver.get(BASE_URL)  # kluczowy krok: otwarcie aplikacji

        assert "CT Demo App" in driver.title

        intro = driver.find_element(By.CSS_SELECTOR, "#intro")
        assert intro.text.strip() == "Prosta aplikacja do testow UI."
    finally:
        driver.quit()
