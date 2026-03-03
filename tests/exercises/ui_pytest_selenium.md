# Proste cwiczenia: pytest + Selenium

Zakladamy uruchomiona aplikacje Flask z `app.py`.

## 1. Pierwszy test UI (smoke)
Cel: napisz test, ktory otwiera strone glowna i sprawdza tytul.
- Plik: `tests/ui/test_homepage.py`
- Wymagania:
  - uzyj fixture `driver` i `base_url`
  - asercja: tytul zawiera `CT Demo App`

## 2. Sprawdzenie elementu po id
Cel: sprawdz, czy element `#intro` zawiera oczekiwany tekst.
- Plik: `tests/ui/test_homepage.py`
- Wymagania:
  - pobierz element `#intro`
  - asercja: tekst == `Prosta aplikacja do testow UI.`

## 3. Nawigacja po linku
Cel: kliknij link `#info-link` i sprawdz, czy trafiles na `/info`.
- Plik: `tests/ui/test_navigation.py`
- Wymagania:
  - kliknij link
  - asercja: `driver.current_url` konczy sie na `/info`

## 4. Asercja naglowka na stronie info
Cel: sprawdz naglowek `#info-title` na stronie `/info`.
- Plik: `tests/ui/test_navigation.py`
- Wymagania:
  - przejdz bezposrednio na `/info`
  - asercja: tekst == `Info Page`

## 5. Parametryzacja
Cel: uzyj `@pytest.mark.parametrize` do sprawdzenia tytulow stron.
- Plik: `tests/ui/test_parametrize.py`
- Wymagania:
  - przypadki: `/` -> `CT Demo App`, `/info` -> `Info`
  - asercja: tytul strony zawiera oczekiwany fragment

## 6. Negatywny scenariusz
Cel: sprawdz, czy brakujacy element powoduje czytelny blad.
- Plik: `tests/ui/test_negative.py`
- Wymagania:
  - spróbuj znalezc `#does-not-exist`
  - owin w `pytest.raises` z `NoSuchElementException`

## 7. Marker i selekcja testow
Cel: oznacz jeden test markerem `slow` i uruchom bez niego.
- Plik: dowolny test UI
- Wymagania:
  - dodaj `@pytest.mark.slow`
  - uruchom: `pytest -m "not slow"`

## 8. Wlasny fixture
Cel: utworz fixture `info_page_url` zwracajace `{base_url}/info`.
- Plik: `tests/conftest.py`
- Wymagania:
  - wykorzystaj fixture w tescie z cwiczenia 4

