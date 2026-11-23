# Working rules

These rules apply to everyone who works on this repository, people and AI assistants alike. Before starting any work, read this file, [plan.md](plan.md) and the latest entry in [LOGBOOK.md](LOGBOOK.md).

## 1. Framing

- This repository is an independent scientific analysis of 30-day hospital readmissions in the UCI "Diabetes 130-US hospitals" dataset (1999–2008).
- Describe it that way everywhere: in code, documents, commit messages, the logbook and conversation.
- Use research language. Call it "the analysis", "the project" or "the study", never a "test", "assessment", "assignment", "exercise" or "challenge". (Unit tests are fine.)
- Do not link the project to any company or organisation. Naming the data sources is fine: UCI, Cerner's Health Facts database, and the dataset's authors.

## 2. Audience: explain everything plainly

- Audience: a data scientist with no biology or medical training.
- Explain every step, decision and result in the plainest and briefest words possible: what was done, why, and what it means.
- Explain every biological or medical term in one plain sentence the first time it appears, and add it to [GLOSSARY.md](GLOSSARY.md).
- Prefer concrete numbers and short examples to jargon. Do not use an abbreviation without explaining it.

## 3. One branch per step

- `main` contains only confirmed work.
- Do each step in `plan.md` on its own branch. Create it from the latest `main` and name it `step-NN-short-name`, for example `step-02-data-quality-audit`.
- Commit and push only to that step's branch. Never commit or push directly to `main`.
- Merge into `main` only after the project owner explicitly confirms the step. Then start the next step from the updated `main`.

## 4. Commit messages

- Prepare every commit message and show it to the project owner in the chat. Then commit and push it to the step's branch.
- Use this format: a topic line, a blank line, then one bullet per changed file.

  ```text
  <Topic: one short sentence that sums up the whole commit>

  - `path/to/file`: one short sentence on what changed in this file and why.
  - `path/to/other_file`: one short sentence on what changed in this file and why.
  ```

- Keep it brief: list every changed file, with one sentence per bullet.

## 5. Logbook

- [LOGBOOK.md](LOGBOOK.md) is a strict, append-only record. Every working session adds a dated entry with:
  - what was discussed
  - what was decided, and why
  - what was changed, file by file
  - what was found
  - what is planned next
  - any open questions
- Never edit or delete old entries. Put corrections in a new entry that refers to the old one.
- Update the logbook in the same commit as the work it describes.

## 6. Data and analysis rules

- Raw data lives in `data/raw/`. It is never edited and never committed. A script downloads it and checks it against recorded fingerprints (SHA-256).
- Load `diabetic_data.csv` with only `?` treated as missing: `na_values="?", keep_default_na=False`. pandas' default settings would turn the real value `None` ("test not done") into missing.
- Look before changing: list the data-quality problems (Step 2) before removing any row.
- Make every exclusion a named, documented rule, with a row count and a reason.
- Always say what is being counted: hospital stays (encounters) or patients.
- Report uncertainty (95% intervals) for small groups. Describe associations; never claim causes.
- Unit tests use small hand-made data frames, never the real file.
- Every reported number must come from a script that can be rerun, never from hand-edited figures.

## 7. When a step is done

- The work meets the step's "done when" list in `plan.md`.
- The tests pass, the logbook entry is written, and the commit message has been shown to the project owner.
- Once the project owner confirms, merge the branch into `main`.
