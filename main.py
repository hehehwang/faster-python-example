import pickle as pkl
from multiprocessing import Pool
from pathlib import Path
from random import randint
from time import perf_counter
from typing import List, Tuple

import numpy as np
from numba import jit

from clib_wrap import worker_clib

criteria = 5


def worker(job: List[Tuple[int, int]]):
    rtn = [(x, y) for x, y in job if x * x + y * y <= criteria * criteria]
    return rtn


@jit(nopython=True)
def worker_numba(job):
    rtn = [(x, y) for x, y in job if x * x + y * y <= criteria * criteria]
    return rtn


def main():
    global criteria

    marker = perf_counter()
    works_filename = "works_small"
    if Path(works_filename + ".pkl").exists():
        print("Loading from pickle")
        works = pkl.load(open(works_filename + ".pkl", "rb"))
        works_np = pkl.load(open(works_filename + "_np.pkl", "rb"))
        print("done")
    else:
        works = [
            [(randint(1, 10), randint(1, 10)) for _ in range(5_000)]
            for _ in range(1_000)
        ]
        works_np = np.array(works, dtype="int64")
        with open(works_filename + ".pkl", "wb") as f:
            pkl.dump(works, f)
        with open(works_filename + "_np.pkl", "wb") as f:
            pkl.dump(works_np, f)

    criteria = 5
    print("initialize: ", perf_counter() - marker)

    marker = perf_counter()
    result_naive = []
    for w in works:
        result_naive.extend(worker(w))
    print(f"result: {len(result_naive)}, naive duration : {perf_counter() - marker}\n")

    marker = perf_counter()
    # worker_numba = jit(lambda w: worker(w))
    result_numba = []
    for w in works_np:
        result_numba.extend(worker_numba(w))
    print(f"result: {len(result_numba)}, numba duration : {perf_counter() - marker}\n")

    marker = perf_counter()
    result_np = works_np[
        works_np[:, :, 0] * works_np[:, :, 0] + works_np[:, :, 1] * works_np[:, :, 1]
        <= criteria * criteria
    ]
    print(f"result: {len(result_np)}, numpy duration : {perf_counter() - marker}\n")

    pool = Pool()
    marker = perf_counter()
    result_mp = []
    for r in pool.map(worker, works):
        result_mp.extend(r)
    print(
        f"result: {len(result_mp)}, multiprocessing duration : {perf_counter() - marker}\n"
    )

    marker = perf_counter()
    result_clib_tmp = [worker_clib(w_np) for w_np in works_np]
    result_clib = np.concatenate(result_clib_tmp, axis=0)
    print(f"result: {len(result_clib)}, clib duration : {perf_counter() - marker}\n")


if __name__ == "__main__":
    main()

"""
on macOS (M1):
initialize:  0.28590524999890476
result: 751089, naive duration : 0.3948318749971804

result: 751089, numba duration : 0.22138149999955203

result: 751089, numpy duration : 0.052155458004563116

result: 751089, multiprocessing duration : 1.1577142919995822

result: 751089, clib duration : 0.06615670800238149
===========================================================
on windows (Ryzen 5 5600X)
initialize:  0.4726191999980074
result: 749200, naive duration : 0.5674392000000807

result: 749200, numpy duration : 0.036203600000590086

result: 749200, multiprocessing duration : 1.012214899998071

result: 749200, clib duration : 0.07173800000236952
"""
