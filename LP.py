import itertools, time, pulp
import config as thread_running

def LP(n, k, j, s, *, time_limit=30):
    """
    线性规划（CBC）精确求解  ―― 仅适用于 j == s 且 n 较小的场景
    返回 (elapsed_time, block_count, selected_K_list)
    """
    t0 = time.time()
    n, k, j, s = map(int, (n, k, j, s))
    print("LP algorithm")

    # ---------- 1. 枚举所有 k-组合 ----------
    def comb(pool, r):         # 小工具：列出 r 子集
        return list(itertools.combinations(pool, r))
    K_list = comb(range(n), k)                 # |K_list| = C(n,k)
    Main    = list(range(n))

    # ---------- 2. 将每个 k-组合映射到覆盖的“标签” ----------
    def encode(tup):                            # 把子集→bit-mask
        m = 0
        for x in tup: m |= 1 << x
        return m

    tags_per_K = []
    all_tags   = set()
    for blk in K_list:
        tag_set = {encode(sub) for sub in comb(blk, s)}   # 因为 j == s
        tags_per_K.append(tag_set)
        all_tags |= tag_set

    # ---------- 3. ILP 建模 ----------
    prob  = pulp.LpProblem("Minimize_K_Groups", pulp.LpMinimize)
    x_var = [pulp.LpVariable(f"x_{i}", cat="Binary") for i in range(len(K_list))]

    #   目标：最少块数
    prob += pulp.lpSum(x_var)

    #   约束：每个 tag 至少被覆盖一次
    for tag in all_tags:
        prob += pulp.lpSum(x_var[i] for i,tags in enumerate(tags_per_K) if tag in tags) >= 1

    status = prob.solve(pulp.PULP_CBC_CMD(msg=False, timeLimit=time_limit))
    if pulp.LpStatus[status] != "Optimal":
        # 求解失败：返回空结果，交由上层决定如何 fallback
        return time.time()-t0, 0, []

    # ---------- 4. 提取解 ----------
    chosen_idx = [i for i,var in enumerate(x_var) if pulp.value(var) == 1]
    sol_list   = [K_list[i] for i in chosen_idx]

    # ---------- 5. 三元组返回 ----------
    return time.time()-t0, len(sol_list), sol_list