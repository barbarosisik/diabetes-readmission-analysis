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
