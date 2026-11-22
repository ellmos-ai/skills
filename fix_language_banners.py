# -*- coding: utf-8 -*-
"""Sprachhinweise (Banner) in SKILL*.md pruefen und reparieren.

WARUM ES DIESES WERKZEUG GIBT
-----------------------------
Der i18n-Lauf vom 2026-07-30 (Sammelcommits 6a2d333a, e5e23e71, b0882187) setzte
in jede Sprachdatei eine feste Banner-Vorlage ein ("Offizielle <Sprache>-Version /
Documento Oficial en <Sprache>", "English Translation ..."), auch in Dateien einer
anderen Sprache, und liess dabei den Text unuebersetzt. Ticket T-20261122-838934534.

Ein Banner ist FEHLERHAFT, wenn
  * es die verunglueckte Mischvorlage "Offizielle X-Version / Documento Oficial en X" ist,
  * sein Sprachlabel nicht zur Dateisprache passt (z. B. "English" in SKILL.fr.md),
  * mehr als ein Banner im Kopf der Datei steht,
  * es eine "offizielle Version" behauptet, der Text darunter aber erkennbar in einer
    anderen Sprache steht (dann gehoert dort ein ehrlicher "Translation pending"-Hinweis hin),
  * ein "Translation pending"-Hinweis auf einer Datei steht, deren Text laengst uebersetzt ist,
  * eine fremdsprachige Datei (nicht SKILL.md) gar keinen Hinweis hat, ihr Text aber erkennbar
    deutsch/englisch ist.
Dateien ohne Banner, deren Text zur Dateisprache passt, sind in Ordnung.

Aufruf (Repo-Wurzel):
    python fix_language_banners.py            # Trockenlauf mit Statistik
    python fix_language_banners.py --diff     # zusaetzlich die geaenderten Zeilen
    python fix_language_banners.py --apply    # Dateien umschreiben (nur Bannerzeilen)
    python fix_language_banners.py --check    # Exit 1, wenn fehlerhafte Banner existieren (CI)
"""
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent

SKILL_RE = re.compile(r"(?:^|/)SKILL(?:\.([a-z]{2}))?\.md$")
IGNORED_PARTS = {"_archive", "_reference", "third-party", "_templates"}

LABEL = {"de": "Deutsch", "en": "English", "es": "Español", "fr": "Français",
         "ja": "日本語", "ru": "Русский", "zh": "中文"}
# Alle Labels, die als Banner-Anfang erkannt werden (inkl. falscher/englischer Schreibweisen).
KNOWN_LABELS = set(LABEL.values()) | {
    "English Translation", "Spanish", "French", "Japanese", "Chinese", "Russian"}
BANNER_RE = re.compile(r"^> \*\*(" + "|".join(sorted(KNOWN_LABELS, key=len, reverse=True)) +
                       r")\*\* — (.*)$")
GARBLED_RE = re.compile(r"Documento Oficial en|Offizielle \w+-Version /")

# Ehrlicher Hinweis: {L} = Sprache des tatsaechlich vorhandenen Textes.
PENDING = {
    "de": "Hinweis: Der Inhalt dieser Datei ist derzeit {L}.",
    "en": "Translation pending: content is currently {L}.",
    "es": "Traducción pendiente: el contenido está actualmente en {L}.",
    "fr": "Traduction en attente : le contenu est actuellement en {L}.",
    "ja": "翻訳待ち：内容は現在{L}のままです。",
    "ru": "Перевод ожидается: содержимое пока на {L} языке.",
    "zh": "翻译待完成：内容目前仍为{L}。",
}
PENDING_RE = re.compile(r"Translation pending|Der Inhalt dieser Datei ist derzeit|Traduction en attente|Übersetzung ausstehend|"
                        r"Traducción pendiente|翻訳待ち|Перевод ожидается|翻译待完成")
BODY_NAME = {  # Name der Textsprache, in der Sprache des Hinweises
    "de": {"en": "englisch"},
    "en": {"de": "German"},
    "es": {"de": "alemán", "en": "inglés"},
    "fr": {"de": "allemand", "en": "anglais"},
    "ja": {"de": "ドイツ語", "en": "英語"},
    "ru": {"de": "немецком", "en": "английском"},
    "zh": {"de": "德文", "en": "英文"},
}
OFFICIAL = {
    "en": "Official English version of `{n}`.",
    "es": "Versión oficial en español de `{n}`.",
    "fr": "Version française officielle de la compétence `{n}`.",
    "ja": "`{n}` の公式日本語版。",
    "ru": "Официальная русская версия `{n}`.",
    "zh": "`{n}` 官方中文版本。",
}
SIBLING_ORDER = ["en", "fr", "es", "ja", "ru", "zh"]

STOP = {k: set(v.split()) for k, v in {
    "de": "und oder nicht werden wird einen eine der die das für mit auch beim nach vor dann wenn "
          "sind kann muss soll ist ein zu von im den dem des auf bei aus nur wie",
    "en": "and or not will the with for also when then are can must should is a to of in on by "
          "from only how this that be as it",
    "es": "y o no se el la los las de que en un una para con por es del al como más",
    "fr": "et ou ne pas le la les des du de que en un une pour avec par est sont dans sur au aux "
          "ce cette",
}.items()}


