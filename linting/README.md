# Krótkie ćwiczenia: Pylint i Black

## Cel

Po wykonaniu ćwiczeń uczestnik:

- uruchomi `pylint`
- zinterpretuje podstawowe komunikaty
- poprawi błędy jakości kodu
- uruchomi `black`
- zobaczy różnicę między lintowaniem a formatowaniem

---

## Wymagania

- Python 3.x
- `pip`

---

## Ćwiczenie 1 — instalacja narzędzi

W terminalu uruchom:

```bash
pip install pylint black
```

```bash
pylint --version
black --version
```

# Pylint i Black — Kompletny kurs i ćwiczenia praktyczne

Kurs poświęcony zautomatyzowanej analizie jakości kodu Python i formatowaniu. Zawiera teorię, 8 ćwiczeń praktycznych, rozwiązania i integrację CI/CD.

**Poziom**: początkujący–średniozaawansowany  
**Czas trwania**: ~2–3 godziny  
**Wymagania**: Python 3.8+, pip

---

## Spis treści

1. [Wstęp](#wstęp)
2. [Wymagania i instalacja](#wymagania-i-instalacja)
3. [Ćwiczenia praktyczne](#ćwiczenia-praktyczne)
4. [Rozwiązania](#rozwiązania)
5. [GitHub Actions workflow](#github-actions-workflow)

---

## Wstęp
Dwa narzędzia pomagają w automatyzacji pracy nad kodem:

- **Pylint** — wykrywa błędy, ostrzeżenia i problemy jakościowe (code smell, nieużywane zmienne, złe nazwy)
- **Black** — automatycznie formatuje kod (wcięcia, spacje, długość linii)

W tym kursie nauczysz się:
- ✅ Instalować i konfigurować oba narzędzia
- ✅ Rozpoznawać problemy jakościowe i stylowe
- ✅ Automatycznie formatować kod
- ✅ Integrować kontrolę jakości z CI/CD (GitHub Actions)

---

### Instalacja narzędzi

#### Opcja 1: Instalacja globalna

```bash
pip install pylint black
```

#### Opcja 2: Instalacja w wirtualnym środowisku (zalecane)

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install pylint black
```

#### Opcja 3: Instalacja z `requirements.txt`

Utwórz plik `requirements.txt`:

```
pylint==3.0.0
black==24.1.1
```

Następnie:

```bash
pip install -r requirements.txt
```

### Weryfikacja instalacji

```bash
pylint --version
black --version
```

Powinieneś zobaczyć:

```
pylint 3.0.0
black, 24.1.1 (compiled: yes)
```

---

## Ćwiczenia praktyczne

### Ćwiczenie 1 — Sprawdzenie wersji narzędzi

#### Zadanie

Uruchom obie komendy i potwierdź, że narzędzia są dostępne.

#### Komendy

```bash
pylint --version
black --version
```

#### Oczekiwany wynik

```
pylint X.X.X (...)
black, X.X.X (...)
```

---

### Ćwiczenie 2 — Analiza kodu z błędami

#### Zadanie

Utwórz plik `app.py`:

```python
import math

def policz(a,b):
    wynik=a+b
    unused = 123
    print( "Suma =", wynik )
    return wynik

def bardzo_dluga_funkcja_z_niezbyt_dobrym_stylem():
    x=1
    y=2
    z=3
    return x+y+z

policz(2,3)
```

Przeczytaj kod i spróbuj zgadnąć:
- **Co może nie podobać się `pylint`?**
  - Nieużywany import `math`
  - Zmienna `unused` zadeklarowana, ale nie używana
  - Brak spacji wokół `=`
  - Brak spacji w argumencie `print()`
  - Bardzo długa nazwa funkcji

- **Co poprawi `black`?**
  - Spacje wokół `=`
  - Spacje w argumencie `print()`
  - Konsystentne formatowanie operatorów

---

### Ćwiczenie 3 — Uruchomienie Pylint

#### Zadanie

Uruchom analizę:

```bash
pylint app.py
```

#### Czego szukać w wynikach?

- **Nieużywany import**: `unused-import`
- **Nieużywana zmienna**: `unused-variable`
- **Problemy ze stylem nazw**: `invalid-name` (funkcja ze spacjami)
- **Problemy z formatowaniem**: `bad-whitespace`

#### Pytania

1. **Które komunikaty dotyczą jakości?**  
   Np. `unused-import`, `unused-variable` — te mogą wpłynąć na wykonanie kodu.

2. **Które dotyczą stylu?**  
   Np. `bad-whitespace`, `line-too-long` — czystość i konwencje.

3. **Czy kod mimo wszystko może się uruchomić?**  
   **Tak**, ale ma problemy, które mogą prowadzić do bugów.

---

### Ćwiczenie 4 — Ręczne poprawienie kodu

#### Zadanie

Popraw `app.py`, aby miał mniej ostrzeżeń:

**Poprawiona wersja:**

```python
def policz(a, b):
    wynik = a + b
    print("Suma =", wynik)
    return wynik


def suma_trzech_liczb():
    x = 1
    y = 2
    z = 3
    return x + y + z


policz(2, 3)
```

**Zmiany:**
- ✅ Usunięty import `math` (nie był używany)
- ✅ Usunięta zmienna `unused`
- ✅ Dodane spacje: `a, b` i `a + b`
- ✅ Zmieniona nazwa funkcji (bez spacji)
- ✅ Poprawione formatowanie `print()`

#### Weryfikacja

```bash
pylint app.py
```

Powinno być mniej ostrzeżeń!

---

### Ćwiczenie 5 — Użycie Black

#### Zadanie

Utwórz plik `format_test.py`:

```python
def powitanie( imie ):
    print(   "Cześć, " + imie )
```

#### Formatowanie

```bash
black format_test.py
```

**Wynik:**

```python
def powitanie(imie):
    print("Cześć, " + imie)
```

#### Pytanie

**Czy `black` poprawił logikę programu, czy tylko wygląd kodu?**

Odpowiedź: **Tylko wygląd**. Logika jest identyczna — zmieniły się tylko spacje i formatowanie.

---

### Ćwiczenie 6 — Różnica między Pylint i Black

#### Zadanie

Utwórz plik `test_tools.py`:

```python
import os

def liczba():
    x=5
    return 10
```

Uruchom kolejno:

```bash
black test_tools.py
pylint test_tools.py
```

#### Obserwacje

- **Black zmienił**: spacje wokół `=` (`x = 5`)
- **Pylint nadal mówi**: 
  - `unused-import` — `os` się nie używa
  - `unused-variable` — `x` się nie używa

#### Wniosek

- **Black** → dba o format (spacje, wcięcia, długość linii)
- **Pylint** → dba o jakość (logika, nieużywane zmienne, nazwy)

---

### Ćwiczenie 7 — Praca na katalogu

#### Zadanie

Utwórz strukturę:

```
project/
├── app.py
├── format_test.py
├── test_tools.py
└── utils.py
```

Uruchom na wszystkich plikach:

```bash
# Formatowanie
black .

# Analiza
pylint *.py
```

#### Co się stanie?

- **Black** sformatuje wszystkie pliki `.py` w bieżącym katalogu
- **Pylint** przeanalizuje każdy plik z osobna

---

### Ćwiczenie 8 — Mini pipeline lokalny

#### Zadanie

Wykonaj sekwencyjnie:

```bash
# 1. Formatuj wszystkie pliki
black .

# 2. Analizuj kod
pylint app.py format_test.py test_tools.py
```

#### Interpretacja

Potraktuj to jak **lokalny pipeline jakości**:

1. **Krok 1**: Automatic formatting (Black)
2. **Krok 2**: Quality check (Pylint)

To jest dokładnie to, co robią GitHub Actions w CI/CD.

---

## Rozwiązania

### Rozwiązanie Ćwiczenia 1

```bash
$ pylint --version
pylint 3.0.0
astroid 3.0.0
Python 3.11.0 (main, ...)

$ black --version
black, 24.1.1 (compiled: yes)
```

✅ **Status**: Narzędzia zainstalowane prawidłowo.

---

### Rozwiązanie Ćwiczenia 2

Kod zawiera:

| Problem | Lokacja | Typ |
|---------|---------|-----|
| `import math` — nieużywany | Linia 1 | Jakość |
| `unused = 123` — nieużywana | Linia 5 | Jakość |
| Brak spacji wokół `=` w `a,b` | Linia 3 | Style |
| Brak spacji w `print( ... )` | Linia 6 | Style |
| Długa nazwa funkcji | Linia 9 | Style |

---

### Rozwiązanie Ćwiczenia 3

```bash
$ pylint app.py

app.py:1:0: W0611: Unused import math (unused-import)
app.py:3:0: C0111: Missing function docstring (missing-function-docstring)
app.py:5:8: W0612: Unused variable 'unused' (unused-variable)
app.py:6:11: C0326: Bad whitespace around operator (bad-whitespace)
app.py:9:0: C0103: Function name "bardzo_dluga_funkcja_z_niezbyt_dobrym_stylem" 
           doesn't conform to snake_case naming style (invalid-name)

Your code has been rated at 3.75/10
```

**Kategorie:**
- `W` = Warning (ostrzeżenie)
- `C` = Convention (konwencja)
- `E` = Error (błąd)

---

### Rozwiązanie Ćwiczenia 4

**Poprawiony kod** (patrz wyżej):

```bash
$ pylint app.py

app.py:1:0: C0111: Missing function docstring (missing-function-docstring)
app.py:12:0: C0111: Missing function docstring (missing-function-docstring)

Your code has been rated at 9.17/10
```

**Poprawa**: Z 3.75 → 9.17 / 10! 🎉

---

### Rozwiązanie Ćwiczenia 5

**Black zmienił:**

```python
# Przed
def powitanie( imie ):
    print(   "Cześć, " + imie )

# Po
def powitanie(imie):
    print("Cześć, " + imie)
```

---

### Rozwiązanie Ćwiczenia 6

```bash
$ black test_tools.py
reformatted test_tools.py

$ pylint test_tools.py

test_tools.py:1:0: W0611: Unused import os (unused-import)
test_tools.py:4:8: W0612: Unused variable 'x' (unused-variable)

Your code has been rated at 5.00/10
```

**Wnioski:**
- Black zmienił `x=5` → `x = 5`
- Pylint nadal widzi problemy logiczne

---

### Rozwiązanie Ćwiczenia 7 & 8

Pipeline:

```bash
$ black .
reformatted app.py
reformatted format_test.py
reformatted test_tools.py

$ pylint app.py format_test.py test_tools.py

app.py:1:0: C0111: Missing function docstring (missing-function-docstring)
...
Your code has been rated at 8.50/10
```

---

## GitHub Actions Workflow

### Konfiguracja CI/CD

Utwórz `.github/workflows/code-quality.yml`:

```yaml
name: Code Quality Check

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  quality:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pylint black
    
    - name: Format check with Black
      run: black --check --diff .
      continue-on-error: true
    
    - name: Lint with Pylint
      run: |
        pylint $(git ls-files '*.py') --fail-under=7.0
      continue-on-error: true
    
    - name: Auto-format (if needed)
      if: always()
      run: |
        black .
        git diff --quiet || echo "⚠️  Code was auto-formatted"
```

### Konfiguracja `.pylintrc`

Utwórz plik `.pylintrc` w głównym katalogu repozytorium:

```ini
[MASTER]
load-plugins=pylint_django
extension-pkg-whitelist=

[MESSAGES CONTROL]
disable=
    missing-docstring,
    too-few-public-methods,
    duplicate-code,

[FORMAT]
max-line-length=88

[DESIGN]
max-locals=15
max-branches=12
max-arguments=5
```

### Konfiguracja `pyproject.toml`

```toml
[tool.black]
line-length = 88
target-version = ['py38', 'py39', 'py310', 'py311']
include = '\.pyi?$'
exclude = '''
/(
    \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | _build
  | buck-out
  | build
  | dist
)/
'''

[tool.pylint.messages_control]
disable = [
    "missing-docstring",
    "too-few-public-methods",
]

[tool.pylint.format]
max-line-length = 88
```

---

## FAQ

### P: Czy muszę używać obu narzędzi?

**O:** Nie musisz, ale to najlepka praktyka. Black automatyzuje format, a Pylint wyłapuje prawdziwe problemy.

### P: Jaki jest domyślny score do zaakceptowania w Pylint?

**O:** Zazwyczaj > 7.0/10 jest uważane za akceptowalne. Możesz to zmienić w CI/CD: `--fail-under=7.0`.

### P: Czy Black zmieni nazwy moich zmiennych?

**O:** Nie. Black zmienia tylko format (spacje, wcięcia). Nazwy zmiennych pozostają niezmienione. Do tego używaj Pylint.

### P: Czy Black obsługuje inne języki?

**O:** Black to tylko dla Pythona. Dla JavaScript jest Prettier, dla Go — gofmt.

### P: Czy mogę wyłączyć reguły w Pylint?

**O:** Tak, za pomocą komentarzy:

```python
# pylint: disable=missing-docstring
def moja_funkcja():
    pass
```

### P: Czym się różni Black od autopep8?

**O:** Black jest bardziej rygorystyczny — narzuca jeden styl. autopep8 ma więcej opcji konfiguracji.

### P: Jaka jest różnica między Warning (W) a Convention (C) w Pylint?

**O:**
- **W** (Warning): potencjalny problem, mogą być błędy
- **C** (Convention): naruszenie konwencji nazewnictwa/stylu
- **E** (Error): kod na pewno się nie uruchomi

---

## Podsumowanie

| Narzędzie | Cel | Automatyczne? | Zmienia logikę? |
|-----------|-----|---------------|-----------------|
| **Black** | Formatowanie | ✅ Tak | ❌ Nie |
| **Pylint** | Analiza jakości | ❌ Nie | — |

### Najlepsze praktyki

1. ✅ Zainstaluj oba narzędzia
2. ✅ Uruchom **Black pierwszy** (format)
3. ✅ Uruchom **Pylint drugi** (jakość)
4. ✅ Zintegruj z CI/CD (GitHub Actions)
5. ✅ Ustal minimalny score w Pylint
6. ✅ Używaj pre-commit hooks (opcjonalnie):

```bash
pip install pre-commit
# Dodaj .pre-commit-config.yaml
pre-commit install
```

### Polecane Score'y

- **Lokalnie**: >= 7.0/10
- **W PR**: >= 8.0/10
- **Na main**: >= 8.5/10

---

## Zadanie domowe

### Cel

Utwórz plik Python z premedytacją zawierający błędy i problemy, a następnie je popraw.

### Kroki

#### 1. Utwórz plik `homework.py` z błędami

```python
import sys,os,json

def GetUserData( username ):
    unused_var = "test"
    result={"name":username,"age":25}
    print(  "User:", result )
    return result

class user_profile:
    def __init__(self,name,age):
        self.name=name
        self.age=age

    def get_info( ):
        return f"Name: {self.name}, Age: {self.age}"

GetUserData("John")
```

#### 2. Uruchom Pylint

```bash
pylint homework.py
```

Zanotuj score i problemy.

#### 3. Uruchom Black

```bash
black homework.py
```

#### 4. Uruchom Pylint ponownie

```bash
pylint homework.py
```

#### 5. Popraw kod ręcznie

**Oczekiwany wynik:**

```python
import json


def get_user_data(username):
    result = {"name": username, "age": 25}
    print("User:", result)
    return result


class UserProfile:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def get_info(self):
        return f"Name: {self.name}, Age: {self.age}"


get_user_data("John")
```

#### 6. Weryfikacja

```bash
pylint homework.py
```

Powinien być score >= 9.0/10.

### Sprawozdanie (opcjonalnie)

Utwórz plik `HOMEWORK_REPORT.md`:

```markdown
# Raport z zadania domowego

## Punkt wyjścia
- Score: X.XX/10
- Liczba problemów: Y

## Po Black
- Score: X.XX/10
- Zmieniono: [lista zmian]

## Po ręcznych poprawkach
- Score: X.XX/10
- Poprawiono: [lista poprawek]

## Wnioski
- ...
```

---

## Zasoby dodatkowe

- [Pylint dokumentacja](https://pylint.pycqa.org/)
- [Black dokumentacja](https://black.readthedocs.io/)
- [PEP 8 — Python Enhancement Proposal (style guide)](https://www.python.org/dev/peps/pep-0008/)
- [Pre-commit framework](https://pre-commit.com/)

---