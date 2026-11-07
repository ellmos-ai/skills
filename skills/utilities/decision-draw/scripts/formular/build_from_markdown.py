#!/usr/bin/env python3
"""Erzeugt das FORMULAR zum Entscheidungsdokument (eine selbstenthaltene HTML-Datei, kein Netz).

Quelle ist allein das Gesamtdokument (Markdown); Texte der Vorlagen und der Avatar-Bewertung werden nicht veraendert,
es kommen nur Formularelemente hinzu. Aus den Tabellen des Dokuments werden gelesen:
  - je Buendel: Kuerzel, Thema, Empfehlung, Geld/Loeschung/Aussen/Lizenz-Spalte, Avatar-Konfidenz,
  - Anhang Messung, Teil 1 (Frage, Optionen, Avatar-Wahl, Konfidenz) und Teil 2 (Empfehlung des Schreibers).
Es werden weder die versiegelte Messdatei noch Register oder Tickets gelesen oder geschrieben.

Aufruf:  python build_formular.py --md <ENTSCHEIDUNGEN_2026-11-07.md> --out <ENTSCHEIDUNGEN_2026-11-07_FORMULAR.html>
Hash:    document_sha256 = SHA-256 der Datei mit 64 Nullen an Stelle des Hashs (ohne Antworten, unveraendert).
"""
import argparse
import hashlib
import html as H
import json
import re
import sys
from pathlib import Path

import markdown

HERE = Path(__file__).resolve().parent
SCHEMA = "ticket-master.decision-answers.v1"
DOC_ID = "ENTSCHEIDUNGEN_2026-11-07"
ZERO = "0" * 64
SENS_RX = re.compile(r"L(ö|oe)schung|Geld|Außen|Lizenz|Rechte Dritter|Veröffentlichung")
SUBITEM_SENS = {"T2.3": "Rechte Dritter (Familie, Freunde)", "T2.5": "spätere Veröffentlichung"}  # T2.x erben sonst nichts aus der T2-Zeile
CONF = {"grün": "gruen", "gelb": "gelb", "rot": "rot"}


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def tables(lines, start=0, stop=None):
    """Liefert (header, rows) aller Pipe-Tabellen zwischen start und stop."""
    out, i, stop = [], start, stop or len(lines)
    while i < stop - 1:
        if lines[i].startswith("|") and re.match(r"^\|[\s:|\-]+\|$", lines[i + 1].strip()):
            header, rows, j = cells(lines[i]), [], i + 2
            while j < stop and lines[j].startswith("|"):
                rows.append(cells(lines[j]))
                j += 1
            out.append((header, rows))
            i = j
        else:
            i += 1
    return out


def parse_options(text):
    writer = "(Optionen vom Schreiber)" in text
    text = text.replace("(Optionen vom Schreiber)", "").strip().rstrip(";")
    parts = re.split(r"(?:^|;\s*)([A-C]):\s*", text)
    opts = [{"k": parts[i], "l": parts[i + 1].strip()} for i in range(1, len(parts) - 1, 2)]
    if not opts:
        raise ValueError(f"keine Optionen erkannt: {text!r}")
    return opts, writer


