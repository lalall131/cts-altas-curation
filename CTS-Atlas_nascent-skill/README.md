# CTS-Atlas nascent-RNA curation skill

## Supplementary Software S1

This package contains the rule set, technology registry, evidence hierarchy, review-output specification, and validation script used to curate public nascent-RNA sequencing Runs for a co-transcriptional splicing atlas.

## Scope

The package supports candidate retrieval, study-level merging and deduplication, Run-level classification, progressive Methods review, audit sampling, and structured evidence reporting. It is designed to identify data that capture RNA during ongoing transcription or before full transcript maturation.

## Contents

- `SKILL.md`: workflow and classification contract.
- `references/search-strategy.md`: search architecture and database roles.
- `references/technology-registry.md`: approved assay names, variants, and conditional rules.
- `references/decision-rules.md`: inclusion, exclusion, timing, evidence, and reason-code rules.
- `references/review-output.md`: review sequence, required fields, and workbook layout.
- `scripts/validate_run_review_csv.py`: CSV schema and quality-control validator.

## Reproducibility

The scientific rules are platform-independent. An implementation should record the rule version, implementation version, search date, database, query family, deduplication key, random seed, and source URLs. The package contains no platform-specific agent adapter, raw sequencing data, credentials, API keys, unpublished sample data, or personal contact information.

## Use in a manuscript

This archive may be cited as **Supplementary Software S1**. The archive should be deposited with a versioned release in a repository that provides a persistent identifier (for example, Zenodo, OSF, or Figshare). Replace the placeholder citation metadata in `CITATION.cff` with the authorship, DOI, and repository information assigned at publication.

## Validation example

```powershell
python scripts/validate_run_review_csv.py path\to\run_review.csv
```

The validator checks required fields, unique Run IDs, and evidence-related quality warnings. Validation warnings should be reviewed before reporting a curation result.

## Version

Version: `1.0.0`

Release type: publication supplement

Release date: 2026-08-28
