import asyncio
import concurrent.futures
import functools
import time
from collections import defaultdict
from multiprocessing import Value
from pathlib import Path

DATA_PATH = (
    Path(__file__).parent
    / "googlebooks-eng-all-1gram-20120701-a"
    / "googlebooks-eng-all-1gram-20120701-a"
)

# python -m multi_processing.6_14_count_maps_in_parallel_map_reduce
# Finished 19 / 1443 map operations
# Finished 133 / 1443 map operations
# Finished 262 / 1443 map operations
# Finished 392 / 1443 map operations
# Finished 525 / 1443 map operations
# Finished 657 / 1443 map operations
# Finished 790 / 1443 map operations
# Finished 924 / 1443 map operations
# Finished 1055 / 1443 map operations
# Finished 1188 / 1443 map operations
# Finished 1322 / 1443 map operations
# Aardvark has appeared 15209 times.
# MapReduce took: 15.2385 seconds

map_progress: Value


def init(progress: Value):
    global map_progress
    map_progress = progress


def partition(data, chunk_size):
    for i in range(0, len(data), chunk_size):
        yield data[i : i + chunk_size]


def map_frequencies(chunk):
    global map_progress

    counter = defaultdict(int)
    for line in chunk:
        word, _, count, _ = line.split("\t")
        counter[word] += int(count)

    with map_progress.get_lock():
        map_progress.value += 1

    return counter


def merge_dictionaries(first, second):
    merged = first
    for key, value in second.items():
        merged[key] += value
    return merged


async def progress_reporter(total_partitions: int):
    global map_progress
    while map_progress.value < total_partitions:
        print(f"Finished {map_progress.value} / {total_partitions} map operations")
        await asyncio.sleep(1)


async def main(partition_size: int):
    with DATA_PATH.open(encoding="utf-8") as f:
        contents = f.readlines()
        word_to_search = "Aardvark"
        loop = asyncio.get_running_loop()
        tasks = []
        start = time.time()
        global map_progress
        map_progress = Value("i", 0)

        with concurrent.futures.ProcessPoolExecutor(
            initializer=init, initargs=(map_progress,)
        ) as process_pool:
            total_partitions = (len(contents) + partition_size - 1) // partition_size
            progress_reporter_task = asyncio.create_task(
                progress_reporter(total_partitions)
            )
            for chunk in partition(contents, partition_size):
                tasks.append(
                    loop.run_in_executor(
                        process_pool, functools.partial(map_frequencies, chunk)
                    )
                )

            intermediate_results = await asyncio.gather(*tasks)
            await progress_reporter_task
            final_result = functools.reduce(merge_dictionaries, intermediate_results)

            print(
                f"{word_to_search} has appeared {final_result[word_to_search]} times."
            )

            end = time.time()
            print(f"MapReduce took: {end - start:.4f} seconds")


if __name__ == "__main__":
    asyncio.run(main(partition_size=60_000))
