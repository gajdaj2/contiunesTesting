import json
import time

import pytest
import requests
from testcontainers.core.container import DockerContainer


def wait_for_wiremock(base_url: str, timeout_seconds: float = 10.0) -> None:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        try:
            response = requests.get(f"{base_url}/__admin/mappings", timeout=1)
            if response.status_code == 200:
                return
        except requests.RequestException:
            pass
        time.sleep(0.5)
    raise RuntimeError("WireMock nie jest gotowy w zadanym czasie")


@pytest.mark.containers
@pytest.mark.slow
def test_wiremock_container_roundtrip():
    print("Start testu: uruchamiam kontener WireMock")
    with DockerContainer("wiremock/wiremock:3.5.2").with_exposed_ports(8080) as container:
        base_url = (
            f"http://{container.get_container_host_ip()}:{container.get_exposed_port(8080)}"
        )
        print(f"WireMock pod: {base_url}")
        print("Czekam az WireMock bedzie gotowy")
        wait_for_wiremock(base_url)

        mapping = {
            "request": {"method": "GET", "url": "/hello"},
            "response": {
                "status": 200,
                "headers": {"Content-Type": "application/json"},
                "jsonBody": {"message": "Hello from WireMock"},
            },
        }
        print("Dodaje stub /hello")
        response = requests.post(
            f"{base_url}/__admin/mappings",
            data=json.dumps(mapping),
            headers={"Content-Type": "application/json"},
            timeout=5,
        )
        print(response.text)

        print("Wysylam zapytanie do /hello")
        hello = requests.get(f"{base_url}/hello", timeout=5)

    assert hello.status_code == 200
    assert hello.json()["message"] == "Hello from WireMock"
