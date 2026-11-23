# Plan

**In one paragraph.** This project answers one question from a hospital manager: *what share of hospital patients with diabetes are admitted to hospital again within 30 days of leaving, and does that differ between age groups?* We use a public dataset of 101,766 hospital stays from 130 US hospitals (1999–2008). The work has four parts, done in this order, each one reviewed before the next begins. **(1)** Load the data and write down every data-quality problem *before* changing anything. **(2)** Write one function, `readmission_rate_by_age(df)`, that returns, for each 10-year age bracket, the number of hospital stays and the share of them followed by a new admission within 30 days. **(3)** Prove the function is right with 2–3 small unit tests on hand-made tables. **(4)** Write a note of under half a page on our assumptions, what we excluded and why, and what we would ask the people who own the data. Two choices shape the answer more than anything else. The first is removing stays that ended in death or hospice care (end-of-life care), because those patients are not expected to come back. The second is being clear whether we count *hospital stays* or *patients*, because one patient can have many stays. A first look shows how much this matters: about **11.4%** of stays are followed by a readmission within 30 days, but only about **9.0%** of patients are readmitted after their first recorded stay, and the age pattern changes too.

> **Status:** Step 0 (set-up) is done and waiting for your confirmation.
> All numbers in sections 1–3 come from a first, read-only look at the data with throw-away code. The notebook recomputes the ones we use, from Step 1 on.

