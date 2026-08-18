# Evidence coding protocol

## Missingness

- `NA:<reason>`: not applicable.
- `NR:<detail>`: checked in the available full text but not reported.
- `UC:<detail>`: the available version does not permit a stable determination.
- `none`: explicitly absent, distinct from `NR`.

## Signal-to-risk relation

| Label | Meaning |
|---|---|
| `not-applicable` | No runtime signal or uncertainty output is evaluated. |
| `none` | A signal exists but is not connected to a safety consequence. |
| `qualitative-narrative` | The connection is argued through prose or examples only. |
| `learned-correlation` | A learned model links the signal and outcome without an independent calibration test. |
| `empirical-validated` | Experiments quantify the relation, without a formal or calibrated guarantee. |
| `formal-quantitative` | A mathematical relation links the signal or set to a constraint, risk, or safety event. |

## Statistical guarantee strength

The guaranteed target is recorded before the strength label. Detection alarms, prediction error, set coverage, collision risk, constraint satisfaction, safe-set invariance, and task safety are not treated as interchangeable targets.

| Level | Operational definition |
|---:|---|
| G0 | No explicit study-level statistical guarantee. |
| G1 | Empirical confidence or empirical performance claim. |
| G2 | Empirical calibration. |
| G3 | Marginal finite-sample coverage or risk guarantee. A finite union bound over marginal guarantees remains G3. |
| G4 | Conditional/groupwise, genuinely online adaptive or sequential risk/coverage control, or time-uniform guarantee. |

Classical sequential-detection guarantees such as false-alarm rate, average run length, or detection delay are coded by their actual target and are not reinterpreted as collision-risk or prediction-coverage guarantees.

## Formal control guarantee

This field is orthogonal to G and may take values such as `conditional-invariance`, `robust-invariance`, `reachability`, `recursive-feasibility`, `chance-constrained-control`, or `hybrid-statistical-formal`. A method can therefore be G0 while still proving a strict deterministic control result.

## Validation maturity

| Level | Operational definition |
|---:|---|
| V0 | Predictive accuracy or probability metrics only. |
| V1 | Offline calibration, coverage, or explicit risk metrics. |
| V2 | Offline planning, log replay, or safety-proxy evaluation. |
| V3 | Closed-loop simulation. |
| V4 | Hardware or controlled-site experiment. |
| V5 | Real-road or transportation-system evidence. |

V measures closure of the risk-to-action validation chain, not overall paper quality. Using real-road images in an offline perception benchmark does not by itself establish V5.

## Decision relevance

`decision_relevance_primary` records the furthest implemented downstream role: `none`, `offline-test`, `monitoring-only`, `constraint-or-cost`, or `triggered-intervention`. Upstream signals are not counted as decision-consumed unless they change a constraint, cost, candidate choice, fallback, or physical action.

## Intervention

The primary intervention is the furthest-downstream mechanism that changes the final candidate or physical action. Monitoring, predictor routing, and other upstream mechanisms may be retained as secondary labels. Trigger rule, fallback policy, intervention cost, online latency, and transportation impact are coded separately.

## Public-field boundary

The public coding table contains the final fields needed for reconstruction. It intentionally excludes verbatim source text, page-level evidence locators, local file paths, operational timestamps, and non-analytical workflow columns.
