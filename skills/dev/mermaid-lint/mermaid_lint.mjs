#!/usr/bin/env node
// mermaid_lint.mjs — prueft alle ```mermaid-Bloecke unter einem Pfad mit dem echten
// Mermaid-Parser (mermaid.parse), ohne Browser/Puppeteer.
//
//   node mermaid_lint.mjs <repo-pfad> [...] [--json] [--config <datei.json>] [--repair]
//   node mermaid_lint.mjs --from <liste.txt> [--json]
//
// Exit 0 = alle Bloecke parsen, 1 = mindestens ein Block defekt.
//
// ponytail: mermaid@latest statt GitHubs exakter Version — die Fehlerklassen
// (reservierte Woerter, unquotierte Klammern) sind versionsstabil; bei Zweifel
// Readback auf github.com.

// DOM-Shim ZUERST: mermaid.parse() ruft DOMPurify auf, das ohne window/document
// scheitert -- dann werden gueltige Flowcharts faelschlich uebersprungen.
import { JSDOM } from 'jsdom';
const _dom = new JSDOM('<!doctype html><html><body></body></html>');
globalThis.window = _dom.window;
globalThis.document = _dom.window.document;
globalThis.Element = _dom.window.Element;
globalThis.Node = _dom.window.Node;
globalThis.DocumentFragment = _dom.window.DocumentFragment;
globalThis.HTMLElement = _dom.window.HTMLElement;
globalThis.SVGElement = _dom.window.SVGElement;

const mermaid = (await import('mermaid')).default;
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join, relative, sep } from 'node:path';
import { loadMermaidLintConfig } from './lint_config.mjs';

const rawArgs = process.argv.slice(2);
const cfgFlagIdx = rawArgs.indexOf('--config');
const customConfigPath = (cfgFlagIdx > -1 && rawArgs[cfgFlagIdx + 1]) ? rawArgs[cfgFlagIdx + 1] : null;
const repairConfig = rawArgs.includes('--repair');
const { config: CFG, warnings: CONFIG_WARNINGS } = loadMermaidLintConfig({
  configPath: customConfigPath,
  repair: repairConfig,
});

mermaid.initialize({
  startOnLoad: Boolean(CFG.mermaid?.start_on_load ?? false),
  securityLevel: String(CFG.mermaid?.security_level || 'loose'),
});

// Fehlertexte, die die Node-Umgebung verursacht und nicht das Diagramm
const ENV_ERRORS = (CFG.scan?.env_error_patterns || []).map(p => new RegExp(p, 'i'));
const IGNORE = new Set(CFG.scan?.ignore_dirs || []);
const EXTENSIONS = (CFG.scan?.file_extensions || ['.md', '.markdown']).map(e => e.toLowerCase());

function walk(dir, out = []) {
  let entries;
  try { entries = readdirSync(dir, { withFileTypes: true }); } catch { return out; }
  for (const e of entries) {
    if (IGNORE.has(e.name)) continue;
    const p = join(dir, e.name);
    if (e.isDirectory()) walk(p, out);
    else if (e.isFile() && EXTENSIONS.some(ext => e.name.toLowerCase().endsWith(ext))) out.push(p);
  }
  return out;
}

// Liefert {startLine (1-basiert, Zeile des ```mermaid), body}
function extractBlocks(text) {
  const lines = text.split(/\r?\n/);
  const blocks = [];
  let open = null;
  for (let i = 0; i < lines.length; i++) {
    const l = lines[i];
    if (open === null) {
      if (/^\s*(```|~~~)mermaid\s*$/.test(l)) open = { startLine: i + 1, body: [] };
    } else {
      if (/^\s*(```|~~~)\s*$/.test(l)) { blocks.push({ startLine: open.startLine, body: open.body.join('\n') }); open = null; }
      else open.body.push(l);
    }
  }
  return blocks;
}

// Vorpruefung: HTML-Entities in Sequenzdiagramm-Nachrichten. Ihr abschliessendes ';'
// liest der Lexer als Statement-Terminator, alles danach wird neue Anweisung.
// Wird auch dann gemeldet, wenn der Parser die Zeile noch durchlaesst -- in
// quotierten Flowchart-Labels sind Entities dagegen unproblematisch.
const ENTITY_RE = new RegExp(CFG.scan?.sequence_entity_regex || '&[a-zA-Z][a-zA-Z0-9]*;', 'g');

function entityWarnings(body) {
  const lines = body.split('\n');
  if (!lines.some(l => /^\s*sequenceDiagram\b/.test(l))) return [];
  const out = [];
  lines.forEach((line, i) => {
    // Nachrichtenzeile: A->>B: text   (auch -->>, ->, -->, -x, --x)
    if (!/(-{1,2}>>?|--?x|--?\))\s*[^:]+:/.test(line)) return;
    const hits = line.match(ENTITY_RE);
    if (hits) out.push({ line: i + 1, entities: [...new Set(hits)], raw: line.trim().slice(0, 120) });
  });
  return out;
}

