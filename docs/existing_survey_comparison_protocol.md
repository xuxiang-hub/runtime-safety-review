# Existing survey comparison protocol

Table I compares the sixteen surveys closest to the review question across nine independent dimensions: motion prediction, planning, distribution shift, calibration, guarantee/assurance, risk propagation, intervention, closed-loop evidence, and traffic impact.

The comparison set locates adjacent survey coverage; it is not a random sample of all surveys and is not used to rank paper quality. Scores describe how a topic functions in the organization of each survey, not whether a keyword appears anywhere in the text.

## Common 0–3 anchors

| Score | Operational meaning |
|---:|---|
| 0 | No substantive coverage. A term appearing only in references, an index, or a cited title does not count. |
| 1 | Mentioned as context, a challenge, an example, or future work, without a dedicated synthesis structure. |
| 2 | Covered in a dedicated subsection, method group, comparison, or recurring analytical thread, but not a defining axis of the survey. |
| 3 | A principal organizing axis, supported by both structural evidence (title, research question, taxonomy, or major section) and synthesis evidence (cross-method comparison or central conclusion). |

When evidence falls between levels, the lower score is used. A topic presented only as a future direction cannot exceed 1. The nine dimensions are scored independently; no total score is used.

## Dimension boundaries

- **Motion prediction:** prediction inputs, outputs, architectures, uncertainty, datasets, and evaluation as an organized topic.
- **Planning:** planning or decision methods, objectives, constraints, and planner evaluation.
- **Shift:** distribution shift, OOD, corner cases, drift, environment change, or runtime change detection.
- **Calibration:** probability reliability, empirical coverage, prediction-set calibration, or recalibration—not generic parameter fitting.
- **Guarantee / assurance:** statistical or formal guarantees and broader structured safety-evidence or assurance arguments. This dimension is broader than the study-level G0–G4 statistical scale.
- **Risk propagation:** an explicit interface from upstream uncertainty or anomaly signals to downstream risk, constraint, cost, or decision quantities.
- **Intervention:** runtime rejection, fallback, filtering, replanning, speed reduction, braking, handoff, or other action-changing mechanisms.
- **Closed loop:** organized treatment of feedback, runtime interaction, closed-loop simulation, hardware, field, or road validation.
- **Traffic impact:** effects on other road users, traffic flow, network efficiency, cooperation, or system-level externalities.

The public score vectors are stored in `data/survey_comparison/existing_survey_scores.csv`.
