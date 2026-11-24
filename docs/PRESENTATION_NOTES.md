# Explanations for presentation

Questions and the simplest answers, in notebook order.

---

## 0. The project files

**Where does what happen?**
All computing happens in two files:
- `notebooks/analysis.ipynb`: loading, data-quality checks, exclusion, results.
- `src/readmission.py`: the function.

Everything else is text, and its numbers are copied from the notebook:
- `RESULTS.md`, `NOTE.md`, `NARRATIVE.md`, `README.md`
- the rules and records in `docs/`

**Order of work:**
1. Load (§1).
2. Checks (§2.1–2.6).
3. List of 8 problems (§2.7).
4. Remove death and hospice stays (§3).
5. The function → the table by age (§3).
6. Overall rate (§3).
7. Unit tests: `tests/test_readmission.py`.

**What is a notebook?**
One file holding text, code and the code's results together. A text editor shows its raw storage format (JSON). Open it in Jupyter or VS Code, or on GitHub, to see it as a page: headings, code boxes, and each result under its box.

---

## 1. The data

**Is this the raw data?**
Yes. It is the UCI file the brief names, unchanged (the SHA-256 fingerprints match the official download). Before publishing, the dataset's authors prepared it from the hospital database:
- they kept only stays that meet five rules
- they removed names and dates for privacy
- they added the `readmitted` column

**How do we know who came back, if there are no dates?**
The `readmitted` column already holds the answer for each stay:
- `<30`: came back within 30 days
- `>30`: came back later
- `NO`: no return on record

The authors computed it from the full database, which has dates. We only count it. We cannot check it, so we trust it (problem 8).

> "I used the UCI file unchanged. The readmission flag was computed by the dataset's authors from the full hospital records, which aren't public, so I take it as given and listed that as a limitation."

---

## 2. Notebook §1: loading

**What does `low_memory=False` do?**
By default, pandas reads a big file in pieces and guesses each column's type piece by piece. `payer_code` (who paid the bill) is empty in the file's first 20,446 rows, so pandas guessed "number" there and "text" further down, and warned about mixed types. With `low_memory=False` it reads each column in one go, makes one guess, and does not warn. The values are identical either way.
*(The notebook text says 20,445; the correct number is 20,446. To be fixed.)*

**Why check that `None` is kept?**
In `A1Cresult` (a blood test of average blood sugar over ~3 months), `None` means "test not done". pandas turns the word `None` into "missing" by default. We switched that off. The check shows `None` with its 84,748 rows and no missing values, so loading changed nothing.

> "`None` means 'test not done' in this data, but pandas reads it as missing by default. I turned that off and checked that it worked."

---

## 3. Notebook §2.2: missing values

**What does the code do, line by line?**
1. `COLUMNS = [...]`: the six columns we use, saved under one name.
2. `df.isna().sum()`: counts the missing values in each of the 50 columns.
3. `missing[missing > 0].sort_values(ascending=False)`: keeps the 7 columns that have any, most missing first.
4. `df[COLUMNS].isna().sum().sum()`: the total number of missing values in our six columns. It is **0**.
5. `pd.DataFrame({...})`: a small table of count and percent. It is shown because it is the cell's last line.

`diag_1` shows 0.0% only because of rounding (21 ÷ 101,766 = 0.02%).

**Summary of the table:**
> "7 of the 50 columns have missing values. Three are largely empty: patient weight (97%), the admitting doctor's specialty (49%) and who paid the bill (40%). Race and the three diagnosis columns are nearly complete (2.2% or less missing). None of the six columns used in this analysis has a missing value, so missing data does not affect the readmission rates."

**Why count per column and not per row?**
A gap only matters if it is in a column we use, and the column view shows exactly that: our six columns have none. Both views are in the notebook:
- per column in §2.2
- per row in §2.7, problem 1: 100,723 of 101,766 rows have at least one gap

Demanding complete rows would keep only 1,043 stays (1%). That would throw away 99% of the data because of columns we never use, mainly `weight`.

A row is one hospital stay, not one patient: one patient can have up to 40 rows.

---

## 4. Notebook §2.3: stays and patients

**What does the code do, line by line?**
1. `stays_per_patient = df["patient_nbr"].value_counts()`: counts the rows (stays) of each patient ID. One number per patient, largest first.
2. `repeat = stays_per_patient > 1`: True for each patient with 2 or more stays.
3. `df["encounter_id"].is_unique`: True if no stay ID appears twice, so one row = one stay. Prints `True`.
4. `len(stays_per_patient)`: the number of different patients: **71,518**.
5. Patients with 2 or more stays:
   - `repeat.sum()` counts them: **16,773**.
   - `repeat.mean()` gives their share: **23.5%**.
   - `stays_per_patient[repeat].sum()` adds up their stays: **47,021**.
6. `stays_per_patient.max()`: the most stays for one patient: **40**.

**Why check `encounter_id` if patients repeat?**
There are two different IDs:
- `encounter_id` is the ID of a **stay**. Every stay gets a new one, and none repeats.
- `patient_nbr` is the ID of a **person**. It repeats once per stay.

Example from the data, one patient with three stays:

| encounter_id | patient_nbr | age | readmitted |
|---|---|---|---|
| 250872 | 41606064 | [20-30) | >30 |
| 2309376 | 41606064 | [20-30) | >30 |
| 11198010 | 41606064 | [20-30) | >30 |

What the check gives us: no stay is recorded twice. The table counts rows as stays, so a duplicated stay would be counted twice and change the rates.

**Formatting in `print(f"...")`:**
- `{x:,}` adds thousands commas.
- `{x:.1%}` shows a share as a percent with one decimal.

