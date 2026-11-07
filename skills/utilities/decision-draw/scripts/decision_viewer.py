"""Standalone file-based decision draw. Python stdlib only; no register writes.

All producers/consumers cooperate on one per-original-file lock. Consumers must
claim processing before external effects; undo never reverses external effects.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import sys
import tempfile
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = "ellmos.decision-draw.v1"
PARTS = ("bundle", "concept", "interaction", "implementation", "boundaries", "acceptance", "return_transfer")
PART_LABELS = ("Bündel und Umfang", "Konzept", "Zusammenspiel", "Umsetzung", "Grenzen", "Abnahme", "Rücktransfer")


class DecisionError(ValueError):
    pass


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encode(data):
    return (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def text(value, field):
    if not isinstance(value, str) or not value.strip() or "\x00" in value:
        raise DecisionError(f"Ungültiges Textfeld: {field}")


def nodes(data):
    """Flatten presentation hierarchy, without inferring dependencies."""
    result = []

    def visit(items):
        if not isinstance(items, list):
            raise DecisionError("Äste müssen eine Liste sein")
        for item in items:
            if not isinstance(item, dict):
                raise DecisionError("Ast muss ein Objekt sein")
            result.append(item)
            visit(item.get("children", []))

    visit(data.get("nodes"))
    return result


def validate_choices(choices, expected_ids, field):
    if not isinstance(choices, dict) or set(choices) != expected_ids:
        raise DecisionError(f"{field} muss exakt eine Auswahl für jeden Ast enthalten")
    for choice in choices.values():
        if (not isinstance(choice, dict) or set(choice) != {"accept", "comment"}
                or type(choice["accept"]) is not bool or not isinstance(choice["comment"], str)):
            raise DecisionError(f"{field}: Auswahl braucht ausschließlich accept (bool) und comment (Text)")


def validate(data):
    if not isinstance(data, dict) or data.get("schema") != SCHEMA:
        raise DecisionError("Unbekanntes Draw-Format")
    for field in ("draw_id", "title", "session_id", "created_at"):
        text(data.get(field), field)
    if type(data.get("revision")) is not int or data["revision"] < 1:
        raise DecisionError("Ungültige Revision")
    if data.get("state") not in {"draft", "submitted"}:
        raise DecisionError("Draw muss draft oder submitted sein")
    if data.get("preselect", "accept") not in {"accept", "none"}:
        raise DecisionError("preselect muss accept oder none sein")
    if not isinstance(data.get("parts"), dict) or any(not isinstance(data["parts"].get(p), str) or not data["parts"][p].strip() for p in PARTS):
        raise DecisionError("Die sieben Konzeptteile müssen vorhanden sein")
    flat = nodes(data)
    ids = set()
    if not flat:
        raise DecisionError("Mindestens ein Ast ist erforderlich")
    for node in flat:
        for field in ("id", "title", "text", "source_ref", "recommendation", "alternatives_ref", "addressee"):
            text(node.get(field), field)
        if node["id"] in ids:
            raise DecisionError("Doppelte Ast-ID")
        ids.add(node["id"])
        if not isinstance(node.get("depends_on", []), list) or any(not isinstance(x, str) for x in node.get("depends_on", [])):
            raise DecisionError("Abhängigkeiten müssen IDs sein")
    graph = {node["id"]: node.get("depends_on", []) for node in flat}
    visited, active = set(), set()

    def check(key):
        if key in active:
            raise DecisionError("Zyklische echte Abhängigkeit")
        if key in visited:
            return
        active.add(key)
        for dep in graph[key]:
            if dep not in ids:
                raise DecisionError("Abhängigkeit referenziert einen fehlenden Ast")
            check(dep)
        active.remove(key)
        visited.add(key)

    for key in ids:
        check(key)
    if "draft_choices" in data:
        validate_choices(data["draft_choices"], ids, "Gespeicherter Entwurf")
    if data["state"] == "submitted":
        submission = data.get("submission", {})
        if not isinstance(submission, dict) or submission.get("explicit_full_submission") is not True:
            raise DecisionError("Ausdrückliche Gesamteinreichung fehlt")
        for field in ("id", "submitted_at", "source_sha256", "source_path"):
            text(submission.get(field), field)
        validate_choices(submission.get("choices"), ids, "Einreichung")
        if (not isinstance(data.get("processing"), dict)
                or data["processing"].get("state") not in {"unprocessed", "processing", "processed"}):
            raise DecisionError("Verarbeitungsstand fehlt")
    return data


def read(path):
    path = Path(path).absolute()
    if path.is_symlink():
        raise DecisionError("Verknüpfte Quelldatei abgelehnt")
    raw = path.read_bytes()
    return validate(json.loads(raw.decode("utf-8"))), sha(raw), raw


def original_path(path, data):
    if data["state"] == "submitted":
        original = Path(data["submission"]["source_path"])
        # Do not trust an arbitrary source path from editable JSON.
        expected = Path(path).with_name(Path(path).stem.removesuffix("_decided") + ".json").absolute()
        if original != expected:
            raise DecisionError("Quellpfad passt nicht zur Ergebnisdatei")
        return original
    return Path(path).absolute()


@contextmanager
def locked(path):
    lock = Path(path).with_name(Path(path).name + ".decision-lock")
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise DecisionError("Ein anderes Fenster oder ein Rücktransfer hält die Dateisperre") from exc
    try:
        os.close(fd)
        yield
    finally:
        lock.unlink(missing_ok=True)


def publish_new(path, raw):
    """Atomic no-clobber publication in the same directory."""
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".draw-", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.link(temporary, path)
    except FileExistsError as exc:
        raise DecisionError(f"Zieldatei existiert bereits: {path.name}") from exc
    finally:
        if temporary:
            temporary.unlink(missing_ok=True)


def replace_expected(path, data, expected):
    if sha(path.read_bytes()) != expected:
        raise DecisionError("Fremdänderung erkannt; neu lesen")
    temp = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".draw-", delete=False) as handle:
            temp = Path(handle.name)
            handle.write(encode(data))
            handle.flush()
            os.fsync(handle.fileno())
        if sha(path.read_bytes()) != expected:
            raise DecisionError("Fremdänderung während Aktualisierung")
        os.replace(temp, path)
    finally:
        if temp:
            temp.unlink(missing_ok=True)


def default_choices(data):
    return {node["id"]: {"accept": True, "comment": ""} for node in nodes(data)}


def initial_choices(data):
    """Opening state: consent preselected as draft, or with preselect=none nothing answered (accept None)."""
    if data.get("preselect", "accept") == "none":
        return {node["id"]: {"accept": None, "comment": ""} for node in nodes(data)}
    return default_choices(data)


def initially_expanded(data):
    """Every branch starts expanded, so no level hides branches that a click could submit as consent."""
    return {node["id"] for node in nodes(data)}


def unseen_ids(data, seen):
    return [node["id"] for node in nodes(data) if node["id"] not in seen]


def check_ready(data, choices, seen):
    """Same refusals as submit(), usable before any dialog: every branch answered and displayed at least once."""
    unanswered = sum(1 for item in choices.values() if isinstance(item, dict) and item.get("accept") is None)
    if unanswered:
        raise DecisionError(f"Noch nicht beantwortet: {unanswered} von {len(choices)} Ästen. Jeder Ast braucht ausdrücklich + oder −.")
    hidden = unseen_ids(data, seen)
    if hidden:
        raise DecisionError(f"Noch nicht angezeigt: {len(hidden)} Äste wurden nie sichtbar. Erst alle Äste ansehen.")


def as_accept(value):
    """Tk variable value to answer: BooleanVar gives bool, an unset or clicked StringVar gives '', '1' or '0'."""
    return None if value in ("", None) else str(value).lower() in ("1", "true")


def submit(path, expected_revision, expected_sha256, choices, seen=None):
    """seen: ids of branches the window has displayed. The GUI always passes it; None (scripts, tests) skips that one check."""
    path = Path(path).absolute()
    if path.suffix.lower() != ".json" or path.stem.endswith("_decided"):
        raise DecisionError("Eine ursprüngliche .json-Datei ist erforderlich")
    output = path.with_name(path.stem + "_decided.json")
    unanswered = sum(1 for item in choices.values() if isinstance(item, dict) and item.get("accept") is None)
    if unanswered:
        raise DecisionError(f"Noch nicht beantwortet: {unanswered} von {len(choices)} Ästen. Jeder Ast braucht ausdrücklich + oder −.")
    with locked(path):
        data, current_sha, _ = read(path)
        if data["state"] != "draft" or data["revision"] != expected_revision or current_sha != expected_sha256:
            raise DecisionError("Entwurf wurde verändert oder bereits eingereicht")
        if seen is not None and unseen_ids(data, seen):
            raise DecisionError(f"Noch nicht angezeigt: {len(unseen_ids(data, seen))} Äste wurden nie sichtbar. Erst alle Äste ansehen.")
        result = copy.deepcopy(data)
        result.update(state="submitted", revision=data["revision"] + 1,
                      submission={"id": str(uuid.uuid4()), "submitted_at": now(), "source_sha256": current_sha,
                                  "source_revision": data["revision"], "source_path": str(path),
                                  "choices": copy.deepcopy(choices), "explicit_full_submission": True},
                      processing={"state": "unprocessed"})
        validate(result)
        raw = encode(result)
        publish_new(output, raw)
        # Cooperative lock covers both files; a crash may leave both. In that
        # case consumers fail closed and must reconcile, never infer acceptance.
        if sha(path.read_bytes()) != current_sha:
            # This is our just-published output; remove only our own postimage.
            if sha(output.read_bytes()) == sha(raw):
                output.unlink()
            raise DecisionError("Quelländerung während Einreichung; nicht überschrieben")
        path.unlink()
        return output, result, sha(raw)


def undo(path, submission_id, expected_sha256):
    path = Path(path).absolute()
    initial, _, _ = read(path)
    original = original_path(path, initial)
    with locked(original):
        data, current_sha, _ = read(path)
        if (current_sha != expected_sha256 or data["state"] != "submitted"
                or data["submission"]["id"] != submission_id):
            raise DecisionError("Einreichung wurde verändert; Rücknahme verweigert")
        if data["processing"]["state"] != "unprocessed":
            raise DecisionError("Rücktransfer hat begonnen; Rücknahme muss über Phase 4 erfolgen")
        if original.exists():
            raise DecisionError("Ursprüngliche Datei existiert wieder; keine Fremdänderung überschrieben")
        restored = copy.deepcopy(data)
        history = restored.setdefault("history", [])
        history.append({"event": "withdrawn", "at": now(), "submission_id": submission_id,
                        "submission_sha256": current_sha, "source_sha256": data["submission"]["source_sha256"]})
        # Preserve comments/selections as a draft, never as accepted decisions.
        restored["draft_choices"] = restored["submission"]["choices"]
        restored.pop("submission")
        restored.pop("processing")
        restored.update(state="draft", revision=data["revision"] + 1)
        validate(restored)
        raw = encode(restored)
        publish_new(original, raw)
        if sha(path.read_bytes()) != current_sha:
            if sha(original.read_bytes()) == sha(raw):
                original.unlink()
            raise DecisionError("Fremdänderung während Rücknahme")
        path.unlink()
        return original, restored, sha(raw)


def mark_processing(path, expected_sha256, state, actor, evidence_ref):
    """Canonical consumer fence before Phase 4; does not perform register writes."""
    path = Path(path).absolute()
    initial, _, _ = read(path)
    original = original_path(path, initial)
    if state not in {"processing", "processed"}:
        raise DecisionError("Ungültiger Verarbeitungsstand")
    text(actor, "actor")
    text(evidence_ref, "evidence_ref")
    with locked(original):
        data, current_sha, _ = read(path)
        if current_sha != expected_sha256 or data["state"] != "submitted" or original.exists():
            raise DecisionError("Veralteter oder widersprüchlicher Einreichungsstand")
        current_state = data["processing"]["state"]
        if ((state == "processing" and current_state != "unprocessed")
                or (state == "processed" and (current_state != "processing" or data["processing"].get("actor") != actor))):
            raise DecisionError("Verarbeitung bereits beansprucht oder falscher Owner")
        data["revision"] += 1
        data["processing"] = {"state": state, "actor": actor, "at": now(), "evidence_ref": evidence_ref}
        replace_expected(path, data, current_sha)
        return data, sha(encode(data))


def handoff_prompt(path, expected_sha256):
    path = Path(path).absolute()
    data, actual, _ = read(path)
    if data["state"] != "submitted" or actual != expected_sha256 or original_path(path, data).exists():
        raise DecisionError("Einreichung ist nicht mehr im erwarteten Stand")
    return (f"Ich habe den Decision-Draw {data['draw_id']} ausdrücklich über das Entscheidungsfenster eingereicht.\n"
            f"Ergebnisdatei: {path}\nSubmission-ID: {data['submission']['id']}\nSHA-256: {actual}\n"
            "Lies die Datei frisch und prüfe ID, Revision, Quellenhash und Verarbeitungsstand. "
            "Beanspruche processing atomar über decision_viewer.py claim, bevor du Wirkungen auslöst. "
            "Die Einreichung bestätigt die Auswahl und Kommentare aller Äste; Kommentare können Mehrdeutigkeiten enthalten. "
            "Prüfe echte Abhängigkeiten ohne andere Äste still zu ändern. Buche ausschließlich über decision-briefing Phase 4. "
            "Falls die Datei fehlt, zurückgenommen oder verändert wurde, nicht aus dieser Kopie buchen.")


class DecisionWindow:
    def __init__(self, root, path):
        import tkinter as tk
        from tkinter import ttk
        self.tk, self.ttk, self.root = tk, ttk, root
        self.path = Path(path).absolute()
        self.data, self.sha, _ = read(self.path)
        self.submission_sha = self.sha
        self.choices = copy.deepcopy(self.data.get("draft_choices", initial_choices(self.data)))
        self.expanded = initially_expanded(self.data)
        self.seen = set()  # ids of branches drawn at least once; Submit is refused while any branch was never displayed
        self.comments_open = set()
        self.variables, self.comment_widgets = {}, {}
        root.title("Decision-Draw · Entscheidung im Gesamtbild")
        sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
        width, height = min(960, max(680, sw//2)), min(1050, sh-70)
        root.geometry(f"{width}x{height}+{max(0, sw-width-8)}+20")
        root.minsize(640, 500)
        style = ttk.Style(root)
        style.theme_use("clam")
        style.configure("TFrame", background="#eef2f7")
        style.configure("TLabel", background="#eef2f7", foreground="#18304a", font=("Segoe UI", 11))
        style.configure("Card.TFrame", background="white")
        style.configure("Card.TLabel", background="white", foreground="#18304a", font=("Segoe UI", 11))
        self.body = ttk.Frame(root, padding=18)
        self.body.pack(fill="both", expand=True)
        self.title = ttk.Label(self.body, text=self.data["title"], font=("Segoe UI", 17, "bold"), wraplength=800)
        self.title.pack(anchor="w", pady=(0, 8))
        self.notice = ttk.Label(self.body, text="Vorwahl: Zustimmung als Entwurf. Erst Absenden bestätigt Ihre Auswahl samt Kommentaren.", wraplength=800)
        self.notice.pack(anchor="w", pady=(0, 10))
        self.canvas = tk.Canvas(self.body, background="#eef2f7", highlightthickness=0)
        bar = ttk.Scrollbar(self.body, command=self.canvas.yview)
        bar.pack(side="right", fill="y")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.configure(yscrollcommand=bar.set)
        self.content = ttk.Frame(self.canvas)
        self.window = self.canvas.create_window((0, 0), window=self.content, anchor="nw")
        self.content.bind("<Configure>", lambda _: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(self.window, width=e.width))
        root.bind_all("<MouseWheel>", self.wheel)
        self.footer = ttk.Frame(self.body)
        self.footer.pack(fill="x", pady=(12, 0))
        self.status = tk.StringVar()
        ttk.Label(self.body, textvariable=self.status, wraplength=800).pack(anchor="w", pady=(8, 0))
        self.render()
        root.after(1200, self.watch)

    def wheel(self, event):
        if not isinstance(event.widget, self.tk.Text):
            self.canvas.yview_scroll(int(-event.delta/120), "units")

    def label(self, parent, value, bold=False):
        label = self.ttk.Label(parent, text=value, style="Card.TLabel", wraplength=max(320, self.canvas.winfo_width()-90), justify="left")
        if bold:
            label.configure(font=("Segoe UI", 11, "bold"))
        label.pack(anchor="w", fill="x", pady=(2, 6))

    def capture(self):
        for key, variable in self.variables.items():
            self.choices[key]["accept"] = as_accept(variable.get())
        for key, widget in self.comment_widgets.items():
            self.choices[key]["comment"] = widget.get("1.0", "end-1c")

    def rerender(self, collection, key):
        self.capture()
        collection.symmetric_difference_update({key})
        self.render()

    def render(self):
        position = self.canvas.yview()[0]
        for child in self.content.winfo_children() + self.footer.winfo_children():
            child.destroy()
        self.variables, self.comment_widgets = {}, {}
        if self.data["state"] == "submitted":
            self.confirmation()
        else:
            if self.data.get("preselect", "accept") == "none":
                self.notice.configure(text="Keine Vorwahl: Jeder Ast braucht Ihre ausdrückliche Antwort (+ oder −). Erst Absenden bestätigt die Auswahl samt Kommentaren.")
            else:
                self.notice.configure(text="Vorwahl: Zustimmung als Entwurf. Erst Absenden bestätigt Ihre Auswahl samt Kommentaren.")
            # The complete prose concept remains available alongside the tree.
            for key, label in zip(PARTS, PART_LABELS):
                box = self.ttk.Frame(self.content, style="Card.TFrame", padding=12)
                box.pack(fill="x", pady=(0, 8))
                self.label(box, label, True)
                self.label(box, self.data["parts"][key])
            self.draw_nodes(self.data["nodes"], self.content)
            self.ttk.Button(self.footer, text="Absenden / Entscheiden", command=self.on_submit).pack(side="right")
            self.ttk.Button(self.footer, text="Technische Quellen & Alternativen", command=self.technical).pack(side="left")
            self.status.set("Auswahl und Kommentare sind noch nicht eingereicht.")
        self.root.update_idletasks()
        self.canvas.yview_moveto(position)

    def draw_nodes(self, items, parent, depth=0):
        for node in items:
            key = node["id"]
            self.seen.add(key)
            box = self.ttk.Frame(parent, style="Card.TFrame", padding=12)
            box.pack(fill="x", padx=(min(depth*20, 100), 0), pady=(0, 10))
            header = self.ttk.Frame(box, style="Card.TFrame")
            header.pack(fill="x")
            has_children = bool(node.get("children"))
            self.ttk.Button(header, text=("▾" if key in self.expanded else "▸") if has_children else "•", width=3,
                            command=lambda k=key: self.rerender(self.expanded, k)).pack(side="left", padx=(0, 8))
            self.label(header, node["title"], True)
            self.label(box, node["text"])
            self.label(box, "Empfehlung: " + node["recommendation"])
            if node.get("depends_on"):
                titles = {n["id"]: n["title"] for n in nodes(self.data)}
                self.label(box, "Echte Voraussetzung: " + ", ".join(titles[x] for x in node["depends_on"]))
            actions = self.ttk.Frame(box, style="Card.TFrame")
            actions.pack(fill="x", pady=(4, 4))
            accept = self.choices[key]["accept"]
            # An unanswered branch (preselect=none) uses '' so that neither radio button shows as selected.
            variable = self.tk.StringVar(value="") if accept is None else self.tk.BooleanVar(value=accept)
            self.variables[key] = variable
            self.ttk.Radiobutton(actions, text="+ Zustimmen", variable=variable, value=True).pack(side="left", padx=(0, 12))
            self.ttk.Radiobutton(actions, text="− Ablehnen", variable=variable, value=False).pack(side="left", padx=(0, 12))
            self.ttk.Button(actions, text="Kommentar schließen" if key in self.comments_open else "Kommentar / Anweisung", command=lambda k=key: self.rerender(self.comments_open, k)).pack(side="left")
            if key in self.comments_open:
                panel = self.ttk.Frame(box, style="Card.TFrame")
                panel.pack(fill="both", expand=True, pady=(5, 0))
                widget = self.tk.Text(panel, height=6, wrap="word", font=("Segoe UI", 11), relief="flat", bg="#f7f9fc", padx=8, pady=8)
                scrollbar = self.ttk.Scrollbar(panel, command=widget.yview)
                scrollbar.pack(side="right", fill="y")
                widget.pack(fill="both", expand=True)
                widget.configure(yscrollcommand=scrollbar.set)
                widget.insert("1.0", self.choices[key]["comment"])
                self.comment_widgets[key] = widget
            if has_children and key in self.expanded:
                self.draw_nodes(node["children"], parent, depth+1)

    def technical(self):
        self.capture()
        dialog = self.tk.Toplevel(self.root)
        dialog.title("Quellen, Alternativen und technische Zuordnung")
        dialog.geometry("850x600")
        output = self.tk.Text(dialog, wrap="word", font=("Segoe UI", 11), padx=14, pady=14)
        scroll = self.ttk.Scrollbar(dialog, command=output.yview)
        scroll.pack(side="right", fill="y")
        output.pack(fill="both", expand=True)
        output.configure(yscrollcommand=scroll.set)
        output.insert("1.0", f"Draw-ID: {self.data['draw_id']}\nRevision: {self.data['revision']}\nDatei: {self.path}\n\n")
        for node in nodes(self.data):
            output.insert("end", f"{node['title']}\nID: {node['id']}\nQuelle: {node['source_ref']}\nAdressat: {node['addressee']}\nAlternativen / Details: {node['alternatives_ref']}\nKonfidenz: {node.get('confidence', 'unbekannt')}\n\n")
        output.configure(state="disabled")

    def fail(self, error):
        from tkinter import messagebox
        messagebox.showerror("Entscheidung nicht gespeichert", str(error), parent=self.root)
        self.status.set(str(error))

    def on_submit(self):
        try:
            self.capture()
            self.path, self.data, self.sha = submit(self.path, self.data["revision"], self.sha, self.choices, self.seen)
            self.submission_sha = self.sha
            self.render()
            self.canvas.yview_moveto(0)
        except (ValueError, OSError) as exc:
            self.fail(exc)

    def confirmation(self):
        self.notice.configure(text="Gespeichert. Der kanonische Rücktransfer erfolgt anschließend über decision-briefing.")
        box = self.ttk.Frame(self.content, style="Card.TFrame", padding=16)
        box.pack(fill="x", pady=(0, 12))
        self.label(box, "Ihre Entscheidung wurde als Datei eingereicht.", True)
        self.label(box, "Der Übergabeprompt informiert Ihre Konsole über die gespeicherte Auswahl. Bis der Rücktransfer beginnt, können Sie diese Einreichung hier rückgängig machen.")
        selected = self.data["submission"]["choices"]
        for node in nodes(self.data):
            item = selected[node["id"]]
            self.label(box, ("+ Zustimmung: " if item["accept"] else "− Ablehnung: ") + node["title"], True)
            if item["comment"]:
                self.label(box, "Kommentar: " + item["comment"])
        self.undo_button = self.ttk.Button(self.footer, text="Rückgängig", command=self.on_undo)
        self.undo_button.pack(side="left")
        if self.data["processing"]["state"] != "unprocessed" or self.sha != self.submission_sha:
            self.undo_button.state(["disabled"])
        self.ttk.Button(self.footer, text="Übergabeprompt kopieren", command=self.copy_prompt).pack(side="right")
        self.status.set("Verarbeitung: " + self.data["processing"]["state"] + " · keine automatische Registerbuchung")

    def on_undo(self):
        try:
            self.path, self.data, self.sha = undo(self.path, self.data["submission"]["id"], self.submission_sha)
            self.choices = copy.deepcopy(self.data["draft_choices"])
            self.render()
        except (ValueError, OSError) as exc:
            self.fail(exc)

    def copy_prompt(self):
        try:
            value = handoff_prompt(self.path, self.submission_sha)
            self.root.clipboard_clear()
            self.root.clipboard_append(value)
            self.root.update()
            self.status.set("Übergabeprompt mit Draw-ID und geprüftem absoluten Dateipfad kopiert.")
        except (ValueError, OSError) as exc:
            self.fail(exc)

    def watch(self):
        try:
            current, current_sha, _ = read(self.path)
            if current_sha != self.sha:
                if self.data["state"] == "submitted" and current.get("submission", {}).get("id") == self.data["submission"]["id"]:
                    self.data, self.sha = current, current_sha
                    self.render()
                else:
                    self.status.set("Quelle wurde verändert; Ihre lokale Auswahl bleibt erhalten. Einreichung erfordert erneutes Öffnen.")
        except (ValueError, OSError):
            self.status.set("Datei fehlt oder wurde verändert; keine automatische Entscheidung.")
        self.root.after(1200, self.watch)


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Dateibasierter Decision-Draw ohne Server")
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("open", "validate", "read", "claim", "processed"):
        item = sub.add_parser(command)
        item.add_argument("file", type=Path)
        if command in {"claim", "processed"}:
            item.add_argument("--sha256", required=True)
            item.add_argument("--actor", required=True)
            item.add_argument("--evidence-ref", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "open":
            # Reject malformed persisted selections before creating any Tk UI.
            read(args.file)
            import tkinter as tk
            root = tk.Tk()
            DecisionWindow(root, args.file)
            root.mainloop()
        elif args.command in {"claim", "processed"}:
            data, current_sha = mark_processing(args.file, args.sha256, "processing" if args.command == "claim" else "processed", args.actor, args.evidence_ref)
            print(json.dumps({"draw_id": data["draw_id"], "revision": data["revision"], "sha256": current_sha, "processing": data["processing"]}, ensure_ascii=False, indent=2))
        else:
            data, current_sha, _ = read(args.file)
            print(json.dumps({"draw_id": data["draw_id"], "revision": data["revision"], "sha256": current_sha, **({"data": data} if args.command == "read" else {})}, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError) as exc:
        parser.exit(2, f"Fehler: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
