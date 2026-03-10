# Playwright Python - Szybki Kurs

## Co to Playwright?

**Playwright** to narzędzie do E2E testowania - automatyzuje przeglądarkę jak człowiek.

```
✅ Automatyzuje Chrome, Firefox, Safari
✅ Czeka na elementy (nie sleep)
✅ Mockuje network requests
✅ Screenshots, videos, traces
✅ Szybki, niezawodny, nowoczesny
```

---

## Instalacja

```bash
pip install pytest-playwright

# Zainstaluj przeglądarki
playwright install
```

---

## Pierwsza Test

```python
from playwright.sync_api import expect
import pytest

def test_example(page):
    # Otworz stronę
    page.goto("https://example.com")
    
    # Sprawdź tytuł
    expect(page).to_have_title("Example Domain")
```

**Uruchomienie:**
```bash
pytest test_example.py
```

---

## Konfig Pytest

Plik: `conftest.py`

```python
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture
def page():
    """Fixture - przeglądarką dostępną w każdym teście"""
    with sync_playwright() as p:
        browser = p.chromium.launch()  # headless=False żeby widzieć
        page = browser.new_page()
        yield page
        browser.close()

@pytest.fixture
def browser_context():
    """Fixture z pełnym contextem"""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        yield context
        context.close()
        browser.close()
```

---

## Selektory - Jak Znaleźć Elementy

### 1. CSS Selectors

```python
# Po ID
page.click("#submit-button")

# Po klasie
page.click(".primary-btn")

# Po tagu
page.click("button")

# Po atrybucie
page.click('input[name="email"]')

# Kombinacja
page.click("form.login input[type='submit']")
```

### 2. XPath

```python
# Po tekstowi
page.click("//button[contains(text(), 'Login')]")

# Po atrybucie
page.click("//input[@id='email']")

# Pierwsze pasujące
page.click("(//button)[1]")
```

### 3. Text Selectors (Najlepsze!)

```python
# Po całym tekście
page.click('text="Click Me"')

# Po częśćtekstu
page.click("text=Click")

# Case insensitive
page.click("button:has-text('submit')")
```

### 4. Data Attributes (Rekomendowane)

```python
# HTML
# <button data-testid="submit-btn">Submit</button>

# Python
page.click('[data-testid="submit-btn"]')
```

### 5. Inne

```python
# Placeholder
page.fill('input[placeholder="Email"]', "user@test.com")

# Label (dla formularz)
page.click('label:has-text("Remember me")')

# Nth child
page.click(".products >> nth=0")  # Pierwszy produkt
```

---

## Interakcje z UI

### Klikanie

```python
page.click('button[type="submit"]')

# Double click
page.dblclick('input[name="quantity"]')

# Right click
page.click('button', button='right')

# Czekaj aż będzie clickable
page.click('button', timeout=5000)
```

### Wypełnianie Formularzy

```python
# Text input
page.fill('input[name="email"]', 'user@test.com')

# Textarea
page.fill('textarea', 'Moja wiadomość')

# Select/dropdown
page.select_option('select[name="country"]', 'PL')

# Checkbox
page.check('input[type="checkbox"]')
page.uncheck('input[type="checkbox"]')

# Radio button
page.click('input[value="male"]')
```

### Czytanie Tekstu

```python
# GetText
text = page.text_content('h1')  # "Witaj!"

# getInputValue
value = page.input_value('input[name="email"]')

# getAttribute
href = page.get_attribute('a', 'href')

# HTML
html = page.inner_html('.container')
```

---

## Czekanie - Bardzo Ważne!

### ❌ Zło - Czekaj Sztywnie

```python
import time
time.sleep(5)  # ŹLE!
```

### ✅ Dobrze - Czekaj na Element

