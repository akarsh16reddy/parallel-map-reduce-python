import asyncio
import concurrent.futures
import functools
import time
from collections import defaultdict
from pathlib import Path

DATA_PATH = (
    Path(__file__).parent
    / "googlebooks-eng-all-1gram-20120701-a"
    / "googlebooks-eng-all-1gram-20120701-a"
)

# python 6_8_parallel_map_with_process_pools.py
# Aardvark has appeared 15209 times.
# MapReduce took: 24.7294 seconds


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
            final_result = functools.reduce(merge_dictionaries, intermediate_results)

            print(
                f"{word_to_search} has appeared {final_result[word_to_search]} times."
            )

            end = time.time()
            print(f"MapReduce took: {end - start:.4f} seconds")


if __name__ == "__main__":
    asyncio.run(main(partition_size=60_000))
