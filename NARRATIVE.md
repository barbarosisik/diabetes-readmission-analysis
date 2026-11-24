# diabetes-readmission-analysis

Barbaros Isik · 23 November 2026

## Overview

I answer one question from a hospital manager: what share of patients with diabetes are readmitted to hospital within 30 days of leaving, and how does that differ by age group? I use a public dataset of 101,766 hospital stays from 130 US hospitals (1999–2008). So far, the project is set up and the data load correctly.

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

## Limitations

- The data have no dates, so the order of a patient's stays and the exact 30-day window cannot be checked.
- The readmission flag was computed by the data's authors from the full hospital database, so I have to trust it.
- Readmissions to hospitals outside the 130 are not recorded, so the true rates are probably somewhat higher.

## AI tools used

- **Claude Code** (an AI coding assistant): helped write the plan and documents, download and check the data, write the notebook code and prepare commit messages. I reviewed and approved every step before it was merged.

## How to reproduce

```bash
git clone https://github.com/barbarosisik/diabetes-readmission-analysis.git
cd diabetes-readmission-analysis
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
jupyter nbconvert --to notebook --execute --inplace notebooks/analysis.ipynb
```
