#!/usr/bin/env python3
"""Baut aus einer kleinen Daten-JSON EIN selbstenthaltenes HTML-Formular (kein Netz, kein Markdown-Gesamtdokument noetig).

Standardweg fuer Entscheidungsvorlagen: Daten schreiben (Format: form.schema.json, Beispiel: example_form.json), dieses Skript aufrufen,
Formular pruefen lassen, zustellen. Das Formular wird nicht jedes Mal neu gebaut; Template (formular.html), Skript (formular.js) und
Stil (form_base.css, formular.css) bleiben gleich.

Aufruf:  python build_form.py <daten.json> --out <formular.html>
Pruefen: Laengengrenzen (Kontext, Wirkung, Grund, ...) und Pflichtfelder sind FEHLER mit Hinweis, nie stilles Kuerzen; Bilder werden als
data:-URI eingebettet (je Bild und gesamt begrenzt, sonst Fehler). Details (details_markdown) werden vor der Umwandlung escaped.
Hash:    document_sha256 = SHA-256 der Datei mit 64 Nullen an Stelle des Hashs (ohne Antworten, unveraendert).
Antwort: ticket-master.decision-answers.v1, erweitert um die Wahl 'rueckfrage' (state 'question') und counts.questions; validate_answers().
"""
import argparse
import base64
import binascii
import hashlib
import html as H
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA = "ticket-master.decision-answers.v1"
DATA_SCHEMA = "ellmos.decision-form.v1"
ZERO = "0" * 64
RQ = "rueckfrage"
RQ_LABEL = "Rückfrage / mehr Info nötig"
LIMITS = {"titel": 80, "kontext_kurz": 400, "kontext": 250, "frage": 200, "label": 100, "wirkung": 160, "grund": 160,
          "kosten_aufwand": 160, "risiko_rueckgaengig": 160, "frist": 160, "folge_bei_nein": 160, "beschriftung": 120,
          "sensitiv_grund": 100, "alt": 200, "seite": 60, "variante": 60, "zielordner": 120, "details_markdown": 4000}
IMG_MAX = 400 * 1024
IMG_TOTAL_MAX = 8 * 1024 * 1024
IMG_TYPES = {"image/png", "image/jpeg", "image/webp", "image/gif"}
EXT_TYPES = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp", ".gif": "image/gif"}
CONF = {"grün": "grün", "gruen": "grün", "gelb": "gelb", "rot": "rot"}
ID_RX = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,39}")
OPT_RX = re.compile(r"[A-Za-z0-9]{1,3}")
DOC_KEYS = {"schema", "dokument_id", "titel", "kontext_kurz", "zielordner", "buendel"}
BUNDLE_KEYS = {"id", "titel", "posten"}
POST_KEYS = {"kuerzel", "titel", "kontext", "frage", "optionen", "empfehlung", "kosten_aufwand", "risiko_rueckgaengig", "frist", "folge_bei_nein",
             "avatar", "sensitiv", "sensitiv_grund", "details_markdown", "bilder"}
IMG_KEYS = {"pfad", "data_uri", "beschriftung", "alt", "seite", "variante"}
HINT = " Kürze den Text; Längeres gehört in details_markdown."


class FormError(Exception):
    """Sammelt alle Fehler der Daten; nichts wird still gekuerzt oder ersetzt."""

    def __init__(self, errors):
        self.errors = list(errors)
        super().__init__("\n".join(self.errors))


def decode_data_uri(uri):
    m = re.fullmatch(r"data:([a-z]+/[a-z0-9.+-]+);base64,([A-Za-z0-9+/=\s]+)", str(uri).strip())
    if not m:
        raise ValueError("kein base64-data:-URI")
    try:
        return m.group(1), base64.b64decode(m.group(2), validate=False)
    except (binascii.Error, ValueError) as exc:
        raise ValueError(f"base64 ungültig: {exc}") from exc


