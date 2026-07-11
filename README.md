# Parallel Map-Reduce in Python

A process-based map-reduce implementation for aggregating Google Books Ngram
data. The installable `parallel_map_reduce` package includes a command-line
interface and processes input incrementally, so the complete dataset does not
need to be loaded into memory.

> Historical single-run results for 86,618,505 rows (excluding file-read time): sequential `80.65s`, parallel map with reduce `24.73s` on 8-core AMD Ryzen 5000 series Machine

## Quick start

Python 3.10 or newer is required.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
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

## How it works

The input is divided into configurable chunks. A process pool maps each chunk
to a partial word-frequency counter, then the partial counters are reduced into
the final result. Reading and partitioning are incremental to keep memory usage
bounded relative to the configured chunk size and process-pool buffering.

The raw Google Books archive and extracted data are intentionally excluded from
Git because they are very large.

Dataset downloadable at ![https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-1gram-20120701-a.gz](https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-1gram-20120701-a.gz)


## Project layout

```text
src/parallel_map_reduce/  Reusable library and command-line interface
tests/                    Dependency-free unit and process-pool integration tests
```

## Notes

- Process worker functions must live at module scope so they can be pickled,
  especially on Windows where workers use the `spawn` start method.
- Larger chunks reduce inter-process communication overhead but use more memory.
- Parallelism helps CPU-heavy mapping. Disk throughput can remain the limiting
  factor for very large files.
