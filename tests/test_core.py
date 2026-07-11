from collections import Counter
import unittest

from parallel_map_reduce.core import (
    map_frequencies,
    merge_counts,
    parallel_word_frequencies,
    partition,
)


ROWS = [
    "Aardvark\t1990\t10\t2\n",
    "Python\t1991\t7\t1\n",
    "Aardvark\t1992\t5\t1\n",
]


class CoreTests(unittest.TestCase):
    def test_partition_keeps_final_partial_chunk(self):
        self.assertEqual(list(partition(iter(ROWS), 2)), [ROWS[:2], ROWS[2:]])

    def test_partition_rejects_non_positive_size(self):
        with self.assertRaisesRegex(ValueError, "at least 1"):
            list(partition(ROWS, 0))

    def test_map_frequencies_sums_years_and_ignores_blanks(self):
        self.assertEqual(
            map_frequencies([*ROWS, "\n"]), Counter(Aardvark=15, Python=7)
        )

    def test_map_frequencies_rejects_malformed_rows(self):
        with self.assertRaisesRegex(ValueError, "Invalid Ngram row"):
            map_frequencies(["not-a-valid-row"])

    def test_merge_counts(self):
        self.assertEqual(
            merge_counts([Counter(a=2), Counter(a=3, b=1)]),
            Counter(a=5, b=1),
        )

    def test_parallel_word_frequencies(self):
        self.assertEqual(
            parallel_word_frequencies(ROWS, chunk_size=2, workers=2),
            Counter(Aardvark=15, Python=7),
        )


if __name__ == "__main__":
    unittest.main()