def embed_json(obj, **kwargs):
    """JSON fuer ein <script type="application/json">: JEDES '<' (auch '<!--<script>'), '>' und '&' sowie U+2028/2029 als \\uXXXX.
    Allein '</' zu schuetzen reicht nicht: '<!--<script>' schaltet den HTML-Parser in den doppelt maskierten Zustand."""
    text = json.dumps(obj, ensure_ascii=False, **kwargs)
    for char in "<>&\u2028\u2029":
        text = text.replace(char, "\\u%04x" % ord(char))
    return text


def _magic_ok(mime, raw):
    return ((mime == "image/png" and raw[:8] == b"\x89PNG\r\n\x1a\n") or (mime == "image/jpeg" and raw[:2] == b"\xff\xd8")
            or (mime == "image/gif" and raw[:4] == b"GIF8") or (mime == "image/webp" and raw[:4] == b"RIFF" and raw[8:12] == b"WEBP"))


def _text(errs, where, obj, name, limit=None, required=True):
    """Pflichtfeld/optionales Feld als Text pruefen; Laengenueberschreitung ist ein Fehler mit Hinweis."""
    value = obj.get(name) if isinstance(obj, dict) else None
    if value is None or (isinstance(value, str) and not value.strip()):
        if required:
            errs.append(f"{where}: {name} fehlt (darf 'keine' lauten, aber nicht fehlen)." if name in ("kosten_aufwand", "risiko_rueckgaengig", "folge_bei_nein")
                        else f"{where}: {name} fehlt.")
        return None
    if not isinstance(value, str):
        errs.append(f"{where}: {name} muss Text sein.")
        return None
    limit = LIMITS.get(name) if limit is None else limit
    if limit and len(value) > limit:
        errs.append(f"{where}: {name} hat {len(value)} Zeichen (Limit {limit})." + HINT)
    return value


def _unknown(errs, where, obj, allowed):
    for key in obj:
        if key not in allowed:
            errs.append(f"{where}: unbekanntes Feld '{key}' (erlaubt: {', '.join(sorted(allowed))}).")


def _inside(value, base_dir):
    """Bildpfad -> Path, der nach resolve() UNTER dem Datenordner liegt, sonst ValueError.

    Erst rein textuell pruefen (absolut, UNC, Laufwerk, \\\\?\\, '..'), also BEVOR irgendein Dateisystemzugriff
    stattfindet: ein UNC-Pfad wuerde unter Windows sonst eine SMB-Verbindung zu einem fremden Rechner oeffnen.
    Danach resolve() und relative_to(): Symlinks und Junctions, die aus dem Ordner hinausfuehren, werden abgelehnt."""
    if not isinstance(value, str) or not value.strip() or "\x00" in value:
        raise ValueError("pfad muss ein nicht leerer Text sein")
    text = value.replace("\\", "/")
    if text.startswith("/") or re.match(r"^[A-Za-z]:", text) or Path(value).is_absolute():
        raise ValueError("pfad: absolute, UNC- und Laufwerkspfade sind nicht erlaubt; nur relativ zum Datenordner")
    parts = [p for p in text.split("/") if p not in ("", ".")]
    if ".." in parts:
        raise ValueError("pfad: '..' ist nicht erlaubt; die Datei muss im Datenordner liegen")
    base = Path(base_dir).resolve()
    target = (base / "/".join(parts)).resolve()
    try:
        target.relative_to(base)
    except ValueError:
        raise ValueError("pfad: die Datei liegt nach dem Aufloesen von Links ausserhalb des Datenordners") from None
    return target


