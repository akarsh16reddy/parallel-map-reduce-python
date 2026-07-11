# Parallel Map-Reduce in Python

A small, practical collection of examples showing how CPU-bound work can be
distributed across processes and coordinated with `asyncio`. The examples build
from basic `multiprocessing.Process` usage to a parallel map-reduce over Google
Books Ngram data.

The repository also includes an installable `parallel_map_reduce` package. Its
CLI processes the input file incrementally, so the complete dataset does not
need to be loaded into memory.

## Quick start

Python 3.10 or newer is required.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev,examples]"
python -m unittest discover -s tests
```

Run the reusable implementation against a tab-separated Google Books 1-gram
file:

```powershell
parallel-map-reduce path\to\googlebooks-eng-all-1gram-20120701-a --word Aardvark
```

Or invoke it without installing the console script:

```powershell
python -m parallel_map_reduce path\to\ngram-file --word Aardvark
```

Useful options include `--chunk-size`, `--workers`, and `--encoding`. Run with
`--help` for details.

## Input format

Each input row is expected to use the Google Books Ngram 1-gram layout:

```text
word<TAB>year<TAB>match_count<TAB>volume_count
```

Counts are summed by word across every year. Blank rows are ignored; malformed
rows produce an error that includes the bad line.

## Learning sequence

The numbered scripts are standalone examples:

| Script | Topic |
| --- | --- |
| `6_1`–`6_5` | Processes, pools, executors, and `asyncio` integration |
| `6_7` | Sequential Google Ngram aggregation |
| `6_8` | Parallel map with a serial reduce |
| `6_9` | Parallel map and multi-stage parallel reduce |
| `6_10`–`6_13` | Shared memory, race conditions, and locks |
| `6_14` | Reporting progress from parallel map workers |

The raw Google Books archive and extracted data are intentionally excluded from
Git because they are very large. Existing local copies remain available to the
scripts.

## Project layout

```text
src/parallel_map_reduce/  Reusable library and command-line interface
tests/                    Dependency-free unit and process-pool integration tests
6_*.py                    Original educational examples
```

## Notes

- Process worker functions must live at module scope so they can be pickled,
  especially on Windows where workers use the `spawn` start method.
- Larger chunks reduce inter-process communication overhead but use more memory.
- Parallelism helps CPU-heavy mapping. Disk throughput can remain the limiting
  factor for very large files.