```python
from playwright.sync_api import expect

# Czekaj aż element będzie widoczny
page.wait_for_selector('.success-message')

# Czekaj aż znika
page.wait_for_selector('.loader', state='hidden')

# Czekaj aż będzie clickable
expect(page.locator('button')).to_be_enabled()

# Czekaj na tekst
page.wait_for_selector('text=Success')

# Czekaj na URL
page.wait_for_url('**/dashboard')
```

### ✅ Czekaj na Network

```python
# Czekaj aż request się zakończy
response = page.wait_for_response(
    lambda resp: 'api/login' in resp.url and resp.status == 200,
    timeout=10000
)

# Mockuj API zamiast czekać
page.route('**/api/products', lambda route: route.abort())

# Intercept i zmodyfikuj response
def handle_route(route):
    response = route.fetch()
    response_body = response.json()
    response_body['products'] = []
    route.fulfill(response=response, body=response_body)

page.route('**/api/products', handle_route)
```

---

## Asercje (Assertions)

```python
from playwright.sync_api import expect

# Tekst
expect(page.locator('h1')).to_contain_text('Witaj')

# Wartość input'u
expect(page.locator('input[name="email"]')).to_have_value('user@test.com')

# Atrybut
expect(page.locator('a')).to_have_attribute('href', '/home')

# CSS class
expect(page.locator('button')).to_have_class('primary')

# Element widoczny
expect(page.locator('.modal')).to_be_visible()

# Element ukryty
expect(page.locator('.loader')).to_be_hidden()

# Element disabled/enabled
expect(page.locator('button')).to_be_disabled()
expect(page.locator('button')).to_be_enabled()

# URL
expect(page).to_have_url('https://example.com/home')

# Title
expect(page).to_have_title('Home Page')

# Count elementów
expect(page.locator('.product-card')).to_have_count(5)

# Checked/unchecked
expect(page.locator('input[type="checkbox"]')).to_be_checked()
```

---

## Praktyczne Przykłady

### 1. Login Test

```python
def test_user_login(page):
    # Przejdź na login
    page.goto("https://app.example.com/login")
    
    # Wpisz dane
    page.fill('input[name="email"]', 'user@test.com')
    page.fill('input[name="password"]', 'password123')
    
    # Kliknij login
    page.click('button[type="submit"]')
    
    # Sprawdzenie - URL się zmienił
    page.wait_for_url('**/dashboard')
    
    # Sprawdzenie - widoczny element
    expect(page.locator('.user-menu')).to_be_visible()
```

### 2. E2E Checkout

```python
def test_complete_purchase(page):
    # Login
    page.goto("https://shop.com")
    page.click('text=Login')
    page.fill('input[name="email"]', 'user@test.com')
    page.fill('input[name="password"]', 'pass123')
    page.click('button:has-text("Sign In")')
    page.wait_for_url('**/products')
    
    # Szukaj produktu
    page.fill('input[placeholder="Search..."]', 'Laptop')
    page.click('.product-card >> text=Laptop')
    
    # Dodaj do koszyka
    page.click('button:has-text("Add to Cart")')
    expect(page.locator('text=Added to cart')).to_be_visible()
    
    # Przejdź do koszyka
    page.click('a[href="/cart"]')
    expect(page.locator('.cart-item')).to_have_count(1)
    
    # Checkout
    page.click('button:has-text("Proceed to Checkout")')
    
    # Adres
    page.fill('input[name="address"]', '123 Main St')
    page.select_option('select[name="country"]', 'US')
    
    # Płatność
    page.fill('input[name="card_number"]', '4111111111111111')
    page.fill('input[name="expiry"]', '12/25')
    page.fill('input[name="cvv"]', '123')
    
    # Potwierdź
    page.click('button[type="submit"]')
    
    # Sprawdzenie
    page.wait_for_url('**/order-confirmation')
    expect(page.locator('.order-number')).to_contain_text('ORD-')
```

### 3. Form Validation

