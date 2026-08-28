# Review and output specification

## Contents

1. Review modes
2. Manual review sequence
3. Sampling rules
4. Evidence contract
5. Required fields
6. Field semantics
7. Workbook layout
8. Summary statistics
9. Reviewer assignment

## 1. Review modes

### Specific Run review

Use when the user provides an SRR/ERR/DRR/CRR. Return a concise decision plus the complete evidence path.

### Random audit

Sample N Runs from each requested original class. Prefer distinct Research IDs. If impossible, prefer distinct samples and disclose the fallback.

### Pending deep review

Attempt full two-way classification. Leave Pending only for a named unresolved high-impact fact after checking available sample and paper Methods.

### Checked/Deleted re-review

Ignore the original label while reading evidence, then compare the independent reviewed class. Report false-positive/false-negative features.

## 2. Manual review sequence

For each Run:

1. Confirm Run ID, Experiment ID, sample IDs, study/project IDs, organism, platform, layout, library fields, and raw availability.
2. Open the sample page and preserve the original title, source, characteristics, treatment, extraction, construction protocol, and database identifiers verbatim before interpretation.
3. Map the current sample to the study's assay branches.
4. Extract `pulse_time`, `chase_time`, `treatment_time`, perturbation time, release/washout, harvest/timepoint, and run-on time separately.
5. Check poly(A)+, 3-prime, small-RNA, chase/stability, contact-ligation, wrong-branch, and non-RNA exclusions.
6. Open paper Methods/supplement when the sample page does not decide the case, conflicts with structured metadata, or cannot establish branch linkage.
7. Record a short exact excerpt from every decisive source, its title, section/location, URL, evidence level, and a Chinese interpretation.
8. Record explicit evidence linking the current Run to the cited assay branch. Never use a study-wide method without this linkage.
9. Apply the rule only after facts and source excerpts have been captured.

Do not merely report `Strategy`, `Source`, and `Selection`; explain what physically selected the RNA.

## 3. Sampling rules

Record:

- random seed;
- audit round;
- source workbook/version;
- original class;
- list of previously sampled Run IDs to exclude.

Sampling priority:

1. unique Research ID;
2. unique Sample ID;
3. unique Run ID.

For multiple rounds, exclude every Run audited earlier. Do not sample two Runs from one study merely because the study has many Runs unless the user requests branch comparison.

## 4. Evidence contract

For every Checked or Deleted Run:

- preserve original database values in dedicated fields; do not silently normalize or replace them;
- quote the decisive source exactly and briefly in its original language; do not paste an entire Methods section;
- identify the source title, section/page/supplement or database-field location, and URL;
- explain in Chinese what the excerpt proves;
- state how the current Run/sample maps to the cited experimental branch;
- store capture, pulse, chase, and exclusion evidence separately when applicable;
- keep `Methods evidence` as a concise synthesis; never use it as a substitute for `Methods exact excerpt`.

The decisive source may be a Run/sample construction protocol, sample metadata, paper Methods, or supplement. If a structured database field alone decides an obvious branch, copy the exact field name and value and label the evidence level accordingly. If no exact evidence can be tied to the current Run, do not classify it as Checked.

A shared Methods excerpt may be reused across biological or technical replicates only when every Run has its own `Run-to-Methods branch evidence`. Never propagate it to another assay branch in the same study.

## 5. Required fields

Use these canonical columns. Chinese labels may be added, but preserve machine-readable names when possible.

### Classification, provenance, and identifiers

```text
Original classification
Final classification
Original source workbook
Original source sheet
Original source row
Atlas Sample ID
Research ID
Source research ID
Sample ID
Source data ID
Experiment ID
Run ID
Source database
Database URL
Sample title
Original source name
Original characteristics
Original treatment protocol
Original extraction protocol
Original construction protocol
Original metadata snapshot/reference
```

### Biological and perturbation metadata

```text
Species
Cell line/Tissue
disease
sex
age
Condition
perturbation_type
perturbation_gene
perturbation_dose
perturbation_time
paired control sample ID
```

### Technology, timing, and library metadata

