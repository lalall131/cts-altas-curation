---
name: cts-atlas-nascent-rna-curation
description: Search, curate, classify, audit, and merge public nascent-RNA sequencing Runs for a co-transcriptional splicing atlas. Use for GEO/SRA/ENA/ENCODE/NGDC searches, technology-name and alias expansion, Run-level Checked/Pending/Deleted decisions, metabolic-label pulse review, ChAR/chromatin-RNA disambiguation, random or full Methods re-review of existing Excel results, false-positive/false-negative analysis, deduplication, reviewer assignment by Research ID, and structured Excel evidence tables.
---

# CTS-Atlas nascent-RNA curation

## Objective

Curate public **Run-level raw sequencing data that capture RNA while transcription is ongoing or before transcript maturation**, for building a co-transcriptional splicing atlas. Require evidence at the current sample/experiment branch; never infer every Run from a study title or from another assay in the same study.

Keep two questions separate:

1. **Biological fit:** does this Run capture nascent, Pol II-associated, run-on, short-pulse newly synthesized, or appropriate chromatin-associated RNA?
2. **Data availability:** is a public raw Run ID available and downloadable?

Only records with a nonempty public Run ID enter official Checked/Pending/Deleted Run counts. Preserve design-compatible records without a Run in a separate no-Run table.

## Load the right knowledge

- Read [references/search-strategy.md](references/search-strategy.md) before a new or expanded database search.
- Read [references/technology-registry.md](references/technology-registry.md) when generating technology aliases or judging assay variants.
- Read [references/decision-rules.md](references/decision-rules.md) for every classification, time interpretation, or false-positive/false-negative investigation.
- Read [references/review-output.md](references/review-output.md) before sampling, Methods re-review, Excel creation, merging, or reviewer assignment.

Do not load every reference for a narrow identifier question.

## Select the workflow

### New search or search expansion

1. Confirm the current screening-standard file and the explicitly allowed technology list. Treat that file and the user's latest exclusions as authoritative.
2. Generate database-appropriate searches from core concepts plus allowed technology names, full names, aliases, spelling, hyphen, and legacy variants.
3. Run query families separately when database syntax, query length, or field behavior differs; union their results afterward. “Independent queries” still means an OR-union candidate set.
4. Normalize identifiers and deduplicate **before** Methods review:
   - study/project level for paper and Methods retrieval;
   - Run ID level for the final dataset.
5. Screen study branches, then inspect every candidate Run/sample using the evidence hierarchy.
6. Deep-read paper Methods or supplements only when sample metadata is insufficient, conflicting, or high-risk.
7. Classify and export using the required evidence fields and reason codes.

### Re-review existing Checked, Pending, or Deleted data

1. Read the workbook structure without changing the source file.
2. Sample by **Run**, while preferring different Research IDs; exclude previously audited Runs. Record the random seed and audit round.
3. For each Run, open the Run page, sample page, study page, and—when necessary—the paper Methods/supplement.
4. Reconstruct the current Run's exact assay branch. Do not accept the original label as evidence.
5. Preserve the current Run's original database fields before interpretation. Return the original class, reviewed class, exact decisive Methods/metadata excerpt, source location, Run-to-Methods branch linkage, rule code, and a concise reason.
6. Summarize the confusion matrix and recurring false-positive/false-negative mechanisms.

For Pending review, continue until a decisive source is found or the missing fact is genuinely irrecoverable. Pending is not a holding area for unprocessed records.

### Merge or update results

1. Use Run ID as the final unique key.
2. Apply newer, deeper Run-level review over older automated classification.
3. Preserve an audit sheet with original class, new class, rule code, reason, source, reviewer, and date.
4. Reconcile class totals, unique Runs, no-Run records, and out-of-scope records.
5. Never overwrite the user's prior version unless explicitly requested.

### Divide work among reviewers

1. Group all Runs by Research ID.
2. Never split one Research ID across reviewers.
3. Balance study counts first; within equal study-count constraints, minimize Run-count imbalance.
4. Validate that every Research ID and Run appears once.

## Classification contract

### Checked

Require all of the following:

- a public nonempty Run ID;
- sample/Run-specific evidence for an accepted positive capture route;
- the current Run is the relevant assay branch;
- no hard exclusion;
- a short exact excerpt from the decisive sample/Methods source, its location and URL;
- explicit evidence tying that source and assay branch to the current Run;
- a recorded Chinese interpretation, rule code, and reason.

Accepted positive routes are defined in `decision-rules.md`: direct run-on/Pol II capture, valid short metabolic pulse, valid chromatin fraction RNA, or direct long-read nascent capture.

### Deleted

