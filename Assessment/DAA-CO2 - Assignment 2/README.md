# DAA Assignment 2 (CO2) - Brute-Force and Exhaustive-Search Techniques

Student: Natesa Krishnan V | Registration: 192511311 | Group A

## Contents

| Path | Purpose |
|---|---|
| `report/DAA_A2_192511311_Report.docx` | Assignment report (Word) |
| `report/DAA_A2_192511311_Report.pdf` | Assignment report (PDF) |
| `src/q1_sorting.py` | Q1 - Selection, Bubble and Insertion sort with comparison and swap/move counters |
| `src/q2_sequential_search.py` | Q2 - Sequential search on tool-issue records |
| `src/q3_string_matching.py` | Q3 - Brute-force string matching with character-comparison counter |
| `src/q4_closest_pair.py` | Q4 - Brute-force closest pair |
| `src/q5_convex_hull.py` | Q5 - Brute-force convex hull from the geometric decision rule, validated against Andrew's monotone chain |
| `src/q6_exhaustive_knapsack.py` | Q6 - Exhaustive search for payload-limited package selection, validated against dynamic programming |
| `src/q7_redesign.py` | Q7 - Redesigned closest pair (sort-and-sweep with pruning) |
| `src/run_all.py` | Runs every experiment, writes `data/*.csv`, draws `results/figures/*.png` |
| `src/plot_hulls.py` | Draws the Q5 boundary figure |
| `src/build_report.py` | Builds the Word report from the measured data |
| `data/` | Raw experimental results (CSV) used for all tables and figures |
| `results/figures/` | Figures used in the report |

## Requirements

Python 3.9 or later, with `matplotlib` and `python-docx` (for the report only). No other third-party packages are needed.

## Reproducing the results

From the project root:

```bash
python3 src/run_all.py        # experiments -> data/*.csv and results/figures/*.png
python3 src/plot_hulls.py     # Q5 boundary figure
python3 src/build_report.py   # report/DAA_A2_192511311_Report.docx
```

To produce the PDF from the DOCX (LibreOffice):

```bash
soffice --headless --convert-to pdf --outdir report report/DAA_A2_192511311_Report.docx
```

All inputs are generated from fixed seeds, so the operation counts are reproducible exactly. Timing figures will vary with hardware.

## Correctness checks built into the code

- Q1: every sorted output is compared with Python's `sorted`.
- Q4 / Q7: the pair count is asserted to equal n(n-1)/2, and the redesigned closest-pair distance is asserted to equal the brute-force distance.
- Q5: each hull is compared with an independent monotone-chain hull.
- Q6: a hand-checked 5-item instance is asserted, and every random instance is asserted against dynamic programming.
