#!/usr/bin/env python3
"""Render one protocol-v2 query in a database's field syntax."""

from __future__ import annotations

import argparse


GROUPS = {
    "A": [
        ['"autonomous driving"', '"automated driving"', '"autonomous vehicle*"', '"automated vehicle*"', '"connected and autonomous vehicle*"', '"intelligent vehicle*"', '"self-driving"'],
        ['"trajectory prediction"', '"motion prediction"', '"motion forecasting"', '"trajectory planning"', '"motion planning"', '"behavior prediction"', 'planner*', '"decision making"', '"end-to-end driving"'],
        ['uncertaint*', 'calibrat*', '"conformal prediction"', '"prediction interval*"', '"perceptual uncertainty"', '"collision risk*"', '"risk estimation"', '"failure prediction"', '"risk-aware"'],
    ],
    "B": [
        ['"autonomous driving"', '"automated driving"', '"autonomous vehicle*"', '"automated vehicle*"', '"intelligent vehicle*"', '"self-driving"'],
        ['"trajectory prediction"', '"motion prediction"', '"trajectory planning"', '"motion planning"', 'planner*', '"decision making"', 'policy'],
        ['"distribution shift"', '"distribution drift"', '"out-of-distribution"', '"change detection"', '"corner case*"', '"edge case*"', 'anomal*', '"safety-critical scenario*"', '"runtime monitor*"', '"failure prediction"', '"failure detection"', '"risk monitoring"'],
    ],
    "C": [
        ['"autonomous driving"', '"automated driving"', '"autonomous vehicle*"', '"connected autonomous vehicle*"', '"intelligent vehicle*"', '"self-driving"'],
        ['"runtime assurance"', '"runtime monitor*"', '"risk monitor*"', '"safety filter*"', '"safety shield*"', '"safety layer*"', '"control filter*"', '"policy filter*"', '"control revision"', '"fallback control"', '"trajectory rejection"', '"safe replanning"', '"emergency braking"', '"minimal intervention"'],
        ['prediction', 'planning', 'planner*', 'trajectory', 'control', 'action', '"decision risk"'],
    ],
    "D": [
        ['"autonomous driving"', '"automated driving"', '"autonomous vehicle*"', '"automated vehicle*"', '"intelligent vehicle*"', '"self-driving"'],
        ['"motion prediction"', '"trajectory prediction"', '"behavior prediction"', 'predictor*', '"perceptual uncertainty"', '"prediction failure"'],
        ['"motion planning"', '"trajectory planning"', 'planner*', 'control', '"decision making"', '"collision risk*"'],
        ['"uncertainty propagation"', '"uncertainty-aware planning"', '"decision risk"', '"risk-aware planning"', '"risk-aware decision making"', '"risk estimation"', '"collision risk*"', '"chance constraint*"', '"safety constraint*"', '"prediction set*"', '"conformal prediction"'],
    ],
    "E": [
        ['"autonomous driving"', '"automated driving"', '"autonomous vehicle*"', '"intelligent vehicle*"', '"autonomous system*"'],
        ['survey', 'review', 'overview', '"unified view"'],
        ['uncertaint*', 'risk', 'calibrat*', '"conformal prediction"', '"runtime assurance"', '"runtime monitoring"', '"safety filter*"', '"safe control"', '"formal verification"', '"motion prediction"', 'planning'],
    ],
}


def render_group(database: str, terms: list[str], title_only: bool) -> str:
    joined = " OR ".join(terms)
    if database == "wos":
        return f"{'TI' if title_only else 'TS'}=({joined})"
    if database == "scopus":
        return f"{'TITLE' if title_only else 'TITLE-ABS-KEY'}({joined})"
    if database == "acm":
        return f"{'Title' if title_only else 'AllField'}:({joined})"
    field = '"Document Title"' if title_only else '"All Metadata"'
    return "(" + " OR ".join(f"{field}:{term}" for term in terms) + ")"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database", choices=("wos", "scopus", "ieee", "acm"), required=True)
    parser.add_argument("--query", choices=tuple(GROUPS), required=True)
    parser.add_argument("--year-end", type=int, default=2026)
    args = parser.parse_args()

    rendered = []
    for index, terms in enumerate(GROUPS[args.query]):
        rendered.append(render_group(args.database, terms, args.query == "E" and index == 1))
    query = " AND\n".join(rendered)
    if args.database == "scopus":
        query += f" AND\nPUBYEAR > 2017 AND PUBYEAR < {args.year_end + 1}"
    print(query)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
