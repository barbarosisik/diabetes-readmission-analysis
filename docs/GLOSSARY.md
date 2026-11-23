# Glossary

Medical, hospital and data terms used in this project, each explained in plain words. New terms are added the first time they appear in the work.

## The body and diabetes

| Term | Plain meaning |
|---|---|
| **Blood sugar (glucose)** | The sugar carried in the blood. It comes from food and is the body's main fuel. |
| **Hormone** | A chemical messenger that the body releases into the blood to tell organs what to do. |
| **Pancreas** | An organ behind the stomach that makes insulin. |
| **Insulin** | A hormone made by the pancreas. It lets the body's cells take sugar out of the blood and use it for energy. Without insulin, sugar builds up in the blood. |
| **Diabetes (diabetes mellitus)** | A long-term condition in which blood sugar stays too high, either because the body makes too little insulin or because it does not respond to insulin properly. |
| **Type 1 diabetes** | The body's own defense (immune) system destroys the insulin-making cells, so the body makes little or no insulin. It usually starts in childhood or young adulthood, and patients need insulin injections for life. |
| **Type 2 diabetes** | The body makes insulin but responds to it poorly, and over time may not make enough. It usually starts in adulthood and is linked to weight and lifestyle. About 90–95% of people with diabetes have type 2. |
| **Diabetic ketoacidosis (DKA)** | A life-threatening emergency, mostly in type 1 diabetes. Without enough insulin, cells cannot use sugar, so the body burns fat instead. That produces acids (ketones) that build up in the blood. It needs hospital treatment and can come back if insulin doses are missed. Its ICD-9 code is `250.1x`. |
| **Glycemic control** | How well blood sugar is kept within a healthy range. |
| **Hemoglobin** | The protein in red blood cells that carries oxygen. Sugar in the blood slowly sticks to it. |
| **HbA1c (A1C), column `A1Cresult`** | A blood test of how much sugar is stuck to hemoglobin. Red blood cells live about 3 months, so it shows the *average* blood sugar over the past ~3 months. A common target is below 7%. In this data: `Norm` (below 7%), `>7` (7–8%), `>8` (above 8%), `None` (not measured). |
| **Serum glucose test, column `max_glu_serum`** | Blood sugar measured at one moment, in mg/dL. In this data: `Norm` (normal), `>200` or `>300` (high), `None` (not measured). |
| **Diabetes medicines (23 columns)** | One column per drug, e.g. `metformin` or `insulin`. `No` = not given, `Steady` = same dose, `Up`/`Down` = dose raised or lowered during the stay. |
| **Metformin** | The most common first tablet for type 2 diabetes. |
| **Sulfonylureas** (`glipizide`, `glyburide`, `glimepiride`, …) | Tablets that make the pancreas release more insulin. |
| **Thiazolidinediones** (`pioglitazone`, `rosiglitazone`, `troglitazone`) | Tablets that make the body more sensitive to insulin. Troglitazone was taken off the US market in 2000, which is why it almost never appears in this data. |
| **Comorbidity** | Another illness a patient has at the same time, e.g. heart disease alongside diabetes. |

## Hospital and care

