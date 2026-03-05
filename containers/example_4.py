import os
import sys
import time
from pathlib import Path

import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from testcontainers.core.container import DockerContainer

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))
from utils.driver_factory import create_driver



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


def main() -> None:
    browser = os.getenv("BROWSER", "chrome")
    headless = False

    static_dir = Path(__file__).resolve().parent / "nginx"
    print("Start: uruchamiam kontener Nginx")
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
            print("Otwieram strone w przegladarce (widoczna)")
            driver.get(base_url)
            WebDriverWait(driver, 5).until(
                ec.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='headline']"))
            )
            driver.implicitly_wait(5000)
            wait_for_nginx(base_url)
            headline = driver.find_element(By.CSS_SELECTOR, "[data-testid='headline']")
            print(f"Naglowek: {headline.text}")
            print("Czekam 10 sekund przed zamknieciem przegladarki")
            time.sleep(10)
        finally:
            driver.quit()


if __name__ == "__main__":
    main()