def _image(errs, where, img, base_dir, sizes):
    """Liefert (mime, bytes) oder None; Fehler landen in errs."""
    if not isinstance(img, dict):
        errs.append(f"{where}: Bild muss ein Objekt sein.")
        return None
    _unknown(errs, where, img, IMG_KEYS)
    _text(errs, where, img, "beschriftung")
    for opt in ("alt", "seite", "variante"):
        _text(errs, where, img, opt, required=False)
    if ("pfad" in img) == ("data_uri" in img):
        errs.append(f"{where}: genau eines von pfad oder data_uri angeben.")
        return None
    try:
        if "data_uri" in img:
            mime, raw = decode_data_uri(img["data_uri"])
        else:
            path = _inside(img["pfad"], base_dir)
            mime = EXT_TYPES.get(path.suffix.lower())
            if mime is None:
                errs.append(f"{where}: Bildtyp {path.suffix or '(keiner)'} nicht erlaubt (png, jpg, webp, gif; kein svg).")
                return None
            raw = path.read_bytes()
    except (OSError, ValueError) as exc:
        errs.append(f"{where}: Bild nicht lesbar ({exc}).")
        return None
    if mime not in IMG_TYPES:
        errs.append(f"{where}: Bildtyp {mime} nicht erlaubt (png, jpeg, webp, gif).")
        return None
    if len(raw) > IMG_MAX:
        errs.append(f"{where}: {len(raw)} Byte sind zu groß (Limit {IMG_MAX} Byte, etwa {IMG_MAX // 1024} KB). Verkleinere das Bild (Breite höchstens 1200 px).")
        return None
    if not _magic_ok(mime, raw):
        errs.append(f"{where}: Dateiinhalt ist kein {mime}.")
        return None
    sizes.append(len(raw))
    return mime, raw


CONTROL_RX = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]")
URL_NOISE_RX = re.compile(r"[\x00-\x20\x7f-\x9f]")  # was ein Browser in einer URL ignoriert: Leerraum und Steuerzeichen
LINK_OK_RX = re.compile(r"^(?:https?:|mailto:|#|/|\./)", re.I)
URL_ATTR_RX = re.compile(r'(\b(?:href|src|action|formaction|xlink:href|srcset|poster|background|data)\s*=\s*)"([^"]*)"', re.I)


def clean_url(raw):
    """Wie ein Browser lesen, dann pruefen: Entities aufloesen, Leerraum und Steuerzeichen entfernen (java<LF>script:,
    <0x01>javascript:), kleinschreiben. Der geprueft Wert ist EXAKT der ausgegebene (T-20261107, F1 der Pruefung von #98)."""
    value = raw
    for _ in range(5):
        decoded = H.unescape(value)
        if decoded == value:
            break
        value = decoded
    return URL_NOISE_RX.sub("", value)


def render_details(md_text, where, errs):
    try:
        import markdown
    except ImportError:
        errs.append(f"{where}: details_markdown braucht das Paket markdown (pip install markdown).")
        return ""
    if CONTROL_RX.search(md_text):
        errs.append(f"{where}: Steuerzeichen in details_markdown (nur Tab, Zeilenumbruch und Wagenruecklauf sind erlaubt).")
        return ""
    out = markdown.markdown(H.escape(md_text, quote=False), extensions=["tables"])
    if re.search(r"<img\b", out, re.I):
        errs.append(f"{where}: Bilder gehoeren in bilder[], nicht in details_markdown (ein Bild aus dem Netz waere eine Verbindung).")
        return ""

    def check(match):
        value = clean_url(match.group(2))
        if not LINK_OK_RX.match(value):
            errs.append(f"{where}: Link nicht erlaubt in details_markdown: {value[:40]!r} "
                        "(erlaubt sind http:, https:, mailto:, #, / und ./).")
        return f'{match.group(1)}"{H.escape(value, quote=True)}"'

    return URL_ATTR_RX.sub(check, out)


