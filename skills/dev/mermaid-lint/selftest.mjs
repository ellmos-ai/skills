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

  assert.equal(r.blocks, 4, `4 Bloecke erwartet, gezaehlt: ${r.blocks}`);
  assert.equal(r.broken, 2, `2 defekte Bloecke erwartet, gemeldet: ${r.broken}`);

  const blocks = r.findings.map(f => f.block).sort();
  assert.deepEqual(blocks, [1, 3], `Bloecke 1 und 3 sollten defekt sein, waren: ${blocks}`);

  assert.match(r.findings[0].error, /ACTOR|loop/i,
    'Block 1 sollte am reservierten Wort scheitern');
  assert.match(r.findings[1].error, /PS|SQE/,
    'Block 3 sollte an der unquotierten Klammer scheitern');

  // Kein Umgebungsfehler: sonst ist der DOM-Shim kaputt und Flowcharts werden blind uebersprungen.
  assert.equal((r.envIssues || []).length, 0,
    `Umgebungsfehler aufgetreten -- DOM-Shim pruefen: ${JSON.stringify(r.envIssues)}`);

  console.log('selftest OK: 4 Bloecke, 2 defekt (1 und 3), 0 Umgebungsfehler');
} finally {
  rmSync(dir, { recursive: true, force: true });
}
