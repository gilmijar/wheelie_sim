import unittest
from collections import Sequence
import interaction_with_database as interaction


class TestNamedTupleCreation(unittest.TestCase):
    def setUp(self):
        self.columns = tuple(f'col_{i}' for i in range(5))
        val = iter(range(300))
        self.rows = [
            tuple(next(val) for _ in self.columns) for _ in range(3)
        ]

    def test_result_has_same_names_as_input_columns(self):
        result = interaction.result_as_named_tuples(self.columns, self.rows)
        self.assertEqual(self.columns, result[0]._fields)

    def test_result_is_flat_sequence_if_input_is_flat_sequence(self):
        result = interaction.result_as_named_tuples(self.columns, self.rows[0])
        self.assertNotIsInstance(result[0], Sequence)

    def test_result_count_is_same_as_input_rowcount(self):
        result = interaction.result_as_named_tuples(self.columns, self.rows)
        self.assertCountEqual(self.rows, result)

    def test_result_returns_empty_list_when_no_rows_provided(self):
        result = interaction.result_as_named_tuples(self.columns, [])
        self.assertCountEqual(result, [])

    def test_result_raises_exception_when_no_columns_provided(self):
        blank_options = (None, [], ())
        for option in blank_options:
            with self.subTest(f"Empty {type(option)} does not raise error"):
                with self.assertRaises(ValueError):
                    interaction.result_as_named_tuples([], self.rows)

    def test_result_produces_subclass_named_with_what_was_provided_as_param(self):
        result = interaction.result_as_named_tuples(self.columns, self.rows, 'Banana')
        self.assertEqual('Banana', result[0].__class__.__name__)

    def test_result_produces_subclass_named_result_when_no_name_provided(self):
        result = interaction.result_as_named_tuples(self.columns, self.rows)
        self.assertEqual('Result', result[0].__class__.__name__)


if __name__ == '__main__':
    unittest.main()