```python
def test_form_validation(page):
    page.goto("https://example.com/register")
    
    # Spróbuj wysłać pusty formularz
    page.click('button[type="submit"]')
    
    # Sprawdź error messages
    expect(page.locator('.error-email')).to_contain_text('Email is required')
    expect(page.locator('.error-password')).to_contain_text('Password is required')
    
    # Wpisz email
    page.fill('input[name="email"]', 'invalid-email')
    page.click('button[type="submit"]')
    
    # Sprawdź że email jest zły
    expect(page.locator('.error-email')).to_contain_text('Invalid email')
    
    # Wpisz prawidłowe dane
    page.fill('input[name="email"]', 'valid@test.com')
    page.fill('input[name="password"]', 'SecurePass123!')
    page.fill('input[name="confirm_password"]', 'SecurePass123!')
    page.check('input[name="terms"]')
    
    # Wyślij
    page.click('button[type="submit"]')
    
    # Sprawdzenie sukcesu
    page.wait_for_url('**/success')
    expect(page.locator('text=Registration successful')).to_be_visible()
```

### 4. API Mocking

```python
def test_with_mocked_api(page):
    # Mock API - zwróć fake dane
    def handle_products(route):
        route.fulfill(
            status=200,
            json=[
                {"id": 1, "name": "Laptop", "price": 1000},
                {"id": 2, "name": "Mouse", "price": 50}
            ]
        )
    
    page.route('**/api/products', handle_products)
    
    # Teraz API zawsze zwróci nasze fake dane
    page.goto("https://shop.com/products")
    
    # Sprawdzenie że produkty się załadowały
    expect(page.locator('text=Laptop')).to_be_visible()
    expect(page.locator('text=Mouse')).to_be_visible()
```

### 5. Screenshots & Videos

```python
def test_with_screenshot(page):
    page.goto("https://example.com")
    
    # Zrób screenshot
    page.screenshot(path="screenshot.png")
    
    # Screenshot konkretnego elementu
    page.locator('.hero').screenshot(path="hero.png")

def test_with_video(page):
    # Video se nagrywał automatycznie (konfiguracja)
    page.goto("https://example.com")
    page.click('button')
    
    # Video będzie w artifacts/
```

---

## Fixtures - Wielokrotne Użycie

```python
import pytest
from playwright.sync_api import sync_playwright, expect

@pytest.fixture
def page():
    """Nowa przeglądarka na każdy test"""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        yield page
        browser.close()

@pytest.fixture
def logged_in_page(page):
    """Już zalogowana przeglądarka"""
    page.goto("https://app.example.com/login")
    page.fill('input[name="email"]', 'test@test.com')
    page.fill('input[name="password"]', 'password123')
    page.click('button[type="submit"]')
    page.wait_for_url('**/dashboard')
    yield page

# Użycie
def test_dashboard_with_logged_in_user(logged_in_page):
    expect(logged_in_page.locator('.dashboard')).to_be_visible()
```

---

## Parametryzacja Testów

```python
import pytest

@pytest.mark.parametrize("email,password,should_login", [
    ("valid@test.com", "ValidPass123!", True),
    ("invalid@test.com", "WrongPass", False),
    ("", "password123", False),
    ("user@test.com", "", False),
])
def test_login_various_cases(page, email, password, should_login):
    page.goto("https://example.com/login")
    page.fill('input[name="email"]', email)
    page.fill('input[name="password"]', password)
    page.click('button[type="submit"]')
    
    if should_login:
        page.wait_for_url('**/dashboard')
        expect(page).to_have_url('**/dashboard')
    else:
        expect(page.locator('.error-message')).to_be_visible()
```

---

## Configuration - pytest.ini

```ini
[pytest]
# Timeout dla każdego testu
timeout = 30

# Verbose output
addopts = -v --tb=short

# Markers
markers =
    slow: slow tests
    e2e: end-to-end tests
    smoke: smoke tests
```

---

## Uruchomienie Testów

