# Optimal Selection System  
*A Minimum-Set-Cover Variant (NP-hard)*

---

## 1 Background & Motivation  

> The explosive growth of data (accelerated by the COVID-19 era, cheap storage and ubiquitous connectivity)  
> makes **sample selection** a crucial first step for data mining, machine learning and statistical experiments.  
> We need a **small, fair and unbiased subset** of samples that still covers every pattern we care about.

Formally, our task can be phrased as a constrained **Minimum Set Coverage** problem—an NP-hard combinatorial optimisation.

---

## 2 Problem Definition  

| Symbol | Meaning | Range |
|--------|---------|-------|
| **m**  | Total number of raw samples available | 45 ≤ m ≤ 54 |
| **n**  | Size of each *candidate pool* randomly drawn from *m* | 7 ≤ n ≤ 25 |
| **j**  | Size of “middle-level” groups (*J*-groups) | s ≤ j ≤ min(k, n) |
| **s**  | Size of *S*-subsets extracted from every **J** | 3 ≤ s ≤ 7 |
| **k**  | Size of the *K*-groups we can finally store | 4 ≤ k ≤ 7 |
| **t**  | **At-least** coverage threshold (each *J* needs ≥ *t* covered *S*) | *t* ∈ ℕ⁺ |

> **Goal:**  
> From the \( nC_k \) possible **K**-groups, select the **smallest subset**  
> such that **every** middle-level group \( J \) has **at least *t*** of its \( C(j,s) \)  
> sub-subsets \( S \) fully contained in the chosen *K*’s.

Mathematically it is a variant of the classic Set Cover problem with multiplicity constraint (*≥ t* instead of ≥ 1).

---

## 3 Algorithm Overview  

| Layer | Technique | Why it works |
|-------|-----------|--------------|
| **Bitwise Mask Encoding** | Encode every combination as an integer; subset test becomes `(mask_K & mask_S) == mask_S`. | O(1) subset checks & popcount; memory-efficient. |
| **α-RCL Beam Search** (`n < 12`) | *Beam width* + *α-Restricted Candidate List* keeps several top-gain paths per layer, balancing exploration & exploitation. | Approaches optimal solutions quickly; naturally supports **≥ t** by tracking *uncovered masks*. |
| **Greedy Cover** (`n ≥ 12`) | Fast heuristic: always pick the K that newly covers the most uncovered *S*. | Runs in milliseconds when search space is huge. |
| **LP exact mode** (`j = s`, `n ≤ 13`) | 0-1 ILP solved by CBC when state space is tiny. | Gives provably minimal answers for small symmetric cases. |

---

## 4 Repository Structure  
Optimal_Selection_System/
├── Algorithm.py          # 主接口文件，统一调用 Beam 和 Greedy 方法
├── Beam.py               # Beam Search 算法（用于 n < 12 或 at least t > 1）
├── Greedy.py             # 简化贪心算法（用于 n >= 12 且 t = 1）
├── config.py             # 全局共享状态或线程开关
├── db.py                 # 数据库逻辑（如有）
├── front.py              # 前端界面入口
├── front.spec            # PyInstaller 打包配置文件
├── front.exe             # 打包后的可执行程序
├── README.md             # 项目说明文档
├── speech_draft.pdf      # 演讲草稿或答辩文稿
├── __pycache__/          # Python 编译缓存
│   ├── AI.cpython-312.pyc
│   └── config.cpython-312.pyc
├── build/                # pyinstaller 的构建缓存目录
│   └── front/
├── dist/                 # 打包后文件目录
│   ├── build/
│   ├── db/
│   ├── dist/
│   ├── front/
│   └── front.exe
└── db/                   # 数据库文件夹（暂为空）