def parse_source(md_text):
    lines = md_text.splitlines()
    bundles = []  # (n, titel, start, stop)
    heads = [(i, m) for i, line in enumerate(lines) if (m := re.match(r"^## (.*)$", line))]
    for k, (i, m) in enumerate(heads):
        mb = re.match(r"B(?:ü|ue)ndel (\d+): (.*)", m.group(1))
        if mb:
            stop = heads[k + 1][0] if k + 1 < len(heads) else len(lines)
            bundles.append((int(mb.group(1)), mb.group(2), i, stop))
    brow = {}  # Kuerzel -> dict
    for n, titel, a, b in bundles:
        for header, rows in tables(lines, a, b):
            if header and header[0] == "Kürzel":
                fi = next((k for k, h in enumerate(header) if re.search(r"L(ö|oe)schung|Geld", h)), None)
                ri = next((k for k, h in enumerate(header) if "Empfehlung" in h), 2)
                for r in rows:
                    brow[r[0]] = {"bundle": n, "theme": r[1], "rec_text": r[ri], "sens_text": r[fi] if fi is not None else "", "table_conf": r[-1]}
    i1 = next(i for i, line in enumerate(lines) if line.startswith("#### Teil 1"))
    i2 = next(i for i, line in enumerate(lines) if line.startswith("#### Teil 2"))
    t1 = next(t for t in tables(lines, i1, i2) if t[0][0] == "Zeile")
    t2 = next(t for t in tables(lines, i2, len(lines)) if t[0][0] == "Zeile")
    rec = {}
    for r in t2[1]:
        m = re.match(r"([A-C])\b\s*(.*)$", r[1])
        rec[r[0]] = (m.group(1), m.group(2).strip()) if m else (None, r[1])
    items = []
    for r in t1[1]:
        id_, frage, optx, av, conf = r[0], r[1], r[2], r[3], r[4]
        opts, writer = parse_options(optx)
        base = id_.split(".")[0]
        b = brow.get(id_) or brow[base]
        sens = []
        if conf == "rot":
            sens.append("rot: Avatar ohne Vorhersage")
        t = b["sens_text"] if "." not in id_ else SUBITEM_SENS.get(id_, "")
        if "." in id_ and id_ in SUBITEM_SENS:
            sens.append(SUBITEM_SENS[id_])
        elif "." not in id_ and SENS_RX.search(t):
            sens.append(t)
        rk, rnote = rec.get(id_, (None, ""))
        items.append({
            "id": id_, "bundle": b["bundle"], "theme": b["theme"], "question": frage, "options": opts, "writer_options": writer,
            "rec": rk, "rec_note": rnote, "av_pred": None if av == "offen" else av, "av_conf": conf,
            "marked": bool(sens), "marked_reason": "; ".join(sens), "sens_text": t,
        })
    return items, {n: t for n, t, *_ in bundles}


def card(it):
    badges = []
    if it["rec"]:
        badges.append(f'<span class="badge rec">Empfehlung des Schreibers: {H.escape(it["rec"])}{(" " + H.escape(it["rec_note"])) if it["rec_note"] else ""}</span>')
    else:
        badges.append('<span class="badge">keine Empfehlung</span>')
    ap = f'Avatar: {H.escape(it["av_pred"])}' if it["av_pred"] else "Avatar: keine Vorhersage"
    badges.append(f'<span class="badge {CONF.get(it["av_conf"], "")}">{ap} · {H.escape(it["av_conf"])}</span>')
    if it["marked"]:
        badges.append(f'<span class="badge sens">markiert: {H.escape(it["marked_reason"])}</span>')
    if it["writer_options"]:
        badges.append('<span class="badge">Optionen vom Schreiber</span>')
    opts = []
    for o in it["options"]:
        mark = '<span class="recmark">Empfehlung</span>' if o["k"] == it["rec"] else ""
        opts.append(f'<label class="opt"><input type="radio" name="{H.escape(it["id"])}" value="{o["k"]}"><span><b>{o["k"]}</b> {H.escape(o["l"])}</span>{mark}</label>')
    return (f'<fieldset class="item" id="item-{H.escape(it["id"])}" data-id="{H.escape(it["id"])}" data-bundle="{it["bundle"]}" data-marked="{1 if it["marked"] else 0}">'
            f'<legend><span class="kid">{H.escape(it["id"])}</span> {H.escape(it["question"])}</legend>'
            f'<div class="badges">{"".join(badges)}</div><div class="opts">{"".join(opts)}</div>'
            f'<textarea aria-label="Anmerkung zu {H.escape(it["id"])}" placeholder="Anmerkung (frei, optional)"></textarea>'
            f'<div class="row"><button type="button" class="reset">Antwort zurücknehmen</button><span class="via"></span></div></fieldset>')


