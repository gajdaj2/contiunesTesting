import pytest
import requests
from src.utils.config import PETSTORE_BASE_URL, PETSTORE_API_KEY


@pytest.mark.api
def test_get_inventory():
    url = f"{PETSTORE_BASE_URL}/store/inventory"
    headers = {"api_key": PETSTORE_API_KEY} if PETSTORE_API_KEY else {}

    # Wywolanie live API Petstore
    response = requests.get(url, headers=headers, timeout=10)

    assert response.status_code == 200
    assert isinstance(response.json(), dict)


@pytest.mark.api
def test_find_pet_by_status_available():
    url = f"{PETSTORE_BASE_URL}/pet/findByStatus"
    params = {"status": "available"}

    response = requests.get(url, params=params, timeout=10)

    assert response.status_code == 200
    assert isinstance(response.json(), list)

