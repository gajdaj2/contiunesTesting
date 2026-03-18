const http = require('http');

async function checkHealth() {
  return new Promise((resolve) => {
    const req = http.get('http://localhost:3000/health', (res) => {
      res.on('data', () => {});
      res.on('end', () => {
        const okStatuses = new Set([200, 503]);
        process.exit(okStatuses.has(res.statusCode) ? 0 : 1);
      });
    });

    req.on('error', () => {
      process.exit(1);
    });

    setTimeout(() => process.exit(1), 3000);
  });
}

checkHealth();