"""Core operations for a parallel Google Books Ngram map-reduce."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Iterator, Sequence
from concurrent.futures import ProcessPoolExecutor


def partition(items: Iterable[str], chunk_size: int) -> Iterator[list[str]]:
    """Yield lists containing at most ``chunk_size`` items."""
    if chunk_size < 1:
        raise ValueError("chunk_size must be at least 1")

    chunk: list[str] = []
    for item in items:
        chunk.append(item)
        if len(chunk) == chunk_size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


def map_frequencies(lines: Sequence[str]) -> Counter[str]:
    """Map Google Books 1-gram rows to cumulative counts by word."""
    frequencies: Counter[str] = Counter()
    for line in lines:
        if not line.strip():
            continue
        try:
            word, _year, count, _volume_count = line.rstrip("\r\n").split("\t")
            frequencies[word] += int(count)
        except (ValueError, TypeError) as error:
            raise ValueError(f"Invalid Ngram row: {line!r}") from error
    return frequencies


def merge_counts(counters: Iterable[Counter[str]]) -> Counter[str]:
    """Reduce partial counters into one counter."""
    result: Counter[str] = Counter()
    for counter in counters:
        result.update(counter)
    return result


def parallel_word_frequencies(
    lines: Iterable[str],
    *,
    chunk_size: int = 60_000,
    workers: int | None = None,
) -> Counter[str]:
    """Count words with a process pool while consuming ``lines`` incrementally."""
    chunks = partition(lines, chunk_size)
    with ProcessPoolExecutor(max_workers=workers) as pool:
        return merge_counts(pool.map(map_frequencies, chunks))
