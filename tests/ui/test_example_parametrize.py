import os
import pytest
from src.utils.config import BASE_URL
from src.utils.driver_factory import create_driver


@pytest.mark.ui
@pytest.mark.parametrize(
    "path, expected_title",
    [
        ("/", "CT Demo App"),
        ("/info", "Info"),
    ],
)
def test_titles_for_pages(path, expected_title):
    browser = os.getenv("BROWSER", "chrome")
    headless = os.getenv("HEADLESS", "true").lower() == "true"

    driver = create_driver(browser, headless)
    try:
        driver.get(f"{BASE_URL}{path}")

        # Parametryzacja ogranicza duplikacje kodu.
        assert expected_title in driver.title
    finally:
        driver.quit()
