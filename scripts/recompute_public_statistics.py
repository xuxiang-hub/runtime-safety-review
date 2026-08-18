#!/usr/bin/env python3
"""Recompute the released G-by-V matrix and synthesis metrics."""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def percent(numerator: int, denominator: int) -> float:
    return round(100 * numerator / denominator, 2) if denominator else 0.0


def make_metric(
    finding_id: str,
    metric_id: str,
    label: str,
    numerator: int,
    denominator: int,
    definition: str,
    source_fields: str,
) -> dict[str, object]:
    return {
        "finding_id": finding_id,
        "metric_id": metric_id,
        "metric_label": label,
        "numerator": numerator,
        "denominator": denominator,
        "percentage": percent(numerator, denominator),
        "filter_definition": definition,
        "source_fields": source_fields,
    }


def build_matrix(profiles: list[dict[str, str]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for role in ("all", "core", "contextual"):
        subset = profiles if role == "all" else [row for row in profiles if row["formal_corpus_role"] == role]
        counts = Counter(
            (row["statistical_guarantee_strength_final"], row["validation_maturity_final"])
            for row in subset
        )
        for guarantee in ("G0", "G1", "G2", "G3", "G4"):
            row: dict[str, object] = {
                "corpus_role": role,
                "statistical_guarantee_strength": guarantee,
            }
            for validation in ("V0", "V1", "V2", "V3", "V4", "V5"):
                row[validation] = counts[(guarantee, validation)]
            row["row_total"] = sum(int(row[validation]) for validation in ("V0", "V1", "V2", "V3", "V4", "V5"))
            rows.append(row)
    return rows


def build_metrics(
    coding: list[dict[str, str]], profiles: list[dict[str, str]]
) -> list[dict[str, object]]:
    profile_by_id = {row["study_id"]: row for row in profiles}
    joined = [{**row, **profile_by_id[row["study_id"]]} for row in coding]
    total = len(joined)

    low_decision = [row for row in joined if row["decision_relevance_primary"] in {"none", "monitoring-only"}]
    low_validation = [row for row in joined if row["validation_maturity_final"] in {"V0", "V1"}]
    contextual = [row for row in joined if row["formal_corpus_role"] == "contextual"]
    contextual_low_validation = [row for row in contextual if row["validation_maturity_final"] in {"V0", "V1"}]

    review_like = re.compile(r"\b(?:survey|review|overview)\b", re.IGNORECASE)
    ood_title = re.compile(
        r"(?:out[- ]of[- ]distribution|\bOOD\b|anomal|corner[- ]case|distribution shift|prediction failure)",
        re.IGNORECASE,
    )
    ood_original = [row for row in joined if ood_title.search(row["title"]) and not review_like.search(row["title"])]
    ood_with_contract = [
        row for row in ood_original
        if row["statistical_guarantee_family_final"]
        in {"safety-risk-calibration", "safety-risk-coverage"}
    ]

    g0 = [row for row in joined if row["statistical_guarantee_strength_final"] == "G0"]
    core = [row for row in joined if row["formal_corpus_role"] == "core"]
    core_g0 = [row for row in core if row["statistical_guarantee_strength_final"] == "G0"]

    no_shift = [row for row in joined if row["shift_construction"] == "NA:no explicit distribution-shift construction"]
    detectable_shift = [row for row in joined if row["shift_detectable"] == "yes"]
    g4 = [row for row in joined if row["statistical_guarantee_strength_final"] == "G4"]

    multiagent = [row for row in joined if row["multiagent_evaluation"] == "yes"]
    multiagent_joint = [row for row in multiagent if row["statistical_guarantee_family_final"] == "joint_multiagent"]
    multiagent_strong = [row for row in multiagent if row["statistical_guarantee_strength_final"] in {"G3", "G4"}]
    all_joint = [row for row in joined if row["statistical_guarantee_family_final"] == "joint_multiagent"]

    no_closed_loop = [row for row in joined if row["closed_loop_evaluation"] != "yes"]
    high_validation = [row for row in joined if row["validation_maturity_final"] in {"V4", "V5"}]
    latency = [row for row in joined if row["online_latency_reported"] == "yes"]
    traffic = [row for row in joined if row["transportation_impact_reported"] == "yes"]
    latency_traffic = [row for row in joined if row["online_latency_reported"] == "yes" and row["transportation_impact_reported"] == "yes"]

    strong = [row for row in joined if row["statistical_guarantee_strength_final"] in {"G3", "G4"}]
    strong_high_validation = [row for row in strong if row["validation_maturity_final"] in {"V4", "V5"}]
    high_validation_g0 = [row for row in high_validation if row["statistical_guarantee_strength_final"] == "G0"]
    strong_closed_loop = [row for row in strong if row["closed_loop_evaluation"] == "yes"]

    formal = [row for row in joined if row["formal_control_guarantee_final"] != "none"]
    formal_hybrid = [row for row in formal if row["formal_control_guarantee_final"] == "hybrid-statistical-formal"]
    formal_g0 = [row for row in formal if row["statistical_guarantee_strength_final"] == "G0"]
    strong_hybrid = [row for row in strong if row["formal_control_guarantee_final"] == "hybrid-statistical-formal"]

    return [
        make_metric("F1", "F1-M1", "无下游决策消费或仅监测", len(low_decision), total, "decision_relevance_primary in {none, monitoring-only}", "decision_relevance_primary"),
        make_metric("F1", "F1-M2", "证据停留在V0/V1", len(low_validation), total, "validation_maturity_final in {V0,V1}", "validation_maturity_final"),
        make_metric("F1", "F1-M3", "contextual中证据停留在V0/V1", len(contextual_low_validation), len(contextual), "formal_corpus_role=contextual and validation_maturity_final in {V0,V1}", "formal_corpus_role; validation_maturity_final"),
        make_metric("F2", "F2-M1", "标题界定的OOD/异常/预测失效原始研究具有下游安全风险契约", len(ood_with_contract), len(ood_original), "title keyword subset; review-like records excluded; guarantee family is safety-risk calibration/coverage", "publication_type; title; statistical_guarantee_family_final"),
        make_metric("F2", "F2-M2", "全部语料为G0", len(g0), total, "statistical_guarantee_strength_final=G0", "statistical_guarantee_strength_final"),
        make_metric("F2", "F2-M3", "core语料为G0", len(core_g0), len(core), "formal_corpus_role=core and statistical_guarantee_strength_final=G0", "formal_corpus_role; statistical_guarantee_strength_final"),
        make_metric("F3", "F3-M1", "没有显式分布偏移构造", len(no_shift), total, "shift_construction=NA:no explicit distribution-shift construction", "shift_construction"),
        make_metric("F3", "F3-M2", "把偏移编码为运行时可检测", len(detectable_shift), total, "shift_detectable=yes", "shift_detectable"),
        make_metric("F3", "F3-M3", "达到G4在线/序列保证", len(g4), total, "statistical_guarantee_strength_final=G4", "statistical_guarantee_strength_final; statistical_guarantee_family_final"),
        make_metric("F4", "F4-M1", "多主体评价中采用联合多主体保证", len(multiagent_joint), len(multiagent), "multiagent_evaluation=yes and statistical_guarantee_family_final=joint_multiagent", "multiagent_evaluation; statistical_guarantee_family_final"),
        make_metric("F4", "F4-M2", "多主体评价达到G3/G4", len(multiagent_strong), len(multiagent), "multiagent_evaluation=yes and G in {G3,G4}", "multiagent_evaluation; statistical_guarantee_strength_final"),
        make_metric("F4", "F4-M3", "全语料明确采用联合多主体保证", len(all_joint), total, "statistical_guarantee_family_final=joint_multiagent", "statistical_guarantee_family_final"),
        make_metric("F5", "F5-M1", "没有闭环评价", len(no_closed_loop), total, "closed_loop_evaluation!=yes", "closed_loop_evaluation"),
        make_metric("F5", "F5-M2", "达到V4/V5", len(high_validation), total, "validation_maturity_final in {V4,V5}", "validation_maturity_final"),
        make_metric("F5", "F5-M3", "报告数值在线延迟/频率", len(latency), total, "online_latency_reported=yes", "online_latency_reported"),
        make_metric("F5", "F5-M4", "报告交通系统/他主体影响", len(traffic), total, "transportation_impact_reported=yes", "transportation_impact_reported"),
        make_metric("F5", "F5-M5", "同时报告延迟与交通影响", len(latency_traffic), total, "online_latency_reported=yes and transportation_impact_reported=yes", "online_latency_reported; transportation_impact_reported"),
        make_metric("F6", "F6-M1", "G3/G4中达到V4/V5", len(strong_high_validation), len(strong), "G in {G3,G4} and V in {V4,V5}", "statistical_guarantee_strength_final; validation_maturity_final"),
        make_metric("F6", "F6-M2", "V4/V5论文为G0", len(high_validation_g0), len(high_validation), "V in {V4,V5} and G=G0", "statistical_guarantee_strength_final; validation_maturity_final"),
        make_metric("F6", "F6-M3", "G3/G4具有闭环评价", len(strong_closed_loop), len(strong), "G in {G3,G4} and closed_loop_evaluation=yes", "statistical_guarantee_strength_final; closed_loop_evaluation"),
        make_metric("F7", "F7-M1", "形式控制保证与统计保证形成混合接口", len(formal_hybrid), len(formal), "formal_control_guarantee_final!=none and equals hybrid-statistical-formal", "formal_control_guarantee_final; statistical_guarantee_strength_final"),
        make_metric("F7", "F7-M2", "形式控制保证仍为G0", len(formal_g0), len(formal), "formal_control_guarantee_final!=none and G=G0", "formal_control_guarantee_final; statistical_guarantee_strength_final"),
        make_metric("F7", "F7-M3", "G3/G4形成统计—形式混合接口", len(strong_hybrid), len(strong), "G in {G3,G4} and formal_control_guarantee_final=hybrid-statistical-formal", "statistical_guarantee_strength_final; formal_control_guarantee_final"),
    ]


def comparable(rows: list[dict[str, object]]) -> list[dict[str, str]]:
    return [{key: str(value) for key, value in row.items()} for row in rows]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="replace the two released derived tables")
    args = parser.parse_args()

    coding = read_csv(DATA / "fulltext_study_coding.csv")
    profiles = read_csv(DATA / "guarantee_validation_profile.csv")
    matrix = build_matrix(profiles)
    metrics = build_metrics(coding, profiles)

    matrix_path = DATA / "guarantee_validation_matrix.csv"
    metrics_path = DATA / "findings_supporting_counts.csv"
    if args.write:
        write_csv(matrix_path, matrix, list(matrix[0]))
        write_csv(metrics_path, metrics, list(metrics[0]))
        print("Rebuilt guarantee_validation_matrix.csv and findings_supporting_counts.csv")
        return 0

    if comparable(matrix) != read_csv(matrix_path):
        raise AssertionError("Released G-by-V matrix differs from recomputation")
    if comparable(metrics) != read_csv(metrics_path):
        raise AssertionError("Released finding counts differ from recomputation")
    print("Recomputation passed: G-by-V matrix and 23 finding metrics match.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
