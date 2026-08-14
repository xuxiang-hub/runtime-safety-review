# Public data dictionary

## Evidence layers

| Layer | Unit | Size | Permitted inference |
|---|---|---:|---|
| Full-text evidence | Eligible study | 303 | Mechanisms, guarantees, interventions, and validation maturity |
| Abstract-level mapping | Retained study | 6,604 | Topic, year, source, and abstract-visible interface patterns |
| Review corpus | Retained study | 6,907 | Overall corpus size and evidence-role accounting |

The two retained layers are mutually exclusive in the public count chain. Abstract-level records do not receive formal `core` or `contextual` roles.

## Missing-value semantics

- `NA:<reason>`: the field is not applicable to the study.
- `NR:<detail>`: the relevant material was checked but the item was not reported.
- `UC:<detail>`: the available record does not permit a stable determination.
- `none`: the study explicitly does not contain the mechanism or guarantee.

Blank values must not be interpreted as any of the above states.

## Main files

### `fulltext_study_coding.csv`

One row per eligible full-text study. The file retains bibliographic identifiers, corpus role, transportation/task context, risk source, uncertainty and calibration semantics, decision relevance, guarantee labels, intervention type, and evaluation fields. It omits verbatim evidence, page locations, local paths, operational timestamps, and non-analytical workflow fields.

### `guarantee_validation_profile.csv`

One row per eligible full-text study. `statistical_guarantee_strength_final` ranges from G0 to G4. `formal_control_guarantee_final` is orthogonal to G. `validation_maturity_final` ranges from V0 to V5 and measures closure of the risk-to-action validation chain rather than overall paper quality.

### `screening_flow.csv`

`stage_id` is a stable public label. `count` is the reported stage total. `relationship` records the arithmetic or role decomposition. `evidence_role` distinguishes identification, screening, eligibility, corpus construction, synthesis, and exclusion.

### `findings_supporting_counts.csv`

Each row is one reproducible metric. `filter_definition` states the selection rule, while `source_fields` lists the public columns used. Percentages are descriptive of their stated denominator and must not be generalized beyond it.

### `mapping/`

These are aggregate tables derived from abstract-visible metadata and terminology. Themes may overlap; percentages across themes therefore need not sum to 100%.

### `survey_comparison/existing_survey_scores.csv`

Rows are the sixteen closest surveys and columns are nine independent coverage dimensions. Scores measure the organizational role of a topic within a survey, not study quality.