def normalize(data, base_dir):
    """Prueft die Daten und liefert (posten_je_buendel, items, bilder_je_posten, details_je_posten). Wirft FormError mit ALLEN Fehlern."""
    errs, items, images, details = [], [], {}, {}
    if not isinstance(data, dict):
        raise FormError(["Die Daten müssen ein JSON-Objekt sein."])
    _unknown(errs, "Dokument", data, DOC_KEYS)
    if data.get("schema") != DATA_SCHEMA:
        errs.append(f"Dokument: schema muss '{DATA_SCHEMA}' sein.")
    if not ID_RX.fullmatch(str(data.get("dokument_id", ""))):
        errs.append("Dokument: dokument_id fehlt oder enthält unerlaubte Zeichen (erlaubt: Buchstaben, Ziffern, _ . -).")
    _text(errs, "Dokument", data, "titel")
    _text(errs, "Dokument", data, "kontext_kurz")
    _text(errs, "Dokument", data, "zielordner", required=False)
    bundles = data.get("buendel")
    if not isinstance(bundles, list) or not bundles:
        raise FormError(errs + ["Dokument: buendel fehlt oder ist leer."])
    seen, sizes = set(), []
    for bi, b in enumerate(bundles, 1):
        w = f"Bündel {bi}"
        if not isinstance(b, dict):
            errs.append(f"{w}: muss ein Objekt sein.")
            continue
        _unknown(errs, w, b, BUNDLE_KEYS)
        if not ID_RX.fullmatch(str(b.get("id", ""))):
            errs.append(f"{w}: id fehlt oder ungültig.")
        _text(errs, w, b, "titel")
        posts = b.get("posten")
        if not isinstance(posts, list) or not posts:
            errs.append(f"{w}: posten fehlt oder ist leer.")
            continue
        for p in posts:
            k = str(p.get("kuerzel", "?")) if isinstance(p, dict) else "?"
            w = f"Posten {k}"
            if not isinstance(p, dict):
                errs.append(f"{w}: muss ein Objekt sein.")
                continue
            _unknown(errs, w, p, POST_KEYS)
            if not ID_RX.fullmatch(k):
                errs.append(f"{w}: kuerzel fehlt oder ungültig.")
            if k in seen:
                errs.append(f"{w}: Kürzel doppelt.")
            seen.add(k)
            for name in ("titel", "kontext", "frage", "kosten_aufwand", "risiko_rueckgaengig", "folge_bei_nein"):
                _text(errs, w, p, name)
            _text(errs, w, p, "frist", required=False)
            opts = p.get("optionen")
            ids = []
            if not isinstance(opts, list) or not 2 <= len(opts) <= 6:
                errs.append(f"{w}: Optionen müssen 2 bis 6 Einträge haben.")
                opts = []
            for o in opts:
                oid = str(o.get("id", "")) if isinstance(o, dict) else ""
                wo = f"{w}, Option {oid or '?'}"
                if not isinstance(o, dict) or not OPT_RX.fullmatch(oid) or oid in ids:
                    errs.append(f"{wo}: id fehlt, ungültig oder doppelt.")
                    continue
                ids.append(oid)
                _text(errs, wo, o, "label")
                _text(errs, wo, o, "wirkung")
            rec = p.get("empfehlung")
            rec_opt = rec_note = None
            if rec is not None:
                if not isinstance(rec, dict) or rec.get("option") not in ids:
                    errs.append(f"{w}: Empfehlung nennt keine vorhandene Option.")
                else:
                    rec_opt = rec["option"]
                    rec_note = _text(errs, f"{w}, Empfehlung", rec, "grund")
            av, av_pred, av_conf = p.get("avatar"), None, None
            if av is not None:
                if not isinstance(av, dict) or av.get("konfidenz") not in CONF or (av.get("wahl") is not None and av.get("wahl") not in ids):
                    errs.append(f"{w}: avatar braucht konfidenz (grün, gelb, rot) und eine vorhandene Option als wahl (oder null).")
                else:
                    av_pred, av_conf = av.get("wahl"), CONF[av["konfidenz"]]
            sens = bool(p.get("sensitiv", False))
            reason = _text(errs, w, p, "sensitiv_grund", required=False) or "sensibel"
            if p.get("details_markdown") is not None:
                text = _text(errs, w, p, "details_markdown")
                if text:
                    details[k] = render_details(text, w, errs)
            imgs = []
            if p.get("bilder") is not None:
                if not isinstance(p["bilder"], list) or len(p["bilder"]) > 12:
                    errs.append(f"{w}: bilder muss eine Liste mit höchstens 12 Bildern sein.")
                else:
                    for n, img in enumerate(p["bilder"], 1):
                        got = _image(errs, f"{w}, Bild {n}", img, base_dir, sizes)
                        if got:
                            imgs.append((img, got))
            images[k] = imgs
            labels = {o["id"]: o["label"] for o in opts if isinstance(o, dict) and o.get("id") in ids}
            items.append({
                "id": k, "bundle": bi, "theme": p.get("titel", ""), "question": p.get("frage", ""),
                "options": [{"k": i, "l": labels[i]} for i in ids if i in labels], "writer_options": False,
                "rec": rec_opt, "rec_note": rec_note or "", "av_pred": av_pred, "av_conf": av_conf,
                "marked": sens, "marked_reason": reason if sens else "",
            })
    if sum(sizes) > IMG_TOTAL_MAX:
        errs.append(f"Bilder Gesamt: {sum(sizes)} Byte (Limit {IMG_TOTAL_MAX} Byte, etwa {IMG_TOTAL_MAX // (1024 * 1024)} MB). Weniger oder kleinere Bilder verwenden.")
    if errs:
        raise FormError(errs)
    return images, details, items


