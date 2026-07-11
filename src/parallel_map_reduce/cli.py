"""Command-line interface for the parallel map-reduce example."""

from __future__ import annotations

import argparse
import time
from pathlib import Path
from typing import Sequence

from .core import parallel_word_frequencies


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Count words in a Google Books 1-gram file in parallel."
    )
    parser.add_argument("input", type=Path, help="path to an extracted 1-gram file")
    parser.add_argument("--word", help="print only the count for this word")
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=60_000,
        help="rows sent to each map task (default: 60000)",
    )
    parser.add_argument(
        "--workers",
        type=int,
        help="worker process count (default: number chosen by Python)",
    )
    parser.add_argument("--encoding", default="utf-8", help="input encoding")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    started = time.perf_counter()

    try:
        with args.input.open(encoding=args.encoding) as lines:
            frequencies = parallel_word_frequencies(
                lines,
                chunk_size=args.chunk_size,
                workers=args.workers,
            )
    except (OSError, UnicodeError, ValueError) as error:
        raise SystemExit(f"error: {error}") from error

    if args.word is not None:
        print(f"{args.word} has appeared {frequencies[args.word]} times.")
    else:
        for word, count in frequencies.most_common():
            print(f"{word}\t{count}")

    print(f"Map-reduce took {time.perf_counter() - started:.4f} seconds.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
