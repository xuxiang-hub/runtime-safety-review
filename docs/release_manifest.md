# Public release manifest

## Inclusion rule

A file or field is included when it is necessary to reconstruct a reported count, classification, figure, table, or citation link and can be redistributed lawfully.

## Included artifact classes

| Class | Public representation | Reason |
|---|---|---|
| Search strategy | Concept blocks, field translations, query generator | Reconstructs search logic without redistributing licensed results |
| Screening | Count-conserving stage table and flow figure | Reconstructs corpus arithmetic and evidence roles |
| Full-text synthesis | Selected coding fields for 303 eligible studies | Supports mechanism, guarantee, intervention, and validation claims |
| Wide-corpus mapping | Aggregate tables only | Supports landscape claims without bulk abstract redistribution |
| Synthesis | Findings, filters, numerators, denominators, caveats | Makes each quantitative conclusion independently checkable |
| Survey comparison | Sixteen 0–3 score vectors and scoring protocol | Supports Table I without turning scores into a quality ranking |
| References | Stable-key bibliographic catalog and audit protocol | Avoids dependence on physical bibliography order |

## Deliberately excluded artifact classes

| Excluded material | Reason |
|---|---|
| Database export files and bulk abstracts | Database licensing and redistribution restrictions |
| Article PDFs and copied full-text passages | Copyright and access restrictions |
| Local paths, caches, and machine-specific configuration | Irrelevant to scholarly reconstruction and may reveal private workspace details |
| Exact execution timestamps and workspace task logs | Operational provenance not needed to reproduce the released snapshot |
| Non-analytical workflow fields | Not needed to recompute published classifications |
| Historical numeric citation matrices | Numeric labels change when the manuscript is reordered; the final audit must use stable bibliography keys |

## Release gate

The public snapshot is releasable only when `scripts/validate_release.py` passes, no manuscript placeholder remains in repository-facing prose, and the final English LaTeX citation audit has been regenerated against stable bibliography keys.
