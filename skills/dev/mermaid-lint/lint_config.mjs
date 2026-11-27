// lint_config.mjs — shared self-healing JSON config loader for mermaid-lint.
import { copyFileSync, existsSync, readFileSync, renameSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
export const BASE_CONFIG_NAME = 'mermaid-lint-config.json';

export const DEFAULT_CONFIG = {
  schema: 'ocean.skill-config.v2',
  skill: 'mermaid-lint',
  version: '1.1.0',
  self_healing: {
    enabled: true,
    on_corrupt: 'fallback_to_defaults_with_backup',
    backup_suffix: '.corrupt.<ts>.bak',
  },
  mermaid: {
    start_on_load: false,
    security_level: 'loose',
  },
  scan: {
    ignore_dirs: [
      '.git', 'node_modules', 'dist', 'build', '.venv', 'venv',
      '__pycache__', '.next', 'vendor', 'target', '.tox', 'site-packages',
    ],
    file_extensions: ['.md', '.markdown'],
    sequence_entity_regex: '&[a-zA-Z][a-zA-Z0-9]*;',
    env_error_patterns: [
      'DOMPurify',
      'addHook is not a function',
      'document is not defined',
      'window is not defined',
      'getBBox',
      'createElementNS',
    ],
  },
  readback: {
    channel: 'msedge',
    launch_args: ['--disable-gpu', '--no-sandbox'],
    retries: 2,
    goto_timeout_ms: 60000,
    render_wait_ms: 8000,
    error_patterns: [
      'Unable to render rich display',
      'Parse error on line',
      'Syntax error in (?:text|graph)',
    ],
  },
};

function isPlainObject(val) {
  return Boolean(val) && typeof val === 'object' && !Array.isArray(val);
}

function deepMerge(base, override) {
  const out = structuredClone(base);
  for (const [k, v] of Object.entries(override || {})) {
    if (isPlainObject(out[k]) && isPlainObject(v)) {
      out[k] = deepMerge(out[k], v);
    } else {
      out[k] = structuredClone(v);
    }
  }
  return out;
}

export function loadMermaidLintConfig(options = {}) {
  const skillRoot = options.skillRoot || HERE;
  const repair = Boolean(options.repair);
  const warnings = [];
  const healed = [];
  let effective = structuredClone(DEFAULT_CONFIG);

  const candidates = [
    join(skillRoot, BASE_CONFIG_NAME),
    join(skillRoot, 'config.json'),
  ];
  if (options.configPath) {
    candidates.push(options.configPath);
  }

  const ts = new Date().toISOString().replace(/[:.]/g, '');
  candidates.forEach((candidate, idx) => {
    if (!existsSync(candidate)) return;
    try {
      const rawText = readFileSync(candidate, 'utf8').replace(/^\uFEFF/, '');
      const parsed = JSON.parse(rawText);
      if (!isPlainObject(parsed)) {
        throw new Error('JSON root must be an object');
      }
      effective = deepMerge(effective, parsed);
    } catch (err) {
      warnings.push(`${candidate}: corrupt config (${err.message}); fell back to defaults`);
      if (repair) {
        const bak = `${candidate}.corrupt.${ts}.bak`;
        copyFileSync(candidate, bak);
        const tmp = `${candidate}.${process.pid}.tmp`;
        writeFileSync(tmp, JSON.stringify(idx === 0 ? DEFAULT_CONFIG : {}, null, 2) + '\n', 'utf8');
        renameSync(tmp, candidate);
        healed.push({ path: candidate, backupPath: bak });
      }
    }
  });

  return { config: effective, warnings, healed };
}
