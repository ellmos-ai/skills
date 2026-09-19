#!/usr/bin/env node
// mermaid_lint.mjs — prueft alle ```mermaid-Bloecke unter einem Pfad mit dem echten
// Mermaid-Parser (mermaid.parse), ohne Browser/Puppeteer.
//
//   node mermaid_lint.mjs <repo-pfad> [--json]
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

mermaid.initialize({ startOnLoad: false, securityLevel: 'loose' });

// Fehlertexte, die die Node-Umgebung verursacht und nicht das Diagramm
const ENV_ERRORS = [/DOMPurify/i, /addHook is not a function/i, /document is not defined/i,
  /window is not defined/i, /getBBox/i, /createElementNS/i];

const IGNORE = new Set(['.git', 'node_modules', 'dist', 'build', '.venv', 'venv',
  '__pycache__', '.next', 'vendor', 'target', '.tox', 'site-packages']);

function walk(dir, out = []) {
  let entries;
  try { entries = readdirSync(dir, { withFileTypes: true }); } catch { return out; }
  for (const e of entries) {
    if (IGNORE.has(e.name)) continue;
    const p = join(dir, e.name);
    if (e.isDirectory()) walk(p, out);
    else if (e.isFile() && /\.(md|markdown)$/i.test(e.name)) out.push(p);
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
const ENTITY_RE = /&[a-zA-Z][a-zA-Z0-9]*;/g;

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

const asJson = process.argv.includes('--json');
let targets = process.argv.slice(2).filter(a => !a.startsWith('--'));
// --from <datei>: eine Pfad pro Zeile (umgeht Shell-Escaping von Windows-Backslashes)
const fromIdx = process.argv.indexOf('--from');
if (fromIdx > -1 && process.argv[fromIdx + 1]) {
  targets = readFileSync(process.argv[fromIdx + 1], 'utf8').split(/\r?\n/).filter(Boolean);
}
if (!targets.length) { console.error('Pfad fehlt: node mermaid_lint.mjs <repo-pfad> [...] | --from <liste.txt> [--json]'); process.exit(2); }

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
