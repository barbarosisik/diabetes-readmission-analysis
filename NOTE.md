# Note

**Assumptions**

- One row is one hospital stay. The rate is per stay ("number of encounters"), so a patient with several stays counts several times.
- A 30-day readmission means `readmitted` is `<30`. `>30` and `NO` both count as not readmitted within 30 days.
- The `readmitted` flag is taken as correct. The data have no dates, so it cannot be checked.
- All ten age brackets are kept. The two youngest are small (160 and 690 stays), so their rates are uncertain.

**Excluded, and why**

- 2,423 stays that ended in death (1,652) or hospice (end-of-life) care (771), because those patients cannot come back, or are not expected to. The codes were looked up in `IDS_mapping.csv`. Even so, 43 hospice stays were followed by a readmission within 30 days.
- Kept: 4,680 stays with an unknown discharge destination (we cannot tell whether those patients died) and 3 stays with gender `Unknown/Invalid` (gender is not used).

**Questions for the data owner**

1. If a patient is readmitted exactly 30 days after discharge, which `readmitted` label do they get?
2. Can we get admission and discharge dates?
3. What do discharge codes 18 ("NULL") and 25 ("Not Mapped") mean? Could they hide deaths?
4. The question asks about patients, but the table counts stays, and one patient can have several. Should each patient count only once?
