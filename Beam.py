# ==========================================================
# adaptive_cover_final.py
# 题目：从 n 个样本中选若干 k-组合，使得
#       每个 j-组合拆出的所有 s-子集，至少被覆盖 t 次
# ----------------------------------------------------------
# n < 12  → 位运算 Beam + α-RCL   （本文件 Part-1）
# n ≥ 12  → 简易贪心             （本文件 Part-2）
# ==========================================================

import itertools, random, math, time, copy

# ---------- 通用工具 ----------
def comb(pool, r):
    """列出 pool 中所有 r 元子集（tuple 形式）"""
    return list(itertools.combinations(pool, r))

def to_mask(tup):
    """
    把一个元素集合 tup 转成『位掩码』整数：
        元素值当作 bit 位序号，出现的位置置 1
    例： tup = (1,3,4)
        1 << 1 = 0b00010
        1 << 3 = 0b01000
        1 << 4 = 0b10000
      OR 起来 = 0b11010  → 十进制 26
    后面判断 “S ⊆ K” 只需做
        (mask_K & mask_S) == mask_S
    整个包含关系判断变成 **常数级位运算**。
    """
    m = 0
    for x in tup:
        m |= 1 << x
    return m
# ==========================================================
#  Part-1 ▸  位运算 Beam + α-RCL  （n < 12，含注释）
# ----------------------------------------------------------
def beam_bit(n, k, j, s, t=1,
             alpha=0.3,
             beam_top=(16, 6),
             seed=None):

    if seed is not None:
        random.seed(seed)

    # ---------- ① 预生成 ----------
    K_elems = comb(range(n), k)                 # 所有 k-组合
    J_elems = comb(range(n), j)                 # 所有 j-组合
    Kmask   = [to_mask(c) for c in K_elems]     # 每个 K 的位掩码
    """
    举例 n=4, k=2 时：
        K_elems = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
        Kmask   = [3,5,9,6,10,12]  # 对应 0b0011 / 0b0101 / ...
    """
    Smask = [[to_mask(c) for c in comb(J_elems[i], s)]
             for i in range(len(J_elems))]
    """
    每个 J 内再列出所有 s-子集：
        J = (0,1,2), s=2 → Smask = [3,5,6]
        J = (0,1,3)      → Smask = [3,9,10]
      整体 Smask 变成二维列表：
        [[3,5,6],
         [3,9,10],
         [5,9,12],
         [6,10,12]]
    """
    mK, mJ  = len(Kmask), len(J_elems)
    SjLen   = len(Smask[0])         # 每个 J 里 S 条数相同 (=C(j,s))
    full    = (1 << SjLen) - 1      # 例如 SjLen=3 → 0b111

    # ---------- ② coverKJ[k][J] 构建 ----------
    coverKJ = [[0]*mJ for _ in range(mK)]
    for ki, km in enumerate(Kmask):
        for ji, slist in enumerate(Smask):
            hit = 0
            for idx, sm in enumerate(slist):
                if km & sm == sm:    # K 覆盖了该 S
                    hit |= 1 << idx  # 把第 idx 位 设 1
            coverKJ[ki][ji] = hit
    """
    仍以 n=4,k=2,j=3,s=2 为例，coverKJ 会是：
      K=(0,1)  → [0b011, 0b011, 0b000, 0b000]
      K=(0,2)  → [0b101, 0b001, 0b101, 0b000]
      ...
    每个元素都是“该 K 对该 J 命中的 S 位掩码”。
    """

    # ---------- ③ Beam 初始化 ----------
    Beam  = [{'sol': set(), 'unc': [full]*mJ}]  # unc = 每个 J 未覆盖 S 的位掩码
    layer = 0
    while True:
        New = []
        for st in Beam:
            sol, unc = st['sol'], st['unc']

            # ---------- (a) 若已满足覆盖 ----------
            if all(bin(unc[J]).count('1') <= SjLen - t for J in range(mJ)):
                New.append(st)
                continue

            # ---------- (b) 计算候选 K 的增益 ----------
            gains = []
            for ki in range(mK):
                if ki in sol:
                    continue
                gain_per_J = [bin(coverKJ[ki][J] & unc[J]).count('1')
                              for J in range(mJ)]
                need_per_J = [bin(unc[J]).count('1') - (SjLen - t)
                              for J in range(mJ)]
                if not any(g >= need for g, need in zip(gain_per_J, need_per_J)):
                    continue
                gains.append((sum(gain_per_J), ki))
            if not gains:
                raise RuntimeError("Beam 无可行扩展，调大 alpha 或 beam_top")

            gains.sort(reverse=True)
            rcl_len = max(1, int(alpha * len(gains)))  # α-RCL

            # ---------- (c) 扩展子路径 ----------
            for _, ki in gains[:rcl_len]:
                new_unc = [unc[J] & ~coverKJ[ki][J] for J in range(mJ)]
                New.append({'sol': sol | {ki}, 'unc': new_unc})

        # ---------- ④ 评分 + 剪枝 ----------
        def score(st):
            covered = [SjLen - bin(st['unc'][J]).count('1') for J in range(mJ)]
            deficit = sum(1 for c in covered if c < t)     # 未满足的 J 数
            over    = sum(max(0, c - t) for c in covered)  # 过度覆盖
            mean    = sum(covered) / mJ
            var     = sum((c - mean)**2 for c in covered) / mJ
            return (deficit, len(st['sol']), over, var)

        New.sort(key=score)
        width = beam_top[0] if layer < 3 else beam_top[1]
        Beam  = New[:width]
        layer += 1

        # 若 Beam 中全部满足阈值 → 退出
        if all(bin(st['unc'][J]).count('1') <= SjLen - t
               for st in Beam for J in range(mJ)):
            break

    best = min(Beam, key=lambda st: len(st['sol']))['sol']
    return [tuple(sorted(K_elems[i])) for i in sorted(best)]

# ==========================================================
#  Part-2 ▸ 简易贪心（n ≥ 12）
# ----------------------------------------------------------
class GreedySolver:
    def manipulate(self, n, k, j, s):
        poss = list(itertools.combinations(range(n), k))
        targ = list(itertools.combinations(range(n), j))
        remain = targ.copy()
        ans = []
        while remain:
            best = max(poss, key=lambda blk:
                       sum(1 for C in remain if len(set(C) & set(blk)) >= s))
            ans.append(best)
            remain = [C for C in remain if len(set(C) & set(best)) < s]
        return ans

greedy_solver = GreedySolver()

# ==========================================================
# 统一接口
# ----------------------------------------------------------
def search_cover(n, k, j, s, t=1, seed=0):
    random.seed(seed)
    if n < 12:
        return beam_bit(n, k, j, s, t=t, seed=seed)
    return greedy_solver.manipulate(n, k, j, s)

# ==========================================================
# Quick demo
# ----------------------------------------------------------
if __name__ == "__main__":
    tests = [
       (10,6,4,4,1)
    ]
    for n, k, j, s, t in tests:
        t0 = time.time()
        sol = search_cover(n, k, j, s, t, seed=0)
        print(f"n={n:<2d}  选 {len(sol):2d} 组K  耗时 {time.time()-t0:.4f}s  {sol}")