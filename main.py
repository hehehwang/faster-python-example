import pickle as pkl
from multiprocessing import Pool
from pathlib import Path
from random import randint
from time import perf_counter
from typing import List, Tuple

import numpy as np

from clib_wrap import worker_clib

criteria = 5


def worker(job: List[Tuple[int, int]]):
    rtn = []
    for x, y in job:
        if x * x + y * y <= criteria * criteria:
            rtn.append((x, y))
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
        works_np = np.array(works)
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
initialize:  6.343260499997996
result: 751089, naive duration : 0.40277645800233586

result: 751089, numpy duration : 0.04539262500475161

result: 751089, multiprocessing duration : 1.0570068339948193

result: 751089, clib duration : 1.7647754159988835
"""