# Search strategy

## Contents

1. Search architecture
2. Query vocabulary
3. Database roles
4. Deduplication
5. Progressive Methods retrieval
6. Search audit

## 1. Search architecture

Use a recall-first candidate search followed by precision-first Run review.

1. Search core concepts and explicitly allowed technologies.
2. Expand full names, aliases, historical names, spelling variants, and hyphen variants.
3. Union all candidate studies.
4. Deduplicate studies before retrieving papers and Methods.
5. Expand candidate studies to samples, experiments, and Runs.
6. Classify the current Run branch using sample-level evidence.

Do not require one giant query. GEO, SRA, ENCODE, and NGDC parse fields and operators differently. Separate query families are often more reproducible; union them afterward.

## 2. Query vocabulary

### Core concepts

Use as recall terms:

```text
"nascent RNA sequencing"
"newly synthesized RNA sequencing"
"co-transcriptional splicing"
"cotranscriptional splicing"
"chromatin-associated RNA"
"chromatin-bound RNA"
"RNA polymerase II nascent RNA"
"Pol II-associated nascent RNA"
"transcription elongation RNA"
```

### Technology terms

Generate the active list from `technology-registry.md` and the user's current standard file. Search canonical names and approved variants. Normalize:

- case;
- Unicode/ASCII hyphens and missing hyphens;
- spaces around `seq`;
- full names and abbreviations;
- legacy names only when technically equivalent or explicitly routed for conditional review.

### Methods clue terms

Use these to inspect candidate sample descriptions and Methods, not as sufficient Checked evidence:

```text
intronic RNA
unspliced RNA
pre-mRNA
nascent transcript
run-on
nuclear run-on
4-thiouridine / 4sU
bromouridine / BrU
Pol II-associated RNA
chromatin fraction / chromatin pellet
non-polyadenylated RNA
rRNA depletion
random priming
```

### Exclusion clues

Do not apply these as universal early `NOT` filters because valid protocols may mention them as controls or inputs. Apply primarily at Run review:

```text
poly(A)+ / oligo(dT)
mRNA-seq
3' RNA-seq / QuantSeq
small RNA / miRNA
half-life / stability / decay
chase / BruChase
RNA-DNA contact / proximity ligation
ChIP-seq / WGS / Bisulfite-seq
```

## 3. Database roles

- **GEO:** study and sample descriptions, treatment/extraction protocols, processed files, publication links.
- **SRA/ENA:** experiment and Run identifiers, raw-data availability, library fields, platform/layout.
- **BioProject/BioSample:** project/sample linkage and biological attributes; usually less detailed than GEO Methods.
- **ENCODE:** assay ontology, biosample, experiment, replicate, file metadata.
- **NGDC GSA:** independent CRA/CRX/CRR projects; search separately because some records are absent from NCBI.

Do not add GEO sample counts and SRA Run counts as if they are the same unit. GEO GSM, SRA Experiment, BioSample, and Run have different cardinalities.

## 4. Identifier and deduplication rules

Common NCBI levels:

```text
Study/project: GSE, SRP, PRJNA
Sample: GSM, SRS, SAMN
Experiment: SRX
Run: SRR (or ERR/DRR)
```

NGDC levels:

```text
Project: CRA/PRJCA
Experiment: CRX
Run: CRR
```

Use:

- canonical study/project ID to avoid reopening one paper for every Run;
- Run ID as the final unique download key;
- explicit cross-database mapping to identify mirrored SRR/ERR/CRR records.

Deduplicate before deep Methods retrieval. Keep all Runs belonging to one experiment when they are distinct raw sequencing runs.

## 5. Progressive Methods retrieval

Use the least expensive source that decisively answers the question:

1. Run/experiment metadata;
2. sample page and construction/treatment/extraction protocols;
3. study page to map assay branches;
4. paper Methods;
5. supplement only when core Methods cannot resolve the branch.

Escalate early for high-risk patterns:

- the study contains both nascent and ordinary RNA-seq;
- title time could be treatment rather than pulse;
- chase, stability, or half-life language;
- technology name is ambiguous or reused;
- structured fields conflict with the title;
- sample metadata is private or incomplete.

## 6. Search audit

Record for each query family:

- database;
- query string and date;
- candidate study/sample/experiment counts;
- identifier unit;
- deduplication key;
- exclusions applied at search stage;
- technologies added or intentionally omitted;
- standard/rule version.

Do not claim completeness without preserving this audit trail.
