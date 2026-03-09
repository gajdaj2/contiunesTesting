# GitHub Actions dla Testerów - Szybki Kurs

## Co to GitHub Actions?

GitHub Actions to wbudowany w GitHub system do automatyzacji - uruchamia testy, deployuje kod, buduje projekty **automatycznie** po każdym `git push`.

**Bez Actions (manual):**
```
Dev pisze kod → git push → Dev czeka → Uruchamia testy ręcznie → Sprawdza wyniki
```

**Z Actions (automatyczne):**
```
Dev pisze kod → git push → GitHub automatycznie uruchamia testy → Dev widzi wynik
```

---

## Kluczowe Pojęcia

| Termin | Wyjaśnienie |
|--------|------------|
| **Workflow** | Plan co zrobić (np. "uruchom testy") |
| **Job** | Część workflow'u (np. "uruchom unit testy") |
| **Step** | Konkretna komenda (np. `npm test`) |
| **Action** | Gotowy blok kodu (np. `actions/checkout@v3`) |
| **Trigger** | Co aktywuje workflow (np. `push` lub `pull_request`) |

---

## Struktura Pliku Workflow

```yaml
name: Moja Automatyzacja                    # Nazwa workflow'u

on:                                         # Kiedy uruchomić?
  push:                                     # Na każdy push
    branches: [main, develop]
  pull_request:                             # Na każdy pull request
    branches: [main]

jobs:
  test:                                     # Nazwa job'u
    runs-on: ubuntu-latest                  # Gdzie uruchomić
    
    steps:
      - name: Checkout kod                  # Step 1
        uses: actions/checkout@v3           # Użyj gotowej akcji
      
      - name: Setup Node                    # Step 2
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Zainstaluj zależności         # Step 3
        run: npm install                    # Wykonaj komendę
      
      - name: Uruchom testy                 # Step 4
        run: npm test
```

---

## Gdzie Umieścić Workflow?

Wszystkie workflow'i idą do folderu:
```
.github/workflows/
├── test.yml
├── e2e.yml
└── security.yml
```

Przykład:
```
moj-projekt/
├── src/
├── tests/
├── .github/
│   └── workflows/
│       └── tests.yml
├── package.json
└── README.md
```

---

## Prosty Workflow - Testy Node.js

Plik: `.github/workflows/test.yml`

```yaml
name: Testy Node.js

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - run: npm install
      - run: npm test
      - run: npm run lint
```

**Co robi:**
1. Sprawdzić kod z GitHub'a
2. Setup Node.js v18
3. Zainstalować npm packages
4. Uruchomić testy
5. Sprawdzić lint (formatowanie kodu)

---

## Workflow - Testy Python

Plik: `.github/workflows/test-python.yml`

```yaml
name: Testy Python

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']
    
    steps:
      - uses: actions/checkout@v3
      
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      - run: pip install pytest pytest-cov
      - run: pip install -r requirements.txt
      - run: pytest --cov=src
```

**Co robi:**
- Testuje kod na 3 wersjach Pythona (3.9, 3.10, 3.11) **jednocześnie**
- Coverage report (`--cov`)

---

## Workflow - E2E Testy z Cypress

Plik: `.github/workflows/e2e.yml`

```yaml
name: E2E Testy

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  cypress:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - run: npm install
      - run: npm run build
      
      - name: Uruchom testy Cypress
        uses: cypress-io/github-action@v5
        with:
          start: npm run serve
          browser: chrome
          spec: cypress/e2e/**/*.cy.js
```

**Co robi:**
- Build aplikacji
- Startuje serwer
- Uruchamia E2E testy w Chrome'ie

---

## Workflow - Testy z Bazą Danych (PostgreSQL)

Plik: `.github/workflows/test-db.yml`

```yaml
name: Testy z Bazą Danych

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: testpass
          POSTGRES_DB: testdb
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
      - uses: actions/checkout@v3
      
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - run: npm install
      
      - name: Uruchom migrations
        run: npm run migrate
        env:
          DATABASE_URL: postgres://postgres:testpass@localhost:5432/testdb
      
      - run: npm test
        env:
          DATABASE_URL: postgres://postgres:testpass@localhost:5432/testdb
```

**Co robi:**
- Spinuje PostgreSQL w Docker'ze
- Migracje bazy danych
- Testuje integrację z bazą

---

## Praktyczne Porady dla Testerów

### 1. Uruchom Testy na PR (Pull Request)

```yaml
on:
  pull_request:
    branches: [main]
```

**Efekt:** Przed merge'em, GitHub uruchomi testy i pokaże wynik na PR.

### 2. Blocking Strategy

```yaml
on:
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm test
```

**Efekt:** Jeśli test failed → PR nie może być merged (ustawić w Settings).

### 3. Notifications na Slack

```yaml
- name: Notify Slack on Failure
  if: failure()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    text: 'Testy failed! Check: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}'
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### 4. Upload Report'ów

```yaml
- name: Uruchom testy
  run: npm test -- --reporter json > test-results.json

- name: Upload test report
  uses: actions/upload-artifact@v3
  if: always()
  with:
    name: test-results
    path: test-results.json
```

**Efekt:** Report dostępny do pobrania w UI GitHub'a.

### 5. Warunkowe Kroki (if conditions)

```yaml
- name: Uruchom tylko na main branch
  if: github.ref == 'refs/heads/main'
  run: npm run deploy

- name: Notify on failure
  if: failure()
  run: echo "Coś poszło nie tak!"

- name: Notify on success
  if: success()
  run: echo "Wszystko OK!"
