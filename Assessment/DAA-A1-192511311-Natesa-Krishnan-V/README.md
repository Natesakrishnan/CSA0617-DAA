# DAA Assignment 1 - Design, Analyse and Validate an Efficient Search Strategy for a Large-Scale Student Record System

| | |
|---|---|
| **Student name** | Natesa Krishnan V |
| **Registration number** | 192511311 |
| **Group** | A |
| **Dataset seed** | 1311 |
| **Project title** | Design, Analyse and Validate an Efficient Search Strategy for a Large-Scale Student Record System |

## Algorithms used

| # | Algorithm | Strategy | File |
|---|-----------|----------|------|
| 1 | Linear Search (iterative) | Brute force | `src/algo1_linear_search.py` |
| 2 | Recursive Binary Search (on sorted data; sorting time measured separately and added to total) | Decrease-and-conquer | `src/algo2_recursive_binary_search.py` |
| 3 | Hash Table Search (Group A; own implementation, separate chaining, `key mod m`, m prime >= n/0.75) | Space-time trade-off | `src/algo3_hash_table.py` |

Search keys: **FOUND = 192511311**, **NOT FOUND = 192511312**.

## Python version and requirements

* Developed and tested with **Python 3.12.3** (Linux). Python 3.8+ should work.
* The dataset generator, the three algorithms and the benchmark use **only the standard library**.
* `src/generate_graphs.py` needs `pandas` and `matplotlib`:

```
pip install -r requirements.txt
```

## Dataset generation method (reproducible, seed 1311)

`src/dataset_generator.py` creates four CSV files with the header `registration_number`
(`data/students_1000.csv`, `_10000`, `_100000`, `_1000000`). For each size *n*:

1. `rng = random.Random(1311)`
2. `rng.sample(range(191_000_000, 193_000_000), n + 1)` - *n+1* distinct 9-digit numbers
3. Remove 192511311 and 192511312 if they were drawn and keep the first *n-1* remaining numbers
4. Insert **192511311** once at position `rng.randrange(n)`

Result: *n* distinct, unsorted registration numbers; 192511311 is present exactly once and 192511312 is never present.
Running the generator twice gives byte-identical files (seeded; verified with `md5sum`). The same file is used by all three algorithms for each size. No external or downloaded datasets are used.

## Folder structure

```
DAA-A1-192511311-Natesa-Krishnan-V/
├── README.md
├── requirements.txt
├── report/
│   ├── DAA_A1_192511311.pdf          full report (Tasks 1-12)
│   └── DAA_A1_192511311.docx         editable version
├── src/
│   ├── algo1_linear_search.py
│   ├── algo2_recursive_binary_search.py
│   ├── algo3_hash_table.py
│   ├── dataset_generator.py          (also holds shared constants / timing helper)
│   ├── benchmark.py                  (benchmark + --correctness tests)
│   └── generate_graphs.py
├── data/
│   ├── students_1000.csv  students_10000.csv  students_100000.csv  students_1000000.csv
├── results/
│   ├── results.csv                   combined benchmark results
│   ├── linear_search_results.csv
│   ├── binary_search_results.csv
│   ├── hash_table_results.csv
│   ├── graphs/
│   │   ├── runtime_comparison.png
│   │   ├── comparisons_comparison.png
│   │   ├── theory_vs_experiment.png
│   │   └── cumulative_cost_1M.png    (extra: preprocessing + q searches)
│   └── logs/                         captured console output of the real runs
└── screenshots/
    ├── task08_correctness_test.png
    ├── task09_runtime_1000.png
    ├── task09_runtime_10000.png
    ├── task09_runtime_100000.png
    └── task09_runtime_1000000.png
```

## Exact commands (run from the project root folder)

