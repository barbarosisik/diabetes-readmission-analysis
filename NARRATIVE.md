# diabetes-readmission-analysis

Barbaros Isik · 24 November 2026

## Overview

A hospital manager asks: *"What share of patients are readmitted within 30 days, and how does that differ by age group?"* I answer it with the public UCI dataset of 101,766 hospital stays of patients with diabetes (130 US hospitals, 1999–2008).

**Answer:** 11.4% of stays are followed by a readmission within 30 days. The rate is lowest under 20 (1.9% at 0–10, 5.8% at 10–20) and highest at 20–30 (14.3%); all other age groups lie between 9.8% and 12.6%.

My rule throughout: the least code that keeps the data correct. This report covers only the choices where another way would also have made good sense. The numbers are in [RESULTS.md](RESULTS.md), the assumptions in [NOTE.md](NOTE.md).

## Resources used, and why

- **The UCI dataset** named in the brief, and **the paper its authors published with it** (Strack et al., 2014), to see how they handled stays that ended in death or hospice care.
- **Python, pandas, Jupyter and pytest:** widely known tools. The notebook reads from top to bottom, and pytest runs the unit tests.
- **Git:** one branch per step, each reviewed before the next one began.

## Part 1: data and loading

The raw files are committed unchanged, with their SHA-256 fingerprints, and the main file is loaded in one line:

```python
pd.read_csv(path, na_values="?", keep_default_na=False, low_memory=False)
```

The usual way (pandas' default settings, then replacing `?`) would be a mistake here: current pandas also reads the word `None` as missing, and in this file `None` means "test not done" for 84,748 A1C results (a blood test of average blood sugar).

## Part 2: data-quality problems (brief task 1)

Six read-only checks come first, and nothing is changed. They end in a table of eight problems, built by code, each with the rows it affects and whether it matters for the question.

The death and hospice discharge codes could simply have been typed (`[11, 19, 20, 21]` and `[13, 14]`), as many public analyses do. Typed lists slip easily, so I read the codes from the mapping file by their labels ("Expired", "Hospice"). It is one short cell, and the check becomes part of the code.

## Part 3: the function and its tests (brief tasks 2–3)

`readmission_rate_by_age(df)` lives in [src/readmission.py](src/readmission.py), so the notebook and the tests share it. It is three chained steps: mark each stay as `<30` or not, group the stays by age bracket, then count them and take the share marked. As I said above, I went for the least code; the longer versions I tried gave exactly the same table.

Two unit tests use small hand-made tables: one checks the counts and rates (`>30` and `NO` count as stays, not as readmissions within 30 days), the other the age order. Each fails when its rule is broken on purpose, and `pytest` reports 2 passed.

## Part 4: results and the note (brief task 4)

The notebook removes the 2,423 stays that ended in death (1,652) or hospice care (771), then runs the function on the other 99,343. Hospice is comfort care for people expected to live only a few months. Three choices here had a real alternative:

- **Stays, not patients.** The manager says "patients", but the brief's function asks for the "number of encounters", so a patient with three stays counts three times. Counting each patient once, as the original paper did (its statistical model needed independent rows), would follow the manager's wording more closely. But the data have no dates, so I cannot tell which of a patient's stays came first.
- **Hospice stays are excluded,** although 43 of them were followed by a readmission within 30 days. The brief counts these patients among those who "could never be readmitted", and the paper removed them too.
- **The 4,680 stays with an unknown destination are kept.** Removing them would be the cautious choice, since some may hide deaths. But many of them were followed by a readmission (notebook section 2.6), so those patients were alive, and the rest cannot be told apart.

## Limitations

- No dates: the order of the stays and the 30-day window cannot be checked, so the `readmitted` flag, computed by the dataset's authors, has to be trusted.
- Readmissions to hospitals outside the 130 are not recorded, so the true rates are probably somewhat higher.
- Counting stays gives frequent patients more weight, and the two youngest groups are small (160 and 690 stays).
- The table shows associations, not causes.

For a one-time analysis I wrote the checks out. If this data arrived every month, I would turn the same rules into a data contract, so the pipeline stops when the data change.

## AI tools used

- **Claude Code** (an AI coding assistant): helped write the plan and documents, download and check the data, write the code (notebook, function and tests), draft the note and the results file, and prepare commit messages. I reviewed and approved every step before it was merged.

## How to reproduce

```bash
git clone https://github.com/barbarosisik/diabetes-readmission-analysis.git
cd diabetes-readmission-analysis
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
jupyter nbconvert --to notebook --execute --inplace notebooks/analysis.ipynb
pytest
```
