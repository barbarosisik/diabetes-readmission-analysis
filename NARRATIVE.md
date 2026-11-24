# Hartwig Assessment: Diabetes Readmission Analysis

Barbaros Isik · 24 November 2026

## Overview

A hospital manager asks: *"What share of patients are readmitted within 30 days, and how does that differ by age group?"* To answer it, I used the public UCI dataset: 101,766 hospital stays of patients with diabetes, from 130 US hospitals between 1999 and 2008.

**Answer:** 11.4% of hospital stays are followed by another admission within 30 days, roughly one in nine. By age, the rate is lowest under 20 (1.9% at ages 0–10 and 5.8% at 10–20) and highest at 20–30 (14.3%). All the other age groups are close to each other, between 9.8% and 12.6%.

The numbers are in [the notebook](notebooks/analysis.ipynb).

## Resources used, and why

- **The UCI dataset** named in the brief, and **the paper its authors published with it** (Strack et al., 2014). I read the paper to understand how the data were collected and how the authors handled stays that ended in death or hospice care.
- **Python, pandas, Jupyter and pytest.** I worked in Python with pandas, kept the whole analysis in one Jupyter notebook that reads from top to bottom, and used pytest for the unit tests.

## Part 1: data and loading

I load the main file with a single line:

```python
pd.read_csv(path, na_values="?", keep_default_na=False, low_memory=False)
```

I chose not to do it the usual way (pandas' default settings, then replacing `?`), because current pandas also reads the word `None` as missing. In this file, `None` means "test not done", and it appears in 84,748 A1C results (A1C is a blood test of average blood sugar). Reading only `?` as missing keeps those answers intact. `low_memory=False` simply makes pandas read each column in full before choosing its type, which avoids a mixed-type warning.

## Part 2: data-quality problems (briefs task 1)

Before changing anything, I looked at the data with six checks that only read it: the size and column types, the missing values, whether rows are stays or patients, whether `age`, `gender` and `readmitted` hold only the expected values, what the discharge codes mean, and whether patients with those codes come back. Everything they found is collected in a table of eight problems. For each problem, the table shows how many rows it affects and whether it matters for the readmission question. For example, 3 stays have an unknown gender, which does not matter here because the table does not use gender; but 1,652 stays ended in death, which matters a lot, because those patients cannot be readmitted.

One choice here deserves attention. The death and hospice discharge codes could simply have been typed in (`[11, 19, 20, 21]` and `[13, 14]`). But a list typed by hand can be wrong without anyone noticing: the labels of codes 19, 20 and 21 also contain the word "hospice", although those patients died, so a death code can easily end up in the hospice list. So I let the code read them from the mapping file by their labels ("Expired" and "Hospice").

## Part 3: the function and its tests (brief tasks 2–3)

The function `readmission_rate_by_age(df)` lives in its own file, [src/readmission.py](src/readmission.py), so the notebook and the unit tests use exactly the same code. It is deliberately small, just three chained steps: it marks each stay as readmitted within 30 days (`<30`) or not, groups the stays by age bracket, and then counts the stays and takes the share that were marked. I tried a few longer versions as well; they all gave exactly the same table, so I kept the shortest one.

Two unit tests run the function on small hand-made tables where the right answer is known in advance. The first checks the counts and rates, including the rule that `>30` and `NO` count as stays but not as readmissions within 30 days. The second checks that the age brackets come out in age order. To make sure the tests would really catch a mistake in these rules, I broke each rule on purpose and checked that the matching test failed. `pytest` reports 2 passed.

## Part 4: results and the note (briefs task 4)

In the notebook, I first removed the 2,423 stays that ended in death (1,652) or in hospice care (771). Then I ran the function on the remaining 99,343 stays. Three choices in this step had a reasonable alternative, so here is why I went the way I did:

- **Stays, not patients.** The manager asks about "patients", but the brief's function asks for the "number of encounters", so I counted stays as; a patient with three stays counts three times. Counting each patient once would follow the manager's wording more closely, and the datasets authors paper did exactly that, keeping each patient's first stay because its statistical model needed independent rows. I could not do the same reliably: the data have no dates, so there is no way to tell which of a patient's stays came first.
- **Hospice stays are excluded,** even though 43 of them were followed by a readmission within 30 days. The brief lists these patients among those who "could never be readmitted", and the original paper removed them too, so I followed both and mention the 43 in the note.
- **The 4,680 stays with an unknown destination are kept.** Removing them would have been the cautious choice, since some of them might hide deaths. But section 2.6 of the notebook shows that many of these stays were followed by a readmission, so those patients were clearly alive, and for the rest there is no way to tell. Removing them all would also remove many ordinary stays.

## Limitations

- There are no dates, so I cannot check the order of a patient's stays or the 30-day window itself. The `readmitted` flag was computed by the dataset's authors from the full hospital records, so I have to trust it.
- Readmissions to hospitals outside the 130 are not recorded, so the true rates are probably somewhat higher.
- Counting stays gives patients with many stays more weight, and the two youngest age groups are small (160 and 690 stays), so their rates are less certain.
- The table shows associations, not causes: it does not say that age itself makes people come back.

Since this was a one-time analysis, I wrote the checks out in the notebook. If this data arrived every month, I would turn the same rules into a data contract (a set of automatic checks), so the pipeline stops as soon as the data change.

## AI tools used

- **Claude Code Opus 5.5 and ChatGPT Sol 6.2** , Opus 5.5 as my pair programmer: it proposed options, drafted code and text from my instructions, and helped check the data and prepare commit messages. I directed the work, made every decision and reviewed every line before it was merged. Sol 6.2 as the research critic: Starting with Opus 5.5, I discussed and exchanged ideas to determine all the task approaches I had provided; then, by giving Sol 6.2 a new, context-free prompt, I tried to find easier ways and made changes accordingly.

## How to reproduce

```bash
git clone https://github.com/barbarosisik/diabetes-readmission-analysis.git
cd diabetes-readmission-analysis
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
jupyter nbconvert --to notebook --execute --inplace notebooks/analysis.ipynb
pytest
```
