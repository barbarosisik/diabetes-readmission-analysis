# Working rules

These rules apply to everyone who works on this repository, people and AI assistants alike. Before starting any work, read this file, [docs/plan.md](docs/plan.md) and the latest entry in [docs/LOGBOOK.md](docs/LOGBOOK.md).

## 1. Ask first, keep it simple

- Present every decision to the project owner before acting on it: the options, a recommendation and a one-line reason. Wait for the answer. Never decide alone.
- Always choose the simplest solution: less code, less time, fewer moving parts. Use a more complex approach only when the project owner asks for it.

## 2. Framing

- This repository is an independent scientific analysis of 30-day hospital readmissions in the UCI "Diabetes 130-US hospitals" dataset (1999–2008).
- Describe it that way everywhere: in code, documents, commit messages, the logbook and conversation.
- Use research language. Call it "the analysis", "the project" or "the study", never a "test", "assessment", "assignment", "exercise" or "challenge". (Unit tests are fine.)
- Do not link the project to any company or organization. Naming the data sources is fine: UCI, Cerner's Health Facts database, and the dataset's authors.

## 3. Audience: explain everything plainly

- Audience: a data scientist with no biology or medical training.
- Explain every step, decision and result in the plainest and briefest words possible: what was done, why, and what it means.
- Explain every biological or medical term in one plain sentence the first time it appears, and add it to [docs/GLOSSARY.md](docs/GLOSSARY.md).
- Prefer concrete numbers and short examples to jargon. Do not use an abbreviation without explaining it.

## 4. One branch per step

- `main` contains only confirmed work.
- Do each step in `docs/plan.md` on its own branch. Create it from the latest `main` and name it `step-NN-short-name`, for example `step-02-data-quality`.
- Commit and push only to that step's branch. Never commit or push directly to `main`.
- Merge into `main` only after the project owner explicitly confirms the step. Then start the next step from the updated `main`.

## 5. Commit messages

- Prepare every commit message and show it to the project owner in the chat. Then commit and push it to the step's branch.
- Use this format: a topic line, a blank line, then one bullet per changed file.

  ```text
  <Topic: one short sentence that sums up the whole commit>

  - `path/to/file`: one short sentence on what changed in this file and why.
  - `path/to/other_file`: one short sentence on what changed in this file and why.
  ```

- Keep it brief: list every changed file, with one sentence per bullet.

## 6. Authorship

- The project owner is the only author and committer. Before committing, run:

  ```bash
  git config user.name "Barbaros IŞIK"
  git config user.email "57237644+barbarosisik@users.noreply.github.com"
  git config commit.gpgsign false
  ```

- Never add assistant attribution (co-author lines, session links, "generated with" notes) to commits, pull requests, code or documents.

## 7. Logbook

- [docs/LOGBOOK.md](docs/LOGBOOK.md) is a strict, append-only record. Every working session adds a dated entry with:
  - what was discussed
  - what was decided, and why
  - what was changed, file by file
  - what was found
  - what is planned next
  - any open questions
- Never edit or delete old entries. Put corrections in a new entry that refers to the old one.
- Update the logbook in the same commit as the work it describes.

## 8. Narrative

- `NARRATIVE.md`, at the top level, is a short report of the work. Update it after finishing a piece of work, not after every step. The first version comes after Step 1.
- Keep it short, with a very short overview. Write it in the first person, in plain words.
- Structure:
  1. Title (the project name), then "Barbaros Isik" and the date
  2. Overview
  3. Resources used, and why
  4. One short section per finished part: input → process → decisions and why → output
  5. Limitations
  6. AI tools used: name the tool and what it was used for, with no model identifiers (the project owner adds those)
  7. How to reproduce
- Never use "candidate" or "assessment" wording.

## 9. Data and analysis rules

- Raw data lives in `data/raw/` and is committed unchanged; it is never edited. `data/README.md` records the source, the license credit and the SHA-256 fingerprints.
- Load `diabetic_data.csv` with only `?` treated as missing: `na_values="?", keep_default_na=False`. pandas' default settings would turn the real value `None` ("test not done") into missing.
- Look before changing: list the data-quality problems (Step 2) before removing any row.
- Make every exclusion a named, documented rule, with a row count and a reason.
- Always say what is being counted: hospital stays (encounters) or patients.
- Describe associations; never claim causes.
- Unit tests use small hand-made data frames, never the real file.
- Every reported number must come from a script that can be rerun, never from hand-edited figures.

## 10. When a step is done

- The work meets the step's "done when" list in `docs/plan.md`.
- The tests pass, the logbook entry is written (and the narrative, when a piece of work is finished), and the commit message has been shown to the project owner.
- Once the project owner confirms, merge the branch into `main`.
