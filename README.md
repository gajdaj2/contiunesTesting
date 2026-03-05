# Continuous Testing - Selenium + Pytest

Repozytorium zawiera przyklady i zadania do zajec z continuous testing.

## Tematy
1. Run tests
2. Run with schedule
3. Cross browser testing
4. Reporting / Archiving reports
5. Run in parallel
6. Tests independecies
7. Sensitive data management
8. Shorten execution time
9. API testing (Petstore)

## Szybki start
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Uruchamianie testow
```bash
pytest -m api
pytest -m ui
pytest -m "not slow"
```

## Opcja -m w pytest
Opcja `-m` filtruje testy po markerach.
```bash
pytest -m api
pytest -m ui
pytest -m "not slow"
pytest -m "ui and not slow"
```

## Uruchamianie testow rownolegle
Testy uruchamiane sa rownolegle przez `pytest-xdist`.
```bash
pytest -n auto
pytest -m ui -n auto
pytest -m api -n auto
```
Aby pominac testy oznaczone markerem `serial`:
```bash
pytest -n auto -m "not serial"
```

## Testcontainers (Postgres)
Test przykladowy znajduje sie w `tests/containers/test_postgres_container.py` i wymaga dzialajacego Dockera.
```bash
pytest -m containers
```

## Testcontainers (WireMock)
Przyklad testu z WireMock jest w `tests/containers/test_wiremock_container.py`.
```bash
pytest -m containers -k wiremock
```
Przyklad uruchomienia jako skrypt:
```bash
python containers/example_2.py
```

## Testcontainers (Nginx + Selenium)
Przyklad uruchamia kontener Nginx z prosta strona HTML i testuje ja w Selenium: `tests/containers/test_nginx_selenium.py`.
```bash
pytest -m containers -k nginx
```
Aby zobaczyc okno przegladarki ustaw `HEADLESS=false`:
```bash
HEADLESS=false pytest -m containers -k nginx
```
Przyklad uruchomienia jako skrypt:
```bash
HEADLESS=false python containers/example_3.py
```

## Example 5 (Nginx + formularz + Selenium)
Przyklad formularza serwowanego przez Nginx i testu Selenium: `tests/containers/test_example_5_nginx_form.py`.
```bash
pytest -m containers -k example_5
```
Aby zobaczyc okno przegladarki ustaw `HEADLESS=false`:
```bash
HEADLESS=false pytest -m containers -k example_5
```
Przyklad uruchomienia jako skrypt:
```bash
HEADLESS=false python containers/example_5.py
```

## Struktura
```
src/
  pages/
  utils/
tests/
  api/
  ui/
  exercises/
.github/workflows/
```

## Uwaga
Testy UI wykorzystuja Selenium. W razie braku drivera dodaj go do PATH.

## Aplikacja demo (Flask)
```bash
python app.py
```
Aplikacja startuje pod `http://127.0.0.1:5000`.

## Testy UI na aplikacji demo
```bash
pytest -m ui
```
