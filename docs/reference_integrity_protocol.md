# Reference integrity audit protocol

The audit unit is a sentence–reference pair, not a paragraph or a numeric citation group. Each manuscript citation is expanded into individual stable bibliography keys before semantic review.

## Linkage checks

1. Resolve every rendered citation number to its bibliography entry.
2. Resolve that entry to a stable BibTeX key.
3. Compare title, author, year, venue, DOI, and URL metadata.
4. Associate the cited source with the precise sentence clause it is expected to support.
5. Record whether the source directly supports, partly supports, exemplifies, limits, or does not support the claim.

Physical row order in a `.bib` file is never treated as a citation number. IEEE-style numeric labels are generated from first-citation order, while the audit joins records by stable BibTeX key.

## Semantic verdicts

| Verdict | Meaning |
|---|---|
| `SUPPORTED` | The cited source directly supports the bounded claim. |
| `SUPPORTED_AS_EXAMPLE` | The source is a valid example but does not establish the field-level generalization alone. |
| `SUPPORTED_SYNTHESIS` | The cautious conclusion follows from several bounded source claims. |
| `SUPPORTED_WITH_SCOPE_LIMIT` | Support holds only under a stated population, assumption, or evaluation boundary. |
| `PARTIAL_SUPPORT` | Only part of the sentence is supported; the sentence or citation group should be narrowed. |
| `PLACEMENT_AMBIGUOUS` | The source may be relevant, but the citation location does not identify which clause it supports. |
| `NOT_SUPPORTED` | The source does not substantiate the current claim. |

## Release rule

The final sentence-level matrix is generated only after the English LaTeX text and BibTeX keys are stable. Historical numeric matrices are not published as current evidence because manuscript edits can change every downstream number without changing the underlying source.
