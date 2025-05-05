import itertools
import time
import pulp
import config as thread_running

def LP(n, k, j, s):
    """
    用线性规划（CBC）精确求解当 j == s 且 n 较小时的情况。
    返回 (耗时, 选中块数, 选中的 K 组合列表)
    """
    # 1) 参数转整型 & 计时开始
    n, k, j, s = map(int, (n, k, j, s))
    time_start = time.time()

    # 2) 枚举所有 k-组合
    def Gen(x, y):
        if y > len(x): return []
        if y == len(x): return [tuple(x)]
        return list(itertools.combinations(x, y))
    NK_Group = Gen(range(n), k)
    NK_Length = len(NK_Group)

    # 3) 构造每个 K 对应的“标签集合”
    #    把每个 k-组合映射到它能覆盖的所有 j→s 的子集编码
    def transform(x):
        return sum(1 << i for i in x)
    Mainlist = list(range(n))
    def find_map(x):
        ans = set()
        for each in Gen(x, s):
            if j == s:
                ans.add(transform(each))
            else:
                rest = tuple(set(Mainlist) - set(each))
                for extra in Gen(rest, j - s):
                    ans.add(transform(each + extra))
        return ans

    Group_map = []
    NJ_Mark = set()
    for i, blk in enumerate(NK_Group):
        if not thread_running.get():
            return 0, 0, []
        mset = find_map(blk)
        Group_map.append(mset)
        NJ_Mark.update(mset)

    # 4) 设定 ILP：x_i ∈ {0,1}, 最小化 ∑ x_i，且对每个标签 ≥1 次覆盖
    prob = pulp.LpProblem("Minimize_K_Groups", pulp.LpMinimize)
    x_vars = [pulp.LpVariable(f"x_{i}", cat="Binary") for i in range(NK_Length)]

    # 每个标签都至少被选中的某个 K 覆盖一次
    for tag in NJ_Mark:
        prob += pulp.lpSum(x_vars[i] for i in range(NK_Length)
                            if tag in Group_map[i]) >= 1

    # 目标：最小化 ∑ x_i
    prob += pulp.lpSum(x_vars)

    # 求解（限制时间可选）
    solver = pulp.PULP_CBC_CMD(msg=False, timeLimit=30)
    status = prob.solve(solver)

    # 如果没找到最优解，直接返回空解
    if pulp.LpStatus[status] != "Optimal":
        return time.time() - time_start, 0, []

    # 5) 收集结果索引
    Final_Ans = [i for i,var in enumerate(x_vars) if pulp.value(var) == 1]
    # 并把索引转成具体的组合
    Final_Ans_example = [NK_Group[i] for i in Final_Ans]

    # 6) 计时结束并返回
    elapsed = time.time() - time_start
    return elapsed, len(Final_Ans_example), Final_Ans_example

if __name__ == "__main__":
    # some representative test cases
    test_cases = [
        (13,6,5,5)
    ]

    for n, k, j, s in test_cases:
        dt, count, sol = LP(n, k, j, s)
        print(f"LP(n={n},k={k},j={j},s={s})  →  time={dt:.4f}s,  #blocks={count}")
        print("  solution:", sol)
        print("-" * 60)