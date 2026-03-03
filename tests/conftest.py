import os
import sys
from pathlib import Path

# Dodaj katalog projektu do sys.path, zeby importy z src dzialaly lokalnie.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pytest
from src.utils.driver_factory import create_driver
from src.utils.config import BASE_URL


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="function")
def driver():
    browser = os.getenv("BROWSER", "chrome")
    headless = os.getenv("HEADLESS", "true").lower() == "true"

    # Jeden test = jeden driver, zeby testy byly niezalezne.
    web_driver = create_driver(browser, headless)
    yield web_driver
    web_driver.quit()
