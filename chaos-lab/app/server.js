const express = require('express');
const { Pool } = require('pg');
const redis = require('redis');
const amqp = require('amqplib');
const promClient = require('prom-client');

const app = express();

// ===== METRYKI =====
const httpRequestDuration = new promClient.Histogram({
  name: 'http_request_duration_ms',
  help: 'Duration of HTTP requests in ms',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [0.1, 5, 15, 50, 100, 500]
});

const dbQueryDuration = new promClient.Histogram({
  name: 'db_query_duration_ms',
  help: 'Duration of database queries',
  labelNames: ['query'],
  buckets: [0.1, 5, 15, 50, 100, 500]
});

const cacheHits = new promClient.Counter({
  name: 'cache_hits_total',
  help: 'Total cache hits',
  labelNames: ['key']
});

const cacheMisses = new promClient.Counter({
  name: 'cache_misses_total',
  help: 'Total cache misses',
  labelNames: ['key']
});

const serviceStatus = new promClient.Gauge({
  name: 'service_health',
  help: 'Service health status (1=healthy, 0=unhealthy)',
  labelNames: ['service']
});

// ===== POŁĄCZENIA =====
const pgPool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

let redisClient = null;
let rabbitmqChannel = null;

// ===== INICJALIZACJA =====
async function initializeServices() {
  console.log('🚀 Inicjalizacja usług...\n');

  // PostgreSQL
  try {
    const client = await pgPool.connect();
    await client.query('SELECT NOW()');
    client.release();
    console.log('✅ PostgreSQL: Połączono');
    serviceStatus.set({ service: 'postgres' }, 1);
  } catch (err) {
    console.error('❌ PostgreSQL:', err.message);
    serviceStatus.set({ service: 'postgres' }, 0);
  }

  // Redis
  try {
    redisClient = redis.createClient({
      url: process.env.REDIS_URL,
      socket: { reconnectStrategy: () => 100 }
    });
    await redisClient.connect();
    console.log('✅ Redis: Połączono');
    serviceStatus.set({ service: 'redis' }, 1);
  } catch (err) {
    console.error('❌ Redis:', err.message);
    serviceStatus.set({ service: 'redis' }, 0);
  }

  // RabbitMQ
  try {
    const connection = await amqp.connect(process.env.RABBITMQ_URL);
    rabbitmqChannel = await connection.createChannel();
    console.log('✅ RabbitMQ: Połączono');
    serviceStatus.set({ service: 'rabbitmq' }, 1);
  } catch (err) {
    console.error('❌ RabbitMQ:', err.message);
    serviceStatus.set({ service: 'rabbitmq' }, 0);
  }

  console.log('\n🎯 Aplikacja gotowa!\n');
}

// ===== MIDDLEWARE =====
app.use((req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    const duration = Date.now() - start;
    httpRequestDuration
      .labels(req.method, req.route?.path || req.url, res.statusCode)
      .observe(duration);
  });
  next();
});

// ===== ENDPOINTY =====

// Health check
app.get('/health', async (req, res) => {
  const health = {
    status: 'ok',
    timestamp: new Date().toISOString(),
    services: {
      postgres: serviceStatus.get({ service: 'postgres' })?.values?.[0]?.value || 0,
      redis: serviceStatus.get({ service: 'redis' })?.values?.[0]?.value || 0,
      rabbitmq: serviceStatus.get({ service: 'rabbitmq' })?.values?.[0]?.value || 0
    }
  };

  const allHealthy = Object.values(health.services).every(s => s === 1);
  res.status(allHealthy ? 200 : 503).json(health);
});

// API - bez cache (zawsze do DB)
app.get('/users/db', async (req, res) => {
  try {
    const start = Date.now();
    const result = await pgPool.query('SELECT * FROM users LIMIT 10');
    dbQueryDuration.labels('SELECT users').observe(Date.now() - start);

    res.json({ source: 'database', data: result.rows });
  } catch (err) {
    console.error('DB Error:', err);
    res.status(503).json({ error: 'Database unavailable', message: err.message });
  }
});

// API - z cache'em
app.get('/users/cached', async (req, res) => {
  try {
    const cacheKey = 'users:all';

    // Sprawdź cache
    if (redisClient) {
      try {
        const cached = await redisClient.get(cacheKey);
        if (cached) {
          cacheHits.inc({ key: cacheKey });
          return res.json({ source: 'cache', data: JSON.parse(cached) });
        }
      } catch (cacheErr) {
        console.warn('Cache error:', cacheErr.message);
      }
    }

    // Cache miss - pobierz z DB
    cacheMisses.inc({ key: cacheKey });
    const start = Date.now();
    const result = await pgPool.query('SELECT * FROM users LIMIT 10');
    dbQueryDuration.labels('SELECT users').observe(Date.now() - start);

    // Zapisz do cache'u
    if (redisClient) {
      try {
        await redisClient.setEx(cacheKey, 60, JSON.stringify(result.rows));
      } catch (err) {
        console.warn('Cache set error:', err.message);
      }
    }

    res.json({ source: 'database', data: result.rows });
  } catch (err) {
    console.error('Error:', err);
    res.status(503).json({ error: 'Service unavailable', message: err.message });
  }
});

// API - queue message
app.post('/jobs', async (req, res) => {
  try {
    if (!rabbitmqChannel) {
      return res.status(503).json({ error: 'RabbitMQ unavailable' });
    }

    const jobId = Date.now();
    await rabbitmqChannel.assertQueue('jobs');
    await rabbitmqChannel.sendToQueue('jobs', Buffer.from(JSON.stringify({ id: jobId, timestamp: new Date() })));

    res.json({ message: 'Job queued', jobId });
  } catch (err) {
    console.error('Queue error:', err);
    res.status(503).json({ error: 'Queue unavailable', message: err.message });
  }
});

// Metryki
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', promClient.register.contentType);
  res.end(await promClient.register.metrics());
});

// Root
app.get('/', (req, res) => {
  res.json({
    name: 'Chaos Engineering Lab',
    endpoints: {
      health: '/health',
      users_from_db: '/users/db',
      users_cached: '/users/cached',
      queue_job: 'POST /jobs',
      metrics: '/metrics'
    }
  });
});

// ===== START =====
const PORT = process.env.PORT || 3000;

initializeServices().then(() => {
  app.listen(PORT, () => {
    console.log(`🎯 Serwer uruchomiony na http://localhost:${PORT}`);
  });
});