# API

Prosta aplikacja FastAPI do obslugi zamowien oraz przykladowe testy (lokalne i live API Petstore).

## Wymagania
- Python 3.12+ (w projekcie jest uzywany 3.14)
- Virtualenv (zalecane)

## Uruchomienie serwisu
Poniższe komendy zakladaja uruchomienie z katalogu projektu (root).

```zsh
cd /continuesTesting
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn api.app:app --reload
```

Serwis startuje domyslnie pod adresem `http://127.0.0.1:8000`.

## Testy w tym katalogu
Testy w katalogu `api` uzywaja lokalnej bazy SQLite dla kazdego testu. Dodatkowo sa testy, ktore uderzaja w live API Petstore.

### Lokalnie (testy zamowien)
```zsh
cd /Users/apple/projekty/continuesTesting
source .venv/bin/activate
pytest api/tests_orders.py
```

### Live API Petstore
Testy wykorzystuja konfiguracje z `src/utils/config.py`.
Opcjonalnie ustaw zmienne srodowiskowe:

```zsh
export PETSTORE_BASE_URL="https://petstore.swagger.io/v2"
export PETSTORE_API_KEY="<opcjonalny_klucz>"
```

Uruchomienie testow Petstore:

```zsh
cd /Users/apple/projekty/continuesTesting
source .venv/bin/activate
pytest api/test_petstore_basic.py -m api
```

## Zadania: dodatkowe testy do napisania (4)
1. **Walidacja ceny**: sprawdz, czy `price <= 0` zwraca `422` i odpowiedni komunikat (analogicznie do `quantity`).
2. **Brakujace pole**: wyslij zadanie bez `product` i sprawdz `422` oraz szczegoly walidacji Pydantic.
3. **Bledny typ pola**: wyslij `quantity` jako string i sprawdz, czy API zwraca `422`.
4. **Nieprawidlowy identyfikator**: wykonaj `GET /orders/abc` i sprawdz `422` (FastAPI waliduje typ parametru).

## Rozwiazania zadan: krok po kroku

Poniższe kroki zakladaja, ze uruchamiasz testy z katalogu glownego projektu i masz aktywne `.venv`.

### 1) Walidacja ceny (`price <= 0`)
**Kroki:**
1. Otworz plik `api/tests_orders.py`.
2. Dodaj nowy test, ktory wysyla `price` rowne `0` i `-1`.
3. Sprawdz `status_code == 422` oraz tresc `detail`.

**Przykladowy test:**
```python
import pytest

@pytest.mark.api
@pytest.mark.parametrize("bad_price", [0, -1])
def test_create_order_rejects_non_positive_price(client, bad_price):
    payload = {"product": "Book", "quantity": 1, "price": bad_price}

    response = client.post("/orders", json=payload)

    assert response.status_code == 422
    assert response.json()["detail"] == "Price must be positive"
```

### 2) Brakujace pole `product`
**Kroki:**
1. W `api/tests_orders.py` dodaj test bez pola `product`.
2. Sprawdz, ze API zwraca `422`.
3. Zweryfikuj, ze walidacja Pydantic wskazuje na brakujace pole.

**Przykladowy test:**
```python
import pytest

@pytest.mark.api
def test_create_order_requires_product(client):
    payload = {"quantity": 2, "price": 10.0}

    response = client.post("/orders", json=payload)

    assert response.status_code == 422
    errors = response.json().get("detail", [])
    assert any(err.get("loc", [])[-1] == "product" for err in errors)
```

### 3) Bledny typ pola `quantity`
**Kroki:**
1. Dodaj test z `quantity` jako string.
2. Sprawdz `422`.
3. Zweryfikuj, ze walidacja dotyczy pola `quantity`.

**Przykladowy test:**
```python
import pytest

@pytest.mark.api
def test_create_order_rejects_string_quantity(client):
    payload = {"product": "Book", "quantity": "two", "price": 10.0}

    response = client.post("/orders", json=payload)

    assert response.status_code == 422
    errors = response.json().get("detail", [])
    assert any(err.get("loc", [])[-1] == "quantity" for err in errors)
```

### 4) Nieprawidlowy identyfikator `GET /orders/abc`
**Kroki:**
1. Dodaj test, ktory wywoluje `/orders/abc`.
2. Sprawdz, ze FastAPI zwraca `422`.
3. Zweryfikuj, ze walidacja dotyczy `order_id`.

**Przykladowy test:**
```python
import pytest

@pytest.mark.api
def test_get_order_rejects_non_int_id(client):
    response = client.get("/orders/abc")

    assert response.status_code == 422
    errors = response.json().get("detail", [])
    assert any(err.get("loc", [])[-1] == "order_id" for err in errors)
```
