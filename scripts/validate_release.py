#!/usr/bin/env python3
"""Validate public-release counts, joins, and prohibited content."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    data = ROOT / "data"
    coding = read_csv(data / "fulltext_study_coding.csv")
    profiles = read_csv(data / "guarantee_validation_profile.csv")
    matrix = read_csv(data / "guarantee_validation_matrix.csv")
    flow = read_csv(data / "screening_flow.csv")

    require(len(coding) == 303, "fulltext_study_coding.csv must contain 303 studies")
    require(len(profiles) == 303, "guarantee_validation_profile.csv must contain 303 studies")
    require({row["study_id"] for row in coding} == {row["study_id"] for row in profiles}, "study IDs must join one-to-one")
    require(Counter(row["formal_corpus_role"] for row in coding) == Counter({"core": 61, "contextual": 242}), "corpus role totals are inconsistent")
    require(sum(int(row["row_total"]) for row in matrix if row["corpus_role"] == "all") == 303, "G-by-V matrix total must equal 303")
    flow_counts = {row["stage"]: int(row["count"]) for row in flow}
    require(flow_counts["baseline_unique_studies"] == 9001, "baseline unique studies must equal 9,001")
    require(flow_counts["full_text_reports_assessed"] == 516, "full-text reports assessed must equal 516")
    require(flow_counts["title_abstract_metadata_only_assessed"] == 8485, "title/abstract/metadata dispositions must equal 8,485")
    require(flow_counts["full_text_reports_assessed"] + flow_counts["title_abstract_metadata_only_assessed"] == flow_counts["baseline_unique_studies"], "9,001 baseline studies must split into 516 full-text and 8,485 title/abstract/metadata dispositions")
    require(flow_counts["baseline_full_text_eligible"] + flow_counts["full_text_excluded_neighbor"] == flow_counts["full_text_reports_assessed"], "516 full-text reports must split into 295 eligible and 221 excluded-neighbor studies")
    require(flow_counts["baseline_full_text_eligible"] + flow_counts["eligible_studies_identified_by_other_methods"] == flow_counts["full_text_evidence_studies"], "295 baseline eligible plus 8 other-method studies must equal 303")
    require(flow_counts["wide_review_corpus"] == 6907, "wide corpus must equal 6,907")

    prohibited_columns = {
        "local_pdf_path",
        "source_text_path",
        "publication_status_last_verified",
        "coding_basis",
        "review_trigger",
        "evidence_locator",
        "quote_location",
    }
    for path in data.rglob("*.csv"):
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            header = next(csv.reader(handle))
        require(not (set(header) & prohibited_columns), f"prohibited columns in {path.relative_to(ROOT)}")

    prohibited_text = re.compile(
        r"(?:/Users/|/private/|local_pdf_path|source_text_path|\[PDF_PAGE|see (?:risk|method|guarantee|intervention|evaluation) evidence locator)",
        re.IGNORECASE,
    )
    public_text_roots = [ROOT / "README.md", ROOT / "docs", ROOT / "data", ROOT / "figures"]
    paths: list[Path] = []
    for root in public_text_roots:
        paths.extend(root.rglob("*") if root.is_dir() else [root])
    for path in paths:
        if path.is_file() and path.suffix.lower() in {".md", ".csv", ".json", ".py", ".txt", ".yml", ".yaml", ".svg"}:
            text = path.read_text(encoding="utf-8-sig", errors="replace")
            require(not prohibited_text.search(text), f"prohibited content in {path.relative_to(ROOT)}")
            require("<dc:date>" not in text, f"embedded creation timestamp in {path.relative_to(ROOT)}")

    print("Public release validation passed: 303 full-text studies; 6,907-study review corpus.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
