# diabetes-readmission-analysis

**How often are hospital patients with diabetes readmitted within 30 days of leaving hospital, and how does that differ by age group?**

This repository analyzes the public UCI dataset *Diabetes 130-US hospitals for years 1999–2008*: 101,766 hospital stays from 130 US hospitals.

## Status

**Done.** The results are in [the notebook](notebooks/analysis.ipynb), the note in [NOTE.md](NOTE.md) and the short report in [NARRATIVE.md](NARRATIVE.md).

## Where to find what

| File | What it is |
|---|---|
| [NOTE.md](NOTE.md) | The note: assumptions, what was excluded and why, questions for the data owner |
| [notebooks/analysis.ipynb](notebooks/analysis.ipynb) | The analysis, in one notebook: loading, data-quality list, results |
| [src/readmission.py](src/readmission.py) | The function `readmission_rate_by_age(df)` |
| [tests/test_readmission.py](tests/test_readmission.py) | Two unit tests on small hand-made tables |
| [NARRATIVE.md](NARRATIVE.md) | The short report: the approach, the choices that had a real alternative, and the limitations |
| [data/README.md](data/README.md) | Source, license credit and fingerprints of the raw data |

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
pytest
```

The `jupyter` line reruns the whole notebook and saves its outputs (to read it interactively instead: `jupyter notebook notebooks/analysis.ipynb`). `pytest` runs the unit tests.

## Citation

- Clore, J., Cios, K., DeShazo, J., & Strack, B. (2014). *Diabetes 130-US Hospitals for Years 1999-2008* [Dataset]. UCI Machine Learning Repository. <https://doi.org/10.24432/C5230J>
- Strack, B., et al. (2014). Impact of HbA1c measurement on hospital readmission rates: analysis of 70,000 clinical database patient records. *BioMed Research International*, 2014, 781670. <https://doi.org/10.1155/2014/781670>