def body_language(text):
    """Sprache des Fliesstextes ('de','en','es','fr','ja','ru','zh') oder '??' bei Unklarheit."""
    if text.startswith("---"):
        i = text.find("\n---", 3)
        text = text[i + 4:] if i > 0 else text
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"^> .*$", "", text, flags=re.M)
    total = len(text) + 1
    if len(re.findall(r"[Ѐ-ӿ]", text)) / total > 0.15:
        return "ru"
    if len(re.findall(r"[぀-ヿ]", text)) / total > 0.05:
        return "ja"
    if len(re.findall(r"[一-鿿]", text)) / total > 0.15:
        return "zh"
    words = re.findall(r"[A-Za-zÀ-ÿ]+", text.lower())
    if len(words) < 30:
        return "??"
    score = {k: sum(1 for w in words if w in s) / len(words) for k, s in STOP.items()}
    best, second = sorted(score, key=score.get, reverse=True)[:2]
    if score[best] >= 0.05 or (score[best] >= 0.025 and score[best] >= 1.5 * score[second]):
        return best
    return "??"


def file_lang(path):
    return SKILL_RE.search(str(path).replace("\\", "/")).group(1) or "de"


def tracked_skill_files():
    out = subprocess.check_output(["git", "ls-files"], cwd=REPO, text=True, encoding="utf-8")
    for f in out.splitlines():
        parts = set(f.split("/"))
        if SKILL_RE.search(f) and f.startswith("skills/") and not parts & IGNORED_PARTS:
            yield REPO / f


def head_banners(lines):
    """Indizes der Banner-Zeilen vor der ersten H1 (nach dem Frontmatter)."""
    start = 0
    if lines and lines[0].startswith("---"):
        for i in range(1, len(lines)):
            if lines[i].startswith("---"):
                start = i + 1
                break
    out = []
    for i in range(start, len(lines)):
        if lines[i].startswith("# "):
            break
        if BANNER_RE.match(lines[i]):
            out.append(i)
    return out


def desired_banner(path, lang, body, kept):
    name = path.parent.name
    if body not in (lang, "??"):
        word = BODY_NAME.get(lang, {}).get(body)
        if word:
            return f"> **{LABEL[lang]}** — " + PENDING[lang].format(L=word)
    if kept:
        return kept
    if lang == "de":
        sib = [f"[{s.upper()}](SKILL.{s}.md)" for s in SIBLING_ORDER
               if (path.parent / f"SKILL.{s}.md").exists()]
        return "> Deutsche Originalfassung." + (" Weitere Sprachen: " + " · ".join(sib) if sib else "")
    return f"> **{LABEL[lang]}** — " + OFFICIAL[lang].format(n=name)


def analyze(path):
    """(neuer_text, probleme) -- neuer_text ist None, wenn nichts zu aendern ist."""
    with open(path, encoding="utf-8", newline="") as fh:
        raw = fh.read()
    nl = "\r\n" if "\r\n" in raw else "\n"
    lines = raw.split(nl)
    idx = head_banners(lines)
    lang = file_lang(path)
    body = body_language(raw)
    if not idx:
        # Kein Banner: nur fremdsprachige Dateien mit erkennbar falscher Textsprache bekommen
        # einen ehrlichen Hinweis (Deutsch ist Leitsprache, dort entscheidet das Sprach-Gate).
        h1 = next((i for i, ln in enumerate(lines) if ln.startswith("# ")), None)
        if lang == "de" or body in (lang, "??") or h1 is None or body not in BODY_NAME[lang]:
            return None, []
        new = lines[:h1]
        if new and new[-1] != "":
            new.append("")
        new += [desired_banner(path, lang, body, None), ""] + lines[h1:]
        return nl.join(new), [f"kein Hinweis, Text ist {body}"]
    problems = []
    kept = None
    for i in idx:
        label, rest = BANNER_RE.match(lines[i]).groups()
        pending = bool(PENDING_RE.search(lines[i]))
        if GARBLED_RE.search(lines[i]):
            problems.append("Mischvorlage")
        elif label != LABEL[lang]:
            problems.append(f"Label '{label}' in {lang}-Datei")
        elif pending and body in (lang, "??"):
            problems.append("veralteter Uebersetzungs-Hinweis")
        elif not pending and body not in (lang, "??"):
            problems.append(f"behauptet offizielle Version, Text ist {body}")
        elif kept is None and not pending:
            kept = lines[i]
    if len(idx) > 1:
        problems.append("mehrere Banner")
    if not problems:
        return None, []
    new_banner = desired_banner(path, lang, body, kept)
    new = list(lines)
    new[idx[0]] = new_banner
    for i in reversed(idx[1:]):
        del new[i]
    # Leerzeilenfolgen im Kopf auf eine reduzieren (nur dort, wo Banner standen).
    j = idx[0] + 1
    while j < len(new) and new[j] == "" and j + 1 < len(new) and new[j + 1] == "":
        del new[j]
    text = nl.join(new)
    return (text if text != raw else None), problems


def main(argv):
    apply_, check, show = "--apply" in argv, "--check" in argv, "--diff" in argv
    changed = []
    for f in tracked_skill_files():
        new, problems = analyze(f)
        if problems:
            changed.append((f, problems))
            if apply_ and new is not None:
                with open(f, "w", encoding="utf-8", newline="") as fh:
                    fh.write(new)
    skills = {f.parent for f, _ in changed}
    print(f"{len(changed)} Dateien in {len(skills)} Skills mit fehlerhaftem Sprachhinweis")
    if show or check:
        for f, p in changed:
            print(f"  {f.relative_to(REPO).as_posix()}: {', '.join(sorted(set(p)))}")
    if check:
        return 1 if changed else 0
    if apply_:
        print("angewendet")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