def bundle_block(n, titel, items):
    mine = [i for i in items if i["bundle"] == n]
    extra = ""
    if n == 1:
        extra = ('<fieldset class="item agpl" id="item-AGPL"><legend>Vorab: „AGPL bleibt“</legend>'
                 '<p class="muted">Das hat heute der Entscheidungs-Avatar gebucht, nicht du. Bestätigen oder korrigieren? Die Variantenfrage (V1) steht getrennt darunter.</p>'
                 '<div class="opts"><label class="opt"><input type="radio" name="agpl" value="bestätigen"><span><b>bestätigen</b> AGPL bleibt für die Dokument-Apps</span></label>'
                 '<label class="opt"><input type="radio" name="agpl" value="korrigieren"><span><b>korrigieren</b> (bitte in der Anmerkung sagen, wie)</span></label></div>'
                 '<textarea id="agpl-note" aria-label="Anmerkung zu AGPL bleibt" placeholder="Anmerkung (frei, optional)"></textarea></fieldset>')
    return (f'<section class="bundle-form" id="antwort-b{n}"><h3>Deine Antworten zu Bündel {n}: {H.escape(titel)}</h3>'
            f'<div class="row actions"><button type="button" data-bulk="{n}">Alle wie empfohlen (Bündel {n})</button>'
            f'<span class="muted" id="bcount-{n}">0 von {len(mine)} beantwortet</span></div>{extra}{"".join(card(i) for i in mine)}</section>')


