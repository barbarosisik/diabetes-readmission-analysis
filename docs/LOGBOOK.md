# Logbook

A strict, append-only record of everything discussed, decided, changed and planned. The newest entry is at the bottom. Old entries are never edited; corrections go in a new entry that refers to the old one. The rules are in the "Logbook" section of [AGENTS.md](../AGENTS.md).

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

---

## Entry 002 · 2026-11-23 · Session 2: general decisions, new working rules and authorship

**Branch:** `step-00-project-setup`. Not yet merged.

### Discussed

- The project owner created the GitHub repository, and `main` and `step-00-project-setup` were pushed to it.
- Eleven general decisions (tools, shape of the work, way of working) were presented, each with options and a recommendation.
- The project owner asked for four new working rules:
  - always present decisions before acting on them
  - always choose the simplest solution
  - the project owner is the only author
  - keep a narrative document of the work
- The narrative document is modelled on an earlier report by the project owner: overview, resources and why, one section per step, limitations, tools used, how to reproduce.

### Decided

- **1A:** Python, pandas and pytest.
- **2A:** `requirements.txt` with exact versions, plus Python's built-in `venv`.
- **3A:** type hints, short docstrings, `ruff`, and an automatic test run on every push, all kept simple. The unit tests themselves will be discussed before any are written.
- **4:** code modules with Markdown reports, and also a notebook. The exact form is to be confirmed.
- **5B:** commit the two raw CSV files to the repository. Their licence (CC BY 4.0) allows this with credit.
- **6A:** strictly the four tasks. Extras only if time is left, and only after approval. Never a predictive model.
- **7A:** commit generated outputs, marked as generated.
- **8:** folder structure to be confirmed. The project owner prefers subfolders.
- **9B:** the function and its unit tests form one step, giving six steps in total.
  - **Reason:** a function and the tests that prove it belong together. Reviewing them as one unit shows both what the code does and the evidence that it is correct. The tests also work as a precise description of the expected behaviour.
- **10A:** each commit message is shown first, then committed and pushed to the step branch. The project owner's approval comes before merging into `main`.
- **11A:** one pull request per step, merged with a merge commit.

### Changed

- **History:** re-authored the two existing commits so that the project owner is the only author and committer, removed extra trailer lines from their messages, and force-pushed both branches. GitHub now attributes both commits to the project owner's account.
- **Git settings:** set the repository's local git identity to the project owner and turned commit signing off.
- `AGENTS.md`:
  - new sections "Ask first, keep it simple", "Authorship" and "Narrative"
  - the data rule now says the raw data are committed unchanged
  - sections renumbered
- `LOGBOOK.md`: this entry; the header now refers to the "Logbook" section by name.

### Found

- After the history rewrite, GitHub's Contributors box on the repository page still showed the previous author. It is a stored summary that GitHub did not rebuild, even after the default branch was switched away and back.

### Planned next

1. The project owner deletes and re-creates the GitHub repository (empty, same name). Both branches are then pushed again from the clean local copy, and the Contributors box is checked.
2. The project owner answers the open questions below.
3. Update `plan.md` and the other documents with all decisions, create the narrative document, and record this in the next logbook entry.

### Open questions

1. **Folder structure (decision 8):** subfolders (`docs/`, `data/`, `notebooks/`, `src/`, `tests/`, `reports/`), or everything at the top level?
2. **Notebook (decision 4):** one notebook that walks through the analysis by calling the same functions?
3. **Data (decision 5B):** drop the download script and commit the CSV files with a `data/README.md`?
4. **Scope (decision 6A):** move the 95% intervals, per-patient check, paper cross-check and chart to a "maybe later" list?
5. **Spelling:** American English throughout?
6. **Tool mentions:** keep `CLAUDE.md` and make the other mentions of tooling neutral, or remove them all?
7. **Narrative:** file name, structure, format and the tools section.

---

## Entry 003 · 2026-11-23 · Session 3, part 1: Step 0 finished

**Branch:** `step-00-project-setup`. Not yet merged.

### Discussed

- The GitHub repository was deleted and re-created (empty, same name), because GitHub's Contributors box kept showing a previous author after the history rewrite in entry 002. Both branches were then pushed again from the clean local copy.
- The open questions from entry 002 were answered (below).
- The plan for brief task 1 (how to load the data and which checks to run) was presented and agreed.

