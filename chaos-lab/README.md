# 🎯 Chaos Engineering Lab - Docker Compose

Laboratorium do nauki **Chaos Engineering** na przykładzie aplikacji Node.js z wieloma zależnościami. Testuj odporność systemu poprzez celowe wyłączanie komponentów i obserwuj, jak aplikacja się zachowuje.

## 📋 Spis treści

- [Wymagania](#-wymagania)
- [Struktura Projektu](#-struktura-projektu)
- [Szybki Start](#-szybki-start)
- [Komponenty Systemu](#-komponenty-systemu)
- [Scenariusze Chaos Engineering](#-scenariusze-chaos-engineering)
- [Monitoring i Metryki](#-monitoring-i-metryki)
- [Endpointy API](#-endpointy-api)
- [Troubleshooting](#-troubleshooting)
- [Lekcje i Best Practices](#-lekcje-i-best-practices)

---

### Czym się zajmujemy w tym labie?

- ✅ Testujemy aplikację **bez bazy danych**
- ✅ Obserwujemy **fallback'i** (cache zamiast bazy)
- ✅ Wyłączamy **message queue** i patrzymy na izolację błędów
- ✅ Dodajemy **opóźnienie sieciowe** i mierzymy timeout'y
- ✅ Monitorujemy metryki **Prometheus**
- ✅ Radzimy sobie z **graceful degradation**

### Architektura

```
┌─────────────────────────────────────────────────┐
│         Docker Compose Network                   │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐    │
│  │   App    │──→│ Postgres │   │  Redis   │    │
│  │ :3000   │   │ :5432   │   │ :6379   │    │
│  └──────────┘   └──────────┘   └──────────┘    │
│        ↓                                         │
│  ┌──────────────┐        ┌──────────────┐     │
│  │  RabbitMQ    │        │ Prometheus   │     │
│  │  :5672       │        │  :9090       │     │
│  └──────────────┘        └──────────────┘     │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## 🔧 Wymagania

- **Docker** v20.10+ ([instalacja](https://docs.docker.com/get-docker/))
- **Docker Compose** v1.29+ ([instalacja](https://docs.docker.com/compose/install/))
- **Bash** (na Linux/macOS) lub PowerShell (na Windows)
- **curl** (do testowania API)
- **jq** (opcjonalnie, do parsowania JSON)

### Sprawdzenie wersji

```bash
docker --version
docker-compose --version
curl --version
```

---

## 📁 Struktura Projektu

```
chaos-lab/
├── docker-compose.yml          # Konfiguracja wszystkich serwisów
├── prometheus.yml              # Konfiguracja Prometheus
├── init-db.sql                 # Inicjalizacja bazy danych
├── README.md                   # Ten plik
│
├── app/                        # Aplikacja Node.js
│   ├── package.json           # Zależności npm
│   ├── server.js              # Główna aplikacja
│   ├── healthcheck.js         # Health check endpoint
│   └── Dockerfile             # Konteneryzacja aplikacji
│
└── scripts/                    # Skrypty do chaos engineering
    ├── test-app.sh            # Test podstawowej funkcjonalności
    ├── chaos-db-down.sh       # Wyłączenie bazy danych
    ├── chaos-redis-down.sh    # Wyłączenie cache'u
    ├── chaos-rabbitmq-down.sh # Wyłączenie message queue
    ├── chaos-network-delay.sh # Dodanie opóźnienia sieciowego
    └── monitor.sh             # Monitoring w czasie rzeczywistym
```

---

## 🚀 Szybki Start

### 1. Klonowanie/Pobieranie projektu

```bash
git clone <repo>
cd chaos-lab
```

### 2. Przygotowanie skryptów

```bash
# Linux/macOS
chmod +x scripts/*.sh

# Windows (PowerShell)
# Pomiń ten krok, skrypty będą uruchamiane poprzez bash scripts/nazwa.sh
```

### 3. Uruchomienie całego stack'u

```bash
docker-compose up -d
```

### 4. Sprawdzenie statusu

```bash
docker-compose ps
```

Powinniśmy zobaczyć:
```
NAME               STATUS
chaos-app          Up (healthy)
chaos-postgres     Up (healthy)
chaos-redis        Up (healthy)
chaos-rabbitmq     Up (healthy)
chaos-prometheus   Up
```

### 5. Test podstawowej funkcjonalności

```bash
./scripts/test-app.sh
```

### 6. Monitoring w rzeczywistym czasie

W **nowym oknie terminalu**:

```bash
./scripts/monitor.sh
```

---

## 🏗️ Komponenty Systemu

### 1. Aplikacja (Node.js + Express)

**Port:** `3000`

Aplikacja demonstruje:
- Połączenia do bazy danych (PostgreSQL)
- Cache (Redis)
- Message queue (RabbitMQ)
- Health check'i
- Metryki (Prometheus)

**Plik:** `app/server.js`

### 2. PostgreSQL

**Port:** `5432`
**Użytkownik:** `user`
**Hasło:** `password`
**Baza:** `testdb`

Zawiera tabelę `users` z przykładowymi danymi.

```bash
# Dostęp do bazy
docker-compose exec postgres psql -U user -d testdb

# W psql
\dt                 # Lista tabel
SELECT * FROM users; # Wyświetl dane
```

### 3. Redis

**Port:** `6379`

Cache dla danych użytkowników. TTL: 60 sekund.

```bash
# Dostęp do Redis
docker-compose exec redis redis-cli

# W redis-cli
KEYS *                    # Lista kluczy
GET users:all            # Wyświetl cache
MONITOR                  # Monitor operacji
```

### 4. RabbitMQ

**Port:** `5672` (AMQP)
**Port:** `15672` (Management UI)
**URL:** http://localhost:15672
**User:** `guest`
**Password:** `guest`

Message queue dla zadań asynchronicznych.

### 5. Prometheus

**Port:** `9090`
**URL:** http://localhost:9090

Zbiera metryki z aplikacji:
- HTTP request duration
- Database query duration
- Cache hits/misses
- Service health status

---

## 💣 Scenariusze Chaos Engineering

### Eksperyment 1: Baza danych wyłączona

**Co testujemy:** Czy aplikacja może funkcjonować bez bazy danych?

```bash
./scripts/chaos-db-down.sh
```

**Obserwacja:**

Uruchom w innym oknie:
```bash
# Health check
curl http://localhost:3000/health | jq '.'

# Dostęp do bazy (❌ powinien zwrócić błąd)
curl http://localhost:3000/users/db | jq '.'

# Cache (✅ powinien działać)
curl http://localhost:3000/users/cached | jq '.'
```

**Oczekiwane wyniki:**

```json
{
  "status": "ok",
  "services": {
    "postgres": 0,
    "redis": 1,
    "rabbitmq": 1
  }
}
```

**Lekcje:**
- ✅ Cache ratuje przed awarią bazy danych
- ✅ Aplikacja nie pada, tylko degraduje się
- ✅ Wymagane fallback'i i timeout'y

---

### Eksperyment 2: Redis wyłączony

**Co testujemy:** Czy aplikacja działa bez cache'u?

```bash
./scripts/chaos-redis-down.sh
```

**Obserwacja:**

```bash
# Cache bez Redis (fallback na bazę)
curl http://localhost:3000/users/cached | jq '.'

# Metryki - zwróć uwagę na cache_misses_total
curl http://localhost:3000/metrics | grep cache
```

**Oczekiwane wyniki:**

```
# HELP cache_misses_total Total cache misses
# TYPE cache_misses_total counter
cache_misses_total{key="users:all"} 5

# HELP cache_hits_total Total cache hits
# TYPE cache_hits_total counter
cache_hits_total{key="users:all"} 0
```

**Lekcje:**
- ✅ Bez cache'u aplikacja działa, ale wolniej
- ✅ Wszystkie żądania idą do bazy danych
- ✅ Metryki pokazują degradację

---

### Eksperyment 3: RabbitMQ wyłączony

**Co testujemy:** Czy brak message queue wyłącza całą aplikację?

```bash
./scripts/chaos-rabbitmq-down.sh
```

**Obserwacja:**

```bash
# Queue niedostępna (❌)
curl -X POST http://localhost:3000/jobs | jq '.'

# Ale pozostałe usługi pracują (✅)
curl http://localhost:3000/users/db | jq '.'
curl http://localhost:3000/users/cached | jq '.'
```

**Oczekiwane wyniki:**

```json
{
  "error": "RabbitMQ unavailable",
  "message": "..."
}
```

**Lekcje:**
- ✅ **Izolacja błędów** - awaria queue'u nie wyłącza całej aplikacji
- ✅ Pozostałe endpointy pracują normalnie
- ✅ Graceful degradation zamiast całkowitego krachu

---

### Eksperyment 4: Opóźnienie sieciowe (Network Chaos)

**Co testujemy:** Jak aplikacja radzi sobie z high latency?

```bash
# 500ms opóźnienia
./scripts/chaos-network-delay.sh 500
```

**Obserwacja:**

```bash
# Zmierz czas odpowiedzi
time curl http://localhost:3000/health

# Lub z curl
curl -w "Response time: %{time_total}s\n" http://localhost:3000/health

# Sprawdź metryki
curl http://localhost:3000/metrics | grep http_request_duration
```

**Oczekiwane wyniki:**

Czasy odpowiedzi znacznie się wydłużają (~500ms dodatkowe).

**Lekcje:**
- ⚠️ Network latency to główna przyczyna timeout'ów
- ⚠️ Timeout'y muszą być wyższe niż oczekiwane latency
- ✅ Circuit breaker pattern chroni przed cascading failures

---

### Eksperyment 5: Kombinacja - Totalna Katastrofa

**Co testujemy:** Granice systemu - co się dzieje gdy wszystko pada?

```bash
# Wyłącz wszystkie zależności
docker-compose stop postgres redis rabbitmq

# Testuj
curl http://localhost:3000/health | jq '.'
curl http://localhost:3000/users/db
curl http://localhost:3000/users/cached
curl -X POST http://localhost:3000/jobs
```

**Oczekiwane wyniki:**

```json
{
  "status": "ok",
  "services": {
    "postgres": 0,
    "redis": 0,
    "rabbitmq": 0
  }
}
```

- ❌ Wszystkie endpointy zwracają 503 Service Unavailable
- ✅ Aplikacja jest nadal żywa (health check zwraca 503)
- ✅ Load balancer może ją usunąć z puli

**Lekcja:**

Zawsze pamiętaj o health check'u, aby orkestrator (Kubernetes) mógł podjąć działania:
- Restart kontenera
- Usunięcie z load balancera
- Paging do DevOps'ów

---

## 📊 Monitoring i Metryki

### 1. Health Check Endpoint

```bash
curl http://localhost:3000/health | jq '.'
```

Zwraca status każdego komponentu:

```json
{
  "status": "ok",
  "timestamp": "2024-03-17T12:34:56.789Z",
  "services": {
    "postgres": 1,
    "redis": 1,
    "rabbitmq": 1
  }
}
```

### 2. Prometheus Metryki

Dostęp: http://localhost:9090

**Ważne metryki:**

```
# HTTP request duration
http_request_duration_ms_bucket{method="GET",route="/users/db",le="100"}

# Database query duration
db_query_duration_ms_bucket{query="SELECT users",le="50"}

# Cache statistics
cache_hits_total{key="users:all"}
cache_misses_total{key="users:all"}

# Service health
service_health{service="postgres"}
service_health{service="redis"}
service_health{service="rabbitmq"}
```

### 3. Monitoring w Czasie Rzeczywistym

```bash
./scripts/monitor.sh
```

Wyświetla:
- Status zdrowotności serwisów
- Użycie CPU i RAM
- Liczniki metryk

---

## 📡 Endpointy API

### GET `/`

Informacje o dostępnych endpunktach.

```bash
curl http://localhost:3000
```

### GET `/health`

Status zdrowotności aplikacji i jej zależności.

```bash
curl http://localhost:3000/health | jq '.'
```

**Kody odpowiedzi:**
- `200` - Wszystko OK
- `503` - Co najmniej jedna zależność niedostępna

---

### GET `/users/db`

Pobierz użytkowników **bezpośrednio z bazy danych**.

```bash
curl http://localhost:3000/users/db | jq '.'
```

**Odpowiedź:**

```json
{
  "source": "database",
  "data": [
    {
      "id": 1,
      "name": "Alice Johnson",
      "email": "alice@example.com",
      "created_at": "2024-03-17T12:34:56.000Z"
    }
  ]
}
```

**Obserwacja:**
- Brak cache'u
- Za każdym razem pytanie do bazy
- Wolniejsze jeśli baza jest wolna

---

### GET `/users/cached`

Pobierz użytkowników z **cache'u (Redis)** lub fallback na **bazę**.

```bash
curl http://localhost:3000/users/cached | jq '.'
```

**Logika:**
1. Spróbuj pobrać z Redis (szybkie)
2. Cache miss → pobierz z bazy
3. Zapisz w Redis na 60 sekund
4. Następne żądanie → z cache'u

**Obserwacja:**

```bash
# Pierwsze żądanie - cache miss
curl http://localhost:3000/users/cached

# Drugie żądanie - cache hit (szybsze)
curl http://localhost:3000/users/cached
```

---

### POST `/jobs`

Wyślij zadanie do **message queue** (RabbitMQ).

```bash
curl -X POST http://localhost:3000/jobs | jq '.'
```

**Odpowiedź:**

```json
{
  "message": "Job queued",
  "jobId": 1710678896000
}
```

**Test bez RabbitMQ:**

```bash
docker-compose stop rabbitmq
curl -X POST http://localhost:3000/jobs
# ❌ Błąd: RabbitMQ unavailable
```

---

### GET `/metrics`

Metryki w formacie Prometheus.

```bash
curl http://localhost:3000/metrics
```

Zawiera:
- Czas trwania HTTP requestów
- Czas trwania query do bazy
- Cache hits/misses
- Status zdrowotności serwisów

---

## 🔍 Troubleshooting

### Problem: Kontenery nie startują

**Symptom:** `docker-compose up` zawiesza się lub zwraca błędy

```bash
# Sprawdź logi
docker-compose logs

# Sprawdź konkretny kontener
docker-compose logs app
docker-compose logs postgres
```

**Rozwiązanie:**

```bash
# Wyczyść wszystko
docker-compose down -v

# Uruchom ponownie z fresh volumen'em
docker-compose up -d
```

---

### Problem: Aplikacja nie łączy się z bazą

**Symptom:** Health check pokazuje `postgres: 0`

```bash
# Sprawdź, czy postgres jest healthy
docker-compose ps postgres

# Sprawdź logi PostgreSQL
docker-compose logs postgres

# Testuj bezpośrednio
docker-compose exec postgres psql -U user -d testdb -c "SELECT 1"
```

**Rozwiązanie:**

Czekaj na startup bazy (do 30 sekund):

```bash
# Manualna inicjalizacja
docker-compose exec postgres psql -U user -d testdb < init-db.sql
```

---

### Problem: Health check zwraca timeout

**Symptom:** `curl: (7) Failed to connect to localhost port 3000`

```bash
# Sprawdź, czy aplikacja jest uruchomiona
docker-compose ps app

# Sprawdź logi aplikacji
docker-compose logs app
```

**Rozwiązanie:**

```bash
# Czekaj na startup (zwykle 10-20 sekund)
docker-compose up -d
sleep 30

# Testuj
curl http://localhost:3000/health
```

---

### Problem: Skrypty chaos nie działają

**Symptom:** Permission denied

```bash
# Przyznaj uprawnienia
chmod +x scripts/*.sh

# Lub uruchom bezpośrednio
bash scripts/chaos-db-down.sh
```

---

### Problem: Port 3000 już zajęty

**Symptom:** `Error starting userland proxy: listen tcp 0.0.0.0:3000`

```bash
# Sprawdź co zajmuje port
lsof -i :3000

# Lub zmień port w docker-compose.yml
# ports:
#   - "8000:3000"  # Zmień 3000 na 8000
```

---

### Problem: Redis/RabbitMQ zwisają

**Symptom:** Health check nigdy nie wraca do statusu healthy

```bash
# Restart kontenera
docker-compose restart redis
docker-compose restart rabbitmq

# Lub
docker-compose down
docker-compose up -d
```

---

## 📚 Lekcje i Best Practices

### 1. **Zawsze dodaj health check'i**

✅ **DOBRZE:**
```yaml
healthcheck:
  test: ["CMD", "pg_isready", "-U", "postgres"]
  interval: 5s
  timeout: 3s
  retries: 5
```

❌ **ŹLE:**
```yaml
# Brak health check'u
# Aplikacja nie wie kiedy baza jest gotowa
```

---

### 2. **Implementuj fallback'i**

✅ **DOBRZE:**
```javascript
// Spróbuj cache
const cached = await redis.get(key);
if (cached) return cached;

// Fallback na bazę
const data = await db.query(sql);
redis.set(key, data, 60);
return data;
```

❌ **ŹLE:**
```javascript
// Tylko cache - brak fallback'u
const data = await redis.get(key);
return data;  // null jeśli cache'u brak
```

---

### 3. **Izoluj błędy**

✅ **DOBRZE:**
```javascript
try {
  await rabbitmq.sendToQueue(job);
  res.json({ ok: true });
} catch (err) {
  // Wyślij błąd, ale nie rzuć wyjątku
  res.status(503).json({ error: 'Queue unavailable' });
}
```

❌ **ŹLE:**
```javascript
// Błąd w queue wyłącza całą aplikację
await rabbitmq.sendToQueue(job);
```

---

### 4. **Ustaw rozsądne timeout'y**

✅ **DOBRZE:**
```javascript
const pool = new Pool({
  connectionTimeoutMillis: 2000,  // 2 sekundy
  idleTimeoutMillis: 30000,
  max: 20
});
```

❌ **ŹLE:**
```javascript
// Brak timeout'u - czeka nieskończenie
const result = await query();
```

---

### 5. **Mierz wszystko**

✅ **DOBRZE:**
```javascript
const requestDuration = new Histogram({
  name: 'http_request_duration_ms',
  buckets: [0.1, 5, 15, 50, 100, 500]
});
```

❌ **ŹLE:**
```javascript
// Bez metryk - nie wiesz co się dzieje
```

---

### 6. **Graceful degradation zamiast crash'u**

✅ **DOBRZE:**
```
Baza wyłączona
└─ Użyj cache'u
   └─ Zwróć pobór dane z ostatniego znanych
      └─ Zwróć 503 Service Unavailable
```

❌ **ŹLE:**
```
Baza wyłączona
└─ Aplikacja pada
└─ Load balancer nie wie, że kontenery martwały
└─ Użytkownicy widzą 500 Internal Server Error
```

---

### 7. **Circuit Breaker Pattern**

Koncepcja do implementacji w kolejnym labie:

```javascript
// Jeśli baza ma 3 consecutive błędy
if (failureCount > 3) {
  // Zamknij circuit - nie pytaj bazę
  return 503;  // Service Unavailable
}

// Po 30 sekundach - spróbuj ponownie
if (Date.now() - lastFailure > 30000) {
  failureCount = 0;  // Reset
}
```

---

### 8. **Dokumentuj SLA**

```markdown
## Service Level Agreements

### /users/db
- Availability: 99% (gdy postgres dostępna)
- Latency: p99 < 100ms
- Dependency: PostgreSQL

### /users/cached
- Availability: 99.9% (fallback na bazę)
- Latency: p99 < 50ms (z cache'u), < 100ms (z bazy)
- Dependencies: Redis, PostgreSQL (fallback)

### /jobs
- Availability: 99% (gdy RabbitMQ dostępna)
- Latency: p99 < 50ms
- Dependency: RabbitMQ
```

---

### 9. **Testuj chaos w CI/CD**

Dodaj do GitHub Actions:

```yaml
jobs:
  chaos-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: docker-compose up -d
      - run: sleep 30  # Czekaj na startup
      
      # Test bez bazy
      - run: |
          docker-compose stop postgres
          curl http://localhost:3000/users/cached
          docker-compose start postgres
      
      # Test bez cache'u
      - run: |
          docker-compose stop redis
          curl http://localhost:3000/users/cached
          docker-compose start redis
```

---

### 10. **Monitoring vs Observability**

| Monitoring | Observability |
|------------|---------------|
| Metryki (CPU, RAM) | Traces (gdzie czas się spędza) |
| Alerty (alert jeśli CPU > 80%) | Logs (szczegółowe zdarzenia) |
| Dashboard (co widzę teraz) | Root cause (co się stało) |

**Ten lab fokusuje się na monitoringu.** Observability to kolejny temat.

---

## 🎓 Dalsze Nauki

Po opanowaniu tego labu:

1. **Kubernetes & Chaos Engineering**
   - Litmus Chaos
   - Gremlin
   - kubelet pod disruption budgets

2. **Advanced Patterns**
   - Circuit Breaker
   - Bulkhead Isolation
   - Retry with exponential backoff

3. **Load Testing**
   - Apache JMeter
   - Locust
   - Gatling

4. **Observability**
   - Distributed Tracing (Jaeger, Zipkin)
   - Centralized Logging (ELK, Loki)
   - Advanced Metrics (Grafana)

---

## 📞 Pomoc i Pytania

### Czy coś nie działa?

1. Sprawdź status: `docker-compose ps`
2. Sprawdź logi: `docker-compose logs app`
3. Testuj health: `curl http://localhost:3000/health`
4. Wyczyść: `docker-compose down -v && docker-compose up -d`

### Gdzie znaleźć więcej informacji?

- 🔗 [Chaos Engineering - Wikipedia](https://en.wikipedia.org/wiki/Chaos_engineering)
- 🔗 [Principles of Chaos Engineering](https://principlesofchaos.org/)
- 🔗 [Docker Compose Documentation](https://docs.docker.com/compose/)
- 🔗 [Prometheus Metrics](https://prometheus.io/docs/)

---

## 📝 Licencja

MIT License - użyj do celów edukacyjnych i komercyjnych.

---

## ✍️ Autor

Przygotowane dla **Politechniki Gdańskiej** - Postgraduate Studies.

Ideal dla:
- 🎓 Studiów DevOps
- 🎓 Cloud Engineering
- 🎓 Site Reliability Engineering (SRE)
- 🎓 Praktyk w bankach i dużych organizacjach (Santander, Nordea, itp.)

---

## 🙌 Dziękuję!

Mam nadzieję, że ten lab pomógł Ci zrozumieć **Chaos Engineering** w praktyce.

**Pytania?** Sprawdzaj logi, monitoruj metryki, eksperymentuj!

```
┌──────────────────────────────┐
│  "With great power comes     │
│   great responsibility..."   │
│                              │
│   - Ben Parker               │
│   (aka: Chaos Engineer)      │
└──────────────────────────────┘
```

🎯 **Happy Chaos Engineering!**