**Contents:**
1. [The question, unpacked](#1-the-question-unpacked)
2. [The data in plain words](#2-the-data-in-plain-words)
3. [Data-quality problems found in the first look](#3-data-quality-problems-found-in-the-first-look)
4. [Scope and decisions](#4-scope-and-decisions)
5. [Step-by-step plan](#5-step-by-step-plan)
6. [Folder structure](#6-folder-structure)
7. [Draft questions for the data owner](#7-draft-questions-for-the-data-owner)
8. [Risks and how we handle them](#8-risks-and-how-we-handle-them)
9. [Sources](#9-sources)

---

## 1. The question, unpacked

### 1.1 Key ideas in plain words

- **Hospital stay (encounter):** one admission to hospital, from the day the patient is admitted to the day they leave. One row in the data.
- **Patient:** one person. The same person can have many stays, so `patient_nbr` repeats.
- **Discharge:** leaving hospital at the end of a stay. The patient may go home, to a care home, to another hospital or to hospice, or may have died. The *discharge disposition* code records which.
- **30-day readmission:** the patient is admitted to hospital again within 30 days after a discharge. Hospitals track this because many such returns are avoidable. They can point to problems with the treatment or with the hand-over to care at home.
- **The `readmitted` column looks forward from each stay:**
  - `<30`: after *this* stay, the patient was admitted again within 30 days.
  - `>30`: they were admitted again, but more than 30 days later.
  - `NO`: no readmission on record.

So, for each age bracket:

```text
30-day readmission rate = (stays flagged "<30") / (stays after which a readmission was possible)
```

Stays flagged `>30` count in the bottom of the fraction (the denominator) but not in the top (the numerator).

### 1.2 Stays or patients? Four ways to count, four answers

The manager asks for the share of *patients*, but the function must report the "number of *encounters*". These are not the same thing:

| | What is counted | Overall 30-day rate (first look) |
|---|---|---|
| **A** | Every stay, nothing removed | 11.2% of 101,766 stays |
| **B** | Every stay, after removing death and hospice | **11.4%** of 99,343 stays |
| **C** | Each patient once, using their first stay (lowest `encounter_id`), after removing death and hospice | **9.0%** of 69,990 patients |
| **D** | Each patient once: "had at least one stay followed by a readmission within 30 days" | 12.6% of 69,990 patients |

**Decided:** the function reports **B**, one row per stay. That is what the brief asks for ("number of encounters"), and it is how hospitals usually measure readmissions. C and D are shown here only to explain why the counting unit matters; they are not part of the analysis.

### 1.3 Why the choice matters: the age pattern changes

| Age | B: per stay (number of stays) | C: per patient, first stay (number of patients) |
|---|---|---|
| [0-10)   | 1.9% (160)          | 2.0% (153) |
| [10-20)  | 5.8% (690)          | 4.9% (534) |
| [20-30)  | **14.3%** (1,649)   | **7.4%** (1,121) |
| [30-40)  | 11.3% (3,764)       | 7.0% (2,692) |
| [40-50)  | 10.7% (9,607)       | 7.4% (6,828) |
| [50-60)  | 9.8% (17,060)       | 7.1% (12,351) |
| [60-70)  | 11.3% (22,059)      | 9.0% (15,689) |
| [70-80)  | 12.1% (25,331)      | 10.2% (17,751) |
| [80-90)  | 12.6% (16,434)      | 10.8% (11,110) |
| [90-100) | 11.9% (2,589)       | 9.5% (1,761) |

- **Counted per stay**, people in their 20s look worst (14.3%). **Counted per patient**, the rate rises with age: about 7% between ages 30 and 60, and about 10–11% between 70 and 90.
- **Why:** a few young patients come back again and again. In the 20–30 group, 11 patients (the top 1%) account for 42% of all its 30-day readmissions, and one person alone has 23. About two-thirds of these 11 patients' stays are for **diabetic ketoacidosis (DKA)**. DKA is a life-threatening emergency, mostly in type 1 diabetes, where a lack of insulin makes the blood acidic. It is the main reason for 30–47% of stays by patients under 30, but for less than 1% of stays by patients over 60.
- **What it means for the manager:** there are two messages, and both are true and useful. *Older patients are more likely to come back.* And *a small group of young patients with repeated emergencies causes many returns.*
- **Small groups:** the two youngest brackets are too small for firm conclusions. The [0-10) bracket has 160 stays and only 3 readmissions.

---

## 2. The data in plain words

- **Source:** the *Health Facts* database from Cerner Corporation, a large collection of electronic health records from 130 US hospitals and hospital networks, covering 1999–2008. The dataset is published on the UCI Machine Learning Repository (CC BY 4.0, DOI 10.24432/C5230J) together with a paper by Strack et al. (2014).
- **One row = one inpatient stay that met all five of these rules:**
  1. The patient was formally admitted to hospital.
  2. Diabetes was recorded as one of the diagnoses.
  3. The stay lasted 1–14 days.
  4. Lab tests were done.
  5. Medication was given.
- **What this means for us:**
  - The results describe *stays of patients with diabetes*, not all hospital patients.
  - The readmission flag was computed from the *whole* hospital database, so the readmission stay itself is often not in this file. For example, 2,166 patients who have only one row are flagged `<30`. We have to trust the flag, because we cannot rebuild it from the file.
  - Readmissions to hospitals outside these 130 are invisible, so the true rates are probably somewhat higher.
  - There are **no dates** in the data, so we cannot be sure of the order of a patient's stays.
- **Files:**
  - `diabetic_data.csv`: 101,766 rows × 50 columns.
  - `IDS_mapping.csv`: three code tables stacked in one file (admission type, discharge disposition, admission source).

### 2.1 The six columns we use

| Column | What it is | First look |
|---|---|---|
| `encounter_id` | ID of one stay | 101,766 values, all unique |
| `patient_nbr` | ID of one patient | 71,518 patients; 23.5% of them have 2 or more stays (up to 40) |
| `age` | 10-year age bracket. `[70-80)` means 70 up to, but not including, 80 | 10 brackets; [0-10) and [10-20) are very small |
| `gender` | `Female`, `Male`, `Unknown/Invalid` | 3 stays are `Unknown/Invalid` |
| `discharge_disposition_id` | code for where the patient went when leaving hospital | 26 different codes used; meanings are in `IDS_mapping.csv` |
| `readmitted` | `NO`, `>30`, `<30` | 54,864 / 35,545 / 11,357 stays |

None of these six columns contains the missing-value marker `?`.

### 2.2 Discharge codes that matter

| Code | Meaning (from `IDS_mapping.csv`) | Stays | Decision |
|---|---|---|---|
| 11 | Expired (the patient died) | 1,642 | exclude |
| 19 | Expired at home. Medicaid only, hospice. | 8 | exclude |
| 20 | Expired in a medical facility. Medicaid only, hospice. | 2 | exclude |
| 21 | Expired, place unknown. Medicaid only, hospice. | 0 | exclude (rule kept for completeness) |
| 13 | Hospice / home | 399 | exclude |
| 14 | Hospice / medical facility | 372 | exclude |
| 18 | NULL (unknown) | 3,691 | keep, and report |
| 25 | Not Mapped (unknown) | 989 | keep, and report |
| 26 | Unknown/Invalid | 0 | keep, and report |

- All 1,652 stays ending in death are flagged `NO`, which is consistent.
- But 86 of the 771 hospice stays *were* followed by a readmission (43 within 30 days), because a patient can leave hospice care. We still exclude hospice stays, as the original paper did, because these patients were not expected to return. The note will say so.

---

## 3. Data-quality problems found in the first look

Step 2 will produce the formal, code-generated version of this list. Problems marked ✱ affect our question.

| # | Problem | How big | Handling |
|---|---|---|---|
| 1 ✱ | Missing values are written as the text `?` | 7 columns: `weight` 96.9%, `medical_specialty` 49.1%, `payer_code` 39.6%, `race` 2.2%, `diag_3` 1.4%, `diag_2` 0.35%, `diag_1` 0.02%. None in our six columns. | Load `?` as missing |
| 2 ✱ | **Loading trap:** pandas' default settings treat the text `None` as missing, but here `None` is a real answer ("test not done") | `max_glu_serum`: 96,420 rows; `A1Cresult`: 84,748 rows | Load with `na_values="?", keep_default_na=False` |
| 3 ✱ | Hidden missing values written as codes ("NULL", "Not Mapped", "Not Available") | discharge 18/25: 4,680 stays (4.6%); admission type 5/6/8: 10,396; admission source 9/17/20: 7,067 | Report; keep unknown-discharge stays, because we cannot tell whether those patients died |
| 4 ✱ | Death and hospice discharges | 1,652 deaths + 771 hospice = 2,423 stays | Exclude from the rate |
| 5 ✱ | Hospice patients sometimes do come back | 86 of 771 (43 within 30 days) | Mention in the note |
| 6 ✱ | The same patient has many stays | 16,773 patients (23.5%) hold 46.2% of all stays; one has 40 | Count per stay, as the brief asks |
| 7 ✱ | Gender is `Unknown/Invalid` | 3 stays | Report; keep for the age analysis, which does not use gender |
| 8 ✱ | Very small age groups | [0-10): 160 stays, 3 readmissions; [10-20): 690 stays | Keep all ten brackets; warn in the note |
| 9 ✱ | No dates, and `encounter_id` is not a reliable time order | 13 patients have a stay with a *higher* ID than the stay in which they died. 18 patients' age bracket goes *down* as the ID goes up. 490 stays are flagged `NO` although the same patient has a higher-ID stay. | Ask the data owner |
| 10 ✱ | The readmission flag cannot be checked against the file | 2,166 single-stay patients are flagged `<30` | Trust the flag; ask the data owner how it is built |
| 11 ✱ | Day 30 itself is ambiguous (`<30` versus `>30`) | not measurable | Ask the data owner |
| 12 | The same patient has a different gender or race across stays | gender: 3 patients; race: 123 patients | Report |
| 13 | Impossible codes | "Neonate" discharge (code 10): all 6 stays are for patients aged 50+. "Newborn" admission (type 4): 9 of its 10 stays are for patients aged 40+. | Report |
| 14 | The mapping file is three tables in one CSV | separator lines `,`; leading spaces; codes out of order (30 before 27); two codes both "Not Available"; typos ("critial") | Read only the discharge table |
| 15 | Columns that never vary | `examide` and `citoglipton` are always `No`; 5 more drug columns are used 3 times or fewer | Report |
| 16 | Mixed coding styles | `NO` in `readmitted` but `No` elsewhere; `change` uses `Ch`/`No` | Match the exact strings |
| 17 | Diagnosis codes mix numbers and letters (ICD-9 `V…` and `E…` codes) | all three `diag_` columns | Keep as text |
| 18 | Windows line endings (CRLF) in both files | not measurable | pandas copes; worth knowing for other tools |

**Background: cross-check with the original paper** (first look only, not part of the analysis). Removing death and hospice stays and then keeping each patient's lowest `encounter_id` leaves 69,990 stays; the paper reports 69,984. The paper's ≤30 and 30–60 age groups match ours exactly (1,808 and 21,871 stays), and the rates are close:

| Age group | Paper | Ours |
|---|---|---|
| ≤30 | 6.2% | 6.2% |
| 30–60 | 7.4% | 7.2% |
| >60 | 10.2% | 9.9% |

So we are reading the data the same way its authors did.

---

## 4. Scope and decisions

### 4.1 Scope

Only the four tasks in the brief, about 60–90 minutes of focused work for the core tasks. Nothing else, and never a predictive model.

### 4.2 Decided

| Topic | Decision |
|---|---|
| Language and tools | Python, pandas and pytest. `requirements.txt` with exact versions, and Python's built-in `venv` |
| Code quality | Type hints and a short docstring. No linter and no automatic test run: the brief does not ask for them |
| Presentation | One Jupyter notebook, `notebooks/analysis.ipynb`, holds the whole analysis |
| Raw data | The two CSV files are committed unchanged to `data/raw/`, with `data/README.md` (source, CC BY 4.0 credit, SHA-256 fingerprints). No download script |
| Outputs | Shown in the notebook, which is committed with its outputs. No `reports/` folder |
| Steps | Five steps (0–4), listed in section 5 |
| Way of working | One branch and one pull request per step. Each commit message is shown first, then committed and pushed. The project owner merges with a merge commit |
| Spelling | American English (old logbook entries stay as written) |
| Narrative | `NARRATIVE.md` at the top level; the rules are in AGENTS.md, section 8 |
| Data-quality list | Built by a code cell in the notebook, so every count is computed, never typed by hand |
| Nothing hard-coded | Values come from the data: the discharge codes are looked up by their labels in `IDS_mapping.csv`. Numbers in the documents are copied from the notebook's outputs |
| Counting unit | Per stay (encounter), as the brief asks |
| Exclusions | Stays that ended in death or hospice care, because those patients cannot or are not expected to come back. Unknown discharge codes and `Unknown/Invalid` gender are kept and listed. The exclusion is done in the notebook, before the function is called |
| Code layout | The function in `src/readmission.py`, imported by the notebook and the tests |
| Unit tests | Two: counts and rates on a hand-made table (`>30` and `NO` both count as not readmitted within 30 days), and age order |
| Results file | `RESULTS.md`: the findings, task by task, kept very simple |

**Why the function and its tests form one step:** a function and the tests that prove it belong together. Reviewing them as one unit shows both what the code does and the evidence that it is correct, and the tests describe the expected behavior precisely.

---

## 5. Step-by-step plan

Each step has its own branch and pull request, reviewed and merged by the project owner before the next step starts (see [AGENTS.md](../AGENTS.md)).

### Step 0: Project set-up · branch `step-00-project-setup`

- **Goal:** a clean repository with the brief, this plan, the working rules, a glossary and a logbook, in the agreed folders.
- **Done when:** the documents are in place and match the decisions in section 4.

### Step 1: Data and loading · branch `step-01-data-loading`

- Commit the two CSV files unchanged to `data/raw/`, plus `data/README.md`. Remove `data/raw/` and `*.zip` from `.gitignore`.
- `requirements.txt` with exact versions.
- `notebooks/analysis.ipynb`, first section: load the data with `pd.read_csv(path, na_values="?", keep_default_na=False)`. `?` becomes missing, and the real value `None` ("test not done") stays a value.
- The first version of `NARRATIVE.md`.
- **Done when:** the notebook loads 101,766 rows × 50 columns, and `None` survives in `A1Cresult`.

### Step 2: Data-quality list, read-only (brief task 1) · branch `step-02-data-quality`

- **Checks**, in the notebook:

  | Check | Function | Why |
  |---|---|---|
  | Size and column types | `df.shape`, `df.dtypes` | Confirms it is the expected file (101,766 × 50) and shows there are no date columns |
  | Missing values (`?`) per column | `df.isna().sum()` | The brief's first known quirk |
  | One row per stay? Repeat patients? | `df["encounter_id"].is_unique`, `df["patient_nbr"].value_counts()` | One patient can have many stays, so stays are not patients |
  | Allowed values in `age`, `gender`, `readmitted` | `value_counts(dropna=False)`, then `isin()` against the allowed values | Shows every value, missing included, and flags missing or unexpected labels such as `Unknown/Invalid` |
  | Discharge codes and what they mean | `value_counts()` on `discharge_disposition_id`, decoded with `pd.read_csv("../data/raw/IDS_mapping.csv", skiprows=10, nrows=30, keep_default_na=False)` | Finds the death, hospice and unknown codes. `keep_default_na=False` keeps code 18's label `NULL` visible |
  | Can those patients come back? | `pd.crosstab(df["discharge_disposition_id"], df["readmitted"])` | Checks death and hospice stays against the outcome |

- **The list:** a small table built by code, one row per problem: what it is, how many rows it affects, and whether it affects the question.
- **Done when:** the list is in the notebook, and nothing in the data has been changed.

### Step 3: The function and its tests (brief tasks 2–3) · branch `step-03-readmission-function`

- `src/readmission.py`: `readmission_rate_by_age(df)` returns a table with the age bracket, the number of encounters and the 30-day readmission rate.
- `tests/test_readmission.py`: the two unit tests in section 4.2, on small hand-made data frames.
- **Done when:** `pytest` passes.

### Step 4: Results, note and final documents (brief task 4) · branch `step-04-results`

- Notebook section 3: exclude the death and hospice stays, then run the function on the real data.
- `NOTE.md`, under half a page: the assumptions, what was excluded and why, and what to ask the data owner.
- `RESULTS.md`: the findings, task by task.
- The final `README.md` and `NARRATIVE.md`.
- **Done when:** every task in `docs/PROJECT_BRIEF.md` is done, and the notebook reruns from a fresh clone.

---

## 6. Folder structure

```text
diabetes-readmission-analysis/
├── README.md, RESULTS.md, NOTE.md, NARRATIVE.md
├── AGENTS.md, CLAUDE.md   working rules
├── requirements.txt       Python packages
├── pytest.ini             tells pytest where the code is
├── data/                  README.md + raw/ (the two CSV files)
├── docs/                  PROJECT_BRIEF.md, plan.md, LOGBOOK.md, GLOSSARY.md
├── notebooks/             analysis.ipynb
├── src/                   readmission.py
└── tests/                 test_readmission.py
```

---

## 7. Draft questions for the data owner

1. How is `readmitted` built? Does it count readmission to any of the 130 hospitals, or only the same one? Does the readmission stay also have to meet the five inclusion rules?
2. Does day 30 count as `<30` or `>30`, and does the clock start on the discharge date?
3. Are readmissions to hospitals outside the network captured at all?
4. Can we get admission and discharge dates, or a reliable order of stays? `encounter_id` does not seem to be in time order.
5. What do discharge codes 18 ("NULL") and 25 ("Not Mapped") mean in practice? Could they hide deaths?
6. Are planned readmissions included, such as a scheduled operation? Standard readmission measures leave them out.
7. Should transfers to another hospital (code 2) and patients who left against medical advice (code 7) be excluded, as some standard measures do?
8. Why do some adult patients carry newborn or neonate codes, and why do some patients change gender or race between stays? Is this a data-entry problem or records being merged?

---

## 8. Risks and how we handle them

| Risk | How we handle it |
|---|---|
| A wrong load silently changes values (`None` read as missing) | Load with `na_values="?", keep_default_na=False`, and check that `None` survives |
| Counting patients when we mean stays, or the other way round | Name the unit everywhere: the function counts stays |
| Over-reading tiny groups | Flag the small brackets in the note |
| Reading cause into a correlation ("age causes readmission") | Describe associations only; older patients also tend to have more other illnesses |
| Scope creep | Only the four tasks in the brief |

---

## 9. Sources

- Clore, J., Cios, K., DeShazo, J., & Strack, B. (2014). *Diabetes 130-US Hospitals for Years 1999-2008* [Dataset]. UCI Machine Learning Repository. <https://doi.org/10.24432/C5230J>
- Strack, B., DeShazo, J. P., Gennings, C., Olmo, J. L., Ventura, S., Cios, K. J., & Clore, J. N. (2014). Impact of HbA1c measurement on hospital readmission rates: analysis of 70,000 clinical database patient records. *BioMed Research International*, 2014, 781670. <https://doi.org/10.1155/2014/781670>
