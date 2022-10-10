import ctypes
import numpy as np

lib = ctypes.CDLL("./clib.so")
f = lib.worker
f.restype = ctypes.POINTER(ctypes.c_long)


def worker_clib(nparr: np.ndarray):
    length = len(nparr)
    ret_raw = f(np.ctypeslib.as_ctypes(nparr), length, 5)
    ret = np.ctypeslib.as_array(ret_raw, shape=[length, 2])
    return ret[ret[:, 0] != -1]
