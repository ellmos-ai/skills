"""Real table loss must fail; ordinary pipe text and spacing may be translated."""
import unittest

import worldset as w


class TableStructureTests(unittest.TestCase):
    def test_wrapped_pipe_prose_is_not_a_table(self):
        source = '- **Rule:** resource | exact call\n  | budget per window | expires.\n'
        candidate = '- **Rule:** resource | exact call | budget per window | expires.\n'
        self.assertEqual(w.gates(source, candidate, 'en'), [])

    def test_blank_lines_before_real_tables_are_not_structure(self):
        table = '| Name | Value |\n| --- | --- |\n| One | Two |\n'
        self.assertEqual(w.gates('Text.\n\n' + table, 'Text.\n\n\n' + table, 'en'), [])

    def test_removed_real_table_row_is_rejected(self):
        header = '| Name | Value |\n| --- | --- |\n'
        source = header + '| One | Two |\n| Three | Four |\n'
        candidate = header + '| One | Two |\n'
        self.assertIn('table_rows', w.gates(source, candidate, 'en'))

    def test_removed_real_table_column_is_rejected(self):
        source = '| Name | Value | Unit |\n| --- | --- | --- |\n| One | Two | Three |\n'
        candidate = '| Name | Value |\n| --- | --- |\n| One | Two |\n'
        self.assertIn('table_rows', w.gates(source, candidate, 'en'))

    def test_table_like_fence_is_preserved_without_false_table(self):
        fence = '```text\n| Name | Value |\n| --- | --- |\n| One | Two |\n```\n'
        self.assertEqual(w.gates('First explanation.\n\n' + fence,
                                 'Second explanation.\n\n' + fence, 'en'), [])


if __name__ == '__main__':
    unittest.main()
