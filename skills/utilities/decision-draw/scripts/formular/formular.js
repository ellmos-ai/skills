(function () {
  'use strict';
  var DATA = JSON.parse(document.getElementById('form-data').textContent);
  var ITEMS = DATA.items, BYID = {};
  ITEMS.forEach(function (it) { BYID[it.id] = it; });
  var LSKEY = 'ticket-master.decisions.' + DATA.document_id + '.' + DATA.doc_sha256.slice(0, 16);
  var st = { choice: {}, note: {}, via: {}, agpl: { choice: null, note: '' }, bulk: {}, gesamt: { explicit: false, at: null }, restored: null };
  var RQ = 'rueckfrage'; /* eigene Wahl je Posten: Rueckfrage / mehr Info noetig; die Anmerkung gilt dann als Frage */
  var answered = false; /* wird in init() gesetzt: das eingebettete Antwort-Skript steht im beantworteten Dokument NACH diesem Skript */
  var restoreHint = false; /* true, wenn ein wiederhergestellter Stand eine Gesamtabnahme trug, die bewusst NICHT uebernommen wurde */
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  function lsGet() { try { return JSON.parse(localStorage.getItem(LSKEY) || 'null'); } catch (e) { return null; } }
  function lsSet() { try { st.savedLocal = new Date().toISOString(); localStorage.setItem(LSKEY, JSON.stringify(st)); } catch (e) { /* Seite funktioniert auch ohne */ } }
  function lsClear() { try { localStorage.removeItem(LSKEY); } catch (e) { /* ignorieren */ } }

  function label(it, k) { if (k === RQ) return 'Rückfrage / mehr Info nötig'; var o = it.options.filter(function (x) { return x.k === k; })[0]; return o ? o.l : ''; }
  function nAnswered() { return ITEMS.filter(function (it) { return st.choice[it.id] && st.choice[it.id] !== RQ; }).length; }
  function nQuestions() { return ITEMS.filter(function (it) { return st.choice[it.id] === RQ; }).length; }
  function hasVorab() { return !!document.getElementById('item-AGPL'); } /* nur das Referenzdokument vom 2026-11-07 hat die Vorab-Frage */
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  function render() {
    ITEMS.forEach(function (it) {
      var card = document.getElementById('item-' + it.id);
      if (!card) return;
      $$('input[type=radio]', card).forEach(function (r) { r.checked = (st.choice[it.id] === r.value); });
      var ta = $('textarea', card); if (ta && ta.value !== (st.note[it.id] || '')) ta.value = st.note[it.id] || '';
      card.classList.toggle('done', !!st.choice[it.id] && st.choice[it.id] !== RQ);
      card.classList.toggle('question', st.choice[it.id] === RQ);
      var v = $('.via', card); if (v) v.textContent = st.choice[it.id] ? (st.via[it.id] === 'bulk' ? 'per Massenaktion gesetzt' : 'von dir gewählt') : '';
    });
    $$('input[name=agpl]').forEach(function (r) { r.checked = (st.agpl.choice === r.value); });
    var at = $('#agpl-note'); if (at && at.value !== st.agpl.note) at.value = st.agpl.note;
    var n = nAnswered(), q = nQuestions();
    $$('.js-progress').forEach(function (e) { e.textContent = n + ' von ' + ITEMS.length + ' beantwortet' + (q ? ', ' + q + (q === 1 ? ' Rückfrage' : ' Rückfragen') : ''); });
    $$('.js-bar').forEach(function (e) { e.style.width = Math.round(100 * n / ITEMS.length) + '%'; });
    var seen = {};
    ITEMS.forEach(function (it) { var b = it.bundle; seen[b] = seen[b] || { n: 0, d: 0 }; seen[b].n++; if (st.choice[it.id] && st.choice[it.id] !== RQ) seen[b].d++; });
    Object.keys(seen).forEach(function (b) { var e = document.getElementById('bcount-' + b); if (e) e.textContent = seen[b].d + ' von ' + seen[b].n + ' beantwortet'; });
    var g = $('#gesamt-state');
    if (g) g.textContent = st.gesamt.explicit ? 'Gesamtabnahme: ausdrücklich ja (' + (st.gesamt.at || '').replace('T', ' ').slice(0, 16) + ' UTC)' : 'Gesamtabnahme: nicht erklärt';
    var onlyOpen = document.body.classList.contains('only-open');
    ITEMS.forEach(function (it) { var c = document.getElementById('item-' + it.id); if (c) c.hidden = onlyOpen && !!st.choice[it.id] && st.choice[it.id] !== RQ; });
    $$('.bundle-form').forEach(function (bf) { var vis = $$('.item', bf).some(function (c) { return !c.hidden; }); bf.classList.toggle('empty', onlyOpen && !vis); });
    var r = $('#restore-note'); if (r) { r.hidden = !st.restored; if (st.restored) $('#restore-text').textContent = 'Zwischenstand vom ' + st.restored.replace('T', ' ').slice(0, 16) + ' UTC wiederhergestellt.' + (restoreHint ? ' Die frühere Gesamtabnahme wurde nicht übernommen: Sie muss erneut ausdrücklich bestätigt werden (Alles wie empfohlen).' : ''); }
  }
  function touch(manual) { if (manual && st.gesamt.explicit) { st.gesamt.explicit = false; st.gesamt.at = null; toast('Gesamtabnahme zurückgenommen: du hast danach einen Posten selbst geändert.'); } lsSet(); render(); }

  function toast(msg) { var t = $('#toast'); if (!t) return; t.textContent = msg; t.classList.add('show'); clearTimeout(toast._t); toast._t = setTimeout(function () { t.classList.remove('show'); }, 5000); }

  /* ---------- Dialog im Dokument (kein Browser-alert) ---------- */
  function ask(title, bodyHtml, buttons) {
    return new Promise(function (resolve) {
      var d = $('#dlg'); $('#dlg-title').textContent = title; $('#dlg-body').innerHTML = bodyHtml;
      var bar = $('#dlg-buttons'); bar.innerHTML = '';
      buttons.forEach(function (b) {
        var e = document.createElement('button'); e.type = 'button'; e.textContent = b.label; e.className = b.primary ? 'primary' : '';
        e.addEventListener('click', function () { var extra = {}; $$('#dlg-body input[type=checkbox]').forEach(function (c) { extra[c.name] = c.checked; }); d.close(); resolve({ id: b.id, extra: extra }); });
        bar.appendChild(e);
      });
      d.addEventListener('cancel', function onc() { d.removeEventListener('cancel', onc); resolve({ id: 'cancel', extra: {} }); }, { once: true });
      if (d.showModal) d.showModal(); else d.setAttribute('open', '');
    });
  }

  /* ---------- Massenaktionen ---------- */
  function scopeItems(scope) { return ITEMS.filter(function (it) { return scope === 'all' || String(it.bundle) === String(scope); }); }
  function bulk(scope) {
    var sc = scopeItems(scope), withRec = sc.filter(function (it) { return it.rec; }), noRec = sc.length - withRec.length;
    var marked = withRec.filter(function (it) { return it.marked; });
    var already = withRec.filter(function (it) { return st.choice[it.id]; }), deviates = already.filter(function (it) { return st.choice[it.id] !== it.rec; });
    var title = scope === 'all' ? 'Alles wie empfohlen annehmen?' : 'Bündel ' + scope + ': alle wie empfohlen annehmen?';
    var body = '<p>' + withRec.length + ' Posten haben eine Empfehlung und werden auf diese Empfehlung gesetzt.' + (noRec ? ' ' + noRec + ' Posten ohne Empfehlung bleiben unberührt.' : '') + '</p>' +
      (marked.length ? '<p class="warn"><b>Markiert (' + marked.length + '):</b> ' + marked.map(function (m) { return esc(m.id); }).join(', ') + ' – rote Avatar-Posten sowie Löschung, Geld, Außenwirkung oder Lizenz. Sie werden mit angenommen, bleiben aber markiert und werden vor dem Speichern noch einmal aufgelistet.</p>' : '') +
      (already.length ? '<p>' + already.length + ' davon hast du schon beantwortet' + (deviates.length ? ', ' + deviates.length + ' weichen von der Empfehlung ab (' + deviates.map(function (m) { return esc(m.id); }).join(', ') + ')' : '') + '.</p><label><input type="checkbox" name="over"> auch bereits beantwortete Posten überschreiben (sonst bleiben sie, wie sie sind)</label>' : '') +
      (scope === 'all' ? '<p>Stehen danach alle Posten wie empfohlen, gilt das als <b>ausdrückliche Gesamtabnahme</b> und wird so gespeichert, solange du danach keinen Posten selbst änderst.</p>' : '');
    ask(title, body, [{ id: 'no', label: 'Abbrechen' }, { id: 'yes', label: 'Ja, ausdrücklich annehmen', primary: true }]).then(function (r) {
      if (r.id !== 'yes') return;
      var over = !!r.extra.over, n = 0;
      withRec.forEach(function (it) { if (!st.choice[it.id] || over) { st.choice[it.id] = it.rec; st.via[it.id] = 'bulk'; n++; } });
      st.bulk['bundle-' + (scope === 'all' ? 'alle' : scope)] = true;
      var msg = n + ' Posten gesetzt.';
      if (scope === 'all') {
        var allRec = nQuestions() === 0 && ITEMS.every(function (it) { return !it.rec || st.choice[it.id] === it.rec; });
        st.gesamt.explicit = allRec; st.gesamt.at = allRec ? new Date().toISOString() : null;
        if (!allRec) msg += ' Keine Gesamtabnahme: ' + deviates.length + ' bereits beantwortete Posten weichen von der Empfehlung ab.';
      }
      touch(false); toast(msg);
    });
  }

  /* ---------- Antwortdatei und beantwortetes Dokument ---------- */
  function buildAnswers() {
    var ans = {};
    ITEMS.forEach(function (it) {
      ans[it.id] = { choice: st.choice[it.id] || null, choice_label: st.choice[it.id] ? label(it, st.choice[it.id]) : null, state: st.choice[it.id] === RQ ? 'question' : (st.choice[it.id] ? 'answered' : 'open'), note: st.note[it.id] || '', via: st.choice[it.id] ? (st.via[it.id] || 'single') : null,
        recommended: it.rec || null, avatar_prediction: it.av_pred || null, avatar_confidence: it.av_conf || null, marked: !!it.marked };
    });
    var out = { schema: DATA.schema, document_id: DATA.document_id, document_sha256: DATA.doc_sha256, saved_at: new Date().toISOString(),
      answers: ans, bulk_actions: st.bulk, gesamtabnahme: { explicit: !!st.gesamt.explicit, at: st.gesamt.at },
      counts: { total: ITEMS.length, answered: nAnswered(), questions: nQuestions(), open: ITEMS.length - nAnswered() - nQuestions() } };
    if (hasVorab()) out.agpl_bleibt = { choice: st.agpl.choice, note: st.agpl.note, state: st.agpl.choice ? 'answered' : 'open' };
    return out;
  }
  function summaryHtml(a) {
    var rows = ITEMS.map(function (it) { var x = a.answers[it.id];
      return '<tr><td>' + esc(it.id) + '</td><td>' + esc(it.question) + '</td><td>' + (x.state === 'question' ? '<i>Rückfrage</i>' : (x.choice ? esc(x.choice) + ': ' + esc(x.choice_label) : '<i>offen</i>')) + '</td><td>' + esc(x.note) + '</td></tr>'; }).join('');
    return '<section id="ergebnis"><h2>Deine Entscheidungen (gespeichert ' + esc(a.saved_at.replace('T', ' ').slice(0, 16)) + ' UTC)</h2><p>' + a.counts.answered + ' von ' + a.counts.total + ' beantwortet, ' + (a.counts.questions ? a.counts.questions + ' Rückfrage(n), ' : '') + a.counts.open + ' offen. Gesamtabnahme: ' + (a.gesamtabnahme.explicit ? 'ausdrücklich ja' : 'nicht erklärt') + '.' + (a.agpl_bleibt ? ' AGPL bleibt: ' + esc(a.agpl_bleibt.choice || 'offen') + (a.agpl_bleibt.note ? ' (' + esc(a.agpl_bleibt.note) + ')' : '') + '.' : '') + '</p><table><thead><tr><th>Kürzel</th><th>Frage</th><th>Entscheidung</th><th>Anmerkung</th></tr></thead><tbody>' + rows + '</tbody></table></section>';
  }
  function buildAnsweredHtml(a) {
    var clone = document.documentElement.cloneNode(true);
    clone.setAttribute('data-mode', 'answered');
    $$('#dlg', clone).forEach(function (d) { d.removeAttribute('open'); });
    $$('#toast', clone).forEach(function (t) { t.className = ''; t.textContent = ''; });
    $$('#save-links,#save-state', clone).forEach(function (e) { e.innerHTML = ''; });
    var js = document.createElement('script'); js.type = 'application/json'; js.id = 'embedded-answers';
    /* Jedes spitze Klammerzeichen, '&' und U+2028/2029 wird als Unicode-Escape geschrieben: schon ein Kommentaranfang mit Skript-Tag in einer Anmerkung wuerde das Skript-Parsing der Kopie kippen. Hier darf das Muster selbst nicht stehen. */
    js.textContent = JSON.stringify(a).replace(/[<>&\u2028\u2029]/g, function (c) { return '\\u' + ('0000' + c.charCodeAt(0).toString(16)).slice(-4); });
    var top = clone.querySelector('#top-panel'); var sec = document.createElement('div'); sec.innerHTML = summaryHtml(a);
    if (top && top.parentNode) top.parentNode.insertBefore(sec.firstChild, top);
    clone.querySelector('body').appendChild(js);
    return '<!doctype html>\n' + clone.outerHTML + '\n';
  }
  /* ---------- Sichern: nie von einem Dialog abhaengig (Regel 9) ---------- */
  function errName(e) { return (e && e.name) ? e.name : 'Fehler'; }
  function errText(e) { return errName(e) + (e && e.message ? ': ' + e.message : ''); }
  function say(html, cls) { var s = $('#save-state'); if (!s) return; s.innerHTML = html; s.className = cls || ''; }
  function fail(title, e) {
    say('<b>' + esc(title) + '</b> (' + esc(errText(e)) + '). Dein Stand geht dadurch nicht verloren: Nimm „Als Datei herunterladen“ oder „Antwort als Text kopieren“.', 'err');
  }
  function nowUtc() { return new Date().toISOString().replace('T', ' ').slice(0, 19) + ' UTC'; }

  /* Antwortdatei und beantwortete Kopie werden getrennt gebaut: scheitert die Kopie, bleibt die Antwort verfuegbar. */
  function makeFiles() {
    var out = { files: [], notes: [] }, a;
    try { a = buildAnswers(); out.json = JSON.stringify(a, null, 2) + '\n'; } catch (e) { out.fatal = e; return out; }
    out.files.push({ name: DATA.answer_name, text: out.json, type: 'application/json', label: 'Antwortdatei (nötig)' });
    try { out.files.push({ name: DATA.answered_name, text: buildAnsweredHtml(a), type: 'text/html', label: 'Beantwortete Kopie (optional)' }); }
    catch (e) { out.notes.push('Die beantwortete Kopie konnte nicht gebaut werden (' + esc(errText(e)) + '). Die Antwortdatei ist davon unabhängig verfügbar.'); }
    return out;
  }
  function showText(json) {
    var t = $('#answer-text'); if (!t) return;
    t.value = json || '';
    var box = $('#answer-box'); if (box) box.open = true;
  }
  /* Je Datei ein eigener sichtbarer Link: jeder Download ist eine eigene Nutzergeste, keiner startet von allein. */
  function renderLinks(files) {
    var box = $('#save-links'); if (!box) return;
    box.innerHTML = '';
    files.forEach(function (f) {
      var a = document.createElement('a');
      a.href = URL.createObjectURL(new Blob([f.text], { type: f.type })); a.download = f.name; a.className = 'dl';
      a.textContent = f.label + ': ' + f.name;
      a.addEventListener('click', function () {
        say('<b>Download angestoßen:</b> ' + esc(f.name) + '. Ob die Datei angekommen ist, kann diese Seite nicht prüfen: Schau in den Download-Ordner. Fehlt sie, nimm „Antwort als Text kopieren“.', 'warn');
      });
      box.appendChild(a); box.appendChild(document.createElement('br'));
    });
  }
  async function writeToFolder(files) {
    var dir = await window.showDirectoryPicker({ id: 'ticket-master-entscheidungen', mode: 'readwrite' });
    for (var i = 0; i < files.length; i++) {
      var fh = await dir.getFileHandle(files[i].name, { create: true });
      var w = await fh.createWritable(); await w.write(files[i].text); await w.close();
    }
    return dir.name;
  }
  function listMarked() { return ITEMS.filter(function (it) { return it.marked; }); }
  async function saveAndSend() {
    var open = ITEMS.filter(function (it) { return !st.choice[it.id]; });
    var qs = ITEMS.filter(function (it) { return st.choice[it.id] === RQ; });
    var marked = listMarked();
    var body = '<p>' + nAnswered() + ' von ' + ITEMS.length + ' beantwortet.</p>';
    if (open.length) body += '<p class="warn"><b>' + open.length + ' unbeantwortet:</b> ' + open.map(function (m) { return esc(m.id); }).join(', ') + '. Sie werden als <b>offen</b> gespeichert und nicht still ersetzt.</p>';
    if (qs.length) body += '<p class="warn"><b>' + qs.length + (qs.length === 1 ? ' Rückfrage' : ' Rückfragen') + ':</b> ' + qs.map(function (m) { return esc(m.id); }).join(', ') + '. Sie werden als <b>Rückfrage</b> gespeichert; deine Anmerkung gilt als Frage, nicht als Entscheidung.' + (qs.filter(function (m) { return !(st.note[m.id] || '').trim(); }).length ? ' Ohne Text in der Anmerkung: ' + qs.filter(function (m) { return !(st.note[m.id] || '').trim(); }).map(function (m) { return esc(m.id); }).join(', ') + '.' : '') + '</p>';
    if (hasVorab() && !st.agpl.choice) body += '<p class="warn">„AGPL bleibt“ ist noch offen.</p>';
    if (marked.length) body += '<p><b>Markierte Posten (rot, Löschung, Geld, Außenwirkung, Lizenz) noch einmal:</b></p><ul>' + marked.map(function (m) { return '<li><b>' + esc(m.id) + '</b> ' + esc(m.theme) + ': ' + (st.choice[m.id] ? esc(st.choice[m.id]) + ' (' + esc(label(m, st.choice[m.id])) + ')' + (st.via[m.id] === 'bulk' ? ', per Massenaktion' : '') : '<i>offen</i>') + ' <span class="muted">[' + esc(m.marked_reason) + ']</span></li>'; }).join('') + '</ul>';
    body += '<p>' + (st.gesamt.explicit ? 'Gesamtabnahme: <b>ausdrücklich ja</b>.' : 'Gesamtabnahme: nicht erklärt (Teilantwort).') + '</p>';
    body += '<p class="muted">Gleich öffnet dein Browser eine Ordnerwahl.' + (DATA.zielordner ? ' Gewünscht ist <code>' + esc(DATA.zielordner) + '</code>.' : '') + ' Lässt dein Browser den Ordner nicht zu oder brichst du ab, geht nichts verloren: Die Download-Links und der Text bleiben unten stehen.</p>';
    var r = await ask('Speichern und abschicken?', body, [{ id: 'back', label: 'Zurück zum Bearbeiten' }, { id: 'save', label: open.length ? 'Offene bleiben offen, speichern' : (qs.length ? 'Mit Rückfragen speichern' : 'Speichern'), primary: true }]);
    if (r.id !== 'save') return;
    var m = makeFiles();
    if (m.fatal) { fail('Die Antwort konnte nicht zusammengestellt werden', m.fatal); return; }
    showText(m.json); renderLinks(m.files); /* das Sicherungsnetz steht, BEVOR ein Dialog aufgeht */
    var notes = m.notes.length ? m.notes.join(' ') + ' ' : '';
    if (!window.showDirectoryPicker) {
      say(notes + '<b>Dieser Browser kann nicht direkt in einen Ordner schreiben.</b> Klicke unten auf die Links (je Datei einzeln) oder nimm „Antwort als Text kopieren“.', 'warn');
      return;
    }
    try {
      var dirName = await writeToFolder(m.files);
      say(notes + '<b>Gespeichert in „' + esc(dirName) + '“</b> um ' + nowUtc() + ': ' + m.files.map(function (f) { return esc(f.name); }).join(' und ') + ' vollständig geschrieben.<br>Der Browser kann keine Nachricht senden: <b>sag ticket-master Bescheid</b>.', 'ok');
      lsSet();
    } catch (e) {
      if (errName(e) === 'AbortError') say(notes + '<b>Speichern abgebrochen.</b> Es wurde nichts geschrieben. Du kannst jederzeit unten „Als Datei herunterladen“ (oder die Links) nehmen oder „Antwort als Text kopieren“.', 'warn');
      else say(notes + '<b>Speichern im Ordner hat nicht geklappt</b> (' + esc(errText(e)) + '). Möglicherweise liegt die erste Datei schon im Ordner: Prüfe das. Sicher geht es über die Links oder „Antwort als Text kopieren“.', 'err');
    }
  }
  function onDownload() {
    var m = makeFiles();
    if (m.fatal) { fail('Die Antwort konnte nicht zusammengestellt werden', m.fatal); return; }
    showText(m.json); renderLinks(m.files);
    try { $('#save-links a').click(); } /* eine Nutzergeste, genau EIN Download: die Antwortdatei */
    catch (e) { say('<b>Der Download konnte nicht angestoßen werden</b> (' + esc(errText(e)) + '). Die Links unten bleiben klickbar, oder nimm „Antwort als Text kopieren“.', 'err'); }
  }
  function onCopy() {
    var m = makeFiles();
    if (m.fatal) { fail('Die Antwort konnte nicht zusammengestellt werden', m.fatal); return; }
    showText(m.json);
    var t = $('#answer-text'); try { t.focus(); t.select(); } catch (e) { /* ignorieren */ }
    var manual = function (why) { say('<b>Kopieren geht nicht automatisch</b> (' + esc(why) + '). Markiere den Text im Feld unten und kopiere ihn mit Strg+C.', 'warn'); };
    if (!navigator.clipboard || !navigator.clipboard.writeText) { manual('keine Zwischenablage'); return; }
    navigator.clipboard.writeText(m.json).then(function () { say('<b>Kopiert.</b> Speichere den Text in eine Datei oder schick ihn weiter.', 'ok'); }, function (e) { manual(errName(e)); });
  }
  function onDraft() {
    try {
      var a = buildAnswers(); a.draft = true;
      var name = DATA.document_id + '.zwischenstand.json', x = document.createElement('a');
      x.href = URL.createObjectURL(new Blob([JSON.stringify(a, null, 2) + '\n'], { type: 'application/json' })); x.download = name; x.style.display = 'none';
      document.body.appendChild(x); x.click(); document.body.removeChild(x);
      say('<b>Zwischenstand-Download angestoßen:</b> ' + esc(name) + '. Ob er angekommen ist, kann diese Seite nicht prüfen: Schau in den Download-Ordner.', 'warn');
    } catch (e) { fail('Der Zwischenstand konnte nicht gesichert werden', e); }
  }

  /* ---------- Verdrahtung ---------- */
  function init() {
    answered = !!document.getElementById('embedded-answers');
    if (answered) { applyAnswered(); return; }
    var saved = lsGet();
    if (saved && saved.choice && Object.keys(saved.choice).length) {
      /* nur Werte uebernehmen, die zu diesem Formular passen: eine Option des Postens oder die Rueckfrage; Notizen nur als Text */
      Object.keys(saved.choice).forEach(function (id) {
        var it = BYID[id], v = saved.choice[id];
        if (it && typeof v === 'string' && (v === RQ || it.options.some(function (o) { return o.k === v; }))) st.choice[id] = v;
      });
      Object.keys(saved.note || {}).forEach(function (id) { if (BYID[id] && typeof saved.note[id] === 'string') st.note[id] = saved.note[id]; });
      Object.keys(saved.via || {}).forEach(function (id) { if (st.choice[id] && (saved.via[id] === 'single' || saved.via[id] === 'bulk')) st.via[id] = saved.via[id]; });
      st.agpl = saved.agpl || st.agpl; st.restored = saved.savedLocal || '';
      /* Gesamtabnahme und Massenaktions-Bestaetigungen werden NIE aus einem alten Stand uebernommen (nur Einzelwahlen und Anmerkungen) */
      restoreHint = !!(saved.gesamt && saved.gesamt.explicit);
    }
    $$('.item[data-id]').forEach(function (card) {
      var id = card.getAttribute('data-id');
      $$('input[type=radio]', card).forEach(function (r) { r.addEventListener('change', function () { st.choice[id] = r.value; st.via[id] = 'single'; touch(true); }); });
      var ta = $('textarea', card); ta.addEventListener('input', function () { st.note[id] = ta.value; lsSet(); });
      var rs = $('.reset', card); if (rs) rs.addEventListener('click', function () { delete st.choice[id]; delete st.via[id]; touch(true); });
    });
    $$('input[name=agpl]').forEach(function (r) { r.addEventListener('change', function () { st.agpl.choice = r.value; lsSet(); render(); }); });
    var an = $('#agpl-note'); if (an) an.addEventListener('input', function () { st.agpl.note = an.value; lsSet(); });
    $$('[data-bulk]').forEach(function (b) { b.addEventListener('click', function () { bulk(b.getAttribute('data-bulk')); }); });
    $$('.js-save').forEach(function (b) { b.addEventListener('click', function () { saveAndSend().catch(function (e) { fail('Unerwarteter Fehler beim Speichern', e); }); }); });
    var bd = $('#btn-download'); if (bd) bd.addEventListener('click', onDownload);
    var bc = $('#btn-copy'); if (bc) bc.addEventListener('click', onCopy);
    var bt = $('#btn-draft'); if (bt) bt.addEventListener('click', onDraft);
    var f = $('#only-open'); if (f) f.addEventListener('change', function () { document.body.classList.toggle('only-open', f.checked); render(); });
    var rr = $('#restore-reset'); if (rr) rr.addEventListener('click', function () { st.choice = {}; st.note = {}; st.via = {}; st.agpl = { choice: null, note: '' }; st.bulk = {}; st.gesamt = { explicit: false, at: null }; st.restored = null; restoreHint = false; lsClear(); render(); });
    document.body.classList.add('ready');
    render();
    if (restoreHint) toast('Gesamtabnahme nicht übernommen: Sie muss erneut ausdrücklich bestätigt werden.');
  }
  function applyAnswered() {
    var a = JSON.parse(document.getElementById('embedded-answers').textContent);
    ITEMS.forEach(function (it) { var x = a.answers[it.id]; if (x && x.choice) { st.choice[it.id] = x.choice; st.via[it.id] = x.via || 'single'; } st.note[it.id] = x ? x.note : ''; });
    if (a.agpl_bleibt) st.agpl = { choice: a.agpl_bleibt.choice, note: a.agpl_bleibt.note }; st.gesamt = a.gesamtabnahme;
    document.body.classList.add('answered');
    $$('input,textarea,button').forEach(function (e) { if (!e.classList.contains('keep')) e.disabled = true; });
    $$('.actions,.sticky-bar,.filter,#restore-note,#backup').forEach(function (e) { e.hidden = true; });
    render();
  }
  window.__FORM__ = { state: st, buildAnswers: buildAnswers, ITEMS: ITEMS };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
