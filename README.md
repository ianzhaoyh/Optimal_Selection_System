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

```
Optimal_Selection_System/
├── Algorithm.py         # Unified interface: calls Beam or Greedy based on inputs
├── Beam.py              # Beam Search with bitmask optimization and α-RCL strategy
├── Greedy.py            # Greedy algorithm for approximate solutions when n ≥ 12
├── config.py            # Global state management (e.g., threading flag)
├── db.py                # Database access logic (optional / for extension)
├── front.py             # GUI entry script (Tkinter or other frontend)
├── front.spec           # PyInstaller build specification
├── front.exe            # Compiled executable (for Windows users)
├── README.md            # Project documentation
├── speech_draft.pdf     # Final presentation or speech draft
├── __pycache__/         # Python bytecode cache
│   ├── AI.cpython-312.pyc
│   └── config.cpython-312.pyc
├── build/               # Intermediate build files (from PyInstaller)
│   └── front/
├── dist/                # Final compiled output (includes front.exe)
│   ├── build/
│   ├── db/
│   ├── dist/
│   ├── front/
│   └── front.exe
└── db/                  # Placeholder for future database files
```
## 🚀 Quickstart

### 1. Clone the Repository

```bash
git clone https://github.com/ianzhaoyh/Optimal_Selection_System.git
cd Optimal_Selection_System
```

### **2 – Install the runtime dependencies**

(The project has no *requirements.txt*, so install the few packages manually.)

```bash
# create & activate a virtual-env if you like …
pip install pulp pyinstaller
```

### **3 – Run the GUI in source form**

```bash
python front.py          # Windows / Linux
python3 front.py         # macOS (or any system where Python 3 is python3)
```

### *4 – (Re-)build a Windows.exe with PyInstaller*

Whenever you change **any** Python source, you must rebuild **front.exe**; the old binary contains only the code that was present when it was packed.
```bash
cd <project-root>        # folder that contains front.spec
pyinstaller front.spec   # produces dist/front.exe
```

The fresh binary appears in dist/front.exe.
Double-click it (or run from cmd/powershell) to launch the program.

### **5 – Run the packaged app on macOS / Linux**

If you pack the project on macOS / Linux with PyInstaller as well, the entry point will be an ELF / Mach-O file named **front** (no extension). Launch it from the terminal:
```bash
./dist/front
```

Make sure it is executable: chmod +x dist/front