**Why it matters:**
There are 101,766 stays but only 71,518 patients. The table counts stays, as the brief asks ("number of encounters"), so a patient with 40 stays counts 40 times. The patients who come back hold almost half of all stays (47,021 of 101,766).

> "Each row is one hospital stay. 71,518 patients make 101,766 stays: about a quarter of the patients have more than one stay, and together they hold almost half of all stays. My table counts stays, as the brief asks."

---

## 5. The data-quality checks: plan and changes

**Initial plan** (before my comments):

| Check | Function | Why |
|---|---|---|
| Size and column types | `df.shape`, `df.dtypes` | Confirms it is the expected file (101,766 × 50) |
| Missing values (`?`) per column | `df.isna().sum()` | The brief's first quirk |
| One row per stay? Repeat patients? | `df["encounter_id"].is_unique`, `df["patient_nbr"].value_counts()` | Stays are not patients |
| Odd values in the analysis columns | `value_counts()` on `gender`, `age`, `readmitted`, `discharge_disposition_id` | Finds `Unknown/Invalid`, the age brackets and the labels |
| What the discharge codes mean | `pd.read_csv("data/raw/IDS_mapping.csv", skiprows=10, nrows=30)` (just the discharge table) | Finds the death and hospice codes |
| Can those patients come back? | `pd.crosstab(df["discharge_disposition_id"], df["readmitted"])` | Checks death and hospice stays against the outcome |

**Final version** (`docs/plan.md` §5, agreed in logbook entry 003):

| Check | Function | Why | Notebook |
|---|---|---|---|
| Size and column types | `df.shape`, `df.dtypes` | Confirms it is the expected file (101,766 × 50) and shows there are no date columns | §2.1 |
| Missing values (`?`) per column | `df.isna().sum()` | The brief's first known quirk | §2.2 |
| One row per stay? Repeat patients? | `df["encounter_id"].is_unique`, `df["patient_nbr"].value_counts()` | One patient can have many stays, so stays are not patients | §2.3 |
| Allowed values in `age`, `gender`, `readmitted` | `value_counts(dropna=False)`, then `isin()` against the allowed values | Shows every value, missing included, and flags missing or unexpected labels such as `Unknown/Invalid` | §2.4 |
| Discharge codes and what they mean | `value_counts()` on `discharge_disposition_id`, decoded with `pd.read_csv("../data/raw/IDS_mapping.csv", skiprows=10, nrows=30, keep_default_na=False)` | Finds the death, hospice and unknown codes. `keep_default_na=False` keeps code 18's label `NULL` visible | §2.5 |
| Can those patients come back? | `pd.crosstab(df["discharge_disposition_id"], df["readmitted"])` | Checks death and hospice stays against the outcome | §2.6 |

The list of problems is built from the results (§2.7).

**What changed:**
- Row 1: also shows there are no date columns.
- Row 4 (my suggestion, logbook entry 003): `dropna=False` counts missing values too, and `isin()` flags anything not on an allowed list. `discharge_disposition_id` moved to its own check (row 5).
- Row 5: also finds the unknown codes, and `keep_default_na=False` keeps code 18's label `NULL` from being read as missing.

**How the list of problems changed:**
1. The first look found 18 problems (plan §3).
2. The six checks gave 9.
3. "Small age groups" was removed, because it is a sample-size warning, not a data fault, and needed a hand-picked cut-off. That left 8.

---

## 6. Notebook §2.4: allowed values

**What does the code do, line by line?**
1. `allowed = {...}`: the values we expect in each column. The ten age brackets are built by code (`range(0, 100, 10)` → `[0-10)` … `[90-100)`), not typed.
2. `for col, values in allowed.items():`: repeats the next two steps for each of the three columns.
3. `value_counts(dropna=False).sort_index()`: every value with its count, missing values included.
4. `~df[col].isin(values)`: True for each value not on the list. A missing value counts as not on the list.
5. `print(...)`: shows those values, or "none".

**Result:**
- `age` has exactly the ten brackets.
- `readmitted` has only `NO`, `>30` and `<30`.
- 3 stays have gender `Unknown/Invalid`.

**The loop, simpler: one round, for `gender`**
- `for col, values in allowed.items():` takes one pair from `allowed`: `col = "gender"`, `values = ["Female", "Male"]`. The loop then does the same for `age` and `readmitted`.
- Line 1 prints every value with its count:
  - `df[col]`: the gender column (101,766 values).
  - `.value_counts(dropna=False)`: counts each value, missing included: Female 54,708, Male 47,055, Unknown/Invalid 3.
  - `.sort_index()`: sorts by the value's name (puts the age brackets in order).
  - `.to_string()`: plain text, without pandas' extra footer line.
- Line 2 finds the values that are not allowed:
  - `df[col].isin(values)`: True/False per stay; True if Female or Male.
  - `~`: flips it, so True means not allowed. A missing value is also not allowed.
  - `df.loc[that, col]`: keeps only those stays' gender values (3 values).
  - `.value_counts(dropna=False)`: counts them: Unknown/Invalid 3.
- Line 3 prints the result:
  - `.to_dict()`: turns the counts into `{'Unknown/Invalid': 3}`.
  - `or "none"`: if nothing was found, the dictionary is empty and "none" is printed instead.
  - `f"...{col}..."`: puts the column name into the text.
  - `"\n"`: an empty line before the next round.

**Why:** the table groups by `age` and counts `readmitted`. A typo or missing label would create a wrong group or be counted wrongly.

> "I checked that age, gender and readmitted hold only the expected values. Age has exactly the ten brackets, readmitted only NO, >30 and <30, and 3 stays have gender Unknown/Invalid."