```
python src/dataset_generator.py                 # 1. create + verify the 4 datasets
python src/algo1_linear_search.py               # 2. Linear Search       -> results/linear_search_results.csv
python src/algo2_recursive_binary_search.py     # 3. Recursive Binary    -> results/binary_search_results.csv
python src/algo3_hash_table.py                  # 4. Hash Table          -> results/hash_table_results.csv
python src/benchmark.py --correctness           # 5. Task 8 correctness tests (36 checks)
python src/benchmark.py                         # 6. full benchmark      -> results/results.csv (+ the 3 CSVs above)
python src/generate_graphs.py                   # 7. graphs              -> results/graphs/*.png
```

(On some systems use `python3` instead of `python`.) The algorithm scripts generate a missing dataset automatically.
Expected run time: well under two minutes in total (the 1,000,000-record hash build takes about 0.6 s per trial).

## Output files

| File | Content |
|------|---------|
| `results/linear_search_results.csv` | algorithm, input_size, search_key, result, index, comparisons, execution_time_seconds, execution_time_ms, repetitions |
| `results/binary_search_results.csv` | algorithm, input_size, search_key, result, index (in the sorted array), comparisons, preprocessing_time_seconds/ms (sorting), search_time_seconds/ms, total_time_seconds/ms, search_repetitions |
| `results/hash_table_results.csv` | algorithm, input_size, search_key, result, index_or_key, key_comparisons, operations (= 1 hash computation + key comparisons), table_size, load_factor, max_chain_length, preprocessing (build) time, search time, total time (s and ms), search_repetitions |
| `results/results.csv` | combined: algorithm, input_size, search_key, result, index, comparisons_operations, preprocessing_time_seconds/ms, search_time_seconds/ms, total_time_seconds/ms (used for Tasks 8-10) |
| `results/graphs/*.png` | graphs drawn from `results.csv` only |
| `results/logs/*.txt` | console output of the runs used for the report and screenshots |

## Measurement method

* `time.perf_counter()`; each timing is the average of repeated calls (linear: `max(5, 1,000,000 // n)` calls; binary/hash search: 2,000 calls; preprocessing: `max(1, 100,000 // n)` calls) and the **fastest of 3 trials** is reported.
* Garbage collection is disabled while timing (as `timeit` does). File loading time is not included.
* Binary-search comparisons are counted as one three-way comparison per recursive call; the hash `operations` count is 1 hash computation + the key comparisons in the bucket chain.
* Times depend on the machine; comparison counts do not. Re-running gives slightly different times, so the numbers in your own run may differ slightly from the report (which was written from one specific run whose output is in `results/logs/`).

## Reproducibility instructions

1. Use the same Python version if possible (3.12) - the seeded `random.sample` sequence is what makes the datasets identical.
2. Delete `data/` and `results/` if you want to start from scratch, then run the seven commands above in order.
3. Check: `python src/dataset_generator.py` must print `All datasets generated and verified.`; `python src/benchmark.py --correctness` must end with `ALL TESTS PASSED`.
4. The 1,000,000-record files are about 11 MB; the hash table for them needs a few hundred MB of RAM.

## Screenshots - IMPORTANT NOTE

The images in `screenshots/` were produced in a headless environment that has no real terminal window to capture. They are
**images rendered from the real console output that the programs printed** (stored in `results/logs/`): the text in them is
genuine, unedited program output including the name and registration number banner, but they are *not* photographs of a live terminal.
If your course requires real screen captures, run these commands on your own computer and take your own screenshots
(each run prints "Name: Natesa Krishnan V / Registration No.: 192511311" at the top) and save them over the files with the same names:

| Screenshot file | Command to run |
|-----------------|----------------|
| `task08_correctness_test.png` | `python src/benchmark.py --correctness` |
| `task09_runtime_1000.png`, `_10000.png`, `_100000.png`, `_1000000.png` | `python src/benchmark.py` (each screenshot shows the section for that dataset size) |

## Report

`report/DAA_A1_192511311.pdf` (and the editable `.docx`) cover Tasks 1-12 using the real results in `results/`.
