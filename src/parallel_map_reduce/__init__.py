"""Utilities for a process-based word-frequency map-reduce."""

from .core import map_frequencies, merge_counts, parallel_word_frequencies, partition

__all__ = [
    "map_frequencies",
    "merge_counts",
    "parallel_word_frequencies",
    "partition",
]