```text
Search technology
Technology
Confirmed technology
pulse_time
chase_time
treatment_time
release/washout_time
harvest/timepoint
run_on_time
Library Strategy
Library Source
Library Selection
Sequencing platform
Library Layout
File type
Read length
```

### Evidence and decision

```text
Methods evidence
Methods exact excerpt
Methods Chinese interpretation
Methods section/location
Evidence source title
Evidence source URL
Evidence level
Run-to-Methods branch evidence
Capture mechanism evidence
Pulse evidence
Chase evidence
Exclusion evidence
Decision reason
Rule code
Paper/Methods URL
Unresolved question
Sources checked
Next action
```

### Publication, data lifecycle, and audit

```text
Publication
Raw data available
File size
Download link
Data status
Reviewer
Review date
Audit round
Notes
```

Allowed evidence levels:

```text
Run/Sample Methods
Paper Methods
Study metadata
Database structured fields
Title only
```

Checked should normally use Run/Sample Methods or Paper Methods. Lower evidence levels require a clear justification and should usually remain Pending.

## 6. Field semantics

- `Atlas Sample ID`: constructed unique atlas identifier, corresponding to the user table's constructed Sample ID; keep it separate from accessions.
- `Research ID`: normalized grouping key used for reviewer assignment.
- `Source research ID`: exact study/project accession reported by the source database.
- `Sample ID`: source sample accession used by the existing workbook.
- `Source data ID`: exact source sample/data-record identifier; it may equal `Sample ID`.
- `Technology`: canonical label from the approved atlas technology list.
- `Confirmed technology`: assay confirmed for this specific Run after review.
- `perturbation_time`: biological treatment duration. Never substitute it for `pulse_time`.
- `paired control sample ID`: atlas or source sample identifier for the matched control; allow multiple IDs separated consistently.
- `Publication`: DOI and/or PMID; keep the Methods URL separately.
- `Data status`: data-lifecycle state such as added, checked, pending, deleted, downloaded, or processed; do not use it in place of `Final classification`.
- `Original metadata snapshot/reference`: relevant raw JSON/XML/text snapshot or a stable local/source reference. Do not store full HTML when the exact source fields are already preserved.
- `Read length`: preserve the source form such as `PE150`, `2x150`, or exact per-read lengths; do not infer when absent.
- `Methods exact excerpt`: shortest verbatim text that supports the decision. Use ` || ` between separately located excerpts and identify each location.

Fields such as disease, sex, age, dose, paired control, file size, and read length may be blank when genuinely unavailable or not applicable, but their columns must remain present.

## 7. Workbook layout

For a full curation workbook, use:

```text
Summary
Checked_Run
Pending_Run
Deleted_Run
Out-of-scope
NoRun_records
Search_audit
Methods_audit
Rule_change_audit
Time_distribution
```

Minimum presentation rules:

- one record per row;
- use the full Run-level schema on Checked, Pending, and Deleted sheets;
- freeze header and identifier columns;
- filters on every data sheet;
- Run IDs stored as text;
- URLs in dedicated cells;
- no color-only status encoding;
- official totals based on nonempty unique Run IDs;
- source file never overwritten unless requested.

NoRun records must include a separate `Design assessment` and `Data availability` field. Do not place them in official Checked Run totals.

## 8. Summary statistics

Always state the unit:

- unique Run;
- unique Sample ID;
- unique Research ID;
- study or sample time bin.

For metabolic pulse time:

- use sample-specific pulse only;
- exclude treatment, harvest, release, chase, and run-on time;
- report missing/ambiguous separately;
- for >30 min distributions, use 30-minute bins: `(30,60]`, `(60,90]`, `(90,120]`, etc.; document boundary handling.

For audit rounds, report:

| Original class | Reviewed Checked | Reviewed Deleted | Still Pending |
|---|---:|---:|---:|

Then summarize the primary false-positive and false-negative mechanisms by rule code.

## 9. Reviewer assignment

When splitting Checked studies:

1. group by Research ID;
2. choose target study counts differing by at most one;
3. assign large studies greedily to the reviewer with the lowest current Run count while respecting study-count targets;
4. sort each sheet by Research ID, then Run ID;
5. add `Reviewer` and preserve all original and evidence fields;
6. validate no Research ID appears in multiple reviewer sheets.
