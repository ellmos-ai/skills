"""Offline regression coverage for worldset's leading-LF parser normalization.

This file is self-contained and provider-free. It can be copied next to
worldset.py in the bilingual-doc-sync scripts directory.
"""
import unittest

from worldset import gates, protect, restore, sha, split_frontmatter

COMMAND = "npx hyperframes skills update pr-to-video"
TICK = chr(96)
FENCE = TICK * 3

DESCRIPTION_SOURCE = (
    "---\n"
    "name: demo\n"
    "description: A short skill description.\n"
    "language: en\n"
    "---\n"
    "\n"
    '<img src="banner.png" alt="banner">\n'
    "> **First:** run the same command " + TICK + COMMAND + TICK + " for setup.\n"
    "> Keep the exact command.\n"
)

INVARIANT_SOURCE = (
    "# Safety\n\n"
    "Run " + TICK + "tool --check" + TICK + ".\n\n"
    "[Docs](https://example.test/docs)\n\n"
    '<img src="banner.png" alt="demo">\n\n'
    + FENCE + "sh\n"
    "printf 'safe'\n"
    + FENCE + "\n\n"
    "    tool --dry-run\n"
)


def roundtrip(source, lang="de"):
    protected, _, _ = protect(source)
    return restore(
        source,
        protected,
        lang,
        "offline-fixture",
        sha(source.encode("utf-8")),
        translated_at="fixed",
    )


class LeadingLfNormalizationTests(unittest.TestCase):
    def test_description_html_boundary_keeps_unchanged_command(self):
        source = DESCRIPTION_SOURCE
        source_body = split_frontmatter(source)[1]
        self.assertTrue(source_body.startswith("\n"))
        self.assertEqual(source.count(COMMAND), 1)

        protected, chunks, _ = protect(source)
        self.assertTrue(any(COMMAND in chunk for chunk in chunks))
        translated = protected.replace("First", "Start")
        candidate = restore(
            source,
            translated,
            "de",
            "offline-fixture",
            sha(source.encode("utf-8")),
            translated_at="fixed",
        )

        self.assertEqual(candidate.count(COMMAND), 1)
        self.assertEqual(gates(source, candidate, "de"), [])

        changed_command = candidate.replace(COMMAND, COMMAND + " --dry-run")
        self.assertIn("protected_regions_changed", gates(source, changed_command, "de"))

    def test_yaml_frontmatter_zero_one_and_multiple_leading_lfs(self):
        header = "---\nname: demo\nlanguage: en\n---\n"
        outputs = []
        for count in (0, 1, 3):
            with self.subTest(leading_lfs=count):
                source = header + ("\n" * count) + "# Heading\n\nBody text.\n"
                protected, chunks, fm = protect(source)
                outputs.append((protected, chunks, fm))
                candidate = roundtrip(source)
                self.assertEqual(gates(source, candidate, "de"), [])
        self.assertEqual(outputs[0], outputs[1])
        self.assertEqual(outputs[0], outputs[2])

    def test_no_frontmatter_zero_one_and_multiple_leading_lfs(self):
        outputs = []
        for count in (0, 1, 3):
            with self.subTest(leading_lfs=count):
                source = ("\n" * count) + "# Heading\n\nBody text.\n"
                outputs.append(protect(source))
                candidate = roundtrip(source)
                self.assertEqual(gates(source, candidate, "de"), [])
        self.assertEqual(outputs[0], outputs[1])
        self.assertEqual(outputs[0], outputs[2])

    def test_interior_blank_lines_are_preserved(self):
        source = (
            "---\nname: demo\nlanguage: en\n---\n"
            "\n\n\n"
            "# Heading\n\n\nBody text.\n"
        )
        protected, _, _ = protect(source)
        self.assertIn("# Heading\n\n\nBody text.\n", protected)

    def test_changed_added_or_removed_code_urls_and_html_are_held(self):
        source = INVARIANT_SOURCE
        candidate = roundtrip(source)
        self.assertEqual(gates(source, candidate, "de"), [])

        link = "[Docs](https://example.test/docs)"
        image = '<img src="banner.png" alt="demo">'
        mutations = {
            "changed inline code": candidate.replace("tool --check", "tool --force"),
            "added inline code": candidate.replace(
                "Run " + TICK + "tool --check" + TICK + ".",
                "Run " + TICK + "tool --check" + TICK + " and "
                + TICK + "tool --verbose" + TICK + ".",
            ),
            "removed inline code": candidate.replace(
                "Run " + TICK + "tool --check" + TICK + ".", "Run the tool."
            ),
            "changed fenced code": candidate.replace("printf 'safe'", "printf 'unsafe'"),
            "changed indented code": candidate.replace("tool --dry-run", "tool --force"),
            "changed URL": candidate.replace(
                "https://example.test/docs", "https://example.test/changed"
            ),
            "added URL": candidate.replace(
                link, link + "\n\nMore at https://example.test/extra"
            ),
            "removed URL": candidate.replace(link + "\n\n", ""),
            "changed HTML": candidate.replace('alt="demo"', 'alt="changed"'),
            "added HTML": candidate.replace(image, image + "\n\n<span>new</span>"),
            "removed HTML": candidate.replace(image + "\n\n", ""),
        }

        for label, mutated in mutations.items():
            with self.subTest(mutation=label):
                self.assertNotEqual(mutated, candidate)
                self.assertIn("protected_regions_changed", gates(source, mutated, "de"))


if __name__ == "__main__":
    unittest.main()
