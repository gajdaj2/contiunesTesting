# Lab 2: Shift Left — Pisanie Unit Testów w Pythonie

Laboratorium poświęcone pisaniu testów jednostkowych, mockingowi i analizie pokrycia kodu. Poznaj kultur "Shift Left" — testuj wcześnie, testuj często.

**Poziom**: początkujący–średniozaawansowany  
**Czas trwania**: ~3–4 godziny  
**Wymagania**: Python 3.8+, pip, git  
**Framework**: pytest, unittest.mock, pytest-cov

---

## Spis treści

2. [Wymagania i instalacja](#wymagania-i-instalacja)
3. [Teoria testowania](#teoria-testowania)
   - [AAA Pattern (Arrange-Act-Assert)](#aaa-pattern-arrange-act-assert)
   - [Typy testów](#typy-testów)
   - [Fixtures w pytest](#fixtures-w-pytest)
   - [Mocking i Patching](#mocking-i-patching)
   - [Code Coverage](#code-coverage)
4. [Funkcja do testowania](#funkcja-do-testowania)
5. [Ćwiczenia praktyczne](#ćwiczenia-praktyczne)
6. [Rozwiązania](#rozwiązania)
7. [GitHub Actions workflow](#github-actions-workflow)
8. [FAQ](#faq)
9. [Best Practices](#best-practices)
10. [Zadanie dodatkowe](#zadanie-dodatkowe)

---

## Wymagania i instalacja

### Wymagania systemowe

- **Python**: 3.8 lub nowszy
- **pip**: 20+
- **System**: Linux, macOS, Windows

### Instalacja zależności

#### Opcja 1: Instalacja minimalna

```bash
pip install pytest pytest-cov pytest-mock
```

#### Opcja 2: Z `requirements-dev.txt`

Utwórz plik `requirements-dev.txt`:

```
pytest==7.4.4
pytest-cov==4.1.0
pytest-mock==3.12.0
pytest-xdist==3.5.0
```

Instalacja:

```bash
pip install -r requirements-dev.txt
```

#### Opcja 3: Środowisko wirtualne (zalecane)

```bash
# Utwórz venv
python -m venv venv

# Aktywuj
source venv/bin/activate  # Linux/macOS
# lub
venv\Scripts\activate     # Windows

# Zainstaluj
pip install pytest pytest-cov pytest-mock
```

### Weryfikacja

```bash
pytest --version
pip show pytest-cov
```

Powinno wyświetlić wersje:

```
pytest 7.4.4
```

---

## Teoria testowania

### AAA Pattern (Arrange-Act-Assert)

Każdy test powinien mieć trzy sekcje:

```python
def test_example():
    # 1. ARRANGE — przygotuj dane i obiekty
    price = 100
    discount = 20
    
    # 2. ACT — wykonaj operację
    result = calculate_discount(price, discount)
    
    # 3. ASSERT — sprawdź wynik
    assert result == 80
```


W tym lab: **Unit Tests**.

### Fixtures w pytest

Fixture to funkcja, która dostarcza dane wejściowe do testu.

```python
import pytest

@pytest.fixture
def sample_price():
    return 100

def test_with_fixture(sample_price):
    result = calculate_discount(sample_price, 20)
    assert result == 80
```

**Zaawansowane: parametryzacja**

```python
@pytest.mark.parametrize("price,discount,expected", [
    (100, 20, 80),
    (50, 10, 45),
    (200, 50, 100),
])
def test_various_discounts(price, discount, expected):
    assert calculate_discount(price, discount) == expected
```

### Mocking i Patching

**Mock** to obiekt zastępczy, który symuluje rzeczywisty obiekt.

```python
from unittest.mock import Mock, patch

def test_with_mock(mocker):
    # Mock funkcji logowania
    mock_logger = mocker.patch('app.logger')
    
    # Uruchom funkcję
    calculate_discount(100, 20)
    
    # Sprawdź, czy logger był wywołany
    assert mock_logger.called
    assert mock_logger.call_count == 1
```

**Kiedy używać?**
- Bazy danych
- API externe
- Logowanie
- Systemy plików
- Zegar (czas)

### Code Coverage

**Coverage** pokazuje, jaki procent kodu jest pokryty testami.

```
Total lines: 50
Lines tested: 50
Coverage: 100%  ✅
```

**Kryteria**:
- < 50%: słaby
- 50–70%: średni
- 70–85%: dobry
- 85–95%: bardzo dobry
- 95–100%: doskonały

**Polecenie**:

```bash
pytest --cov=app --cov-report=html
```

---

## Funkcja do testowania

### Specyfikacja

Utwórz plik `discount_calculator.py`:

```python
"""
Module for calculating discounts on prices.
"""
import logging

logger = logging.getLogger(__name__)


def calculate_discount(price: float, discount_percent: float) -> float:
    """
    Calculate final price after applying discount.
    
    Args:
        price: Original price (must be >= 0)
        discount_percent: Discount percentage (0-100)
    
    Returns:
        Final price after discount
    
    Raises:
        ValueError: If price is negative or discount is invalid
        TypeError: If inputs are not numeric
    
    Examples:
        >>> calculate_discount(100, 20)
        80.0
        >>> calculate_discount(50, 0)
        50.0
    """
    # Walidacja typów
    if not isinstance(price, (int, float)):
        logger.error(f"Invalid price type: {type(price)}")
        raise TypeError(f"Price must be numeric, got {type(price).__name__}")
    
    if not isinstance(discount_percent, (int, float)):
        logger.error(f"Invalid discount type: {type(discount_percent)}")
        raise TypeError(f"Discount must be numeric, got {type(discount_percent).__name__}")
    
    # Walidacja wartości
    if price < 0:
        logger.error(f"Negative price: {price}")
        raise ValueError(f"Price cannot be negative: {price}")
    
    if not 0 <= discount_percent <= 100:
        logger.error(f"Invalid discount percentage: {discount_percent}")
        raise ValueError(f"Discount must be between 0 and 100, got {discount_percent}")
    
    # Kalkulacja
    discount_amount = price * (discount_percent / 100)
    final_price = price - discount_amount
    
    logger.info(f"Calculated discount: ${discount_amount:.2f} on ${price:.2f}")
    
    return round(final_price, 2)


def apply_bulk_discount(price: float, quantity: int) -> float:
    """
    Apply bulk discount based on quantity.
    
    Bulk discounts:
    - 1-5 items: 0%
    - 6-10 items: 5%
    - 11-20 items: 10%
    - 21+ items: 15%
    
    Args:
        price: Unit price
        quantity: Number of items
    
    Returns:
        Final unit price after bulk discount
    """
    if quantity < 1:
        raise ValueError("Quantity must be at least 1")
    
    if quantity <= 5:
        discount = 0
    elif quantity <= 10:
        discount = 5
    elif quantity <= 20:
        discount = 10
    else:
        discount = 15
    
    logger.info(f"Applied bulk discount: {discount}% for quantity {quantity}")
    
    return calculate_discount(price, discount)
```

### Wymagania funkcji

✅ Obsługuje ceny pozytywne  
✅ Obsługuje rabaty 0-100%  
✅ Zwraca wynik zaokrąglony do 2 miejsc  
✅ Loguje wszystkie operacje  
✅ Wyrzuca `ValueError` dla błędnych wartości  
✅ Wyrzuca `TypeError` dla błędnych typów  
✅ Ma obsługę bulk discount

---

## Ćwiczenia praktyczne

### Ćwiczenie 1 — Pierwszy test (Happy Path)

#### Zadanie

Utwórz plik `test_discount_calculator.py` i napisz test dla normalnego przypadku:

```python
import pytest
from discount_calculator import calculate_discount


def test_calculate_discount_normal_case():
    """Test basic discount calculation."""
    # ARRANGE
    price = 100
    discount = 20
    
    # ACT
    result = calculate_discount(price, discount)
    
    # ASSERT
    assert result == 80.0
```

#### Uruchomienie

```bash
pytest test_discount_calculator.py::test_calculate_discount_normal_case -v
```

#### Oczekiwany wynik

```
test_discount_calculator.py::test_calculate_discount_normal_case PASSED [100%]
```

---

### Ćwiczenie 2 — Edge Cases (granice)

#### Zadanie

Dodaj testy dla przypadków granicznych:

```python
def test_calculate_discount_zero_discount():
    """Test with 0% discount (no discount)."""
    result = calculate_discount(100, 0)
    assert result == 100.0


def test_calculate_discount_full_discount():
    """Test with 100% discount."""
    result = calculate_discount(100, 100)
    assert result == 0.0


def test_calculate_discount_zero_price():
    """Test with zero price."""
    result = calculate_discount(0, 50)
    assert result == 0.0


def test_calculate_discount_decimal_values():
    """Test with decimal inputs."""
    result = calculate_discount(99.99, 10)
    assert result == pytest.approx(89.99, abs=0.01)
```

#### Co sprawdzamy?

- ✅ Rabat 0% = bez zmian
- ✅ Rabat 100% = cena 0
- ✅ Cena 0 = wynik 0
- ✅ Wartości dziesiętne są obsługiwane

---

### Ćwiczenie 3 — Błędy (Error Cases)

#### Zadanie

Dodaj testy dla przypadków błędnych:

```python
def test_calculate_discount_negative_price():
    """Test with negative price raises ValueError."""
    with pytest.raises(ValueError, match="Price cannot be negative"):
        calculate_discount(-50, 20)


def test_calculate_discount_invalid_discount_too_high():
    """Test with discount > 100% raises ValueError."""
    with pytest.raises(ValueError, match="Discount must be between"):
        calculate_discount(100, 150)


def test_calculate_discount_invalid_discount_negative():
    """Test with negative discount raises ValueError."""
    with pytest.raises(ValueError, match="Discount must be between"):
        calculate_discount(100, -10)


def test_calculate_discount_invalid_price_type():
    """Test with non-numeric price raises TypeError."""
    with pytest.raises(TypeError, match="Price must be numeric"):
        calculate_discount("100", 20)


def test_calculate_discount_invalid_discount_type():
    """Test with non-numeric discount raises TypeError."""
    with pytest.raises(TypeError, match="Discount must be numeric"):
        calculate_discount(100, "20%")
```

#### Co sprawdzamy?

- ✅ Cena ujemna = błąd
- ✅ Rabat > 100% = błąd
- ✅ Rabat < 0% = błąd
- ✅ Cena nie-numeryczna = TypeError
- ✅ Rabat nie-numeryczny = TypeError

---

### Ćwiczenie 4 — Mocking i Logowanie

#### Zadanie

Mockuj logger i sprawdź, czy funkcja loguje prawidłowo:

```python
def test_calculate_discount_logs_info(mocker):
    """Test that discount calculation is logged."""
    # ARRANGE
    mock_logger = mocker.patch('discount_calculator.logger')
    
    # ACT
    result = calculate_discount(100, 20)
    
    # ASSERT
    assert result == 80.0
    # Sprawdź, że logger.info był wywołany
    assert mock_logger.info.called
    mock_logger.info.assert_called_once()


def test_calculate_discount_logs_error_on_invalid_price(mocker):
    """Test that error is logged for invalid price."""
    # ARRANGE
    mock_logger = mocker.patch('discount_calculator.logger')
    
    # ACT & ASSERT
    with pytest.raises(ValueError):
        calculate_discount(-50, 20)
    
    # Sprawdź, że logger.error był wywołany
    mock_logger.error.assert_called()


def test_calculate_discount_logs_error_on_type_error(mocker):
    """Test that TypeError is logged."""
    # ARRANGE
    mock_logger = mocker.patch('discount_calculator.logger')
    
    # ACT & ASSERT
    with pytest.raises(TypeError):
        calculate_discount("100", 20)
    
    # Sprawdź zawartość loga
    call_args = mock_logger.error.call_args[0][0]
    assert "Invalid price type" in call_args
```

#### Co sprawdzamy?

- ✅ Logger jest wywołany przy sukcesie
- ✅ Logger.error jest wywołany dla ValueError
- ✅ Logger.error jest wywołany dla TypeError

---

### Ćwiczenie 5 — Fixtures i Parametryzacja

#### Zadanie

Refactor testów używając fixtures i parametryzacji:

```python
@pytest.fixture
def valid_price():
    """Fixture providing valid price."""
    return 100


@pytest.fixture
def valid_discount():
    """Fixture providing valid discount."""
    return 20


def test_with_fixtures(valid_price, valid_discount):
    """Test using fixtures."""
    result = calculate_discount(valid_price, valid_discount)
    assert result == 80.0


@pytest.mark.parametrize("price,discount,expected", [
    (100, 20, 80.0),
    (50, 10, 45.0),
    (200, 50, 100.0),
    (99.99, 10, 89.99),
    (1000, 99, 10.0),
])
def test_various_discounts(price, discount, expected):
    """Test various discount scenarios."""
    result = calculate_discount(price, discount)
    assert result == pytest.approx(expected, abs=0.01)
```

#### Zalety

- ✅ Mniej powtarzającego się kodu
- ✅ Łatwiej dodać nowe przypadki
- ✅ Jasne dane testowe

---

### Ćwiczenie 6 — Bulk Discount Tests

#### Zadanie

Napisz testy dla funkcji `apply_bulk_discount`:

```python
from discount_calculator import apply_bulk_discount


@pytest.mark.parametrize("quantity,expected_discount", [
    (1, 0),
    (5, 0),
    (6, 5),
    (10, 5),
    (11, 10),
    (20, 10),
    (21, 15),
    (100, 15),
])
def test_bulk_discount_tiers(quantity, expected_discount):
    """Test bulk discount tiers."""
    result = apply_bulk_discount(100, quantity)
    expected = calculate_discount(100, expected_discount)
    assert result == expected


def test_bulk_discount_invalid_quantity():
    """Test that quantity < 1 raises error."""
    with pytest.raises(ValueError, match="Quantity must be at least 1"):
        apply_bulk_discount(100, 0)
```

---

### Ćwiczenie 7 — Code Coverage (100%)

#### Zadanie

Uruchom analizę pokrycia kodu:

```bash
# Uruchom testy z coverage
pytest test_discount_calculator.py --cov=discount_calculator --cov-report=term-missing

# Wygeneruj raport HTML
pytest test_discount_calculator.py --cov=discount_calculator --cov-report=html
```

#### Oczekiwany wynik

```
discount_calculator.py  50   50   100%
```

#### Otwarcie raportu HTML

```bash
# Linux/macOS
open htmlcov/index.html

# Windows
start htmlcov/index.html
```

#### Zadanie

Dodaj testy, aż pokrycie będzie **100%**.

---

### Ćwiczenie 8 — Uruchomienie testu w CI/CD

#### Zadanie

Skonfiguruj GitHub Actions do automatycznego testowania.

Utwórz `.github/workflows/tests.yml`:

```yaml
name: Unit Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10', '3.11']
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pytest pytest-cov pytest-mock
    
    - name: Run tests
      run: pytest test_discount_calculator.py -v
    
    - name: Check coverage
      run: |
        pytest test_discount_calculator.py --cov=discount_calculator --cov-report=term-missing
        pytest test_discount_calculator.py --cov=discount_calculator --cov-fail-under=90
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        files: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
```

---

## Rozwiązania

### Kompletny plik `test_discount_calculator.py`

```python
"""
Unit tests for discount_calculator module.

Tests cover:
- Normal cases (happy path)
- Edge cases (boundaries)
- Error cases (exceptions)
- Logging with mocks
- Code coverage
"""

import pytest
from unittest.mock import patch, MagicMock
from discount_calculator import calculate_discount, apply_bulk_discount


# ===== FIXTURES =====

@pytest.fixture
def valid_price():
    """Fixture: valid price."""
    return 100.0


@pytest.fixture
def valid_discount():
    """Fixture: valid discount percentage."""
    return 20


@pytest.fixture
def sample_prices():
    """Fixture: multiple test prices."""
    return [10, 50, 100, 500, 999.99]


# ===== NORMAL CASES (HAPPY PATH) =====

def test_calculate_discount_basic(valid_price, valid_discount):
    """Test basic discount calculation."""
    result = calculate_discount(valid_price, valid_discount)
    assert result == 80.0


def test_calculate_discount_returns_float():
    """Test that result is always float."""
    result = calculate_discount(100, 20)
    assert isinstance(result, float)


# ===== EDGE CASES =====

def test_calculate_discount_zero_discount():
    """Test with 0% discount (no discount applied)."""
    result = calculate_discount(100, 0)
    assert result == 100.0


def test_calculate_discount_full_discount():
    """Test with 100% discount (price becomes zero)."""
    result = calculate_discount(100, 100)
    assert result == 0.0


def test_calculate_discount_zero_price():
    """Test with zero price."""
    result = calculate_discount(0, 50)
    assert result == 0.0


def test_calculate_discount_decimal_values():
    """Test with decimal (float) inputs."""
    result = calculate_discount(99.99, 10)
    assert result == pytest.approx(89.99, abs=0.01)


def test_calculate_discount_small_amount():
    """Test with very small price."""
    result = calculate_discount(0.01, 50)
    assert result == pytest.approx(0.005, abs=0.001)


def test_calculate_discount_large_amount():
    """Test with very large price."""
    result = calculate_discount(1000000, 50)
    assert result == 500000.0


def test_calculate_discount_rounding():
    """Test that result is properly rounded to 2 decimal places."""
    result = calculate_discount(100, 33.33)  # 33.33
    assert result == pytest.approx(66.67, abs=0.01)


# ===== PARAMETRIZED TESTS =====

@pytest.mark.parametrize("price,discount,expected", [
    (100, 0, 100.0),
    (100, 10, 90.0),
    (100, 20, 80.0),
    (100, 50, 50.0),
    (100, 100, 0.0),
    (50, 10, 45.0),
    (200, 25, 150.0),
    (75, 33, 50.25),
])
def test_various_discount_scenarios(price, discount, expected):
    """Test multiple discount scenarios using parametrization."""
    result = calculate_discount(price, discount)
    assert result == pytest.approx(expected, abs=0.01)


# ===== ERROR CASES (VALUE ERRORS) =====

def test_calculate_discount_negative_price():
    """Test that negative price raises ValueError."""
    with pytest.raises(ValueError, match="Price cannot be negative"):
        calculate_discount(-50, 20)


def test_calculate_discount_negative_price_boundary():
    """Test boundary: -0.01 should raise ValueError."""
    with pytest.raises(ValueError):
        calculate_discount(-0.01, 20)


def test_calculate_discount_discount_above_100():
    """Test that discount > 100% raises ValueError."""
    with pytest.raises(ValueError, match="Discount must be between"):
        calculate_discount(100, 150)


def test_calculate_discount_discount_negative():
    """Test that negative discount raises ValueError."""
    with pytest.raises(ValueError, match="Discount must be between"):
        calculate_discount(100, -10)


def test_calculate_discount_discount_above_100_boundary():
    """Test boundary: 100.01% should raise ValueError."""
    with pytest.raises(ValueError):
        calculate_discount(100, 100.01)


# ===== ERROR CASES (TYPE ERRORS) =====

def test_calculate_discount_price_string():
    """Test that string price raises TypeError."""
    with pytest.raises(TypeError, match="Price must be numeric"):
        calculate_discount("100", 20)


def test_calculate_discount_price_none():
    """Test that None price raises TypeError."""
    with pytest.raises(TypeError):
        calculate_discount(None, 20)


def test_calculate_discount_discount_string():
    """Test that string discount raises TypeError."""
    with pytest.raises(TypeError, match="Discount must be numeric"):
        calculate_discount(100, "20%")


def test_calculate_discount_discount_list():
    """Test that list discount raises TypeError."""
    with pytest.raises(TypeError):
        calculate_discount(100, [20])


# ===== LOGGING TESTS WITH MOCKS =====

def test_calculate_discount_logs_info_on_success(mocker):
    """Test that successful calculation is logged at INFO level."""
    # ARRANGE
    mock_logger = mocker.patch('discount_calculator.logger')
    
    # ACT
    result = calculate_discount(100, 20)
    
    # ASSERT
    assert result == 80.0
    mock_logger.info.assert_called_once()


def test_calculate_discount_logs_error_negative_price(mocker):
    """Test that negative price is logged at ERROR level."""
    # ARRANGE
    mock_logger = mocker.patch('discount_calculator.logger')
    
    # ACT & ASSERT
    with pytest.raises(ValueError):
        calculate_discount(-50, 20)
    
    mock_logger.error.assert_called()
    call_args = mock_logger.error.call_args[0][0]
    assert "Negative price" in call_args


def test_calculate_discount_logs_error_invalid_discount_type(mocker):
    """Test that invalid discount type is logged."""
    # ARRANGE
    mock_logger = mocker.patch('discount_calculator.logger')
    
    # ACT & ASSERT
    with pytest.raises(TypeError):
        calculate_discount(100, "20")
    
    mock_logger.error.assert_called()
    call_args = mock_logger.error.call_args[0][0]
    assert "Invalid discount type" in call_args


def test_calculate_discount_logs_calculation_details(mocker):
    """Test that log contains calculation details."""
    # ARRANGE
    mock_logger = mocker.patch('discount_calculator.logger')
    
    # ACT
    calculate_discount(100, 20)
    
    # ASSERT
    log_message = mock_logger.info.call_args[0][0]
    assert "$20.00" in log_message  # discount amount
    assert "$100.00" in log_message  # original price


# ===== BULK DISCOUNT TESTS =====

@pytest.mark.parametrize("quantity,expected_discount_percent", [
    (1, 0),    # 1-5 items: 0%
    (5, 0),
    (6, 5),    # 6-10 items: 5%
    (10, 5),
    (11, 10),  # 11-20 items: 10%
    (20, 10),
    (21, 15),  # 21+ items: 15%
    (100, 15),
    (1000, 15),
])
def test_apply_bulk_discount_tiers(quantity, expected_discount_percent):
    """Test bulk discount tier calculations."""
    # ARRANGE
    unit_price = 100
    
    # ACT
    result = apply_bulk_discount(unit_price, quantity)
    
    # ASSERT
    expected = calculate_discount(unit_price, expected_discount_percent)
    assert result == expected


def test_apply_bulk_discount_quantity_zero():
    """Test that quantity < 1 raises ValueError."""
    with pytest.raises(ValueError, match="Quantity must be at least 1"):
        apply_bulk_discount(100, 0)


def test_apply_bulk_discount_negative_quantity():
    """Test that negative quantity raises ValueError."""
    with pytest.raises(ValueError):
        apply_bulk_discount(100, -5)


def test_apply_bulk_discount_returns_float():
    """Test that bulk discount returns float."""
    result = apply_bulk_discount(100, 10)
    assert isinstance(result, float)


# ===== INTEGRATION TESTS =====

def test_chained_operations():
    """Test chaining multiple discount operations."""
    price = 100
    discount1 = calculate_discount(price, 10)  # 90
    discount2 = calculate_discount(discount1, 10)  # 81
    
    assert discount1 == 90.0
    assert discount2 == 81.0


def test_bulk_discount_with_manual_calculation():
    """Test that bulk discount matches manual calculation."""
    # Buy 15 items at $10 each = 10% discount
    unit_price = 10
    quantity = 15
    
    result = apply_bulk_discount(unit_price, quantity)
    expected = 9.0  # $10 * (1 - 0.10)
    
    assert result == expected
```

### Uruchomienie i wyniki

```bash
# Uruchom wszystkie testy
pytest test_discount_calculator.py -v

# Wynik:
test_discount_calculator.py::test_calculate_discount_basic PASSED
test_discount_calculator.py::test_calculate_discount_returns_float PASSED
test_discount_calculator.py::test_calculate_discount_zero_discount PASSED
...
test_discount_calculator.py::test_chained_operations PASSED

====== 40 passed in 2.34s ======
```

### Coverage Report

```bash
pytest test_discount_calculator.py --cov=discount_calculator --cov-report=term-missing

discount_calculator.py      50      50    100%
```

---

## GitHub Actions Workflow

### Konfiguracja CI/CD

Utwórz `.github/workflows/tests.yml`:

```yaml
name: Unit Tests CI/CD

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    # Codziennie o 2:00 AM
    - cron: '0 2 * * *'

jobs:
  test:
    runs-on: ${{ matrix.os }}
    
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ['3.8', '3.9', '3.10', '3.11', '3.12']
      fail-fast: false
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
        cache: 'pip'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pytest pytest-cov pytest-mock
    
    - name: Run unit tests
      run: |
        pytest test_discount_calculator.py -v --tb=short
    
    - name: Generate coverage report
      run: |
        pytest test_discount_calculator.py \
          --cov=discount_calculator \
          --cov-report=term-missing \
          --cov-report=xml \
          --cov-report=html
    
    - name: Check coverage threshold
      run: |
        pytest test_discount_calculator.py \
          --cov=discount_calculator \
          --cov-fail-under=90
    
    - name: Upload coverage to Codecov
      if: matrix.os == 'ubuntu-latest' && matrix.python-version == '3.11'
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
        fail_ci_if_error: true
    
    - name: Archive coverage reports
      if: always()
      uses: actions/upload-artifact@v3
      with:
        name: coverage-report-py${{ matrix.python-version }}-${{ matrix.os }}
        path: htmlcov/
        retention-days: 30
    
    - name: Comment PR with coverage
      if: github.event_name == 'pull_request'
      uses: py-cov-action/python-coverage-comment-action@v3
      with:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Konfiguracja `pytest.ini`

Utwórz plik `pytest.ini`:

```ini
[pytest]
testpaths = .
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --strict-markers
    --tb=short
    --disable-warnings
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests
```

### Konfiguracja `.coveragerc`

Utwórz plik `.coveragerc`:

```ini
[run]
source = .
omit =
    */tests/*
    */test_*.py
    setup.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:
    @abstractmethod
    @abc.abstractmethod
```

---

## FAQ

### P: Co to jest "mock"?

**O:** Mock to obiekt zastępczy. Zamiast rzeczywistego loggera, bazy danych czy API, używamy fake'a, aby izolować test.

```python
real_logger = logger  # Nieznany stan
mock_logger = mocker.patch('app.logger')  # Kontrolujemy
```

### P: Czy powinno być 100% coverage?

**O:** Nie zawsze. 100% jest ideałem, ale:
- < 70%: zbyt mało
- 70–85%: dobry start
- 85–100%: aspiracja

W produkcji: >= 80%. W critical path: >= 90%.

### P: Co to "parametryzacja"?

**O:** To uruchomienie tego samego testu z różnymi danymi:

```python
@pytest.mark.parametrize("x,y,z", [(1,2,3), (4,5,6)])
def test_func(x, y, z):
    pass
```

Zamiast pisać 2 funkcje, piszesz 1.

### P: Jaka różnica między `assert` a `pytest.raises`?

**O:**

```python
# assert — sprawdza, że wynik jest prawdziwy
assert result == 80

# pytest.raises — sprawdza, że wyjątek został wyrzucony
with pytest.raises(ValueError):
    function_that_fails()
```

### P: Czy muszę mockować logger?

**O:** Nie musisz. Ale to dobre praktyka, bo:
- ✅ Nie zapisujesz do pliku podczas testu
- ✅ Kontrolujesz dokładnie, co się loguje
- ✅ Testy działają szybciej

### P: Czym się różni `mocker.patch` od `unittest.mock.patch`?

**O:** To to samo — `mocker` to pytest plugin, który opakowuje `unittest.mock`. Używaj `mocker` w pytest.

### P: Czy testy mogą się sobie przeszkadzać?

**O:** Tak, jeśli dzielą stan. Dlatego:
- ✅ Używaj fixtures zamiast globalnych zmiennych
- ✅ Każdy test powinien być niezależny
- ✅ Mocki są resetowane po każdym teście

### P: Jak szybko powinny działać testy?

**O:** Cała bateria unit testów < 10 sekund. Jeśli dłużej:
- Może są to testy integracyjne
- Może jest za dużo logiki
- Może brak izolacji (mocków)

---

## Best Practices

### 1. **Jeden assert na test (ideał)**

```python
# ✅ DOBRZE
def test_discount_is_calculated():
    assert calculate_discount(100, 20) == 80

def test_discount_is_float():
    assert isinstance(calculate_discount(100, 20), float)

# ❌ ŹLE
def test_discount():
    result = calculate_discount(100, 20)
    assert result == 80  # Multiple asserts
    assert isinstance(result, float)
```

### 2. **AAA Pattern zawsze**

```python
# ✅ DOBRZE
def test_example():
    # Arrange
    value = 100
    
    # Act
    result = function(value)
    
    # Assert
    assert result == expected

# ❌ ŹLE
def test_example():
    result = function(100)
    assert result == 100  # Gdzie się przygotowuje dane?
```

### 3. **Descriptive names**

```python
# ✅ DOBRZE
def test_calculate_discount_with_negative_price_raises_value_error():
    pass

# ❌ ŹLE
def test_discount():
    pass

def test_calc():
    pass
```

### 4. **Nie testuj implementacji, testuj zachowanie**

```python
# ❌ ŹLE — testuje implementation
def test_discount_calculation():
    price = 100
    discount = price * 0.2  # Same obliczenia
    assert discount == 20

# ✅ DOBRZE — testuje behavior
def test_discount_calculation():
    assert calculate_discount(100, 20) == 80
```

### 5. **Fixtures dla powtarzających się danych**

```python
# ❌ ŹLE
def test_1():
    price = 100
    assert calculate_discount(price, 20) == 80

def test_2():
    price = 100
    assert calculate_discount(price, 10) == 90

# ✅ DOBRZE
@pytest.fixture
def valid_price():
    return 100

def test_1(valid_price):
    assert calculate_discount(valid_price, 20) == 80

def test_2(valid_price):
    assert calculate_discount(valid_price, 10) == 90
```

### 6. **Parametryzacja zamiast loop'ów**

```python
# ❌ ŹLE
def test_discounts():
    for price, discount, expected in [(100, 20, 80), (50, 10, 45)]:
        assert calculate_discount(price, discount) == expected

# ✅ DOBRZE
@pytest.mark.parametrize("price,discount,expected", [
    (100, 20, 80),
    (50, 10, 45),
])
def test_discounts(price, discount, expected):
    assert calculate_discount(price, discount) == expected
```

### 7. **Mockuj tylko granice**

```python
# ❌ ŹLE — mockujesz za dużo
mock_price = mocker.patch('app.price')
mock_discount = mocker.patch('app.discount')

# ✅ DOBRZE — mockujesz tylko logger (external dependency)
mock_logger = mocker.patch('app.logger')
assert calculate_discount(100, 20) == 80
```

### 8. **Test names should be runnable documentation**

Patrząc na nazwy testów, powinno być jasne, co aplikacja robi:

```
✅ test_calculate_discount_with_valid_inputs_returns_correct_amount
✅ test_calculate_discount_with_zero_percent_returns_original_price
✅ test_calculate_discount_with_negative_price_raises_value_error
❌ test_calc
❌ test_discount
```

---

## Zadanie dodatkowe

### Zadanie 1: Napisz testy dla `apply_bulk_discount`

Napisz co najmniej 10 testów dla funkcji `apply_bulk_discount`, obejmując:
- ✅ Każdy tier rabatu (0%, 5%, 10%, 15%)
- ✅ Granice tier'ów
- ✅ Błędy (quantity < 1)
- ✅ Decimal prices
- ✅ Mocking

### Zadanie 2: Dodaj nową funkcję z testami

Dodaj funkcję `apply_seasonal_discount`:

```python
def apply_seasonal_discount(price: float, season: str) -> float:
    """
    Apply seasonal discount.
    
    Seasons:
    - "spring": 5%
    - "summer": 10%
    - "autumn": 7%
    - "winter": 20%
    """
```

Napisz testy:
- ✅ Wszystkie sezony
- ✅ Invalid season (ValueError)
- ✅ Case-insensitive
- ✅ Null/None

### Zadanie 3: Integracyjny test

Napisa test, który łączy wiele funkcji:

```python
def test_full_discount_flow():
    """Test: customer buys 25 items at $10 each in winter."""
    # 25 items = 15% bulk discount = $8.50
    # Winter = 20% seasonal = $6.80
    # Total = $170
    
    unit_price = 10
    quantity = 25
    
    price_with_bulk = apply_bulk_discount(unit_price, quantity)
    final_price = apply_seasonal_discount(price_with_bulk, "winter")
    
    assert final_price == pytest.approx(6.80, abs=0.01)
```

### Zadanie 4: Performance test

Napisz test wydajności:

```python
import time

def test_calculate_discount_performance():
    """Test that calculation is fast (< 1ms)."""
    start = time.time()
    for _ in range(10000):
        calculate_discount(100, 20)
    elapsed = time.time() - start
    
    assert elapsed < 1.0  # 10k calculations < 1 second
```

### Zadanie 5: Raport z pokrycia

Wygeneruj raport HTML i:
1. Otwórz `htmlcov/index.html`
2. Znajdź linie, które nie są pokryte
3. Dodaj testy, aby je pokryć
4. Osiągnij 100%

```bash
pytest test_discount_calculator.py --cov=discount_calculator --cov-report=html
open htmlcov/index.html
```

---

## Struktury katalogów projektu

```
project/
├── discount_calculator.py          # Kod aplikacji
├── test_discount_calculator.py     # Testy jednostkowe
├── requirements-dev.txt            # Zależności dev
├── pytest.ini                      # Konfiguracja pytest
├── .coveragerc                     # Konfiguracja coverage
├── .github/
│   └── workflows/
│       └── tests.yml              # GitHub Actions CI/CD
├── htmlcov/                       # Raport HTML coverage
│   └── index.html
└── README.md                       # Ten plik
```

---

## Uruchomienie całego projektu

### Setup (jednorazowo)

```bash
# 1. Klonuj lub utwórz projekt
mkdir lab2-unit-tests && cd lab2-unit-tests

# 2. Utwórz venv
python -m venv venv
source venv/bin/activate  # Linux/macOS

# 3. Zainstaluj zależności
pip install pytest pytest-cov pytest-mock

# 4. Utwórz pliki
# — discount_calculator.py
# — test_discount_calculator.py
# — pytest.ini
# — .coveragerc
```

### Lokalne testowanie

```bash
# Uruchom wszystkie testy
pytest -v

# Z coverage
pytest --cov=discount_calculator --cov-report=html

# Spesyficzne testy
pytest test_discount_calculator.py::test_calculate_discount_basic -v

# Testy z keyword
pytest -k "bulk" -v
```

### CI/CD

```bash
# Push do GitHub
git push origin feature/tests

# GitHub Actions uruchomi się automatycznie
# Sprawdź status w Actions tab
```

---

## Podsumowanie

| Koncepcja | Opis | Przykład |
|-----------|------|----------|
| **Unit Test** | Testuje jedną funkcję | `test_calculate_discount_basic` |
| **Edge Case** | Granice, zero, duplikaty | `test_zero_discount`, `test_negative_price` |
| **Mock** | Fake obiekt | `mocker.patch('logger')` |
| **Fixture** | Przygotowanie danych | `@pytest.fixture def valid_price` |
| **Parametryzacja** | Wiele danych do jednego testu | `@pytest.mark.parametrize` |
| **Coverage** | % pokrycia kodu | `pytest --cov=app` |
| **Shift Left** | Testuj wcześnie | Testy podczas kodzenia |

---

## Zasoby

- [pytest dokumentacja](https://docs.pytest.org/)
- [unittest.mock dokumentacja](https://docs.python.org/3/library/unittest.mock.html)
- [pytest-cov dokumentacja](https://pytest-cov.readthedocs.io/)
- [Test Driven Development (TDD)](https://en.wikipedia.org/wiki/Test-driven_development)
- [PEP 8 Testing](https://www.python.org/dev/peps/pep-0008/#should-a-test-subclass-unittest-testcase-or-pytest)

---

## Autor

Materiał przygotowany jako część kursu **Shift Left & Code Quality**.

**Ostatnia aktualizacja:** 2025-03-15

---

**Happy testing! 🧪**