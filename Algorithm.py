# Al.py //backend
import itertools
import copy
import time
import random
import math
import config as thread_running
import threading
import pulp
from concurrent.futures import ThreadPoolExecutor

# manipulate.py (原 Al.py 简化) ---------------------------------
import time
from Beam import beam_bit
from Greedy import greedy_cover

def manipulate(n, k, j, s, t=1, *, seed=0):
    """
    自动分派：n < 12 → Beam；n ≥ 12 → Greedy
    返回 (耗时, 选中块数, 列表[tuple])
    """
    n = int(n); k = int(k); j = int(j); s = int(s); t = int(t)
    time_start = time.time()

    if n < 12:
        sol = beam_bit(n, k, j, s, t=t, seed=seed)
    else:
        sol = greedy_cover(n, k, j, s)

    return time.time() - time_start, len(sol), sol


# ---------------- Quick demo ----------------
if __name__ == "__main__":
    cases = [(8,6,4,4,1), (8,6,6,5,4), (10,6,6,4,1)]
    for n,k,j,s,t in cases:
        dt, m, sol = manipulate(n,k,j,s,t)
        print(f"n={n:<2d}  选 {m:2d} 组K  耗时 {dt:.4f}s  {sol[:3]} ...")