def build(md_path):
    md_text = Path(md_path).read_text(encoding="utf-8")
    items, titles = parse_source(md_text)
    m = markdown.Markdown(extensions=["toc", "tables"], extension_configs={"toc": {"title": "Inhalt", "toc_depth": "2-3"}})
    body = m.convert(md_text)
    title = re.match(r"# (.*)", md_text).group(1)
    # Formularbloecke je Buendel vor das Ende des Buendels (vor die letzte <hr /> vor der naechsten h2)
    for n in sorted(titles, reverse=True):
        h = re.search(r'<h2 id="[^"]+">B(?:ü|ue)ndel %d:' % n, body)
        nxt = body.find("<h2", h.end())
        cut = body.rfind("<hr />", h.end(), nxt)
        pos = cut if cut != -1 else nxt
        body = body[:pos] + bundle_block(n, titles[n], items) + "\n" + body[pos:]
    nav = " ".join(f'<a href="#antwort-b{n}">Bündel {n}</a>' for n in sorted(titles))
    panel = ('<section class="panel" id="top-panel"><h2 id="antwortbogen">Antwortbogen</h2>'
             '<p>Hier direkt anklicken statt im Chat zu antworten. Nichts ist vorausgewählt. Am Ende „Speichern und abschicken“: Es entstehen die Antwortdatei und eine Kopie dieses Dokuments mit deinen Entscheidungen. '
             'Die Hinweise zur Antwort im Chat weiter unten gelten weiter, du musst sie aber nicht benutzen. Dieses Formular schreibt nichts in Register oder Tickets.</p>'
             '<div class="row"><b class="js-progress">0 von %d beantwortet</b><label class="filter"><input type="checkbox" id="only-open"> nur unbeantwortete zeigen</label></div>'
             '<div class="bar"><i class="js-bar"></i></div><p class="nav">Antworten: %s</p>'
             '<div class="row actions"><button type="button" class="primary" data-bulk="all">Alles wie empfohlen</button>'
             '<button type="button" class="primary js-save">Speichern und abschicken</button></div>'
             '<p id="gesamt-state" class="muted">Gesamtabnahme: nicht erklärt</p>'
             '<div id="restore-note" class="warn" hidden><span id="restore-text"></span> <button type="button" id="restore-reset">Zwischenstand verwerfen</button></div>'
             '<div id="backup"><p class="muted">Gewünschter Ordner für „Speichern und abschicken“: <code>.USR\\entscheidungen</code>. '
             'Lässt Edge diesen Ordner nicht zu oder brichst du ab, geht nichts verloren: Die drei Knöpfe hier funktionieren jederzeit, ohne Ordnerwahl.</p>'
             '<div class="row actions"><button type="button" id="btn-download">Als Datei herunterladen</button>'
             '<button type="button" id="btn-copy">Antwort als Text kopieren</button><button type="button" id="btn-draft">Zwischenstand sichern</button></div>'
             '<div id="save-state" role="status" aria-live="polite"></div><div id="save-links"></div>'
             '<details id="answer-box"><summary>Antwort als Text (JSON)</summary><p class="muted">Kopiere den Text in eine Datei oder schick ihn weiter.</p>'
             '<textarea id="answer-text" readonly rows="8" aria-label="Antwort als Text (JSON)"></textarea></details></div></section>') % (len(items), nav)
    t1 = body.index("</h1>") + len("</h1>")  # Antwortbogen direkt unter der Ueberschrift, vor dem langen Inhaltsverzeichnis
    body = body[:t1] + "\n" + panel + body[t1:]
    css_base = ('<style>\n:root{--bg:#fdfdfb;--fg:#1d1f21;--muted:#5b6168;--line:#d9dcdf;--accent:#1f5fae;--code:#f1f2f4;--head:#eef2f7}\n'
                '@media (prefers-color-scheme: dark){:root{--bg:#16181b;--fg:#e6e8ea;--muted:#a3a9b0;--line:#33383e;--accent:#7fb2ff;--code:#22262b;--head:#1f242b}}\n'
                'html{background:var(--bg)}body{background:var(--bg);color:var(--fg);font:16px/1.6 "Segoe UI",system-ui,sans-serif;max-width:60rem;margin:0 auto;padding:1.5rem 16px 4rem}\n'
                'h1,h2,h3,h4{line-height:1.25;margin-top:2em}h1{font-size:1.9rem;margin-top:.5em}h2{border-bottom:1px solid var(--line);padding-bottom:.3em}\n'
                'a{color:var(--accent)}code{background:var(--code);padding:.1em .3em;border-radius:4px;font-size:.92em;word-break:break-word}\n'
                'table{border-collapse:collapse;width:100%;display:block;overflow-x:auto;margin:1em 0}th,td{border:1px solid var(--line);padding:.4em .6em;vertical-align:top;text-align:left}\n'
                'th{background:var(--head)}hr{border:0;border-top:2px solid var(--line);margin:2.5em 0}\n.toc{background:var(--head);border:1px solid var(--line);border-radius:6px;padding:.6em 1.2em}.toc .toctitle{font-weight:600}\n</style>\n')
    css = (HERE / "formular.css").read_text(encoding="utf-8")
    js = (HERE / "formular.js").read_text(encoding="utf-8")
    data = {"schema": SCHEMA, "document_id": DOC_ID, "doc_sha256": ZERO, "answer_name": f"{DOC_ID}.antwort.json",
            "answered_name": f"{DOC_ID}_BEANTWORTET.html", "zielordner": ".USR\\entscheidungen", "items": items}
    data_json = json.dumps(data, ensure_ascii=False, indent=1).replace("</", "<\\/")
    page = ('<!doctype html>\n<html lang="de">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<meta name="document-id" content="{DOC_ID}">\n<meta name="document-sha256" content="{ZERO}">\n<meta name="color-scheme" content="light dark">\n'
            f'<title>{H.escape(title)} – Formular</title>\n{css_base}<style>\n{css}</style>\n</head>\n<body>\n{body}\n'
            '<div class="sticky-bar"><div class="grow"><span class="js-progress">0 von {{N}} beantwortet</span><div class="bar"><i class="js-bar"></i></div></div>'
            '<button type="button" class="primary js-save">Speichern und abschicken</button></div>\n'
            '<dialog id="dlg" aria-labelledby="dlg-title"><h3 id="dlg-title" style="margin-top:0"></h3><div id="dlg-body"></div><div id="dlg-buttons"></div></dialog>\n'
            '<div id="toast" role="status" aria-live="polite"></div>\n'
            f'<script type="application/json" id="form-data">\n{data_json}\n</script>\n<script>\n{js}</script>\n</body>\n</html>\n').replace("{{N}}", str(len(items)))
    digest = hashlib.sha256(page.encode("utf-8")).hexdigest()
    return page.replace(ZERO, digest), digest, items


