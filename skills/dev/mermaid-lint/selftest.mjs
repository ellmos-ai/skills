#!/usr/bin/env node
// selftest.mjs — kleinster Check, der fehlschlaegt, wenn mermaid_lint.mjs bricht.
//   node selftest.mjs
// Prueft: kaputte Bloecke werden gefunden, gueltige NICHT gemeldet (kein Fehlalarm),
// und ein gueltiger Flowchart mit quotiertem Label parst durch (DOM-Shim wirkt).

import { mkdtempSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';
import assert from 'node:assert/strict';

const here = dirname(fileURLToPath(import.meta.url));

const FIXTURE = `# Fixture

Kaputt: reserviertes Wort als Teilnehmer.

\`\`\`mermaid
sequenceDiagram
    participant User
    participant Loop
    User->>Loop: run(goal)
\`\`\`

Gut: Alias.

\`\`\`mermaid
sequenceDiagram
    participant User
    participant L as Loop
    User->>L: run goal
\`\`\`

Kaputt: unquotierte Klammern im Knoten.

\`\`\`mermaid
flowchart TD
    A[Start (hier)] --> B[Ende]
\`\`\`

Gut: quotiertes Label -- darf NICHT an DOMPurify scheitern.

\`\`\`mermaid
flowchart TD
    A["Start (hier)"] --> B[Ende]
\`\`\`

Warnung erwartet: HTML-Entity in einer Sequenznachricht.

\`\`\`mermaid
sequenceDiagram
    participant A
    participant B
    A->>B: Gap validated &ge; 8.69
\`\`\`

Keine Warnung: Entity in einem quotierten Flowchart-Label ist unproblematisch.

\`\`\`mermaid
flowchart TD
    X["Gap &ge; 8.69"] --> Y[Ende]
\`\`\`
`;

const dir = mkdtempSync(join(tmpdir(), 'mermaid-selftest-'));
try {
  writeFileSync(join(dir, 'README.md'), FIXTURE, 'utf8');

  let out;
  try {
    out = execFileSync('node', [join(here, 'mermaid_lint.mjs'), dir, '--json'],
      { encoding: 'utf8' });
  } catch (e) {
    // Exit 1 ist erwartet (es gibt defekte Bloecke) -- stdout trotzdem auswerten.
    out = e.stdout;
  }
  const r = JSON.parse(out);

  assert.equal(r.blocks, 6, `6 Bloecke erwartet, gezaehlt: ${r.blocks}`);
  // Block 5 zaehlt mit: die Entity bricht den Parser wirklich, die Warnung erklaert nur warum.
  assert.equal(r.broken, 3, `3 defekte Bloecke erwartet, gemeldet: ${r.broken}`);

  const blocks = r.findings.map(f => f.block).sort();
  assert.deepEqual(blocks, [1, 3, 5], `Bloecke 1, 3 und 5 sollten defekt sein, waren: ${blocks}`);

  assert.match(r.findings[0].error, /ACTOR|loop/i,
    'Block 1 sollte am reservierten Wort scheitern');
  assert.match(r.findings[1].error, /PS|SQE/,
    'Block 3 sollte an der unquotierten Klammer scheitern');

  // Kein Umgebungsfehler: sonst ist der DOM-Shim kaputt und Flowcharts werden blind uebersprungen.
  assert.equal((r.envIssues || []).length, 0,
    `Umgebungsfehler aufgetreten -- DOM-Shim pruefen: ${JSON.stringify(r.envIssues)}`);

  // Entity-Vorpruefung: warnt in Sequenznachrichten, nicht in Flowchart-Labels.
  const warns = r.warnings || [];
  assert.equal(warns.length, 1,
    `genau 1 Entity-Warnung erwartet (Block 5), gemeldet: ${JSON.stringify(warns)}`);
  assert.equal(warns[0].block, 5, `Warnung sollte Block 5 betreffen, war: ${warns[0].block}`);
  assert.match(warns[0].detail, /&ge;/, 'Warnung sollte die gefundene Entity nennen');

  console.log('selftest OK: 6 Bloecke, 3 defekt (1, 3, 5), 1 Entity-Warnung (5), 0 Umgebungsfehler');
} finally {
  rmSync(dir, { recursive: true, force: true });
}
