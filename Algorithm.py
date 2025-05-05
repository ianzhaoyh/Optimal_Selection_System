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
from LP import LP

def manipulate(n, k, j, s, t=1, *, seed=0):
    """
    自动分派：n < 12 → Beam；n ≥ 12 → Greedy
    返回 (耗时, 选中块数, 列表[tuple])
    """
    n = int(n); k = int(k); j = int(j); s = int(s); t = int(t)
    time_start = time.time()
    
    try:
        # 参数验证
        if not all(x > 0 for x in [n,k,j,s,t]):
            raise ValueError("所有参数必须为正整数")
        if k > n or j > n or s > j:
            raise ValueError("参数关系错误: 需要 k<=n, j<=n, s<=j")
            
        # 选择算法
        if t!=1:
            sol = beam_bit(n, k, j, s, t=t, seed=seed)
        elif n <=13 and j==s and j>=5:
            return LP(n,k,j,s)
        else:
            sol = greedy_cover(n, k, j, s)
        return time.time() - time_start, len(sol), sol
        
    except Exception as e:
        print(f"Error in manipulate: {str(e)}")
        return time.time() - time_start, 0, []


# ---------------- Quick demo ----------------
if __name__ == "__main__":
    cases = [(9,6,5,4,1),(12,6,5,4,1),(13,6,5,4,1),(16,6,5,4,1),(10,6,6,4,1),(12,6,6,4,1),(13,6,6,4,1),(16,6,6,4,1)]
    for n,k,j,s,t in cases:
        dt, m, sol = manipulate(n,k,j,s,t)
        print(f"n={n:<2d}  选 {m:2d} 组K  耗时 {dt:.4f}s  {sol[:3]} ...")