```bash
# Wszystkie testy
pytest

# Z przeglądarką widoczną (headed)
pytest --headed

# Konkretny plik
pytest test_login.py

# Konkretny test
pytest test_login.py::test_user_login

# Z verbose outputem
pytest -v

# Pause na failure (debug)
pytest --pdb

# Kilka workerów (parallel)
pytest -n 4

# Pokaż printy
pytest -s

# Zaznaczony marker
pytest -m e2e
```

---

## Markers - Organizacja Testów

```python
import pytest

@pytest.mark.slow
def test_long_running_flow(page):
    # Ten test zajmuje dużo czasu
    pass

@pytest.mark.e2e
def test_full_checkout(page):
    # E2E test
    pass

@pytest.mark.smoke
def test_homepage_loads(page):
    # Smoke test
    pass

# Uruchomienie
# pytest -m e2e         # Tylko E2E testy
# pytest -m "not slow"  # Wszystko poza wolnymi
```

---

## Debugging

```python
def test_debug(page):
    page.goto("https://example.com")
    
    # Pauza - otworzy debugger
    page.pause()
    
    # Debuguj elementu
    print(page.locator('h1').text_content())
    
    # Sprawdzenie jeśli element istnieje
    try:
        page.click('button', timeout=1000)
    except Exception as e:
        print(f"Element not found: {e}")
    
    # Pobierz wszytskie elementu
    buttons = page.locator('button').all()
    for btn in buttons:
        print(btn.text_content())
```

**Uruchomienie z debuggerem:**
```bash
pytest --pdb
```

---

## Best Practices

✅ **DO's:**
```python
# Używaj data-testid
page.click('[data-testid="submit"]')

# Czekaj na elementy
page.wait_for_selector('.modal')

# Mockuj API
page.route('**/api/**', lambda r: r.abort())

# Isoluj testy
@pytest.fixture
def clean_page(page):
    # Setup na każdy test
    yield page
    # Cleanup

# Parametryzuj
@pytest.mark.parametrize("input,expected", [...])
```

❌ **DON'Ts:**
```python
# Nie czekaj sztywnie
time.sleep(5)  # ŹLE!

# Nie używaj hardcoded timeouts
page.click('button', timeout=10000)  # Złe

# Nie testuuj implementacji
page.click('.internal-class')  # Zła klasa

# Nie tworz zależności między testami
def test_a():
    # Setup
    pass

def test_b():
    # Polega na test_a - ŹLE!
    pass
```

---

## Struktura Projektu

```
project/
├── tests/
│   ├── conftest.py              # Fixtures
│   ├── test_auth.py             # Testy logowania
│   ├── test_shopping.py         # Testy koszyka
│   ├── test_payments.py         # Testy płatności
│   └── fixtures/
│       ├── users.json           # Test data
│       └── products.json
└── pytest.ini                   # Konfiguracja
```

---

## Podsumowanie

**Playwright:**
- ✅ Nowoczesne, szybkie, niezawodne
- ✅ Automatyzuje 3 przeglądarki
- ✅ Wbudowane czekanie (nie sleep)
- ✅ Mockowanie network'u
- ✅ Screenshots, videos, traces

**Workflow:**
1. `pip install pytest-playwright`
2. `playwright install`
3. Napisz test
4. `pytest --headed` (z przeglądarką)
5. Debug jeśli trzeba
6. Uruchom w CI/CD

**Quick Reference:**

```python
# Nawigacja
page.goto(url)
page.wait_for_url(pattern)

# Znalezienie
page.click(selector)
page.fill(selector, text)
page.select_option(selector, value)

# Czekanie
page.wait_for_selector(selector)
page.wait_for_response(lambda r: ...)

# Asercje
expect(page.locator(selector)).to_be_visible()
expect(page.locator(selector)).to_contain_text(text)

# Debugging
page.pause()
page.screenshot()
```

**Happy Testing! 🎭✅**
