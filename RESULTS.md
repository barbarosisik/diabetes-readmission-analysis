# Results

Question: *"What share of patients are readmitted within 30 days, and how does that differ by age group?"*

**Answer:** 11.4% of hospital stays are followed by a readmission within 30 days. By age, the rate is lowest under 20 (1.9% at 0–10, 5.8% at 10–20) and highest at 20–30 (14.3%). In all other age groups it is between 9.8% and 12.6%. The two youngest groups are small (160 and 690 stays).

All numbers come from [the notebook](notebooks/analysis.ipynb).

## Task 1: data-quality problems (notebook section 2)

1. Missing values are written as `?`, in 7 columns (`weight`: 97% missing). None are in the six analysis columns.
2. By default, pandas would read the real value `None` ("test not done") as missing (101,468 rows). Avoided when loading.
3. One patient can have many stays: 16,773 of 71,518 patients have 2 or more (47,021 stays).
4. 3 stays have gender `Unknown/Invalid`.
5. 1,652 stays ended in death. All are flagged `NO`.
6. 771 stays ended in hospice care. 86 were readmitted anyway, 43 within 30 days.
7. 4,680 stays have an unknown discharge destination.
8. There are no dates, so the order of stays and the 30-day window cannot be checked.

## Task 2: readmission rate by age (notebook section 3)

Function: [`src/readmission.py`](src/readmission.py). Excluded: 2,423 stays that ended in death or hospice care, because those patients cannot come back, or are not expected to. Remaining: 99,343 stays.

| Age bracket | Encounters | 30-day readmission rate |
|---|---|---|
| [0-10) | 160 | 1.9% |
| [10-20) | 690 | 5.8% |
| [20-30) | 1,649 | 14.3% |
| [30-40) | 3,764 | 11.3% |
| [40-50) | 9,607 | 10.7% |
| [50-60) | 17,060 | 9.8% |
| [60-70) | 22,059 | 11.3% |
| [70-80) | 25,331 | 12.1% |
| [80-90) | 16,434 | 12.6% |
| [90-100) | 2,589 | 11.9% |
| **All** | **99,343** | **11.4%** |

## Task 3: unit tests

[`tests/test_readmission.py`](tests/test_readmission.py): two tests on hand-made tables (counts and rates; age order). `pytest`: 2 passed.

## Task 4: the note

See [NOTE.md](NOTE.md).