| Term | Plain meaning |
|---|---|
| **Encounter** | One contact between a patient and the hospital. In this dataset, one encounter = one inpatient stay = one row. |
| **Inpatient** | A patient formally admitted to a hospital bed, usually for at least one night. |
| **Outpatient visit** | A visit to a clinic or doctor without staying in hospital (column `number_outpatient`: such visits in the year before the stay). |
| **Emergency visit** | A visit to the emergency department (column `number_emergency`: such visits in the year before the stay). |
| **Admission** | Formally taking a patient into hospital as an inpatient. |
| **Admission type** | How urgent the admission was. *Emergency* = needed immediately; *urgent* = needed soon; *elective* = planned in advance, e.g. a scheduled operation; *newborn*; *trauma center* = a unit for serious injuries. |
| **Admission source** | Where the patient came from, e.g. the emergency room, a doctor's referral or another hospital. |
| **Discharge** | Leaving hospital at the end of a stay. |
| **Discharge disposition** | Where the patient went at discharge: home, home with nursing help, a care home, another hospital, hospice, or the patient died ("expired"). |
| **Length of stay (`time_in_hospital`)** | Number of days between admission and discharge; 1–14 in this dataset. |
| **Readmission** | Being admitted to hospital again after a discharge. |
| **30-day readmission** | A readmission within 30 days of discharge. It is a standard measure of care quality, because many of these returns are avoidable. |
| **Index stay (index admission)** | The stay from which the 30 days are counted. |
| **Hospital Readmissions Reduction Program (HRRP)** | A US program, started in 2012, that cuts payments to hospitals with more 30-day readmissions than expected. It is why hospital managers care about this number. (Our data, 1999–2008, are from before it existed.) |
| **Expired** | Hospital wording for "the patient died". Codes 11, 19, 20 and 21. |
| **Hospice** | Care for people expected to live only a few months, aimed at comfort rather than cure, given at home (code 13) or in a facility (code 14). Patients rarely return to hospital, but they can leave hospice and come back. |
| **SNF (skilled nursing facility)** | A care home with nurses and therapists, often used to recover after a hospital stay (code 3). |
| **ICF (intermediate care facility)** | A care home for people who need some nursing, but less than in an SNF (code 4). |
| **Home health service** | Nurses or therapists who visit the patient at home (code 6). |
| **IV (intravenous)** | Into a vein, through a drip. "Home IV provider" (code 8) = a service that gives drip medicines at home. |
| **Left AMA (against medical advice)** | The patient chose to leave before the doctors said it was safe (code 7). |
| **Swing bed** | A bed in a (usually small, rural) hospital that can switch between hospital care and nursing-home care (code 15). |
| **Rehab (rehabilitation) facility** | A place to regain strength and skills after illness or surgery (code 22). |
| **Long-term care hospital** | A hospital for patients who need hospital-level care for a long time (code 23). |
| **Critical access hospital (CAH)** | A small rural US hospital with a special government status (code 29). |
| **Neonate / newborn** | A baby in its first 4 weeks of life. |
| **Medical specialty** | The field of the doctor who admitted the patient, e.g. *InternalMedicine* (general adult medicine), *Cardiology* (heart), *Nephrology* (kidneys), *Orthopedics* (bones and joints), *Endocrinology* (hormones, including diabetes), *Pediatrics* (children). |
| **Lab procedure** | A laboratory test, usually on blood or urine (column `num_lab_procedures`). |
| **Procedure** | A medical action other than a lab test, e.g. a scan or an operation (column `num_procedures`). |
| **Diagnosis** | The doctor's conclusion about what illness or condition the patient has. |
| **Payer** | Whoever pays the hospital bill: an insurer, a government program or the patient (column `payer_code`). |
| **Medicare / Medicaid** | US public health insurance. Medicare is mainly for people aged 65 and over (code `MC`); Medicaid is for people with low incomes (code `MD`). |
| **Integrated delivery network** | A group of hospitals, clinics and doctors run as one organization. |

## Data and coding

| Term | Plain meaning |
|---|---|
| **EHR (electronic health record)** | The digital patient record kept by a hospital. |
| **Health Facts database (Cerner)** | A large US collection of EHR data from hospitals that use Cerner's software (Cerner is now part of Oracle). It is the source of this dataset. |
| **De-identified data** | Data with names and personal details removed; the IDs are scrambled numbers. |
| **ICD-9 code (`diag_1`, `diag_2`, `diag_3`)** | A code from the *International Classification of Diseases, 9th revision*, used in the US until 2015. Examples: `250.xx` diabetes, `428` heart failure, `410` heart attack, `486` pneumonia. Codes starting with `V` describe circumstances (e.g. a check-up); codes starting with `E` describe external causes of injury (e.g. a fall). |
| **Primary diagnosis (`diag_1`)** | The main reason for the stay. `diag_2` and `diag_3` are other conditions recorded during it. |
| **Age bracket notation `[70-80)`** | A square bracket means "included" and a round bracket means "excluded", so `[70-80)` means 70 ≤ age < 80. |

## Statistics (less common terms only)

| Term | Plain meaning |
|---|---|
| **95% confidence interval (Wilson)** | A range that likely contains the true rate. The Wilson version behaves well for small groups and rates near zero, where the simple "± 1.96 × standard error" formula fails. |
| **Sensitivity analysis** | Re-running the analysis with a different reasonable choice, to check whether the conclusion changes. |
