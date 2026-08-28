# Technology registry

## Contents

1. General rule
2. Direct run-on and Pol II capture
3. Metabolic-label assays
4. Chromatin-associated RNA
5. Long-read nascent RNA
6. Single-cell scope
7. Never infer from platform alone

## 1. General rule

Technology names retrieve candidates; the current sample design decides classification. Variants below are search aliases only when they are technically equivalent or explicitly marked conditional.

## 2. Direct run-on and Pol II capture

| Family | Search names and variants | Run-level rule |
|---|---|---|
| PRO-seq | `PRO-seq`, `precision run-on sequencing`, approved p/uPRO variants | Checked when the current Run is the run-on branch and nascent RNA is captured from engaged polymerase. |
| GRO-seq | `GRO-seq`, `global run-on sequencing`, `GROseq` | Same rule; do not exclude at search stage for expected junction coverage. |
| ChRO-seq | `ChRO-seq`, `chromatin run-on sequencing`, `pChRO-seq` | Checked when chromatin/nuclei run-on with labeled NTP enrichment is explicit. |
| NET-seq | `NET-seq`, `native elongating transcript sequencing` | Checked when Pol II/elongation-complex-associated RNA is explicit. |
| mNET/tNET/PlaNET | `mNET-seq`, `mNETseq`, `tNET-seq`, `PlaNET-seq` | Confirm the immunoprecipitated polymerase/elongation complex and current branch. |
| POINT | `POINT-seq`, `POINT-nano` | Exact technology match only; never match ordinary phrases such as `time point`. |

Nuclear run-on duration is not the in vivo metabolic-label pulse and is not subject to the 30 min pulse threshold.

## 3. Metabolic-label assays

Require sample-specific pulse, chase, selection, and library evidence.

| Family | Search names and variants | Conditional Checked rule |
|---|---|---|
| TT-seq | `TT-seq`, `TT seq`, `transient transcriptome sequencing` | Actual RNA pulse ≤30 min, chase 0/immediate harvest, newly labeled RNA enrichment, no poly(A)+ branch. |
| TTchem-seq | `TTchem-seq`, `TT-chem-seq`, `TT chem seq` | Same pulse/chase rule; confirm chemical enrichment branch. |
| chrTT-seq | `chrTT-seq`, `chromatin-associated TT-seq` | Require both valid short pulse and chromatin-fraction design. |
| 4sU-seq | `4sU-seq`, `4SU-seq`, `4-thiouridine sequencing` | Pulse ≤30 min, chase 0, labeled/new RNA captured or identifiable, no poly(A)+. |
| Bru-seq | `Bru-seq`, `bromouridine sequencing`, `BrU-seq` | Pulse ≤30 min and BrU-labeled RNA immunopurification. |
| SLAM-seq | `SLAM-seq`, full name and spelling variants | Require pulse ≤30 min, no chase/stability branch, sample-level newly synthesized RNA design, and no poly(A)+ exclusion. |
| TimeLapse-seq | `TimeLapse-seq`, `TimeLapse seq` | Same conditional rule as SLAM; conversion chemistry alone is not proof of immediate nascent RNA. |

### Excluded related variants

- `BruChase-seq` and pulse-chase/half-life/stability branches are Deleted when chase >0 or the objective is RNA aging/decay.
- A label pulse >30 min is Deleted under the current rule, even when the assay name is otherwise accepted.
- A sample title containing a long treatment time can still be Checked if the actual RNA pulse is short and separately documented.

## 4. Chromatin-associated RNA

| Family | Search names | Rule |
|---|---|---|
| Chromatin RNA-seq | `chromatin RNA-seq`, `chromatin-associated RNA-seq`, `chromatin-bound RNA-seq`, `chrRNA-seq`, `chromatin fraction RNA-seq` | Checked when RNA is extracted from a chromatin fraction/pellet, ordinary RNA library construction is used, and poly(A)+ enrichment is absent. |
| ChAR label | `ChAR-seq`, `ChAR seq`, `chromatin-associated RNA sequencing` | Always disambiguate at sample Methods level. |

`ChAR-seq` has two incompatible meanings:

1. chromatin-fraction RNA sequencing: conditionally eligible;
2. formal RNA–DNA contact/proximity-ligation mapping: Deleted.

Do not propagate one meaning across every study using the same label.

`ribo-minus`, `nuclear RNA`, `intronic RNA`, and `total RNA` are supportive clues only. Without direct nascent/chromatin/Pol II enrichment, ordinary total or nuclear RNA-seq is Deleted.

## 5. Long-read nascent RNA

| Family | Search names | Rule |
|---|---|---|
| nano-COP | `nano-COP`, full name variants | Confirm nascent/chromatin-associated RNA capture and the current nanopore branch. |
| POINT-nano | `POINT-nano` | Confirm Pol II-associated nascent RNA capture. |
| FLEP-seq | `FLEP-seq`, approved full name | Confirm direct elongating/nascent transcript capture. |
| Generic PacBio/ONT direct RNA | `long-read nascent RNA`, `direct RNA sequencing` | Platform or direct-RNA chemistry alone is insufficient. Require explicit nascent, chromatin, or Pol II enrichment. Poly(A)-dependent mature direct RNA is Deleted. |

## 6. Single-cell scope

Proactively search only the single-cell technologies explicitly allowed by the current standard. In the established CTS scope these are:

```text
scGRO-seq
scFLUENT-seq
```

Do not automatically expand every bulk assay into an `sc` variant such as scPRO-seq. If an unapproved single-cell variant appears incidentally, classify it according to the current scope and record an explicit single-cell scope reason.

## 7. Never infer from platform alone

Illumina, PacBio, ONT, paired/single-end, `RNA-Seq`, `OTHER`, `cDNA`, and `TRANSCRIPTOMIC` do not determine biological eligibility. Use the extraction, enrichment, labeling, run-on, or Pol II-capture protocol.
