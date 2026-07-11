import asyncio
import time
from asyncio import AbstractEventLoop
from concurrent.futures import ProcessPoolExecutor
from functools import partial


def count(count_to: int) -> int:
    start = time.time()
    counter = 0
    while counter < count_to:
        counter += 1
    end = time.time()

    print(f"Finished counting to {count_to} in {end - start}")
    return counter


async def main():
    with ProcessPoolExecutor() as process_pool:
        loop: AbstractEventLoop = asyncio.get_event_loop()
        numbers = [100_000_000, 1, 3, 5, 22]
        calls = [partial(count, num) for num in numbers]
        call_coroutines = []

        for call in calls:
            call_coroutines.append(loop.run_in_executor(process_pool, call))

        results = await asyncio.gather(*call_coroutines)

        for result in results:
            print(result)

        print("Let's use as_completed")
        await asyncio.sleep(2)
        call_coroutines = []

        for call in calls:
            call_coroutines.append(loop.run_in_executor(process_pool, call))
        for result in asyncio.as_completed(call_coroutines):
            print(await result)


if __name__ == "__main__":
    asyncio.run(main())