def _card(p, it, imgs, detail_html):
    e = H.escape
    pid = e(it["id"])
    badges = []
    if it["rec"]:
        badges.append(f'<span class="badge rec">Empfehlung: {e(it["rec"])}. {e(it["rec_note"])}</span>')
    else:
        badges.append('<span class="badge">keine Empfehlung</span>')
    if it["av_conf"]:
        pred = f'Avatar: {e(it["av_pred"])}' if it["av_pred"] else "Avatar: keine Vorhersage"
        badges.append(f'<span class="badge {"gruen" if it["av_conf"] == "grün" else e(it["av_conf"])}">{pred} · {e(it["av_conf"])}</span>')
    if it["marked"]:
        badges.append(f'<span class="badge sens">markiert: {e(it["marked_reason"])}</span>')
    opts = []
    for o, src in zip(it["options"], p["optionen"]):
        mark = '<span class="recmark">Empfehlung</span>' if o["k"] == it["rec"] else ""
        opts.append(f'<label class="opt"><input type="radio" name="{pid}" value="{e(o["k"])}"><span><b>{e(o["k"])}</b> {e(o["l"])}'
                    f'<span class="wirkung">{e(src["wirkung"])}</span></span>{mark}</label>')
    opts.append(f'<label class="opt rq"><input type="radio" name="{pid}" value="{RQ}"><span><b>?</b> {RQ_LABEL}'
                '<span class="wirkung">Schreib deine Frage in die Anmerkung; sie gilt dann als Frage, nicht als Entscheidung.</span></span></label>')
    facts = [("Kosten / Aufwand", p["kosten_aufwand"]), ("Risiko / rückgängig?", p["risiko_rueckgaengig"])]
    if p.get("frist"):
        facts.append(("Frist", p["frist"]))
    facts.append(("Folge bei „Nein“", p["folge_bei_nein"]))
    fakten = '<dl class="fakten">' + "".join(f"<dt>{e(k)}</dt><dd>{e(v)}</dd>" for k, v in facts) + "</dl>"
    figs = ""
    if imgs:
        parts = []
        for img, (mime, raw) in imgs:
            cap = e(img["beschriftung"])
            extra = " · ".join(x for x in (img.get("seite"), img.get("variante")) if x)
            alt = e(img.get("alt") or img["beschriftung"])
            uri = f"data:{mime};base64," + base64.b64encode(raw).decode("ascii")
            parts.append(f'<figure><img src="{uri}" alt="{alt}" loading="lazy"><figcaption>{cap}{(" (" + e(extra) + ")") if extra else ""}</figcaption></figure>')
        figs = '<div class="bilder">' + "".join(parts) + "</div>"
    more = f'<details class="mehr"><summary>Mehr Details</summary>{detail_html}</details>' if detail_html else ""
    return (f'<fieldset class="item" id="item-{pid}" data-id="{pid}" data-bundle="{it["bundle"]}" data-marked="{1 if it["marked"] else 0}">'
            f'<legend><span class="kid">{pid}</span> {e(p["titel"])}</legend><p class="kontext">{e(p["kontext"])}</p>{figs}'
            f'<p class="frage">{e(p["frage"])}</p><div class="badges">{"".join(badges)}</div>{fakten}<div class="opts">{"".join(opts)}</div>{more}'
            f'<textarea aria-label="Anmerkung zu {pid}" placeholder="Anmerkung (frei, optional; bei Rückfrage deine Frage)"></textarea>'
            f'<div class="row"><button type="button" class="reset">Antwort zurücknehmen</button><span class="via"></span></div></fieldset>')


