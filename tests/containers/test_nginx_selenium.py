import os
import time
from pathlib import Path

import pytest
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from testcontainers.core.container import DockerContainer

from src.utils.driver_factory import create_driver


def wait_for_nginx(base_url: str, timeout_seconds: float = 10.0) -> None:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        try:
            response = requests.get(base_url, timeout=1)
            if response.status_code == 200:
                return
        except requests.RequestException:
            pass
        time.sleep(0.5)
    raise RuntimeError("Nginx nie jest gotowy w zadanym czasie")


@pytest.mark.containers
@pytest.mark.ui
@pytest.mark.slow
def test_nginx_page_in_selenium():
    browser = os.getenv("BROWSER", "chrome")
    headless = os.getenv("HEADLESS", "true").lower() == "true"

    static_dir = Path(__file__).resolve().parents[2] / "containers" / "nginx"
    print("Start testu: uruchamiam kontener Nginx")
    with (
        DockerContainer("nginx:1.27-alpine")
        .with_exposed_ports(80)
        .with_volume_mapping(str(static_dir), "/usr/share/nginx/html", "ro")
    ) as container:  # kluczowy krok: start kontenera
        base_url = (
            f"http://{container.get_container_host_ip()}:{container.get_exposed_port(80)}"
        )
        print(f"Nginx pod: {base_url}")
        print("Czekam az Nginx bedzie gotowy")
        wait_for_nginx(base_url)

        driver = create_driver(browser, headless)
        try:
            print("Otwieram strone w przegladarce")
            driver.get(base_url)
            WebDriverWait(driver, 5).until(
                ec.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='headline']"))
            )
            headline = driver.find_element(By.CSS_SELECTOR, "[data-testid='headline']")
            assert headline.text == "Nginx Demo App"

            driver.find_element(By.CSS_SELECTOR, "[data-testid='more']").click()
            WebDriverWait(driver, 5).until(
                ec.title_is("More")
            )
            assert driver.title == "More"
        finally:
            driver.quit()

