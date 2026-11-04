// Share interpreter selection across npm commands, including Windows Store aliases.
const { spawnSync } = require('node:child_process');
const { existsSync, readdirSync } = require('node:fs');
const path = require('node:path');
const candidates = [];
if (process.env.NOTEJS_PYTHON) candidates.push(process.env.NOTEJS_PYTHON);
if (process.platform === 'win32' && process.env.LOCALAPPDATA) {
  const root = path.join(process.env.LOCALAPPDATA, 'Python');
  if (existsSync(root)) {
    for (const name of readdirSync(root).sort().reverse()) {
      const executable = path.join(root, name, 'python.exe');
      if (existsSync(executable)) candidates.push(executable);
    }
  }
}
candidates.push('python3', 'python');
const python = candidates.find(executable =>
  spawnSync(executable, ['--version'], { windowsHide: true }).status === 0);
if (!python) {
  console.error('Python no encontrado. Instala Python o configura NOTEJS_PYTHON.');
  process.exit(1);
}
const result = spawnSync(python, process.argv.slice(2), { stdio: 'inherit', windowsHide: true });
if (result.error) console.error(result.error.message);
process.exit(result.status ?? 1);
