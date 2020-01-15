"""Zaimplementuj kopiec binarny. Korzystając z tego kopca napisz funkcję
sortującą listę elementów w czasie O(n log n).
Przeprowadź analizę eksperymentalną czasu wykonania algorytmu.
"""

import matplotlib.pyplot as plt
import timeit
import numpy as np


def experiment(n):
    """Function to count average time of run heap_sort - function to sort Nodes in tree
    Experiment for every heap in size from 0 to n"""

    ran = list(range(1, n, 100))
    times = []
    statement = """from z2 import heap_sort; heap_sort(to_heap)"""

    for num in ran:
        # to_heap - random list
        setup = """import random; to_heap = [random.randrange(1, 30) for _ in range(0, {n})];""".format(n=num)

        # timeit count time of run function given in stmt
        t = timeit.timeit(stmt=statement, setup=setup, number=100)

        times.append(t)

    # Make plot:

    x = np.linspace(0, n)

    plt.plot(x, x * np.log(x)/2000, 'blue', label="O(nlogn)")

    plt.plot(ran, times, 'ro')
    plt.xlabel('Size of input (n)')
    plt.ylabel('Average time')
    plt.title('Time complexity of sort function')
    plt.legend()
    plt.grid()

    plt.show()

experiment(2001)
