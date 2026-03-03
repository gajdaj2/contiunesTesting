# Zadania do tematow continuous testing

## 1. Run tests
- Zadanie: uruchom testy tylko z markerem `api` i zapisz wynik w pliku.
- Podpowiedz: `pytest -m api --junitxml=reports/junit.xml`

## 2. Run with schedule
- Zadanie: przygotuj harmonogram uruchomienia testow co dzien w GitHub Actions.
- Podpowiedz: `on.schedule` w `.github/workflows/ci.yml`.

## 3. Cross browser testing
- Zadanie: uruchom testy UI w Chrome i Firefox.
- Podpowiedz: ustaw zmienna `BROWSER`.

## 4. Reporting / Archiving reports
- Zadanie: generuj raport HTML z testow i archiwizuj go w CI.
- Podpowiedz: `pytest --html=reports/report.html`.

## 5. Run in parallel
- Zadanie: uruchom testy z `-n auto` i porownaj czas.

## 6. Tests independence
- Zadanie: zmien fixture w `tests/conftest.py` tak, aby driver byl tworzony per test.

## 7. Sensitive data management
- Zadanie: uruchom testy z `PETSTORE_API_KEY` przekazana jako sekret w CI.

## 8. Shorten execution time
- Zadanie: dodaj `@pytest.mark.slow` do jednego testu i uruchom z `-m "not slow"`.

## 9. API testing
- Zadanie: dodaj test tworzenia i usuniecia zwierzaka w Petstore.