def blank_hash(page_text):
    """Hash des unveraenderten Formulars: den eingebetteten Hash durch Nullen ersetzen und neu rechnen."""
    d = re.search(r'name="document-sha256" content="([0-9a-f]{64})"', page_text).group(1)
    return d, hashlib.sha256(page_text.replace(d, ZERO).encode("utf-8")).hexdigest()


def validate_answers(obj, items, expected_sha=None):
    """Prueft eine Antwortdatei (ticket-master.decision-answers.v1) gegen die Posten des Formulars. Liefert eine Liste von Fehlern (leer = gueltig)."""
    err = []
    need = {"schema", "document_id", "document_sha256", "saved_at", "answers", "agpl_bleibt", "bulk_actions", "gesamtabnahme", "counts"}
    if not isinstance(obj, dict) or not need <= set(obj):
        return [f"Pflichtfelder fehlen: {sorted(need - set(obj if isinstance(obj, dict) else []))}"]
    if obj["schema"] != SCHEMA:
        err.append("schema")
    if obj["document_id"] != DOC_ID:
        err.append("document_id")
    if not re.fullmatch(r"[0-9a-f]{64}", str(obj["document_sha256"])) or (expected_sha and obj["document_sha256"] != expected_sha):
        err.append("document_sha256")
    if not re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(\.\d+)?Z", str(obj["saved_at"])):
        err.append("saved_at (UTC, ISO)")
    by_id = {i["id"]: i for i in items}
    if set(obj["answers"]) != set(by_id):
        err.append("answers: Kuerzel stimmen nicht mit dem Formular ueberein")
    for k, a in obj["answers"].items():
        it = by_id.get(k)
        if not it:
            continue
        keys = {"choice", "choice_label", "state", "note", "via", "recommended", "avatar_prediction", "avatar_confidence", "marked"}
        if not keys <= set(a):
            err.append(f"{k}: Felder fehlen {sorted(keys - set(a))}")
            continue
        valid = {o["k"]: o["l"] for o in it["options"]}
        if a["state"] == "answered":
            if a["choice"] not in valid or a["choice_label"] != valid[a["choice"]]:
                err.append(f"{k}: choice/choice_label passt nicht zu den Optionen")
        elif a["state"] == "question":
            if a["choice"] != "rueckfrage":
                err.append(f"{k}: Rueckfrage, aber choice ist nicht 'rueckfrage'")
        elif a["state"] == "open":
            if a["choice"] is not None:
                err.append(f"{k}: offen, aber choice gesetzt")
        else:
            err.append(f"{k}: state")
        if a["recommended"] != it["rec"] or a["avatar_prediction"] != it["av_pred"] or a["avatar_confidence"] != it["av_conf"]:
            err.append(f"{k}: recommended/avatar weichen vom Formular ab")
        if not isinstance(a["note"], str):
            err.append(f"{k}: note")
    n_ans = sum(1 for a in obj["answers"].values() if a.get("state") == "answered")
    n_q = sum(1 for a in obj["answers"].values() if a.get("state") == "question")
    expected = {"total": len(items), "answered": n_ans, "open": len(items) - n_ans}
    if "questions" in obj["counts"]:  # Schema v1, erweitert um die Wahl Rueckfrage
        expected = {"total": len(items), "answered": n_ans, "questions": n_q, "open": len(items) - n_ans - n_q}
    if obj["counts"] != expected:
        err.append("counts")
    if not isinstance(obj["gesamtabnahme"].get("explicit"), bool) or not isinstance(obj["bulk_actions"], dict):
        err.append("gesamtabnahme/bulk_actions")
    if obj["gesamtabnahme"].get("explicit") and any(by_id[k]["rec"] and a.get("choice") != by_id[k]["rec"] for k, a in obj["answers"].items() if k in by_id):
        err.append("gesamtabnahme.explicit=true, aber nicht alle Posten wie empfohlen")
    if obj["agpl_bleibt"].get("choice") not in (None, "bestätigen", "korrigieren"):
        err.append("agpl_bleibt")
    return err


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--md", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    page, digest, items = build(a.md)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(page, encoding="utf-8", newline="\n")
    print(f"geschrieben: {a.out} | {len(page)} Zeichen | {len(items)} Posten | document_sha256 {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
