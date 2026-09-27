"""Tests for the reusable SKILL*.md frontmatter gate (parse + required fields + --fix)."""
from __future__ import annotations

import contextlib
import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("skill_frontmatter_gate.py")
SPEC = importlib.util.spec_from_file_location("skill_frontmatter_gate", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate)


@contextlib.contextmanager
def _temp_repo(skill_md_content: str):
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        skill_dir = root / "skills" / "utilities" / "example"
        skill_dir.mkdir(parents=True)
        md = skill_dir / "SKILL.md"
        md.write_text(skill_md_content, encoding="utf-8")
        yield root, md


class SkillFrontmatterGateTests(unittest.TestCase):
    def test_repo_frontmatter_is_all_valid(self) -> None:
        repo = gate.REPO
        befunde = [
            (str(md), fehler)
            for md in gate.gefundene_skill_dateien(repo)
            for fehler in gate.pruefe(md)
        ]
        self.assertEqual(befunde, [], f"{len(befunde)} Befund(e): {befunde[:5]}")

    def test_gefundene_skill_dateien_findet_echte_skills(self) -> None:
        dateien = gate.gefundene_skill_dateien(gate.REPO)
        self.assertGreater(len(dateien), 0)
        self.assertTrue(any(p.name == "SKILL.md" for p in dateien))

    def test_gefundene_skill_dateien_schliesst_template_assets_aus(self) -> None:
        dateien = gate.gefundene_skill_dateien(gate.REPO)
        self.assertFalse(any("template" in p.name for p in dateien))

    def test_pruefe_erkennt_unquotierte_beschreibung(self) -> None:
        with _temp_repo(
            "---\nname: x\ndescription: Routes to tools: A and B\n---\nbody\n"
        ) as (_root, md):
            self.assertNotEqual(gate.pruefe(md), [])

    def test_pruefe_akzeptiert_quotierte_beschreibung(self) -> None:
        with _temp_repo(
            '---\nname: x\ndescription: "Routes to tools: A and B"\n---\nbody\n'
        ) as (_root, md):
            self.assertEqual(gate.pruefe(md), [])

    def test_pruefe_erkennt_fehlendes_pflichtfeld(self) -> None:
        with _temp_repo('---\nname: x\n---\nbody\n') as (_root, md):
            befunde = gate.pruefe(md)
            self.assertTrue(any("description" in b for b in befunde))

    def test_pruefe_akzeptiert_uebersetzungs_marker_ohne_name(self) -> None:
        """A translation stub with only `language:` (no `name`, no
        `description`) is a deliberate, documented pattern (e.g.
        skills/assist/dev/SKILL.fr.md) -- it inherits from its sibling
        primary SKILL.md and must not be flagged as incomplete."""
        with _temp_repo("---\nlanguage: fr\n---\nbody\n") as (_root, md):
            self.assertEqual(gate.pruefe(md), [])

    def test_pruefe_akzeptiert_yaml_kommentar_als_abschnittsueberschrift(self) -> None:
        """Real files (e.g. skills/dev/human-loop-audit/SKILL.md) use a full-line
        `# Comment` as a section divider between frontmatter groups -- valid
        YAML, must not be misread as a broken key line."""
        with _temp_repo(
            "---\nname: x\ndescription: \"fine\"\n\n# Section Header\nstandalone: true\n"
            "---\nbody\n"
        ) as (_root, md):
            self.assertEqual(gate.pruefe(md), [])

    def test_pruefe_still_requires_description_when_name_is_present(self) -> None:
        """A file that DOES declare its own `name` is a real primary/skill,
        not a marker stub -- required fields still apply."""
        with _temp_repo("---\nname: x\nlanguage: fr\n---\nbody\n") as (_root, md):
            befunde = gate.pruefe(md)
            self.assertTrue(any("description" in b for b in befunde))

    def test_fix_repariert_unquotierte_beschreibung_und_wird_danach_gruen(self) -> None:
        broken = "---\nname: x\ndescription: Routes to tools: A and B\n---\nbody\n"
        with _temp_repo(broken) as (_root, md):
            self.assertNotEqual(gate.pruefe(md), [])  # rot vorher
            ergebnis = gate.fixe(md)
            self.assertEqual(ergebnis, "requotiert")
            self.assertEqual(gate.pruefe(md), [])  # gruen nachher
            # Wortlaut unveraendert, nur Quotierung:
            self.assertIn("Routes to tools: A and B", md.read_text(encoding="utf-8"))

    def test_fix_repariert_kaputten_faltblock(self) -> None:
        broken = (
            "---\nname: x\ndescription: >\n  First line continues,\n"
            "second line lost its indent.\nstandalone: true\n---\nbody\n"
        )
        with _temp_repo(broken) as (_root, md):
            self.assertNotEqual(gate.pruefe(md), [])
            ergebnis = gate.fixe(md)
            self.assertEqual(ergebnis, "requotiert")
            self.assertEqual(gate.pruefe(md), [])

    def test_fix_laesst_bereits_gueltige_datei_unveraendert(self) -> None:
        valid = '---\nname: x\ndescription: "already fine: yes"\n---\nbody\n'
        with _temp_repo(valid) as (_root, md):
            before = md.read_text(encoding="utf-8")
            self.assertIsNone(gate.fixe(md))
            self.assertEqual(md.read_text(encoding="utf-8"), before)

    def test_cli_fix_end_to_end(self) -> None:
        """A whole broken fixture repo: --fix must turn a red gate green."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill_dir = root / "skills" / "utilities" / "example"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(
                "---\nname: x\ndescription: Routes to tools: A and B\n---\nbody\n",
                encoding="utf-8",
            )

            exit_before = gate.main(["--repo", str(root)])
            self.assertEqual(exit_before, 1)

            exit_fix = gate.main(["--repo", str(root), "--fix"])
            self.assertEqual(exit_fix, 0)

            exit_after = gate.main(["--repo", str(root)])
            self.assertEqual(exit_after, 0)


if __name__ == "__main__":
    unittest.main()
