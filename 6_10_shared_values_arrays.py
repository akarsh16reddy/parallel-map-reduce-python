from multiprocessing import Array, Process, Value


def increment_value(shared_int: Value):
    shared_int.value = shared_int.value + 1


def increment_array(shared_array: Array):
    for index, integer in enumerate(shared_array):
        shared_array[index] = integer + 1


if __name__ == "__main__":
    integer = Value("i", 0)
    integer_array = Array("i", [0, 0])
    normal_array = [0, 0]

    # This won't have an impact because process uses it's own memory reference
    # When the current process forks a child process, the child won't be able to
    # Access memory location inside the parent, hence, use multiprocessing.Array

    procs = [
        Process(target=increment_value, args=(integer,)),
        Process(target=increment_array, args=(integer_array,)),
        Process(target=increment_array, args=(normal_array,)),
    ]

    [p.start() for p in procs]
    [p.join() for p in procs]

    print(integer.value)
    print(integer_array[:])
    print(normal_array)
