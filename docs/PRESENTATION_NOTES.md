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

---

## 7. Notebook §2.5: discharge codes and what they mean

**What is the discharge code?**
`discharge_disposition_id` is a code for where the patient went when leaving hospital: home, a care home, another hospital, hospice, or the patient died ("Expired" in hospital wording). *Hospice* is comfort care for people expected to live only a few months. The data hold only the number; what each number means is in `IDS_mapping.csv`.

**What does cell 1 do, line by line?**
1. `pd.set_option("display.max_colwidth", None)`: pandas cuts text longer than 50 characters when it shows a table. This turns that off, so the full labels are visible.
2. `pd.read_csv(..., skiprows=10, nrows=30, keep_default_na=False)`: reads only the discharge table. The mapping file holds three code tables, one under the other: admission type (lines 1–9, then a separator line `,` on line 10), discharge (header on line 11, codes on lines 12–41) and admission source (from line 43).
   - `skiprows=10`: skips the first table and the separator, so line 11 becomes the header.
   - `nrows=30`: reads the 30 discharge codes and stops.
   - `keep_default_na=False`: code 18's label is the word `NULL`, which pandas would otherwise read as missing (the same trap as `None`). Cell 2 could then not find code 18 by its label.
3. `.set_index("discharge_disposition_id").sort_index()`: the code number becomes the row label, so codes can be looked up by number. Sorted 1 to 30 (in the file, 30 comes before 27).
4. `discharge["stays"] = ...value_counts().reindex(discharge.index, fill_value=0)`: counts the stays for each code in the data and lines the counts up with the mapping's 30 codes. Codes nobody has (21, 26, 29, 30) show 0 instead of missing. It adds a column to the mapping table; `df` is not changed.
5. `set(...) - set(...) or "none"`: the codes in the data that are not in the mapping file, so codes with no meaning. Line 4 only counts codes that are in the mapping; this checks the other direction. It prints "none": every code in the data has a meaning.
6. `discharge`: shows the table: 30 codes, each with its label and number of stays.

**Line 2, simpler: what the mapping file looks like**
`IDS_mapping.csv` is not one table but three small tables, one under the other, separated by a line holding only a comma:

```text
 1  admission_type_id,description          <- table 1: admission type
 2  1,Emergency
 …
 9  8,Not Mapped
10  ,                                      <- separator
11  discharge_disposition_id,description   <- table 2: discharge (the one we need)
12  1,Discharged to home
 …
29  18,NULL
 …
41  29,Discharged/transferred to a Critical Access Hospital (CAH).
42  ,                                      <- separator
43  admission_source_id,description        <- table 3: admission source
 …
```

A plain `pd.read_csv` would read all three as one table, with the discharge codes mixed into the admission codes. So:
- `skiprows=10`: skip lines 1–10. Line 11 is the first line read, and pandas uses it as the column names.
- `nrows=30`: read the next 30 lines (12–41, the 30 discharge codes), then stop before the separator and table 3.
- `keep_default_na=False`: line 29 has the word `NULL`, which pandas would read as missing. Switched off, it stays the text "NULL", so cell 2 can find code 18 by its label.

The 10 and 30 come from looking at the file. The file never changes (its fingerprint is in `data/README.md`), and line 5 confirms that no code in the data is missing from the table.

**What does cell 2 do, line by line?**
1. `label = discharge["description"]`: a short name for the label column.
2. `DEATH`: the codes whose label starts with "Expired" (died): 11, 19, 20, 21.
3. `HOSPICE`: the codes whose label starts with "Hospice": 13, 14. "Starts with" matters: the labels of 19–21 (e.g. "Expired at home. Medicaid only, hospice.") also contain "hospice", but they are deaths. The "Medicaid only, hospice" part is only a billing note; Medicaid is US public health insurance for people with low incomes.
4. `UNKNOWN`: the codes whose label is exactly one of the three "we don't know" labels: 18 (`NULL`), 25 (`Not Mapped`), 26 (`Unknown/Invalid`).
5. `discharge.loc[DEATH + HOSPICE + UNKNOWN]`: `+` joins the three lists into one; `.loc` shows those 9 codes with their labels and stays.

`.tolist()` turns each result into a plain list like `[11, 19, 20, 21]`, used again in §2.6, §2.7 and §3. With lists, `+` joins them (on pandas objects it would add the numbers), and they print as `[11, 19, 20, 21]` in the §2.7 table.