Use when decisive evidence shows an incompatible branch, including poly(A)+ mature RNA, ordinary RNA-seq without nascent enrichment, 3′/small-RNA assays, chase/stability designs, excessive metabolic pulse, formal RNA–DNA contact mapping, wrong single-cell scope, non-RNA assays, or a same-study wrong branch.

Record one primary exclusion reason code. Add secondary reasons only when useful.
Record the exact decisive sample/Methods/structured-metadata excerpt, source location, and current-Run branch linkage. Do not delete from a paraphrase alone.

### Pending

Use only after reasonable evidence retrieval when a high-impact fact remains unresolved. Record:

- the exact unresolved question;
- sources already checked;
- why study-level evidence cannot be propagated to this Run;
- next action, or `evidence exhausted`.

If title, sample Methods, paper Methods, or library preparation already decides the case, do not leave it Pending.

### Out-of-scope and no-Run

- Use Out-of-scope for aggregators, reprocessing compendia, excluded search scopes, or non-original collections that should not be expanded into candidate Runs.
- Place records without SRR/ERR/DRR/CRR in a separate no-Run table. Store a design assessment, but do not count them as Checked Runs or download targets.

## Evidence discipline

Use this order:

1. current Run/sample Methods and construction protocol;
2. paper Methods or supplement tied to the sample branch;
3. study design and branch map;
4. structured library fields;
5. title and keywords.

Structured fields such as `RNA-Seq`, `OTHER`, `cDNA`, or `other` are weak evidence. A technology name is a retrieval clue, not proof. Conversely, `total RNA` can describe the extraction input of a valid TT-seq protocol; interpret the whole method rather than deleting on one phrase.

## Time rule

Apply the **≤30 min threshold only to the actual in vivo RNA-label incorporation pulse** for metabolic-label assays.

- Do not substitute drug treatment, infection, protein depletion, washout/release, harvest, or timepoint duration for pulse time.
- Treat chase separately. A positive chase means labeled RNA has aged; exclude immediate-nascent use unless the standard explicitly changes.
- Do not apply the 30 min metabolic threshold to nuclear run-on reaction duration.
- Resolve multiple listed times to the current sample. Never copy a study-wide list such as `5; 30; 60 min` into every Run.

## Search-stage versus downstream QC

Do not filter candidates at search stage by gene-body coverage, junction coverage, read length, depth, or file size. Preserve those as downstream suitability/QC fields. Large Runs requiring SRA Toolkit receive the same biological classification as small Runs.

## Required review output

For every reviewed Run, preserve the union of the source-record fields, atlas sample fields, experiment fields, evidence fields, decision fields, and audit fields defined in `review-output.md`. At minimum:

- atlas/sample/source Research IDs, Experiment ID, Run ID, database, species, cell line/tissue, disease, sex, age, condition, perturbation and paired-control fields;
- search technology, canonical technology, sample-confirmed technology, sample title;
- `pulse_time`, `chase_time`, `treatment_time`, perturbation time, release/washout, harvest/timepoint, and `run_on_time` as separate fields;
- Library Strategy, Source, Selection, platform, layout, file type, and read length;
- original source name, characteristics, treatment, extraction, construction protocol, and original metadata reference;
- exact decisive Methods excerpt, source title, section/location, source URL, Chinese interpretation, evidence level, and Run-to-Methods branch evidence;
- original classification, reviewed classification, rule code, decision reason;
- unresolved question and next action for Pending;
- publication, raw-data availability, data status, download link, reviewer, review date, audit round, and notes.

Use the full schema and workbook layout in `review-output.md`.

## Quality gates

Before reporting completion:

- confirm unique nonempty Run IDs and reconcile class totals;
- confirm one Research ID is not split across reviewers;
- confirm Checked rows have positive evidence and no hard exclusion;
- confirm every Checked or Deleted row has a short exact decisive excerpt, source location, source URL, Chinese interpretation, and explicit current-Run branch linkage;
- confirm original metadata fields are preserved verbatim and are not overwritten by interpretations;
- confirm metabolic Checked rows have resolved pulse time ≤30 min and no positive chase;
- confirm Pending rows state a genuine unresolved fact;
- confirm Deleted rows contain a reproducible reason code;
- confirm file size/download method did not affect classification;
- scan a random audit set after any automated reclassification;
- distinguish prompt/rule version from implementation version; if results disagree with the written rules, fix the implementation before processing the full dataset.

For CSV exports, run:

```powershell
python scripts/validate_run_review_csv.py path\to\run_review.csv
```

Treat validation errors as blockers. Review warnings before final delivery.

## Communication

Lead with counts and decision outcomes. State the counting unit explicitly: Run, unique sample, or unique Research ID. Distinguish structured-field statistics from text-derived cell-line/tissue inference. Cite database and Methods pages near each important decision.
