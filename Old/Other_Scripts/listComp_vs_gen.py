__author__ = "Charles Engen"

from time import time


def list_vs_gen(num_1, num_2):
    start_list = time()
    a = [n_1 * n_2 for n_1 in range(1, num_1 + 1) for n_2 in range(1, num_2 + 1)]
    print(len(a), "\n%s\n" % (time() - start_list))
    start_gen = time()
    b = (n_1 * n_2 for n_1 in range(1, num_1 + 1) for n_2 in range(1, num_2 + 1))
    print(len(*b), time() - start_gen)


list_vs_gen(500, 500)
