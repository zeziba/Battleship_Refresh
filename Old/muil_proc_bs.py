__author__ = "Charles Engen"

import multiprocessing
import datetime
import cProfile
import sys

from Old import Battleship_1_0_0

max_processes = multiprocessing.cpu_count() - 1
iterations = 100


def update_progress(progress):
    print("\r[{0}] {1}%".format("#" * (progress / 10), progress))


def save_time_stamp(start, end):
    with open(
        Battleship_1_0_0.join_(
            Battleship_1_0_0.path_gamedata_, "battleship_M_time.txt"
        ),
        "a+",
    ) as file:
        file.write("%s\n" % (start - end))


def worker(x=0):
    start = Battleship_1_0_0.time.time()
    while True:
        if x % 100 == 0:
            if sys.flags.interactive:
                update_progress(int(x / iterations * 100))
        Battleship_1_0_0._start_game(override=x, display=False)
        return save_time_stamp(start, Battleship_1_0_0.time.time())


def main():
    try:
        start = datetime.datetime.now()

        process_pool = multiprocessing.Pool(max_processes)

        results = process_pool.map_async(worker, range(iterations))

        process_pool.close()
        process_pool.join()

        print("Job took: %s" % (datetime.datetime.now() - start))

        input()

    except KeyboardInterrupt:
        print(KeyboardInterrupt)
        process_pool.close()
        process_pool.join()

        input("Waiting for keypress")


if __name__ == "__main__":
    cProfile.run("main()")
