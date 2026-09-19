#!/usr/bin/env node
// readback.mjs — prueft auf GitHub-Seiten, ob die Mermaid-Diagramme wirklich rendern.
// GitHub rendert Mermaid per JavaScript im Browser, deshalb genuegt ein DOM-Dump nicht;
// hier wartet ein echter Browser (vorhandener Edge, kein Download) auf das Ergebnis.
//
//   node readback.mjs <url> [<url> ...]
//
// Ausgabe je URL: ERR=<renderfehler> SVG=<gerenderte diagramme> PRE=<mermaid-bloecke> <url>
// Aussagekraeftig ist nur ERR=0 BEI PRE>0 und SVG>0.

import { chromium } from 'playwright-core';

const urls = process.argv.slice(2);
if (!urls.length) { console.error('URLs fehlen'); process.exit(2); }

// GitHub zeigt waehrend des Ladens kurz einen Platzhalter, der wie ein Renderfehler
// aussieht. Ein einzelner DEFEKT-Befund ist deshalb nicht belastbar -- gemessen am
// 2026-09-20: dieselbe Seite meldete erst ERR=1, dann zweimal ERR=0.
const RETRIES = 2;

const browser = await chromium.launch({
  channel: 'msedge',
  args: ['--disable-gpu', '--no-sandbox'],
});
const ctx = await browser.newContext();
let bad = 0;

async function probe(url) {
  const page = await ctx.newPage();
  let err = -1, svg = -1, pre = -1;
  try {
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
    // Mermaid-Bloecke sind als <pre lang="mermaid"> im Markdown-Body vorhanden.
    pre = await page.locator('pre[lang="mermaid"], .js-render-target[data-type="mermaid"]').count();
    if (pre > 0) {
      // GitHub rendert Mermaid in sandboxed iframes von viewscreen.githubusercontent.com.
      // Die Hauptseite sieht deren Inhalt NICHT -- ohne Frame-Auswertung meldet jede
      // Seite faelschlich "kein Fehler".
      await page.waitForTimeout(8000);
    }
    err = 0; svg = 0;
    const texts = [];
    for (const fr of page.frames()) {
      try {
        const t = await fr.evaluate(() => document.body ? document.body.innerText : '');
        texts.push(t);
        svg += await fr.locator('svg[aria-roledescription], svg[id^="mermaid"], .mermaid svg').count();
      } catch { /* abgeloester Frame */ }
    }
    const all = texts.join('\n');
    err = (all.match(/Unable to render rich display|Parse error on line|Syntax error in (?:text|graph)/g) || []).length;
  } catch (e) {
    await page.close();
    return { verdict: 'LADEFEHLER', err, svg, pre, note: String(e.message).split('\n')[0] };
  }
  await page.close();
  const verdict = pre === 0 ? 'KEIN-MERMAID' : (err > 0 ? 'DEFEKT' : (svg > 0 ? 'OK' : 'UNKLAR'));
  return { verdict, err, svg, pre, note: '' };
}

for (const url of urls) {
  let r = await probe(url);
  let tries = 1;
  // Nur negative Befunde wiederholen -- ein OK ist nie ein Ladeartefakt.
  while ((r.verdict === 'DEFEKT' || r.verdict === 'UNKLAR' || r.verdict === 'LADEFEHLER') && tries <= RETRIES) {
    const again = await probe(url);
    tries++;
    if (again.verdict === 'OK') { r = again; break; }
    r = again;
  }
  if (r.verdict !== 'OK' && r.verdict !== 'KEIN-MERMAID') bad++;
  console.log(`${r.verdict.padEnd(12)} ERR=${r.err} SVG=${r.svg} PRE=${r.pre} (Versuche: ${tries})  ${url}${r.note ? ' :: ' + r.note : ''}`);
}

await browser.close();
process.exit(bad ? 1 : 0);
