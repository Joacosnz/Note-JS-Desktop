const { spawn } = require('child_process');

// Proxy a server.py para asegurar compatibilidad universal con entornos Node y Python
const child = spawn('python3', ['server.py', ...process.argv.slice(2)], {
  stdio: 'inherit',
  env: process.env
});

child.on('error', (err) => {
  console.error('[server.js] Error al iniciar python3 server.py:', err);
  process.exit(1);
});

child.on('exit', (code) => {
  process.exit(code || 0);
});
