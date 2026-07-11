import asyncio
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from functools import partial

shared_counter: Value


def init(counter: Value):
    global shared_counter
    shared_counter = counter


def increment():
    with shared_counter.get_lock():
        shared_counter.value += 1


def increment_with_counter(counter: Value):
    with shared_counter.get_lock():
        shared_counter.value += 1


async def main_pattern_a():
    counter = multiprocessing.Value("d", 0)
    with ProcessPoolExecutor(initializer=init, initargs=(counter,)) as pool:
        await asyncio.get_running_loop().run_in_executor(pool, increment)
        await asyncio.get_running_loop().run_in_executor(pool, increment)
        await asyncio.get_running_loop().run_in_executor(pool, increment)
        print(counter.value)


# This won't work as multiprocessing.Value cannot be pickled.

# async def main_pattern_b():
#     counter = multiprocessing.Value("d", 0)
#     with ProcessPoolExecutor() as pool:
#         await asyncio.get_running_loop().run_in_executor(
#             pool, partial(increment_with_counter, counter)
#         )
#         await asyncio.get_running_loop().run_in_executor(
#             pool, partial(increment_with_counter, counter)
#         )
#         await asyncio.get_running_loop().run_in_executor(
#             pool, partial(increment_with_counter, counter)
#         )
#         print(counter.value)


if __name__ == "__main__":
    asyncio.run(main_pattern_a())