def _bundle(n, b, items, images, details):
    by_id = {i["id"]: i for i in items}
    cards = "".join(_card(p, by_id[p["kuerzel"]], images[p["kuerzel"]], details.get(p["kuerzel"], "")) for p in b["posten"])
    return (f'<section class="bundle-form" id="antwort-b{n}"><h3>Bündel {n}: {H.escape(b["titel"])}</h3>'
            f'<div class="row actions"><button type="button" data-bulk="{n}">Alle wie empfohlen (Bündel {n})</button>'
            f'<span class="muted" id="bcount-{n}">0 von {len(b["posten"])} beantwortet</span></div>{cards}</section>')


def build(data, base_dir=None):
    """Daten (dict) -> (seite, document_sha256, items). base_dir loest relative Bildpfade auf."""
    images, details, items = normalize(data, base_dir or Path.cwd())
    e = H.escape
    zo = data.get("zielordner", "")
    hint = ((f"Gewünschter Ordner für „Speichern und abschicken“: <code>{e(zo)}</code>. " if zo else "")
            + "Lässt dein Browser den Ordner nicht zu oder brichst du ab, geht nichts verloren: Die drei Knöpfe hier funktionieren jederzeit, ohne Ordnerwahl.")
    nav = " ".join(f'<a href="#antwort-b{n}">Bündel {n}</a>' for n in range(1, len(data["buendel"]) + 1))
    bundles = "\n".join(_bundle(n, b, items, images, details) for n, b in enumerate(data["buendel"], 1))
    doc = data["dokument_id"]
    form = {"schema": SCHEMA, "document_id": doc, "doc_sha256": ZERO, "answer_name": f"{doc}.antwort.json", "answered_name": f"{doc}_BEANTWORTET.html",
            "zielordner": zo, "items": items}
    parts = {"DOC_ID": e(doc), "HASH": ZERO, "TITLE": e(data["titel"]), "KONTEXT": e(data["kontext_kurz"]), "N": str(len(items)), "NAV": nav,
             "BACKUP_HINT": hint, "BUNDLES": bundles,
             "BASE_CSS": (HERE / "form_base.css").read_text(encoding="utf-8"), "CSS": (HERE / "formular.css").read_text(encoding="utf-8"),
             "JS": (HERE / "formular.js").read_text(encoding="utf-8"),
             "FORM_DATA": embed_json(form, indent=1)}
    template = (HERE / "formular.html").read_text(encoding="utf-8")
    page = re.sub(r"\{\{([A-Z_]+)\}\}", lambda m: parts[m.group(1)], template)  # ein Durchgang: Inhalte werden nie erneut ersetzt
    digest = hashlib.sha256(page.encode("utf-8")).hexdigest()
    # Nur an den zwei Stellen ersetzen, an denen build() den Hash eingesetzt hat: 64 Nullen in Nutzertext bleiben Nutzertext.
    page = page.replace(f'name="document-sha256" content="{ZERO}"', f'name="document-sha256" content="{digest}"', 1)
    page = page.replace(f'"doc_sha256": "{ZERO}"', f'"doc_sha256": "{digest}"', 1)
    return page, digest, items


def blank_hash(page_text):
    """Hash des unveraenderten Formulars: den eingebetteten Hash durch Nullen ersetzen und neu rechnen."""
    d = re.search(r'name="document-sha256" content="([0-9a-f]{64})"', page_text).group(1)
    blank = page_text.replace(f'content="{d}"', f'content="{ZERO}"', 1).replace(f'"doc_sha256": "{d}"', f'"doc_sha256": "{ZERO}"', 1)
    return d, hashlib.sha256(blank.encode("utf-8")).hexdigest()


