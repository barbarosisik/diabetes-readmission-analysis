# Logbook

A strict, append-only record of everything discussed, decided, changed and planned. The newest entry is at the bottom. Old entries are never edited; corrections go in a new entry that refers to the old one. The rules are in [AGENTS.md](AGENTS.md), section 5.

---

## Entry 001 · 2026-11-23 · Session 1: project set-up and first look at the data

**Branch:** `step-00-project-setup`, created from `main`. Not yet merged.

### Discussed

- **The research question:** "What share of patients are readmitted within 30 days, and how does that differ by age group?", using the UCI Diabetes 130-US hospitals dataset (1999–2008).
- **The four tasks:**
  1. List the data-quality problems before changing anything.
  2. Write `readmission_rate_by_age(df)`.
  3. Add 2–3 unit tests on hand-made tables.
  4. Write a note of under half a page on assumptions, exclusions and questions for the data owner.
- **The working rules** (now in `AGENTS.md`):
  - one branch per step, merged into `main` only after confirmation
  - commit messages shown to the project owner first, in a fixed format (a topic line plus one bullet per file)
  - plain explanations, with every medical term explained
  - this logbook
  - consistent framing of the project as an independent scientific analysis

### Done

- Read the official UCI dataset page and the original paper (Strack et al., 2014, *BioMed Research International*).
  - What the paper did: it kept each patient's first stay and removed death and hospice discharges, which left 69,984 stays. It grouped ages into ≤30, 30–60 and >60.
- Downloaded the official zip from UCI into a temporary scratch folder outside the repository. Recorded the SHA-256 fingerprints:
  - `diabetic_data.csv`: `0689e7ec031237dc63031b938805c48377748761a3b26acab621567afa24df97` (101,767 lines including the header)
  - `IDS_mapping.csv`: `f1bb82b471cb34649352597572c9b1fb00bd27f77b9f5a22a03dc3eb1039749e`
- Ran a first look at the data with throw-away code. It was read-only, so no data were changed. The findings are summarised below and in `plan.md`, sections 1–3.
- Tried to create the GitHub repository `barbarosisik/diabetes-readmission-analysis` from this session. GitHub refused, because the connected app is not allowed to create repositories. The repository was built locally instead. It will be pushed once the project owner has created an empty repository on GitHub.
- Created the local git repository:
  - `main` has one bootstrap commit: a minimal `README.md`, so that branches have a starting point.
  - `step-00-project-setup` holds the documents listed below.

### Changed (file by file)

- `README.md`: front page with the research question, status, file guide, data source and citations.
- `PROJECT_BRIEF.md`: the project description for future reference, in neutral wording.
- `plan.md`: overview paragraph, the question unpacked (stays versus patients), the data in plain words, the first-look data-quality list, the step-by-step plan (Steps 0–6), decisions to confirm, draft questions for the data owner, risks and sources.
- `AGENTS.md`: the working rules (framing, plain explanations, branches, commit messages, logbook, data rules, definition of done).
- `CLAUDE.md`: imports `AGENTS.md`, so Claude Code loads the same rules automatically.
- `GLOSSARY.md`: plain-language explanations of medical, hospital, coding and statistics terms.
- `LOGBOOK.md`: started, with this entry.
- `.gitignore`: keeps downloaded data, zip files, Python caches and local editor or assistant settings out of git.

### Found: the first look, to be confirmed by tested code in Step 2

- **Size:** 101,766 stays × 50 columns, from 71,518 patients. `encounter_id` is unique.
- **Missing values:** none of the six analysis columns contains `?`.
- **Loading trap:** pandas' default settings turn the real value `None` ("test not done") into missing, in `max_glu_serum` (96,420 rows) and `A1Cresult` (84,748 rows). The fix is `na_values="?", keep_default_na=False`.
- **Death and hospice:**
  - Death codes 11/19/20/21 cover 1,652 stays, all flagged `NO`.
  - Hospice codes 13/14 cover 771 stays, of which 43 are flagged `<30` and 43 `>30`. Hospice patients can come back.
- **Unknown discharge:** codes 18/25 cover 4,680 stays (4.6%).
- **Gender:** 3 stays are `Unknown/Invalid`, and 3 patients have different genders on different stays.
- **No time order:** there are no dates, and `encounter_id` is not reliably in time order. 13 patients have a stay with a higher ID than the stay in which they died.
- **Repeat patients:** 23.5% of patients have 2 or more stays, and together they account for 46.2% of all stays.
- **Overall 30-day rate:**
  - per stay, after removing death and hospice: 11.4% (99,343 stays)
  - per patient, using the first stay: 9.0% (69,990 patients)
- **Age pattern:**
  - Per stay, the 20–30 group is highest (14.3%).
  - Per patient, the rate rises with age, from about 7% (ages 30–60) to about 10–11% (ages 70–90).
  - The difference comes from a few young patients with repeated emergencies, mainly diabetic ketoacidosis (DKA). The top 1% of 20–30-year-old patients hold 42% of that group's readmissions.
- **Cross-check with the paper:**
  - Rebuilding the paper's sample gives 69,990 stays against the paper's 69,984. The ≤30 and 30–60 groups match exactly (1,808 and 21,871 stays).
  - Rates are within 0.3 percentage points.

### Decided

- **Repository name:** `diabetes-readmission-analysis`, kept private until the project owner chooses otherwise.
- **The brief:** stored as `PROJECT_BRIEF.md` in neutral wording.
- **Raw data:** not committed. A download script with fingerprint checks will fetch it (Step 1).
- **Proposed, waiting for the project owner's confirmation** (`plan.md`, section 6):
  - Python with pandas and pytest.
  - Count per stay, with a per-patient check.
  - Exclude death (codes 11/19/20/21) and hospice (codes 13/14).
  - Keep the unknown discharge codes and the `Unknown/Invalid` gender stays, and report both.
  - Show 95% intervals for small age groups.

### Planned next

1. **Project owner:** create the empty GitHub repository, then read `plan.md` and answer the decisions in section 6.
2. **Then:** push `main` and `step-00-project-setup`, merge Step 0 into `main` after confirmation, and start Step 1 (`step-01-data-loading`).

### Open questions

- The decisions in `plan.md`, section 6.
- Whether commit messages should be approved before each commit, or shown at commit time with the approval given at merge time (the current rule).
