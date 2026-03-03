import os
import pytest
from selenium.common import NoSuchElementException
from src.utils.config import BASE_URL
from src.utils.driver_factory import create_driver


@pytest.mark.ui
def test_missing_element_is_handled():
    browser = os.getenv("BROWSER", "chrome")
    headless = os.getenv("HEADLESS", "true").lower() == "true"

    driver = create_driver(browser, headless)
    try:
        driver.get(BASE_URL)

        # Negatywny scenariusz: oczekujemy bledu, gdy element nie istnieje.
        with pytest.raises(NoSuchElementException):
            driver.find_element("css selector", "#does-not-exist")
    finally:
        driver.quit()
