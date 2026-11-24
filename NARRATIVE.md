# diabetes-readmission-analysis

Barbaros Isik · 23 November 2026

## Overview

I answer one question from a hospital manager: what share of patients with diabetes are readmitted to hospital within 30 days of leaving, and how does that differ by age group? I use a public dataset of 101,766 hospital stays from 130 US hospitals (1999–2008). Result: 11.4% of stays are followed by a readmission within 30 days. By age, the rate ranges from 1.9% (ages 0–10) to 14.3% (ages 20–30).

## Resources used, and why

- **The UCI dataset *Diabetes 130-US hospitals for years 1999–2008*** (CC BY 4.0): the data named in the project brief.
- **Strack et al. (2014)**, the paper published with the dataset: to understand how the data were collected and how the authors handled stays that ended in death or hospice care.
- **Python, pandas and Jupyter:** widely known tools for working with tables. One notebook keeps the whole analysis readable from top to bottom.
- **Git and GitHub:** one branch and one pull request per step, so each piece of work is reviewed before it is merged.

## Part 1: set-up, data and loading

- **Input:** the project brief and the official UCI zip file.
- **Process:** I wrote a plan, working rules, a glossary of medical terms and a logbook. I downloaded the data, checked both files against their SHA-256 fingerprints (checksums that prove the files are exactly the expected ones) and committed them unchanged. The notebook then loads the main file.
- **Decisions and why:**
  - I committed the raw data instead of writing a download script: the license allows it, and it is the simplest way for anyone to rerun the analysis.
  - Only `?` is read as missing (`na_values="?", keep_default_na=False`). pandas' default settings would also turn the real answer `None` ("test not done") into missing.
  - `low_memory=False` makes pandas read the whole file before choosing column types, which avoids a mixed-type warning on `payer_code`.
  - One notebook holds the whole analysis, so it reads like a report.
- **Output:** `data/raw/` with `data/README.md`, and `notebooks/analysis.ipynb`, which loads 101,766 rows × 50 columns and keeps `None` as a value.

## Part 2: data-quality problems (brief task 1)

- **Input:** the loaded data (101,766 stays × 50 columns) and the discharge table in `IDS_mapping.csv`.
- **Process:** six read-only checks in the notebook: size and column types; missing values; stays versus patients; the allowed values of `age`, `gender` and `readmitted`; the discharge codes and their meanings; and the discharge codes against the readmission flag.
- **Decisions and why:**
  - Nothing in the data is changed in this part, so every problem is on record before any choice is made.
  - The list is a table built by code, so every count is computed, not typed by hand.
  - `age`, `gender` and `readmitted` are checked against lists of allowed values, so missing and unexpected labels are both caught.
  - The death, hospice and unknown discharge codes are looked up by their labels in the mapping file, not typed by hand.
- **Output:** a list of eight problems (notebook section 2.7), each with the number of rows it affects and whether it affects the question. The main ones: 1,652 stays ended in death and 771 in hospice care; 4,680 stays have an unknown discharge destination; and 16,773 patients have more than one stay.

## Part 3: the function and its tests (brief tasks 2–3)

- **Input:** the brief's definition: a table with the age bracket, the number of encounters and the 30-day readmission rate.
- **Process:** one small function in `src/readmission.py`. It marks each stay as readmitted within 30 days (`<30`) or not, groups the stays by age bracket, then counts them and takes the share marked. Two unit tests run it on small hand-made tables.
- **Decisions and why:**
  - The function lives in a `.py` file, not in the notebook, so that the tests can import it; the notebook imports it too.
  - The function does only what the brief asks. Which stays are eligible is decided in the notebook, where the codes are looked up in the mapping file.
  - The function and its tests are one step: a function and the tests that prove it belong together. Reviewing them as one unit shows both what the code does and the evidence that it is correct, and the tests describe the expected behavior precisely.
  - Two tests: one checks counts and rates on a table whose answer is known by hand (`>30` and `NO` both count as "not readmitted within 30 days"); the other checks that the brackets come out in age order. I checked that each test fails when its rule is broken on purpose.
  - No linter and no automatic test run on GitHub: the brief does not ask for them.
- **Output:** `src/readmission.py` and `tests/test_readmission.py`; `pytest` passes (2 tests).

## Part 4: results, note and results file (brief task 4)

- **Input:** the loaded data, the discharge codes from part 2 and the function from part 3.
- **Process:** in the notebook, I excluded the death and hospice stays, ran the function on the remaining stays and computed the overall rate. Then I wrote the note and the results file.
- **Decisions and why:**
  - I excluded the 2,423 stays that ended in death or hospice care, because those patients cannot come back, or are not expected to. Their codes are looked up by label in the mapping file, not typed by hand.
  - I kept the 4,680 stays with an unknown discharge destination and the 3 `Unknown/Invalid` gender stays: I cannot tell whether those patients died, and gender is not used. Both are listed as problems.
  - I count per stay, as the brief asks ("number of encounters").
  - The exclusion is done in the notebook, before calling the function, so the function does exactly what the brief asks.
  - One very simple results file, `RESULTS.md`, holds the findings task by task, so they can be read in one place.
  - Numbers in the documents are copied from the notebook's outputs, never worked out by hand.
- **Output:** notebook section 3 (the table and the overall rate), `NOTE.md` and `RESULTS.md`.

## Limitations

- The data have no dates, so the order of a patient's stays and the exact 30-day window cannot be checked.
- The readmission flag was computed by the data's authors from the full hospital database, so I have to trust it.
- Readmissions to hospitals outside the 130 are not recorded, so the true rates are probably somewhat higher.
- 4,680 stays have an unknown discharge destination; some of them may have ended in death.
- The two youngest age groups are small (160 and 690 stays), so their rates are uncertain.
- Counting per stay means that patients with many stays weigh more.

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
