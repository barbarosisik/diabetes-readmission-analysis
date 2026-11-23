# Plan

**In one paragraph.** This project answers one question from a hospital manager: *what share of hospital patients with diabetes are admitted to hospital again within 30 days of leaving, and does that differ between age groups?* We use a public dataset of 101,766 hospital stays from 130 US hospitals (1999–2008). The work has four parts, done in this order, each one reviewed before the next begins. **(1)** Load the data and write down every data-quality problem *before* changing anything. **(2)** Write one function, `readmission_rate_by_age(df)`, that returns, for each 10-year age bracket, the number of hospital stays and the share of them followed by a new admission within 30 days. **(3)** Prove the function is right with 2–3 small unit tests on hand-made tables. **(4)** Write a note of under half a page on our assumptions, what we excluded and why, and what we would ask the people who own the data. Two choices shape the answer more than anything else. The first is removing stays that ended in death or hospice care (end-of-life care), because those patients are not expected to come back. The second is being clear whether we count *hospital stays* or *patients*, because one patient can have many stays. A first look shows how much this matters: about **11.4%** of stays are followed by a readmission within 30 days, but only about **9.0%** of patients are readmitted after their first recorded stay, and the age pattern changes too.

> **Status:** Step 0 (set-up) is done and waiting for your confirmation.
> All numbers in this plan come from a first, read-only look at the data with throw-away code. Tested code will recompute them in Steps 2 and 5.