def validate_answers(obj, items, expected_sha=None, document_id=None):
    """Prueft eine Antwortdatei (ticket-master.decision-answers.v1, mit Wahl 'rueckfrage') gegen die Posten. Liefert Fehler (leer = gueltig)."""
    need = {"schema", "document_id", "document_sha256", "saved_at", "answers", "bulk_actions", "gesamtabnahme", "counts"}
    if not isinstance(obj, dict) or not need <= set(obj):
        return [f"Pflichtfelder fehlen: {sorted(need - set(obj if isinstance(obj, dict) else []))}"]
    err = []
    if obj["schema"] != SCHEMA:
        err.append("schema")
    if not isinstance(obj["document_id"], str) or (document_id and obj["document_id"] != document_id):
        err.append("document_id")
    if not re.fullmatch(r"[0-9a-f]{64}", str(obj["document_sha256"])) or (expected_sha and obj["document_sha256"] != expected_sha):
        err.append("document_sha256")
    if not re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(\.\d+)?Z", str(obj["saved_at"])):
        err.append("saved_at (UTC, ISO)")
    by_id = {i["id"]: i for i in items}
    if set(obj["answers"]) != set(by_id):
        err.append("answers: Kuerzel stimmen nicht mit dem Formular ueberein")
    keys = {"choice", "choice_label", "state", "note", "via", "recommended", "avatar_prediction", "avatar_confidence", "marked"}
    for k, a in obj["answers"].items():
        it = by_id.get(k)
        if not it:
            continue
        if not keys <= set(a):
            err.append(f"{k}: Felder fehlen {sorted(keys - set(a))}")
            continue
        valid = {o["k"]: o["l"] for o in it["options"]}
        if a["state"] == "answered":
            if a["choice"] not in valid or a["choice_label"] != valid[a["choice"]]:
                err.append(f"{k}: choice/choice_label passt nicht zu den Optionen")
        elif a["state"] == "question":
            if a["choice"] != RQ or a["choice_label"] != RQ_LABEL:
                err.append(f"{k}: Rueckfrage, aber choice/choice_label stimmen nicht")
        elif a["state"] == "open":
            if a["choice"] is not None:
                err.append(f"{k}: offen, aber choice gesetzt")
        else:
            err.append(f"{k}: state")
        if a["recommended"] != it["rec"] or a["avatar_prediction"] != it["av_pred"] or a["avatar_confidence"] != it["av_conf"]:
            err.append(f"{k}: recommended/avatar weichen vom Formular ab")
        if not isinstance(a["note"], str):
            err.append(f"{k}: note")
    states = [a.get("state") for a in obj["answers"].values()]
    n_ans, n_q = states.count("answered"), states.count("question")
    if obj["counts"] != {"total": len(items), "answered": n_ans, "questions": n_q, "open": len(items) - n_ans - n_q}:
        err.append("counts")
    if not isinstance(obj["gesamtabnahme"].get("explicit"), bool) or not isinstance(obj["bulk_actions"], dict):
        err.append("gesamtabnahme/bulk_actions")
    elif obj["gesamtabnahme"]["explicit"] and (n_q or any(by_id[k]["rec"] and a.get("choice") != by_id[k]["rec"] for k, a in obj["answers"].items() if k in by_id)):
        err.append("gesamtabnahme.explicit=true, aber Rueckfragen oder nicht alle Posten wie empfohlen")
    return err


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("daten", help="Daten-JSON (Format: form.schema.json)")
    ap.add_argument("--out", required=True, help="Ziel: eine HTML-Datei")
    a = ap.parse_args(argv)
    src = Path(a.daten)
    try:
        page, digest, items = build(json.loads(src.read_text(encoding="utf-8")), src.resolve().parent)
    except FormError as exc:
        print(f"{len(exc.errors)} Fehler in {src}:", file=sys.stderr)
        for line in exc.errors:
            print(" -", line, file=sys.stderr)
        return 2
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(page, encoding="utf-8", newline="\n")
    print(f"geschrieben: {a.out} | {len(page)} Zeichen | {len(items)} Posten | document_sha256 {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
