# Project brief: 30-day hospital readmissions by age

The original project description, kept for reference. How we will carry it out is in [plan.md](plan.md); medical terms are explained in [GLOSSARY.md](GLOSSARY.md).

## Research question

A hospital manager asks:

> **"What share of patients are readmitted within 30 days, and how does that differ by age group?"**

## Dataset

**UCI "Diabetes 130-US hospitals for years 1999–2008"**

- Source: UCI Machine Learning Repository — <https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008>
- Licence: CC BY 4.0 (free to use and share with credit). DOI: [10.24432/C5230J](https://doi.org/10.24432/C5230J)
- Files:
  - `diabetic_data.csv`: about 100,000 hospital encounters (one row per hospital stay), 50 columns.
  - `IDS_mapping.csv`: decodes the numeric ID columns (admission type, discharge disposition, admission source) into text.

### Columns used in this analysis

| Column | Meaning |
|---|---|
| `encounter_id` | ID of one hospital stay (encounter) |
| `patient_nbr` | ID of one patient |
| `age` | age bracket as a string, e.g. `[70-80)` |
| `gender` | patient gender |
| `discharge_disposition_id` | code for where the patient went when leaving hospital |
| `readmitted` | `NO`, `<30` (readmitted within 30 days) or `>30` (readmitted after more than 30 days) |

### Known quirks

- Missing values are the literal string `?`, not blanks.
- `patient_nbr` repeats, because one patient can have many encounters.
- A few `gender` values are `Unknown/Invalid`.
- Some discharge codes mean the patient died or went to hospice, so they could never be readmitted. The exact codes must be checked in the mapping file.

## Tasks

1. Load the data and list any data-quality problems found, **before changing anything**.
2. Write a function `readmission_rate_by_age(df)` that returns a table with **age bracket**, **number of encounters** and **30-day readmission rate**.
3. Add 2–3 unit tests, using **small hand-made data frames** rather than the real file.
4. Write a short note (**under half a page**) with the assumptions, what was excluded and why, and what to ask the data owner.

## Scope

- Timebox: about 60–90 minutes of focused work for the core tasks.
- Language: free choice.