const asJson = rawArgs.includes('--json');
const skipValues = new Set();
const fromIdx = rawArgs.indexOf('--from');
if (fromIdx > -1 && rawArgs[fromIdx + 1]) skipValues.add(fromIdx + 1);
if (cfgFlagIdx > -1 && rawArgs[cfgFlagIdx + 1]) skipValues.add(cfgFlagIdx + 1);

let targets = rawArgs.filter((a, idx) => !a.startsWith('--') && !skipValues.has(idx));
// --from <datei>: eine Pfad pro Zeile (umgeht Shell-Escaping von Windows-Backslashes)
if (fromIdx > -1 && rawArgs[fromIdx + 1]) {
  targets = readFileSync(rawArgs[fromIdx + 1], 'utf8').split(/\r?\n/).filter(Boolean);
}
if (!targets.length) {
  console.error('Pfad fehlt: node mermaid_lint.mjs <repo-pfad> [...] | --from <liste.txt> [--json] [--config <datei.json>]');
  process.exit(2);
}

async function lintTarget(target) {
  let isDir = false;
  try { isDir = statSync(target).isDirectory(); } catch { return { target, error: 'nicht gefunden', files: 0, filesWithBlocks: 0, blocks: 0, broken: 0, findings: [] }; }
  const root = isDir ? target : null;
  const files = root ? walk(root) : [target];

  const findings = [];
  const envIssues = [];
  const warnings = [];
  let blockCount = 0, fileWithBlocks = 0;

  for (const f of files) {
    let text;
    try { text = readFileSync(f, 'utf8'); } catch { continue; }
    const blocks = extractBlocks(text);
    if (blocks.length) fileWithBlocks++;
    for (let bi = 0; bi < blocks.length; bi++) {
      blockCount++;
      const b = blocks[bi];
      const relFile = root ? relative(root, f).split(sep).join('/') : f;
      for (const w of entityWarnings(b.body)) {
        warnings.push({
          file: relFile, block: bi + 1, blockStartLine: b.startLine,
          fileLine: b.startLine + w.line,
          type: 'html_entity_in_sequence_message',
          detail: `HTML-Entity in Sequenznachricht: ${w.entities.join(', ')} -- das ';' beendet die Anweisung. `
            + `Durch das literale Zeichen ersetzen. Zeile: ${w.raw}`,
        });
      }
      try {
        await mermaid.parse(b.body);
      } catch (err) {
        const msg = String(err && err.message ? err.message : err);
        // Mermaid meldet "Parse error on line N" relativ zum Block
        const m = msg.match(/line (\d+)/i);
        const relLine = m ? parseInt(m[1], 10) : null;
        const rec = {
          file: root ? relative(root, f).split(sep).join('/') : f,
          block: bi + 1,
          blockStartLine: b.startLine,
          fileLine: relLine ? b.startLine + relLine : null,
          error: msg.split('\n').slice(0, 4).join(' | ').trim(),
        };
        if (ENV_ERRORS.some(re => re.test(msg))) envIssues.push(rec);
        else findings.push(rec);
      }
    }
  }
  return { target, files: files.length, filesWithBlocks: fileWithBlocks, blocks: blockCount,
    broken: findings.length, findings, envIssues, warnings };
}

for (const w of CONFIG_WARNINGS) {
  console.error(`[CONFIG-WARN] ${w}`);
}

const results = [];
for (const t of targets) results.push(await lintTarget(t));

if (asJson) {
  console.log(JSON.stringify(targets.length === 1 ? results[0] : { results }, null, 2));
} else {
  for (const r of results) {
    console.log(`=== mermaid_lint: ${r.target}`);
    if (r.error) { console.log(`  !! ${r.error}`); continue; }
    console.log(`Dateien: ${r.files} | mit Mermaid: ${r.filesWithBlocks} | Bloecke: ${r.blocks} | defekt: ${r.broken}`);
    for (const f of r.findings) {
      console.log(`\n[FAIL] ${f.file} (Block ${f.block}, beginnt Zeile ${f.blockStartLine}${f.fileLine ? `, Fehler ~Zeile ${f.fileLine}` : ''})`);
      console.log(`  ${f.error}`);
    }
    for (const w of r.warnings || []) {
      console.log(`[WARN] ${w.file} (Block ${w.block}, ~Zeile ${w.fileLine})\n  ${w.detail}`);
    }
    for (const f of r.envIssues || []) {
      console.log(`[SKIP-ENV] ${f.file} Block ${f.block}: ${f.error.slice(0, 80)} (Node-Umgebung, kein Syntaxfehler)`);
    }
  }
}
process.exit(results.some(r => r.broken) ? 1 : 0);
