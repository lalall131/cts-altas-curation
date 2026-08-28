# Run-level decision rules

## Contents

1. Target definition
2. Positive gates
3. Hard exclusions
4. Time interpretation
5. Evidence hierarchy
6. Frequent error mechanisms
7. Reason codes
8. Program-rule alignment

## 1. Target definition

The target is RNA captured while transcription is ongoing or before full maturation, suitable in principle for a co-transcriptional splicing atlas. Biological capture is judged first; gene-body/junction coverage, depth, and read-length suitability are downstream QC, not search-stage exclusion.

## 2. Positive gates

Checked requires at least one sample-specific positive gate and no hard exclusion.

### A. Direct engaged-polymerase/run-on capture

Evidence includes nuclear/chromatin run-on with labeled NTPs, Pol II immunoprecipitation, or native elongating complex RNA.

### B. Short metabolic pulse

Require all:

- actual 4sU/BrU/EU or equivalent RNA-incorporation pulse ≤30 min;
- chase 0 or immediate harvest;
- newly labeled RNA is enriched or explicitly identified by the assay;
- current Run is the labeled/new RNA branch;
- no poly(A)+ selection.

### C. Chromatin-fraction RNA

Require RNA extracted from a chromatin-bound/fraction/pellet preparation, no poly(A)+ enrichment, and an RNA library rather than RNA–DNA contact ligation.

### D. Direct long-read nascent capture

Require explicit nascent, Pol II-associated, or chromatin-associated input. Long-read platform or direct-RNA chemistry alone is not enough.

## 3. Hard exclusions

| Exclusion | Decision |
|---|---|
| poly(A)+, oligo(dT), mature mRNA enrichment | Deleted |
| ordinary total/ribo-minus/nuclear RNA-seq without a positive gate | Deleted |
| 3′ RNA-seq, QuantSeq, tag-based mature 3′ assay | Deleted |
| small-RNA/miRNA branch | Deleted |
| metabolic pulse >30 min | Deleted |
| chase >0, BruChase, half-life, stability, or decay branch | Deleted |
| formal RNA–DNA contact/proximity-ligation ChAR | Deleted |
| wrong assay branch within a mixed study | Deleted |
| WGS, ChIP-seq, Bisulfite-seq, ATAC-seq, DNA assay | Deleted |
| single-cell technology outside the explicit search scope | Deleted or Out-of-scope according to the current standard |

Do not delete on file size, browser download limit, sequencing depth, or SRA Toolkit requirement.

## 4. Time interpretation

Store the following separately:

| Field | Meaning | Apply ≤30 min? |
|---|---|---|
| `pulse_time` | time RNA label is present and incorporating | Yes, for metabolic-label assays |
| `chase_time` | time after label removal before harvest | No; positive chase is an exclusion under immediate-nascent scope |
| `treatment_time` | drug, depletion, stress, infection, stimulation | No |
| `release/washout_time` | time after treatment removal | No |
| `harvest/timepoint` | experimental collection time | No |
| `run_on_time` | isolated nuclei/chromatin extension reaction | No metabolic threshold |

Examples of correct reasoning:

- `TT_12h`, Methods: treatment 12 h and 4sU pulse 5 min → pulse is 5 min.
- infection `6 hpi`, Methods: 4sU pulse 60 min → pulse is 60 min; Deleted.
- `4sU pulse 20 min + chase 120 min` → Deleted because chase >0.
- `DRB 4 h, release 10 min, PRO-seq run-on 3 min` → treatment/release/run-on are not metabolic pulse.
- `IAA 3 h ChAR/chromatin RNA` → judge chromatin protocol; 3 h is protein-depletion treatment.

If one row contains multiple times, resolve the exact sample. A study-wide time list cannot be used as a sample pulse value.

## 5. Evidence hierarchy

1. Run/sample construction, treatment, and extraction protocol.
2. Paper Methods/supplement tied to the current branch.
3. Study design used to map branches.
4. Library Strategy/Source/Selection.
5. Sample title and keyword match.

Minimum Checked evidence should describe the capture mechanism, not merely repeat the assay label.

`Library Selection=cDNA` neither proves nor disproves nascent capture. `RNA-Seq` can describe a valid TT/chromatin sample. `polyA` or oligo(dT) is strong negative evidence when it describes the current library.

## 6. Frequent error mechanisms

### False positives

Prioritize review for:

- same-study branch leakage: a study contains PRO/GRO/TT plus ordinary RNA-seq, input, ChIP, ATAC, small-RNA, or control Runs;
- treatment duration mistaken for pulse duration;
- chase/stability/half-life studies retained because they use 4sU/BrU;
- homonyms such as `time point` mapped to POINT-seq;
- ChAR contact mapping mistaken for chromatin RNA-seq;
- 3′ or poly(A)+ assays retained because the study discusses nascent transcription;
- study-level technology copied to every Run;
- keyword-only confirmation without Methods.

### False negatives

Prioritize rescue for:

- short 4sU/BrU pulse hidden in Methods while structured fields say `RNA-Seq/cDNA`;
- PRO/GRO/Pol II capture hidden behind `OTHER` or an incorrect strategy field;
- chromatin pellet/fraction RNA described only in extraction Methods;
- `total RNA` describing the input before labeled-RNA enrichment;
- small-RNA-compatible adapters used by a valid run-on protocol, mistaken for miRNA-seq;
- long treatment time in the title while pulse is short.

## 7. Reason codes

### Included

```text
IN-RUNON       direct run-on capture
IN-POL2        Pol II/elongation-complex RNA
IN-METAB       valid short metabolic pulse
IN-CHROMATIN   valid chromatin-fraction RNA
IN-LONGREAD    direct long-read nascent capture
```

### Excluded

```text
EX-POLYA       poly(A)+/oligo(dT)/mature mRNA
EX-ORDINARY    ordinary RNA-seq without a positive gate
EX-3END        3′ RNA-seq/QuantSeq
EX-SMALLRNA    small-RNA/miRNA branch
EX-BRANCH      wrong branch in a mixed study
EX-LONGPULSE   metabolic pulse >30 min
EX-CHASE       chase >0
EX-STABILITY   half-life/stability/decay objective
EX-CONTACT     RNA–DNA contact/proximity-ligation assay
EX-SINGLECELL  unapproved single-cell scope
EX-NONRNA      non-RNA sequencing assay
EX-HOMONYM     keyword/technology-name false match
```

### Pending

```text
PD-PRIVATE     relevant sample metadata remains private
PD-METHODS     sample Methods cannot be located
PD-CONFLICT    sample evidence conflicts
PD-LINKAGE     Run-to-sample/branch linkage unresolved
PD-TIME        actual pulse/chase cannot be resolved
```

### Out-of-scope

```text
OOS-AGGREGATOR reprocessing/compendium rather than original study
OOS-SCOPE      explicitly excluded technology or collection scope
```

## 8. Program-rule alignment

Natural-language rules and executable classification logic must match. Before full processing:

1. encode reason codes and gates explicitly;
2. test representative archetypes, not memorized Run IDs;
3. audit random results from every class;
4. stop if the implementation leaves clearly classifiable records Pending or violates a hard exclusion;
5. version the written rule set and the implementation together.

Do not train rules to reproduce a short list of known Run outcomes. Generalize from capture mechanism, sample branch, time type, and library selection.