**Result:**

| Group | Codes | Stays |
|---|---|---|
| Death | 11, 19, 20, 21 | 1,642 + 8 + 2 + 0 = 1,652 |
| Hospice | 13, 14 | 399 + 372 = 771 |
| Unknown | 18, 25, 26 | 3,691 + 989 + 0 = 4,680 |

**Why:** the brief says some codes mean death or hospice and "the exact codes must be checked in the mapping file". Looking them up by label means no code number is typed by hand: the code reads the meaning from the file.

> "The discharge code says where the patient went after the stay. I read each code's meaning from the mapping file and picked out the death, hospice and unknown codes by their labels, not by typing numbers: 1,652 stays ended in death, 771 in hospice care, and 4,680 have an unknown destination."

---

## 8. Notebook §2.6: can those patients come back?

**What does the code do, line by line?**
1. `outcome = pd.crosstab(df["discharge_disposition_id"], df["readmitted"])`: counts the stays for each pair of discharge code and `readmitted` value. One row per code used in the data (26), one column each for `<30`, `>30` and `NO`.
2. `outcome.reindex(DEATH + HOSPICE + UNKNOWN, fill_value=0)`: keeps only the 9 codes from §2.5, in that order. Codes 21 and 26 have no stays, so they are not in the crosstab; `fill_value=0` adds them as rows of zeros.

**Why this way?**
- `crosstab`: one line gives all three outcomes for every code.
- `reindex`: uses the code lists from §2.5, so no code is typed by hand. `.loc` would stop with an error on codes 21 and 26.

**Result:**

| Code | Meaning | <30 | >30 | NO |
|---|---|---|---|---|
| 11 | Expired | 0 | 0 | 1,642 |
| 19 | Expired at home | 0 | 0 | 8 |
| 20 | Expired in a medical facility | 0 | 0 | 2 |
| 21 | Expired, place unknown | 0 | 0 | 0 |
| 13 | Hospice / home | 19 | 36 | 344 |
| 14 | Hospice / medical facility | 24 | 7 | 341 |
| 18 | NULL | 459 | 1,027 | 2,205 |
| 25 | Not Mapped | 92 | 376 | 521 |
| 26 | Unknown/Invalid | 0 | 0 | 0 |

- Death: every stay is `NO`, as it must be, so the flag is consistent.
- Hospice: 86 of 771 came back (19 + 36 + 24 + 7), 43 within 30 days (19 + 24). Patients can leave hospice care.
- Unknown: 1,954 of 4,680 came back (459 + 1,027 + 92 + 376), so at least those patients were alive. The other 2,726 are `NO`: alive or dead, we can't tell.

**Why:** the brief says these patients "could never be readmitted". This checks that against the data: true for death, not quite true for hospice, and not true for many unknown-destination stays.

> "All death stays are marked NO, as they should be. Hospice patients did sometimes come back: 86 of 771, 43 within 30 days. And at least 1,954 of the 4,680 unknown-destination stays were followed by a return, so many of those patients were alive."

**Simpler version**

The question: the brief says patients who died or went to hospice "could never be readmitted". Is that true in the data?

1. `pd.crosstab(...)` makes a counting table: one row per discharge code, one column per outcome (`<30`, `>30`, `NO`). Each box is the number of stays with that code and that outcome. Example with 3 stays, (11, NO), (13, <30) and (13, NO):

   | code | <30 | >30 | NO |
   |---|---|---|---|
   | 11 | 0 | 0 | 1 |
   | 13 | 1 | 0 | 1 |

2. `.reindex(...)` keeps only the 9 codes we care about (death, hospice, unknown). Codes 21 and 26 have no stays, so they get a row of zeros.

