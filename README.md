# diabetes-readmission-analysis

**How often are hospital patients with diabetes readmitted within 30 days of leaving hospital, and how does that differ by age group?**

This repository analyzes the public UCI dataset *Diabetes 130-US hospitals for years 1999–2008*: 101,766 hospital stays from 130 US hospitals.

## Status

**Step 1 of 4 (data and loading).** See [docs/plan.md](docs/plan.md) for the full plan and [docs/LOGBOOK.md](docs/LOGBOOK.md) for progress.

## Where to find what

| File | What it is |
|---|---|
| [notebooks/analysis.ipynb](notebooks/analysis.ipynb) | The analysis, in one notebook (so far: loading the data) |
| [NARRATIVE.md](NARRATIVE.md) | A short report of the work: what was done, how and why |
| [data/README.md](data/README.md) | Source, license credit and fingerprints of the raw data |
| [docs/PROJECT_BRIEF.md](docs/PROJECT_BRIEF.md) | The research question, the data and the tasks |
| [docs/plan.md](docs/plan.md) | What the question really asks, what the data look like, and the step-by-step plan |
| [AGENTS.md](AGENTS.md) | Working rules: branches, commit messages, explanations, data handling |
| [docs/GLOSSARY.md](docs/GLOSSARY.md) | Medical, hospital and data terms in plain words |
| [docs/LOGBOOK.md](docs/LOGBOOK.md) | Strict record of everything discussed, decided and changed |

## Data

The data come from the UCI Machine Learning Repository under the CC BY 4.0 license:
<https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008>.
The two raw files are in `data/raw/`, unchanged. Their source, license credit and SHA-256 fingerprints are in [data/README.md](data/README.md).

## How to run

Needs Python 3.12 or newer.

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter nbconvert --to notebook --execute --inplace notebooks/analysis.ipynb
```

The last line reruns the whole notebook and saves its outputs. To read it interactively instead, run `jupyter notebook notebooks/analysis.ipynb`.

## Citation

- Clore, J., Cios, K., DeShazo, J., & Strack, B. (2014). *Diabetes 130-US Hospitals for Years 1999-2008* [Dataset]. UCI Machine Learning Repository. <https://doi.org/10.24432/C5230J>
- Strack, B., et al. (2014). Impact of HbA1c measurement on hospital readmission rates: analysis of 70,000 clinical database patient records. *BioMed Research International*, 2014, 781670. <https://doi.org/10.1155/2014/781670>