### Decided

- **Answers to entry 002's open questions:**
  1. **Folder structure:** subfolders. `README.md`, `NOTE.md`, `NARRATIVE.md`, `AGENTS.md`, `CLAUDE.md` and `requirements.txt` at the top level; `data/` (README plus `raw/`), `docs/` (brief, plan, logbook, glossary), `notebooks/`, `src/`, `tests/` and `reports/`.
  2. **Notebook:** one notebook, `notebooks/analysis.ipynb`, holds the whole analysis. Two points stay open until Step 3: whether the function lives in one small `.py` file in `src/` that the notebook imports (recommended, so pytest can import it), and whether `reports/` is still needed.
  3. **Data:** the two CSV files are committed unchanged to `data/raw/`, with `data/README.md` (source, CC BY 4.0 credit, SHA-256 fingerprints). No download script. This happens in Step 1.
  4. **Scope:** only what the brief asks. No 95% intervals, no per-patient check, no cross-check with the paper, no chart and no "maybe later" list.
  5. **Spelling:** American English everywhere, except old logbook entries, which are append-only.
  6. **Tool mentions:** `CLAUDE.md` and every mention of AI tooling stay exactly as they are. AI assistance is allowed.
  7. **Narrative:** `NARRATIVE.md` at the top level, short, written after finishing a piece of work rather than after every step. The first version comes after Step 1. Its structure is in `AGENTS.md`, section 8.
