import ctypes
import os

import numpy as np

lib = ctypes.CDLL("./clib.so" if os.name == "posix" else "./clib.dll")
f = lib.worker
f.restype = ctypes.POINTER(ctypes.c_longlong)


def worker_clib(nparr: np.ndarray):
    length = len(nparr)
    nparr = nparr.astype("int64")
    ret_raw = f(np.ctypeslib.as_ctypes(nparr), length, 5)
    ret = np.ctypeslib.as_array(ret_raw, shape=[length, 2])
    return ret[ret[:, 0] != -1]


def test():
    print(worker_clib(np.array([[1, 2], [3, 4], [5, 6]], dtype="int64")))


def main():
    test()


if __name__ == "__main__":
    main()
