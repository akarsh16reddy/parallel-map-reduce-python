import time
from concurrent.futures import ProcessPoolExecutor


def count(count_to: int) -> int:
    start = time.time()
    counter = 0
    while counter < count_to:
        counter += 1
    end = time.time()

    print(f"Finished counting to {count_to} in {end - start}")
    return counter


if __name__ == "__main__":
    start_time = time.time()
    with ProcessPoolExecutor() as process_pool:
        numbers = [100_000_000, 1, 3, 5, 22]
        for result in process_pool.map(count, numbers):
            print(result)

    end_time = time.time()
    print(f"Completed in {end_time - start_time}")
