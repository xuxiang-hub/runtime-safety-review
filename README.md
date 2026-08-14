# Reproducibility Materials for the Runtime-Safety Review

This repository contains the public, license-safe research artifacts supporting the systematic review of risk estimation, guarantees, and runtime intervention for learning-enabled transportation systems.

## What is included

- the search concepts and database-specific syntax;
- the count-conserving screening flow;
- a public coding table for all 303 eligible full-text studies;
- the guarantee-strength and validation-maturity profile and cross-tabulation;
- aggregate mapping results for the 6,907-study review corpus;
- numerator, denominator, filter, and caveat records for the seven synthesis findings;
- the 0–3 existing-survey comparison matrix used in Table I;
- a stable-key reference catalog and the citation-integrity audit protocol;
- editable and raster versions of the main screening and G-by-V figures;
- scripts that render the database queries, recompute the released statistics, and validate counts, joins, and prohibited fields.

After deduplication and version consolidation, 9,001 baseline unique studies were disposed under a common topical scope. Full reports were retrieved through DOI resolution, title–author matching, open repositories, and existing project holdings. The 516 successfully retrieved and verified reports underwent full-text eligibility assessment, yielding 295 eligible studies and 221 excluded neighbors. Eight additional eligible studies identified through other prespecified methods were assessed under the same criteria, producing 303 studies for full-text synthesis. A further 6,604 retained records support abstract-level systematic mapping, for a broad review corpus of 6,907 studies.

## Quick validation

Run from the repository root:

```bash
conda run -n py39 python scripts/validate_release.py
conda run -n py39 python scripts/recompute_public_statistics.py
conda run -n py39 python scripts/checksums.py
```

The validators check the 303-study join, the 61/242 role split, the G-by-V total, all 23 quantitative finding metrics, the 6,907-study count, prohibited columns, local paths, and file checksums.

## Repository map

| Path | Purpose |
|---|---|
| `docs/` | Search, eligibility, coding, scoring, and audit protocols |
| `data/screening_flow.csv` | Count-conserving screening and evidence-depth flow |
| `data/fulltext_study_coding.csv` | Public mechanism-level fields for 303 studies |
| `data/guarantee_validation_profile.csv` | Public G, formal-guarantee, and V labels |
| `data/findings_*.csv` | Recomputable synthesis findings and filters |
| `data/mapping/` | Aggregate wide-corpus mapping tables |
| `data/survey_comparison/` | Table I scores and method comparison |
| `data/reference_integrity/` | Stable-key bibliography catalog |
| `figures/` | Public review-flow and evidence-map figures |
| `scripts/` | Query renderer, statistical recomputation, and integrity validator |

## Materials not redistributed

Database exports, bulk abstracts, article PDFs, and verbatim full-text excerpts are not redistributed because of database terms and copyright. Local file paths, exact operational timestamps, and non-analytical workflow metadata are also excluded because they are not necessary to reproduce the published counts or claims. Stable bibliographic identifiers are provided where available so that readers can retrieve source records through lawful access.

## Citable release

The manuscript cites an immutable GitHub release together with its full commit identifier. Use the matching entry on the repository's Releases page when reproducing or auditing the submitted results; later development on the default branch is not part of that frozen snapshot.