```

---

## Zmienne Dostępne w Workflow

```yaml
steps:
  - run: echo "Branch: ${{ github.ref }}"           # refs/heads/main
  - run: echo "Event: ${{ github.event_name }}"     # push, pull_request
  - run: echo "Autor: ${{ github.actor }}"          # username
  - run: echo "Commit: ${{ github.sha }}"           # commit hash
  - run: echo "Run ID: ${{ github.run_id }}"        # ID workflow'u
```

---

## Secrets - Dane Wrażliwe

Nie umieszczaj hasła/API keys w workflow!

**1. Dodaj Secret w GitHub:**
Settings → Secrets and variables → New repository secret
```
Nazwa: DATABASE_PASSWORD
Wartość: super_tajne_haslo
```

**2. Użyj w Workflow:**
```yaml
env:
  DB_PASSWORD: ${{ secrets.DATABASE_PASSWORD }}
```

---

## Praktyczny Przykład - Full Testing Workflow

Plik: `.github/workflows/full-test.yml`

```yaml
name: Full Testing Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    name: Run Tests
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
          POSTGRES_DB: testdb
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
      # 1. Checkout
      - uses: actions/checkout@v3
      
      # 2. Setup
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      # 3. Install
      - run: npm install
      
      # 4. Lint
      - name: Lint Check
        run: npm run lint
      
      # 5. Unit Tests
      - name: Unit Tests
        run: npm run test:unit -- --coverage
      
      # 6. Integration Tests
      - name: Integration Tests
        run: npm run test:integration
        env:
          DATABASE_URL: postgres://postgres:test@localhost:5432/testdb
      
      # 7. E2E Tests
      - name: E2E Tests
        run: npm run test:e2e
      
      # 8. Coverage Report
      - name: Upload Coverage
        uses: codecov/codecov-action@v3
        if: always()
        with:
          files: ./coverage/coverage-final.json
      
      # 9. Notify Slack
      - name: Notify Slack
        if: always()
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

---

## Jak Debugować Workflow

1. **Sprawdź Actions tab w GitHub:**
   - Naciśnij kod → Actions tab
   - Wybierz workflow run
   - Sprawdź logs każdego step'u

2. **Lokalnie uruchom testy zanim push'niesz:**
   ```bash
   npm test
   npm run lint
   ```

3. **Dodaj debug logs:**
   ```yaml
   - run: echo "Debug: ${{ github.event }}"
   - run: ls -la
   - run: pwd
   ```

---

## Best Practices dla Testerów

✅ **Rób:**
- Testuj na każdy `push` i `pull_request`
- Zablokuj PR jeśli testy failed
- Upload test reports
- Notifikuj zespół na Slack
- Używaj secrets dla danych wrażliwych
- Cache dependencies (szybsze workflow'i)

❌ **Nie rób:**
- Nie umieszczaj haseł w YAML
- Nie ignoruj failed testów
- Nie robić 30-minutowych testów (timeout)
- Nie run'uj 100 testów seryjnie (paralelizuj!)

---

## Parallelizacja Testów

```yaml
strategy:
  matrix:
    test-suite: [unit, integration, e2e]

steps:
  - run: npm run test:${{ matrix.test-suite }}
```

**Efekt:** 3 job'y uruchamiają się **jednocześnie**, nie sekwencyjnie.

---

## Timing - Kiedy Uruchomić Testy

```yaml
# Po każdym push'u i PR
on: [push, pull_request]

# Tylko na main branch
on:
  push:
    branches: [main]

# Schedules - co dzień o 2 AM
on:
  schedule:
    - cron: '0 2 * * *'

# Manual trigger (workflow_dispatch)
on:
  push:
  workflow_dispatch:
```

---

## Caching dla Szybszych Workflow'ów

```yaml
- uses: actions/cache@v3
  with:
    path: node_modules
    key: ${{ runner.os }}-npm-${{ hashFiles('package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-npm-

- run: npm install  # Jeśli cache miss, zainstaluj
```

**Efekt:** Pierwszy run → 30s (install), kolejne → 5s (cache hit).

---

## Troubleshooting - Częste Błędy

| Problem | Rozwiązanie |
|---------|------------|
| `npm: command not found` | Dodaj `actions/setup-node@v3` |
| `Database connection refused` | Czekaj aż `health-check` przejdzie |
| `Permission denied: ./run.sh` | `chmod +x run.sh` zanim `git push` |
| `Timeout after 360 minutes` | Testy za długo trwają, paralelizuj |
| `Secret not accessible` | Sprawdź czy secret istnieje w Settings |

---

## Quick Reference - Copy-Paste Workflow'i

### Node.js + Testy
```yaml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm install
      - run: npm test
```

### Python + Pytest
```yaml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install pytest
      - run: pytest
```

### Java + Maven
```yaml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-java@v3
        with:
          java-version: '17'
          distribution: 'temurin'
      - run: mvn test
```

---

## Podsumowanie

**GitHub Actions dla Testerów:**

1. ✅ **Automatyzacja** - testy uruchamiają się bez ręcznej interwencji
2. ✅ **Szybka feedback** - deweloper wie o błędach w sekundy
3. ✅ **Continuous Testing** - shift left - testowanie wcześnie
4. ✅ **Blokowanie PR** - nie merge'ujesz broken code
5. ✅ **Skalowanie** - paralelne job'y na wielu testach

**Krok po kroku:**
1. Stwórz folder `.github/workflows/`
2. Dodaj `test.yml` z workflow'em
3. `git push` i obserwuj Actions tab
4. Skonfiguruj branch protection rules
5. Ciesz się automatycznym testowaniem 🎉

---

## Przydatne Linki

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Starter Workflows](https://github.com/actions/starter-workflows)
- [GitHub Marketplace](https://github.com/marketplace?type=actions)

---

**Happy Testing! 🚀**
