import asyncio
import concurrent.futures
import functools
import time
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List

DATA_PATH = (
    Path(__file__).parent
    / "googlebooks-eng-all-1gram-20120701-a"
    / "googlebooks-eng-all-1gram-20120701-a"
)


def partition(data, chunk_size):
    for i in range(0, len(data), chunk_size):
        yield data[i : i + chunk_size]


def map_frequencies(chunk):
    counter = defaultdict(int)
    for line in chunk:
        word, _, count, _ = line.split("\t")
        counter[word] += int(count)
    return counter


def merge_dictionaries(first, second):
    merged = first
    for key, value in second.items():
        merged[key] += value
    return merged


async def reduce(loop, pool, counters, chunk_size) -> Dict[str, int]:
    chunks = list(partition(counters, chunk_size))
    reducers: List[Any] = []
    while len(chunks[0]) > 1:
        for chunk in chunks:
            reducer = functools.partial(functools.reduce, merge_dictionaries, chunk)
            reducers.append(loop.run_in_executor(pool, reducer))
        reducer_chunks = await asyncio.gather(*reducers)
        chunks = list(partition(reducer_chunks, chunk_size))
        reducers.clear()
    return chunks[0][0]


async def main(partition_size: int):
    with DATA_PATH.open(encoding="utf-8") as f:
        contents = f.readlines()
        word_to_search = "Aardvark"
        loop = asyncio.get_running_loop()
        tasks = []
        start = time.time()
        with concurrent.futures.ProcessPoolExecutor() as process_pool:
            for chunk in partition(contents, partition_size):
                tasks.append(
                    loop.run_in_executor(
                        process_pool, functools.partial(map_frequencies, chunk)
                    )
                )

            intermediate_results = await asyncio.gather(*tasks)
            # final_result = functools.reduce(merge_dictionaries, intermediate_results)
            final_result = await reduce(loop, process_pool, intermediate_results, 500)

            print(
                f"{word_to_search} has appeared {final_result[word_to_search]} times."
            )

            end = time.time()
            print(f"MapReduce took: {end - start:.4f} seconds")


if __name__ == "__main__":
    asyncio.run(main(partition_size=60_000))