**Contents:**
1. [The question, unpacked](#1-the-question-unpacked)
2. [The data in plain words](#2-the-data-in-plain-words)
3. [Data-quality problems found in the first look](#3-data-quality-problems-found-in-the-first-look)
4. [Step-by-step plan](#4-step-by-step-plan)
5. [What a good result looks like](#5-what-a-good-result-looks-like)
6. [Decisions for you](#6-decisions-for-you)
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

**Plan:** the function reports **B**: one row per stay. That is what the brief asks for, and it is how hospitals usually measure readmissions. We report **C** next to it to check whether the conclusion depends on how we count. C is also how the dataset's original paper counted. D is mentioned in the note only.

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
- **Small groups:** the two youngest brackets are too small for firm conclusions. The [0-10) bracket has 160 stays and only 3 readmissions, so its 95% interval runs from roughly 0.6% to 5.4%.

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

| Code | Meaning (from `IDS_mapping.csv`) | Stays | Plan |
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

| # | Problem | How big | What we will do |
|---|---|---|---|
| 1 ✱ | Missing values are written as the text `?` | 7 columns: `weight` 96.9%, `medical_specialty` 49.1%, `payer_code` 39.6%, `race` 2.2%, `diag_3` 1.4%, `diag_2` 0.35%, `diag_1` 0.02%. None in our six columns. | Load `?` as missing |
| 2 ✱ | **Loading trap:** pandas' default settings treat the text `None` as missing, but here `None` is a real answer ("test not done") | `max_glu_serum`: 96,420 rows; `A1Cresult`: 84,748 rows | Load with `na_values="?", keep_default_na=False` |
| 3 ✱ | Hidden missing values written as codes ("NULL", "Not Mapped", "Not Available") | discharge 18/25: 4,680 stays (4.6%); admission type 5/6/8: 10,396; admission source 9/17/20: 7,067 | Report; keep unknown-discharge stays, because we cannot tell whether those patients died |
| 4 ✱ | Death and hospice discharges | 1,652 deaths + 771 hospice = 2,423 stays | Exclude from the rate |
| 5 ✱ | Hospice patients sometimes do come back | 86 of 771 (43 within 30 days) | Mention in the note |
| 6 ✱ | The same patient has many stays | 16,773 patients (23.5%) hold 46.2% of all stays; one has 40 | Count per stay, plus a per-patient check |
| 7 ✱ | Gender is `Unknown/Invalid` | 3 stays | Report; keep for the age analysis, which does not use gender |
| 8 ✱ | Very small age groups | [0-10): 160 stays, 3 readmissions; [10-20): 690 stays | Show 95% intervals and a warning |
| 9 ✱ | No dates, and `encounter_id` is not a reliable time order | 13 patients have a stay with a *higher* ID than the stay in which they died. 18 patients' age bracket goes *down* as the ID goes up. 490 stays are flagged `NO` although the same patient has a higher-ID stay. | Treat "first stay" as approximate; ask the data owner |
| 10 ✱ | The readmission flag cannot be checked against the file | 2,166 single-stay patients are flagged `<30` | Trust the flag; ask the data owner how it is built |
| 11 ✱ | Day 30 itself is ambiguous (`<30` versus `>30`) | not measurable | Ask the data owner |
| 12 | The same patient has a different gender or race across stays | gender: 3 patients; race: 123 patients | Report |
| 13 | Impossible codes | "Neonate" discharge (code 10): all 6 stays are for patients aged 50+. "Newborn" admission (type 4): 9 of its 10 stays are for patients aged 40+. | Report |
| 14 | The mapping file is three tables in one CSV | separator lines `,`; leading spaces; codes out of order (30 before 27); two codes both "Not Available"; typos ("critial") | Write a small parser |
| 15 | Columns that never vary | `examide` and `citoglipton` are always `No`; 5 more drug columns are used 3 times or fewer | Report |
| 16 | Mixed coding styles | `NO` in `readmitted` but `No` elsewhere; `change` uses `Ch`/`No` | Match the exact strings |
| 17 | Diagnosis codes mix numbers and letters (ICD-9 `V…` and `E…` codes) | all three `diag_` columns | Keep as text |
| 18 | Windows line endings (CRLF) in both files | not measurable | pandas copes; worth knowing for other tools |

**Cross-check with the original paper.** Removing death and hospice stays and then keeping each patient's lowest `encounter_id` leaves 69,990 stays; the paper reports 69,984. The paper's ≤30 and 30–60 age groups match ours exactly (1,808 and 21,871 stays), and the rates are close:

| Age group | Paper | Ours |
|---|---|---|
| ≤30 | 6.2% | 6.2% |
| 30–60 | 7.4% | 7.2% |
| >60 | 10.2% | 9.9% |

So we are reading the data the same way its authors did.

---

## 4. Step-by-step plan

Each step has its own branch. Each branch is reviewed and confirmed before it is merged into `main` (see [AGENTS.md](AGENTS.md)). The core deliverables are small; most of the work is getting the definitions right.

### Step 0: Project set-up · branch `step-00-project-setup` · *done, waiting for your confirmation*

- **Goal:** a clean repository with the brief, this plan, the working rules, a glossary and a logbook.
- **Files:** `README.md`, `PROJECT_BRIEF.md`, `plan.md`, `AGENTS.md`, `CLAUDE.md`, `GLOSSARY.md`, `LOGBOOK.md`, `.gitignore`.
- **Done when:** you have read this plan and answered the decisions in [section 6](#6-decisions-for-you).
- **In plain words:** we wrote down what we will do and how we will work, before touching any code.

### Step 1: Environment and data loading · branch `step-01-data-loading`

- **Goal:** anyone can download the data and load it correctly, with one command for each.
- **Tasks:**
  1. Project skeleton: `src/readmission/` for our code, plus `tests/`, `scripts/` and `requirements.txt` (pandas, pytest).
  2. `scripts/download_data.py`: downloads the official UCI zip file into `data/raw/`, which git ignores. It then checks each file's SHA-256 fingerprint, so we know we have exactly the expected files:
     - `diabetic_data.csv`: `0689e7ec031237dc63031b938805c48377748761a3b26acab621567afa24df97`
     - `IDS_mapping.csv`: `f1bb82b471cb34649352597572c9b1fb00bd27f77b9f5a22a03dc3eb1039749e`
  3. `load_encounters(path)`: reads `diabetic_data.csv` with only `?` treated as missing, so `None` stays a real value.
  4. `load_id_mappings(path)`: splits `IDS_mapping.csv` into its three tables, trims stray spaces, and returns code-to-meaning lookups.
- **Done when:** loading gives 101,766 rows × 50 columns and three lookups with 8, 30 and 25 codes, and the value `None` survives in `A1Cresult`.
- **In plain words:** a wrong load silently changes the answer, so we first make loading boring and reliable.

### Step 2: Data-quality audit, read-only · branch `step-02-data-quality-audit`

- **Goal:** brief task 1, listing every data-quality problem before changing anything.
- **Tasks:**
  - Small check functions in `src/readmission/quality.py`.
  - `scripts/run_audit.py`, which writes the report `reports/data_quality.md`.
  - What gets checked:
    - shape and column types
    - `?` counts per column, and missing values hidden behind codes
    - unique IDs and the number of stays per patient
    - the values of gender, age and `readmitted`
    - discharge codes decoded and crossed with `readmitted`
    - codes in the data compared with the mapping file
    - contradictions within one patient's stays
    - impossible codes and columns that never vary
- **Each problem gets:** what it is, how many rows, whether it affects our question, and what we will do about it.
- **Done when:** code has confirmed or corrected every item in [section 3](#3-data-quality-problems-found-in-the-first-look), and nothing in the data has been changed.
- **In plain words:** like a mechanic, we inspect before we repair, and write the inspection report first.

### Step 3: Cleaning rules and the main function · branch `step-03-readmission-function`

- **Goal:** brief task 2, the function `readmission_rate_by_age(df)`.
- **What the function does, in order:**
  1. Checks that the needed columns exist and that `readmitted` contains only `NO`, `>30` and `<30`. If not, it stops with a clear error.
  2. Removes stays that ended in death or hospice (codes 11, 13, 14, 19, 20, 21). The codes are kept in one named constant that is easy to change.
  3. Marks `<30` as 1 and both `>30` and `NO` as 0.
  4. Groups by age bracket, counts stays and readmissions, and computes rate = readmissions ÷ stays.
  5. Sorts the brackets by their starting age (0, 10, 20, …), not alphabetically.
- **Output columns:**
  - `age_bracket`, `n_encounters`, `n_readmitted_30d`
  - `readmission_rate_30d`, as a share between 0 and 1
  - a 95% interval (`ci_low`, `ci_high`), so that small groups are not over-read
- **Small helpers:**
  - `overall_readmission_rate(df)`, for the first half of the manager's question.
  - `first_encounter_per_patient(df)`, for the per-patient check.
- **Done when:** the function runs on the real data and its docstring states every rule.
- **In plain words:** one function turns the raw table into the answer table, with every rule written down.

### Step 4: Unit tests · branch `step-04-unit-tests`

- **Goal:** brief task 3, 2–3 `pytest` tests on tiny hand-made tables, never on the real file.
- **Proposed tests:**
  1. **Counting is right:** 6 rows in 2 brackets with a known mix of `<30`, `>30` and `NO` give exact counts and rates. This also proves that `>30` is *not* counted as a 30-day readmission.
  2. **Death and hospice stays are removed:** rows with codes 11 and 13 disappear from both the top and the bottom of the rate.
  3. **Brackets come out in age order:** shuffled input rows give one output row per bracket, ordered `[0-10)`, `[10-20)`, …, `[90-100)`.
  - *Optional extras:* a patient with two stays is counted twice, because we count stays; bad `readmitted` values raise an error.
- **Done when:** `pytest` passes in under a second without the real data.
- **In plain words:** we build small tables where we know the right answer by hand, and prove the function gets it.

### Step 5: Results on the real data · branch `step-05-results`

- **Goal:** run the tested function on the real data and answer the manager.
- **Tasks:**
  - `scripts/run_analysis.py`, which writes `reports/readmission_by_age.csv` and a `.md` version.
  - The overall rate.
  - Checks:
    - (a) per patient, using each patient's first stay
    - (b) unknown discharge codes excluded as well
    - (c) comparison with the paper
  - Optional: one bar chart with intervals.
- **Done when:** one command reproduces all the numbers, and the checks are recorded in the logbook.
- **In plain words:** we run the proven function on the real data and check that the answer does not hinge on one choice.

### Step 6: The note and final review · branch `step-06-note-and-review`

- **Goal:** brief task 4, plus a final check of everything.
- **Tasks:**
  - `NOTE.md`, under half a page: assumptions, exclusions with counts and reasons, and questions for the data owner.
  - `README.md` with how-to-run instructions and the headline result.
  - Tick off every item in the brief.
  - Test a fresh clone end to end: download, audit, tests, results.
- **Done when:** every item in `PROJECT_BRIEF.md` is done and a fresh clone runs end to end.
- **In plain words:** a short, honest summary a manager can read in two minutes, and a repository anyone can rerun.

### Target layout

```text
diabetes-readmission-analysis/
├── README.md             how to run + headline results
├── PROJECT_BRIEF.md      research question, data and tasks
├── plan.md               this plan
├── AGENTS.md, CLAUDE.md  working rules
├── GLOSSARY.md           medical terms in plain words
├── LOGBOOK.md            strict record of the work
├── NOTE.md               the half-page note                (Step 6)
├── requirements.txt      Python packages                   (Step 1)
├── data/raw/             downloaded data, not in git       (Step 1)
├── scripts/              download, audit, analysis         (Steps 1, 2, 5)
├── src/readmission/      loading, quality checks, metrics  (Steps 1–3)
├── tests/                unit tests on hand-made tables    (Step 4)
└── reports/              generated outputs                 (Steps 2, 5)
```

---

## 5. What a good result looks like

- **We look before we clean.** Every problem is listed with a count, before any row is removed.
- **The definitions are explicit.** We state the numerator, the denominator and the unit of counting (stay or patient).
- **Every exclusion has a reason and a count.**
- **The loading is correct.** `?` becomes missing, and `None` stays a real value.
- **Age brackets are in age order, and small groups are flagged.**
- **The tests pin down the tricky rules,** not just the easy ones.
- **The note is honest.** It covers the assumptions and limits, and asks the data owner sensible questions.
- **Everything is reproducible.** There is one command per step and no hand-typed numbers.
- **The scope is disciplined.** The core tasks come first (about 60–90 minutes of work), and extras are clearly marked as optional.

---

## 6. Decisions for you

My recommendation is listed first in each case.

1. **Language:** Python with pandas and pytest. *(Alternative: R.)*
2. **Main counting unit:** per stay (B), with the per-patient first-stay view (C) as a check.
3. **Exclusions:**
   - Exclude death (codes 11, 19, 20, 21) and hospice (codes 13, 14).
   - Keep the unknown discharge codes (18, 25) and report them.
   - Do not exclude "left against medical advice" (code 7, 623 stays) or transfers to another hospital (code 2, 2,128 stays). Ask the data owner instead.
4. **`Unknown/Invalid` gender (3 stays):** keep these stays for the age analysis, and list them as a data problem.
5. **Small age groups:** keep all ten brackets as the brief asks, and add 95% intervals and a "small group" warning.
6. **Raw data:** do not commit it to git. A download script with a fingerprint check fetches it instead.

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
| A wrong load silently changes values (`None` read as missing) | An explicit loader with checks, plus a test |
| Counting patients when we mean stays, or the other way round | Name the unit everywhere; show both B and C |
| Over-reading tiny groups | 95% intervals and a warning for small brackets |
| Reading cause into a correlation ("age causes readmission") | Describe associations only; older patients also tend to have more other illnesses |
| Scope creep beyond the timebox | Core tasks first; extras clearly marked as optional |

---

## 9. Sources

- Clore, J., Cios, K., DeShazo, J., & Strack, B. (2014). *Diabetes 130-US Hospitals for Years 1999-2008* [Dataset]. UCI Machine Learning Repository. <https://doi.org/10.24432/C5230J>
- Strack, B., DeShazo, J. P., Gennings, C., Olmo, J. L., Ventura, S., Cios, K. J., & Clore, J. N. (2014). Impact of HbA1c measurement on hospital readmission rates: analysis of 70,000 clinical database patient records. *BioMed Research International*, 2014, 781670. <https://doi.org/10.1155/2014/781670>
