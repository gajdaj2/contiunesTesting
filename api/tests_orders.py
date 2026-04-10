# test_orders.py – testy integracyjne

import pytest

# ── scenariusz 1: tworzenie zamówienia ──────────────────
def test_create_order_returns_201(client):
    response = client.post("/orders", json={
        "product": "Laptop",
        "quantity": 2,
        "price": 3499.99
    })

    # asercja 1 – status HTTP
    assert response.status_code == 201

    data = response.json()

    # asercja 2 – struktura odpowiedzi
    assert data["product"] == "Laptop"
    assert data["quantity"] == 2
    assert "id" in data        # baza wygenerowała ID


# ── scenariusz 2: odczyt zapisanego zamówienia ──────────
def test_get_order_after_create(client):
    # najpierw tworzymy
    post_resp = client.post("/orders", json={
        "product": "Monitor",
        "quantity": 1,
        "price": 899.00
    })
    order_id = post_resp.json()["id"]

    # potem odczytujemy z bazy przez GET
    get_resp = client.get(f"/orders/{order_id}")

    assert get_resp.status_code == 200
    assert get_resp.json()["product"] == "Monitor"


# ── scenariusz 3: walidacja błędnych danych ─────────────
def test_create_order_invalid_quantity(client):
    response = client.post("/orders", json={
        "product": "Klawiatura",
        "quantity": -1,   # nieprawidłowa wartość
        "price": 199.00
    })

    assert response.status_code == 422
    assert "Quantity must be positive" in response.json()["detail"]


# ── scenariusz 4: zamówienie nie istnieje ───────────────
def test_get_nonexistent_order(client):
    response = client.get("/orders/9999")

    assert response.status_code == 404

import pytest

@pytest.mark.api
@pytest.mark.parametrize("bad_price", [-1, -1])
def test_create_order_rejects_non_positive_price(client, bad_price):
    payload = {"product": "Book", "quantity": 1, "price": bad_price}

    response = client.post("/orders", json=payload)

    assert response.status_code == 422
    assert response.json()["detail"] == "Price must be positive"