What we got (the notebook's rows added up per group):

| Group | Stays | Back within 30 days | Back later | Never back |
|---|---|---|---|---|
| Died | 1,652 | 0 | 0 | 1,652 |
| Hospice | 771 | 43 | 43 | 685 |
| Unknown | 4,680 | 551 | 1,403 | 2,726 |

What it means for §3:
- Died: no one came back, as expected. Removed.
- Hospice: a few came back, but they are not expected to. Removed, as the dataset's authors also did.
- Unknown: 1,954 came back, so many were alive. Kept.

---

## 9. Notebook §2.7: the list of problems

**What does the code do?** Three parts.

1. Helper counts (first six lines):
   - `discharge_code`: a short name for the discharge column.
   - `death`, `hospice`, `unknown`: True/False for each stay: is its code in that group?
   - `death_no`: death stays marked `NO` (1,652).
   - `hospice_back`: hospice stays that came back (86); `hospice_30`: of those, within 30 days (43).
   - `none_value`: True where either lab column says `None` (101,468). `|` means "or".
2. `problems = pd.DataFrame([...])`: a table with 8 rows. Each row is (problem, rows affected, affects the question?). The texts use f-strings, so every number in them comes from code. `.sum()` on True/False counts the Trues.
3. Tidying: `problems.index += 1` numbers the rows from 1; `.map("{:,}".format)` adds thousands commas.

**Result:**

| # | Problem | Stays | Affects our answer? |
|---|---|---|---|
| 1 | `?` means missing, in 7 columns (`weight` 97% empty) | 100,723 | No: none in our six columns |
| 2 | pandas would read the real value `None` ("test not done") as missing | 101,468 | No: loaded correctly; columns not used |
| 3 | One patient, many stays (16,773 of 71,518 patients have 2 or more) | 47,021 | Yes: we count stays, not patients |
| 4 | gender `Unknown/Invalid` | 3 | No: gender is not used |
| 5 | The patient died | 1,652 | Yes: removed in §3 |
| 6 | The patient went to hospice | 771 | Yes: removed in §3, though 86 came back (43 within 30 days) |
| 7 | Destination unknown | 4,680 | Yes: kept, but could hide deaths |
| 8 | No dates | 101,766 | Yes: the `readmitted` flag has to be trusted |

**Why does problem 1 touch 99% of stays?**
100,723 of 101,766 stays have a `?` somewhere, but only in columns we don't use, such as `weight`. Our six columns have none, and row 1 says so. Kept as it is.

**Why:** brief task 1: list the problems before changing anything. Each row says how many stays it touches and whether it changes the answer, which leads straight to §3.

> "Before changing anything, I listed 8 data problems, each with how many stays it touches and whether it affects the answer. Three don't, because they are in columns I don't use. The other five shape the analysis: I count stays, not patients; I remove death and hospice stays; I keep the unknown destinations; and I trust the readmission flag, because there are no dates."

---

## 10. Notebook §3: 30-day readmission rate by age

**What does the code do?** Three cells.

1. Remove death and hospice stays:
   - `excluded`: True for each stay with a death or hospice code (from §2.5).
   - `eligible = df[~excluded]`: `~` flips True and False, so this keeps all other stays. `df` itself is not changed.
   - Prints: Excluded 2,423 (1,652 + 771). Remaining 99,343.
2. The table by age:
   - `sys.path.append("../src")`: the function is in its own file, `src/readmission.py`, so the unit tests can use the same function. This line tells Python to look in that folder.
   - `from readmission import readmission_rate_by_age`: loads the function.
   - `rates = readmission_rate_by_age(eligible)`: for each age bracket, the number of stays and the share of them flagged `<30`.
   - `rates.assign(...)`: shows the rate as a percent, like 14.3%. `rates` keeps the exact numbers.
3. The overall rate:
   - `(eligible['readmitted'] == '<30')`: True or False for each stay.
   - `.mean()`: the average of True (1) and False (0) is the share of True. Example: True, False, False, False → 1 of 4 = 25%.
   - Prints: 11.4% of 99,343 stays.

**Result:**

| Age | Stays | Back within 30 days |
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
| All | 99,343 | 11.4% |

- Overall: about 1 in 9 stays is followed by a return within 30 days.
- Lowest under 20, highest at 20–30; all other ages between 9.8% and 12.6%.
- The two youngest groups are small (160 and 690 stays), so their rates are uncertain.
- These are patterns, not causes: the table does not say that age causes returns.

**Why:** this is the answer to the manager's question (brief task 2).

> "After removing the 2,423 stays that ended in death or hospice, 11.4% of the remaining 99,343 stays were followed by a readmission within 30 days, about 1 in 9. By age, it is lowest under 20 and highest at 20–30 (14.3%); all other age groups are between about 10% and 13%."

---

## 11. The function: `src/readmission.py`

**What is the function?** The code that turns stays into the table by age. It is in its own file so the notebook and the unit tests use the same code.

**What does it do, line by line?**
1. `import pandas as pd`: loads pandas; needed for `pd.DataFrame` in the next line.
2. `def readmission_rate_by_age(df: pd.DataFrame) -> pd.DataFrame:`: creates the function, with the name the brief asks for. A table goes in, a table comes out (`: pd.DataFrame` and `-> pd.DataFrame` are only labels saying so).
3. The text in `"""..."""`: a short description for readers. Only `<30` counts, and death and hospice stays must be removed before calling.
4. `readmitted_30d = df["readmitted"] == "<30"`: True or False for each stay. `>30` and `NO` are False.
5. `.groupby(df["age"])`: puts each True/False into its stay's age group.
6. `.agg(encounters="size", readmission_rate_30d="mean")`: two numbers per group. `size` = how many stays; `mean` = the share of True = the rate. The names before `=` become the column names.
7. `.reset_index(names="age_bracket")`: the age groups become a normal column called `age_bracket`.

**Example** (the same 5 stays as in the first unit test):

| age | readmitted | `<30`? |
|---|---|---|
| [0-10) | <30 | True |
| [0-10) | NO | False |
| [50-60) | <30 | True |
| [50-60) | >30 | False |
| [50-60) | NO | False |

Output:

| age_bracket | encounters | readmission_rate_30d |
|---|---|---|
| [0-10) | 2 | 1 of 2 = 0.5 |
| [50-60) | 3 | 1 of 3 = 0.333 |

**Age order:** `groupby` sorts the groups alphabetically. For these ten labels that is also age order, because each starts with a different digit after `[`.

**Why:** it returns exactly the three columns the brief asks for: age bracket, number of encounters and 30-day readmission rate.

> "The function marks each stay as 'back within 30 days' or not, groups the stays by age bracket, and gives for each group the number of stays and the share that came back within 30 days."

---

## 12. The unit tests: `tests/test_readmission.py`

**What is a unit test?** A small piece of code that runs the function on a tiny hand-made table, where we know the right answer, and checks that the function gives that answer. `pytest` runs every function whose name starts with `test_`.

**Test 1: counts and rates**
- A table of 5 stays: [0-10) with `<30`, `NO`; [50-60) with `<30`, `>30`, `NO`.
- The answer worked out by hand: [0-10) has 2 stays, 1 back within 30 days → 1/2. [50-60) has 3 stays, 1 back within 30 days → 1/3.
- `pd.testing.assert_frame_equal(...)`: checks that the function's table equals that answer exactly: column names, numbers, types and order.
- It proves that `>30` and `NO` count as stays, but not as 30-day returns.

**Test 2: age order**
- 3 stays given in the wrong order: [90-100), [0-10), [10-20).
- `assert ... == ["[0-10)", "[10-20)", "[90-100)"]`: checks that the function puts them in age order. `assert` means "this must be true, or the test fails".

**Why two are enough:** the brief asks for 2–3. Test 1 covers the counting rule and the numbers; test 2 covers the order. Each test was checked to fail when its rule is broken on purpose (logbook entry 007).

**Result:** `pytest`: 2 passed.

> "I wrote two unit tests on tiny hand-made tables where I know the answer. One checks the counts and rates, including that '>30' and 'NO' don't count as 30-day returns; the other checks that the age groups come out in age order. Both pass."

---

## 13. Why these approaches, and what else we could have done

Every "same result" below was checked, on the real data or on small tables. Numbers marked *(quick check)* come from code outside the notebook: fine to say, not for the deliverables.

**Summary**
- Our approach is the simplest correct one almost everywhere.
- One small switch is worth making: problem 3's count in §2.7 (see 8).
- The original paper kept each patient's first stay, removed death and hospice stays, and counted `<30` against everything else. We do the same, except that we count every stay, because the brief asks for the "number of encounters".

### 1. Loading (§1)
**Ours:** `pd.read_csv(path, na_values="?", keep_default_na=False, low_memory=False)`: only `?` becomes missing; `None` stays "test not done".
**Other ways:**
- A. `pd.read_csv(path)`, then `df.replace("?", np.nan)`: the most common way online. Current pandas already turns `None` into missing when reading, so 84,748 A1C "test not done" values are lost. Older pandas did not, so the same code gives different data on different versions.
- B. `pd.read_csv(path, na_values="?")`: one setting fewer, same loss (84,748 in `A1Cresult`, 96,420 in `max_glu_serum`).
- C. A download package (`ucimlrepo`): no file in the repository, but it needs internet and an extra package, and we no longer control how `?` and `None` are read.

**Verdict:** keep. It is the only one-line way that keeps both rules.

### 2. Size and column types (§2.1)
**Ours:** `df.shape`, `df.dtypes`: the size on one line, then the types.
**Other ways:**
- A. `df.info()`: one line of code; prints the size, the types and the non-missing counts (57 lines). Equally good; the non-missing counts repeat §2.2 in a harder-to-read form.
- B. An automatic report (`ydata-profiling`, `ProfileReport(df)`): one line describes every column. An extra package, a long report, and it cannot judge what matters for our question (it doesn't know that code 11 means death).
- C. The file's fingerprint (SHA-256): proves it is the exact official file. Already done, in `data/README.md`.

**Verdict:** keep. If asked: "`df.info()` would do the same job; I wanted the size on one line."

### 3. Missing values (§2.2)
**Ours:** `df.isna().sum()`, only the columns with gaps, with percent, plus the total for our six columns (0).
**Other ways:**
- A. `df.isna().mean()`: the share directly, one step shorter for the percent; but we wanted the counts too.
- B. A picture (`missingno.matrix(df)`): shows where the gaps are, e.g. that `payer_code` is empty at the start of the file. An extra package, and a picture is not a number for the list.
- C. Per row (`df.isna().any(axis=1).sum()` = 100,723): used in §2.7. As the main view it misleads: 99% of rows look "incomplete" because of columns we never use.

**Verdict:** keep.

### 4. Stays and patients (§2.3)
**Ours:** `df["encounter_id"].is_unique` (True) and `df["patient_nbr"].value_counts()`.
**Other ways:**
- A. `df["encounter_id"].duplicated().sum()` (0) and `df.duplicated().sum()` (0 fully repeated rows): counts instead of True/False; same answer.
- B. `df["patient_nbr"].nunique()` (71,518): shorter for the number of patients, but we also need the stays per patient (repeats, maximum 40), and `value_counts()` gives all of it at once.
- C. `df["patient_nbr"].duplicated(keep=False).sum()` (47,021): the stays of repeat patients in one line.

**Verdict:** keep.

### 5. Allowed values (§2.4)
**Ours:** `value_counts(dropna=False)` to see every value, then `isin(allowed)` to flag anything else, for 3 columns in a loop.
**Other ways:**
- A. Only `value_counts()`, read by eye (our first plan): simpler, but nothing is flagged automatically, and §2.7 would need the label typed by hand.
- B. `set(df["gender"]) - {"Female", "Male"}` → `{'Unknown/Invalid'}`: one line, but no counts.
- C. A data contract (`pandera`): write the rules once (allowed values, `encounter_id` unique), then `schema.validate(df, lazy=True)` lists every break. Best when new data arrives regularly; an extra package and set-up for a one-time analysis.

**Verdict:** keep. These checks are also what make the short function safe (see 10).

> "For a one-time analysis I wrote the checks out. If this data arrived every month, I'd put the same rules in a data contract, so the pipeline stops when the data changes."

### 6. Discharge codes (§2.5)
**Ours:** read only the discharge table, then pick the codes by their labels.
**Other ways:**
- A. Type the codes: `DEATH = [11, 19, 20, 21]`, `HOSPICE = [13, 14]`. Two lines, and what most public analyses do. Risk: typed lists slip. One public notebook removes `[11, 13, 14, 19, 20, 26]`, calls 19, 20 and 26 "hospice" (19 and 20 are deaths, 26 is unknown) and misses 21. Here 21 and 26 have no stays, so its counts happen to be right.
- B. Search the labels for "hospice" anywhere (`str.contains("hospice", case=False)`): finds 13, 14, 19, 20 and 21, mixing deaths into hospice. That is why we use "starts with".
- C. Find the table by its header line instead of `skiprows=10, nrows=30`: no typed positions, but 3–4 more lines. The file never changes (fingerprint), and line 5 checks that no code is missing, so the typed positions are safe.

**Verdict:** keep. The label lookup costs one short cell and removes the typing risk.

### 7. Can they come back? (§2.6)
**Ours:** `pd.crosstab(code, readmitted)`, then keep our 9 codes.
**Other ways:**
- A. `df.groupby([code, readmitted]).size().unstack(fill_value=0)`: the identical table, more code.
- B. A crosstab per group with totals (codes mapped to died / hospice / unknown, `margins=True`): the 3-row table from the simpler notes; easier to present, but the per-code detail is gone and it needs one more line.
- C. `normalize="index"`, shares instead of counts *(quick check)*: back within 30 days: died 0%, hospice 5.6%, unknown 11.8%. Unknown-destination stays come back about as often as all stays (11.4%), so they behave like ordinary stays, not like deaths: a good argument for keeping them.

**Verdict:** keep (the brief asks to check the exact codes); use B's group totals when speaking.

### 8. The list of problems (§2.7)
**Ours:** a table built by code; the numbers in the text come from f-strings.
**Other ways:**
- A. A table typed in markdown: no code, but numbers typed by hand can go out of date.
- B. One `print` per problem: simpler, but less tidy.

**Suggested switch:** problem 3's count. Now `df["patient_nbr"].isin(stays_per_patient[repeat].index).sum()`; simpler: `stays_per_patient[repeat].sum()`, the same 47,021 already printed in §2.3.

### 9. What is excluded, and what is counted (§3)
**Ours:** remove death and hospice stays; count every stay.
**Other ways:**
- A. One stay per patient, the first (the original paper): 9.0% of 69,990 patients *(quick check)*. The paper did this because its regression model needs independent rows ("the observations could not be considered as statistically independent"). The brief's function asks for the "number of encounters", and we describe rather than model, so we count per stay.
- B. Medicare's readmission measures (Medicare: US public insurance, mainly for people 65 and over) also leave out patients who left against medical advice, and a stay that is itself a readmission does not start a new 30-day count. The second needs dates, which we don't have; the first is question 4 in the note. *(quick check)*: also removing "left against medical advice" (code 7) keeps 11.4%; also removing transfers to another hospital (code 2) gives 11.3%.
- C. Also remove the unknown destinations: 11.4% of 94,663 *(quick check)*, the same as now.

**Verdict:** keep. It is what the brief asks, and the other reasonable exclusions move the overall rate by at most 0.1 point. The choice that really matters is stays versus patients (11.4% versus 9.0%).

### 10. The function
**Ours:** three steps: True/False per stay → group by age → count and average.
**Other ways (same result, checked):**
- A. Count with a crosstab, then divide: `t = pd.crosstab(df["age"], df["readmitted"])`, rate = `t["<30"] / t.sum(axis=1)`. Reads like the formula "back within 30 days ÷ all stays"; a few more lines.
- B. Named aggregation on the whole table (`df.assign(...).groupby("age", as_index=False).agg(encounters=("r", "size"), ...)`, then rename): longer.
- C. SQL, e.g. with DuckDB: `SELECT age AS age_bracket, COUNT(*) AS encounters, AVG(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS readmission_rate_30d FROM df GROUP BY age ORDER BY age`. Very readable for people who know SQL; an extra package. (Not run here.)
- D. A small function inside: `.agg(encounters="size", readmission_rate_30d=lambda s: (s == "<30").mean())`: reads naturally, but slower and harder for beginners.

**Known limits of ours (tested):** a label like `[100-110)` would sort wrong; a stay with no age is silently left out; an unexpected value like `YES` silently counts as "not back". None of these happens in this data: §2.4 proved it.
**Verdict:** keep. It is the shortest of all the versions tested.

### 11. The unit tests
**Ours:** two tests: the exact table for 5 hand-made stays, and the age order.
**Other ways (A–C were run and pass on our function):**
- A. One test, many small cases (`@pytest.mark.parametrize`): e.g. all `NO` → 0.0, all `<30` → 1.0, `>30` and `<30` → 0.5. A compact way to add cases.
- B. The example inside the function's description (a doctest, run with `pytest --doctest-modules`): the documentation is also a test. Long tables in a description get messy.
- C. Random tables (property-based testing with `hypothesis`): generates many small tables and checks rules that must always hold: the stays add up to all rows, every rate is between 0 and 1, and rate × stays = the number of `<30`. Finds cases nobody thought of; an extra package, harder to explain.
- D. A test on the real file (11.4%): ruled out by the brief (hand-made tables only).

**Verdict:** keep. Our two tests cover the two rules that matter (what counts as a return, and the order), and each was shown to fail when its rule is broken. If asked about more: "With more time, I'd add random-table tests for the rules that must always hold."

### 12. How the project is organized
**Ours:** a notebook (the analysis with its results), the function in `src/`, the tests in `tests/`.
**Other ways:**
- A. One script, `analysis.py`: easy to review as text, but the results are not shown next to the code.
- B. Everything in the notebook, function included: fewer files, but pytest can't run the tests and the function can't be reused.

**Verdict:** keep: results visible, function reusable and tested.

> "For each step I chose the shortest code that keeps the data correct, and I checked the alternatives: they give the same numbers, or they lose information, like the default loading that turns 'test not done' into missing. The choice that really matters is counting stays rather than patients, and there I followed the brief."

**Sources:** the original paper (Strack et al. 2014, <https://pmc.ncbi.nlm.nih.gov/articles/PMC3996476/>); pandas `read_csv` (<https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html>); Medicare's heart-attack readmission measure (<https://www.qualityforum.org/Projects/a-b/All_Cause_Admissions_and_Readmissions/Measure_Worksheet_-_0505.aspx>); pandera (<https://pandera.readthedocs.io/>); a public notebook with typed codes (<https://kev9527.github.io/readmission_using_pipeline.html>).

---

## 14. Keep for the presentation

**Which original paper?**
Strack, B., DeShazo, J. P., Gennings, C., Olmo, J. L., Ventura, S., Cios, K. J., & Clore, J. N. (2014). *Impact of HbA1c measurement on hospital readmission rates: analysis of 70,000 clinical database patient records.* BioMed Research International, 2014, 781670. <https://doi.org/10.1155/2014/781670>. It was written by the dataset's own authors and published with the dataset.

> "The original paper kept each patient's first stay, removed death and hospice stays, and counted `<30` against everything else. We do the same, except that we count every stay, because the brief asks for the 'number of encounters'."

**Loading: one pass (ours), or read and then replace?**

| Goal | Code |
|---|---|
| Only `?` is missing; every other word is real data | `pd.read_csv(path, na_values="?", keep_default_na=False)` (ours) |
| `?` and pandas' usual missing words are all missing | `pd.read_csv(path, na_values="?")` |
| Read, then replace `?` | `pd.read_csv(path).replace("?", np.nan)`: never needed; one of the two above does it in one pass |

- Ours turns `?` into missing while reading, in one pass. It is faster: 0.39 s against 0.56 s on this file *(quick check)*. Memory use is about the same.
- The difference in meaning: with `keep_default_na=False`, pandas' usual missing words (`NA`, `N/A`, `NULL`, `null`, `NaN`, an empty field, …) are read as text. Checked on our file *(quick check)*: the only one of those words in it is `None` (181,168 cells, in `max_glu_serum` and `A1Cresult`), and there are no empty fields. In current pandas, `None` is on the usual list, but here it is a real answer ("test not done"). So for this file only ours is right: the other two turn 84,748 A1C results into missing.
- `low_memory=False` is a separate matter. pandas then chooses each column's type after reading the whole column, not piece by piece. Without it, pandas warns about mixed types (a `DtypeWarning`) in `payer_code`.

**Why `df.shape` and `df.dtypes`, and not `df.info()`?**
> "`df.info()` would do the same job; I wanted the size on one line."

`df.info()` prints 57 lines (one per column, plus a header and the memory use) and mixes in the non-missing counts, which §2.2 shows more clearly as missing counts. Ours prints the size on one clean line, then the types.

**For the notebook speech, before the questions:**
> "For a one-time analysis I wrote the checks out. If this data arrived every month, I'd put the same rules in a data contract, so the pipeline stops when the data changes."

**Why the discharge codes are not typed by hand:**
> "`DEATH = [11, 19, 20, 21]`, `HOSPICE = [13, 14]`. Two lines, and it's what most public analyses do. The risk is that typed lists slip. One public notebook removes `[11, 13, 14, 19, 20, 26]`. It calls 19, 20 and 26 'hospice', but 19 and 20 are deaths and 26 is unknown, and it misses 21. In this data, 21 and 26 have no stays, so its counts happen to come out right."

**The general rule:**
> "I always tried to do with less code, so I always went for the least code approach for most of the cases."

**To do, to finalize:** a presentation speech for the notebook and the code, given before the questions. It uses the lines above.
