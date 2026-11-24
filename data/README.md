# Data

The raw data, committed exactly as they come from the source. These files are never edited.

| File | What it is |
|---|---|
| `raw/diabetic_data.csv` | 101,766 hospital stays (one row per stay) × 50 columns. Missing values are written as the text `?`. |
| `raw/IDS_mapping.csv` | Three code tables stacked in one file: admission type, discharge disposition (where the patient went when leaving hospital) and admission source. |

## SHA-256 fingerprints

A fingerprint is a checksum that changes if even one byte of a file changes, so a match proves the files are exactly the expected ones.

```text
0689e7ec031237dc63031b938805c48377748761a3b26acab621567afa24df97  raw/diabetic_data.csv
f1bb82b471cb34649352597572c9b1fb00bd27f77b9f5a22a03dc3eb1039749e  raw/IDS_mapping.csv
```

Check them from the repository folder with `shasum -a 256 data/raw/*.csv` (or `sha256sum`, or PowerShell's `Get-FileHash`).

## Source

- UCI Machine Learning Repository, *Diabetes 130-US Hospitals for Years 1999-2008*: <https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008>
- Downloaded on 2026-11-23 from <https://archive.ics.uci.edu/static/public/296/diabetes+130-us+hospitals+for+years+1999-2008.zip>. Both files are unchanged from that zip file, including their Windows line endings.
- The records come from the Health Facts database (Cerner Corporation): 130 US hospitals and hospital networks, 1999–2008.

## License and credit

CC BY 4.0 (<https://creativecommons.org/licenses/by/4.0/>): free to use and share with credit.

Clore, J., Cios, K., DeShazo, J., & Strack, B. (2014). *Diabetes 130-US Hospitals for Years 1999-2008* [Dataset]. UCI Machine Learning Repository. <https://doi.org/10.24432/C5230J>

## How to load

```python
pd.read_csv("data/raw/diabetic_data.csv", na_values="?", keep_default_na=False, low_memory=False)
```

Only `?` is read as missing. pandas' default settings would also turn the text `None` into missing, but here `None` is a real answer ("test not done") in `max_glu_serum` and `A1Cresult`.

`low_memory=False` makes pandas read the whole file before choosing each column's type, so it does not warn about `payer_code`, whose first 20,445 rows are all missing.