- **Steps:** five steps (0–4) replace the six of entry 002. Decision 9B still holds: the function and its unit tests form one step, because a function and the tests that prove it belong together. Reviewing them as one unit shows both what the code does and the evidence that it is correct, and the tests describe the expected behavior precisely.
- **Brief task 1:**
  - Load with `pd.read_csv(path, na_values="?", keep_default_na=False)`, so `?` becomes missing and the real value `None` stays a value.
  - Six read-only checks, listed under Step 2 in `docs/plan.md`.
  - `age`, `gender` and `readmitted` are checked with `value_counts(dropna=False)` and a list of allowed values, so missing and unexpected labels are both flagged (the project owner's suggestion).
  - The problem list is a small table built by code (option A), because `AGENTS.md` requires every reported number to come from code, never typed by hand.
- **Raw data:** committed in Step 1, as planned.

### Changed (file by file)

- `docs/PROJECT_BRIEF.md`, `docs/plan.md`, `docs/LOGBOOK.md`, `docs/GLOSSARY.md`: moved from the top level into `docs/` with `git mv`, so their history is kept.
- `docs/plan.md`: rewritten from section 4 on (scope and decisions, five steps, folder structure). Sections 1–3 are kept; the per-patient check, the 95% intervals and the mapping-file parser are no longer planned work.
- `AGENTS.md`: new narrative rule (section 8), the 95%-interval line removed, paths updated to `docs/`, American spelling.
- `README.md`: paths updated, status set to "Step 0 of 4", the data section now says the CSV files are committed in Step 1, American spelling.
- `docs/PROJECT_BRIEF.md`, `docs/GLOSSARY.md`: American spelling.
- `docs/LOGBOOK.md`: header link updated; this entry.

### Found

- On this machine, the official UCI zip was downloaded again. Both SHA-256 fingerprints match entry 001. The two files sit in `data/raw/`, still ignored by git until Step 1.
- In `IDS_mapping.csv`, the discharge table is on lines 11–41, so `skiprows=10, nrows=30` reads exactly that table. Its labels that contain commas are quoted. pandas' default settings would turn code 18's label `NULL` into missing, so the mapping file is also read with `keep_default_na=False`.
- Every line of both CSV files ends with a Windows line ending, which confirms problem 18 in `docs/plan.md`.

### Planned next

1. **Step 1** (`step-01-data-loading`): commit the data with `data/README.md`, add `requirements.txt`, the loading section of the notebook and the first `NARRATIVE.md`.
2. **Step 2** (`step-02-data-quality`): the task 1 checks and the problem list.

### Open questions

- Step 3: the code layout (`src/` file) and whether `reports/` is needed.
- Step 3: the analysis choices (counting unit, exclusions, gender, small age groups).

---

## Entry 004 · 2026-11-23 · Session 3, part 2: Step 1, data and loading

**Branch:** `step-01-data-loading`, created from `step-00-project-setup` because Step 0 was not merged yet. Merge Step 0 first; this pull request then shows only the Step 1 changes. Not yet merged.

### Discussed

- The project owner asked to start brief task 1 and to put everything where it was planned.

### Decided

- The raw data are committed on this branch, as planned for Step 1.
- `requirements.txt` pins only the two packages the work needs: pandas and Jupyter.
- `low_memory=False` is added to the loading line, to remove a mixed-type warning (see Found). The rule itself is unchanged: only `?` is read as missing.

### Changed (file by file)

- `data/raw/diabetic_data.csv`, `data/raw/IDS_mapping.csv`: the raw data, committed unchanged from the UCI zip file.
- `data/README.md`: source, CC BY 4.0 credit, SHA-256 fingerprints and how to load the files.
- `.gitignore`: no longer ignores `data/raw/` and `*.zip`.
- `requirements.txt`: pandas 3.1.1 and Jupyter 1.1.1, with exact versions.
- `notebooks/analysis.ipynb`: new notebook with the title, the question and section 1, "Load the data".
- `NARRATIVE.md`: first version, covering the set-up, the data and the loading.
- `README.md`: status "Step 1 of 4", file guide, data section and how to run.
- `docs/LOGBOOK.md`: this entry.

### Found

- The notebook loads 101,766 rows × 50 columns. `None` survives in `A1Cresult` as a real value (84,748 rows).
- `payer_code` is missing in the first 20,445 rows. pandas reads large files in chunks and guessed a different type for that first chunk, so it warned about mixed types. With `low_memory=False` it reads the whole file first; the warning is gone and the column is text.

### Planned next

- Step 2 (`step-02-data-quality`): the task 1 checks and the problem list in the notebook.

### Open questions

- None new. The Step 3 questions in entry 003 remain.

---

## Entry 005 · 2026-11-23 · Session 3, part 3: Step 2, the data-quality list (brief task 1)

**Branch:** `step-02-data-quality`, created from `step-01-data-loading` because Steps 0 and 1 were not merged yet. Merge Steps 0 and 1 first; this pull request then shows only the Step 2 changes. Not yet merged.

### Discussed

- Brief task 1: run the agreed checks and write the list of problems into the notebook, before changing anything.

### Decided

- Nothing new. The checks and the list follow the plan agreed in entry 003.
- One small display choice: from section 2.5 on, the notebook shows full text labels, because pandas cuts labels longer than 50 characters.

### Changed (file by file)

- `notebooks/analysis.ipynb`: new section 2 with the six read-only checks (2.1–2.6) and the problem list built by code (2.7).
- `NARRATIVE.md`: new part on the data-quality problems; overview, limitations and the AI tools line updated.
- `README.md`: status "Step 2 of 4".
- `docs/LOGBOOK.md`: this entry.

### Found

All counts come from the notebook and confirm the first look in `docs/plan.md`, section 3.

- 101,766 stays × 50 columns, no date column. `encounter_id` is unique.
- `?` appears in 7 columns (`weight` 96.9% missing), but in none of the six analysis columns.
- 71,518 patients; 16,773 of them (23.5%) have 2 or more stays, together 47,021 stays. One patient has 40.
- `age` holds exactly the ten brackets; `[0-10)` has 161 stays and `[10-20)` 691. `readmitted` holds only `NO`, `>30` and `<30`. `gender` has 3 `Unknown/Invalid` stays.
- Every discharge code in the data appears in the mapping file. Death codes cover 1,652 stays, all flagged `NO`. Hospice codes cover 771 stays; 86 of them were followed by a readmission, 43 within 30 days. Unknown codes (18, 25, 26) cover 4,680 stays.
- The first-look counts in `docs/plan.md` for the age brackets (160 and 690) were taken after removing death and hospice stays; the raw counts are 161 and 691.

### Planned next

- Step 3 (`step-03-readmission-function`): first the open questions (code layout, `reports/`, and the analysis choices), then agree on the unit tests, then write the function and the tests.

### Open questions

- The Step 3 questions listed in entry 003.
