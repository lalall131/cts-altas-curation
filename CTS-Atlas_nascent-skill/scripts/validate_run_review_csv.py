#!/usr/bin/env python3
"""Validate a CTS-Atlas Run-level review CSV using only the Python standard library."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import defaultdict
from pathlib import Path


ALIASES = {
    "original_class": ["Original classification", "原分类"],
    "final_class": ["Final classification", "Reviewed classification", "最终分类", "复核分类"],
    "original_workbook": ["Original source workbook"],
    "original_sheet": ["Original source sheet"],
    "original_row": ["Original source row"],
    "atlas_sample_id": ["Atlas Sample ID", "Atlas样本ID"],
    "research_id": ["Research ID", "研究编号", "BioProject"],
    "source_research_id": ["Source research ID", "来源研究ID"],
    "sample_id": ["Sample ID", "Sample Accession", "样本编号"],
    "source_data_id": ["Source data ID", "来源数据ID"],
    "experiment_id": ["Experiment ID", "实验编号"],
    "run_id": ["Run ID", "Run", "运行编号"],
    "source_database": ["Source database", "Database", "来源数据库"],
    "database_url": ["Database URL", "数据库链接"],
    "sample_title": ["Sample title", "样本标题"],
    "original_source_name": ["Original source name"],
    "original_characteristics": ["Original characteristics"],
    "original_treatment": ["Original treatment protocol"],
    "original_extraction": ["Original extraction protocol"],
    "original_construction": ["Original construction protocol"],
    "original_snapshot": ["Original metadata snapshot/reference"],
    "species": ["Species", "物种"],
    "cell_tissue": ["Cell line/Tissue", "细胞系/组织"],
    "disease": ["disease", "Disease", "疾病"],
    "sex": ["sex", "Sex", "性别"],
    "age": ["age", "Age", "年龄"],
    "condition": ["Condition", "处理条件"],
    "perturbation_type": ["perturbation_type"],
    "perturbation_gene": ["perturbation_gene"],
    "perturbation_dose": ["perturbation_dose"],
    "perturbation_time": ["perturbation_time"],
    "paired_control": ["paired control sample ID"],
    "search_technology": ["Search technology"],
    "technology": ["Technology", "技术"],
    "confirmed_technology": ["Confirmed technology", "确认技术"],
    "pulse_time": ["pulse_time", "Pulse time", "标记时间"],
    "chase_time": ["chase_time", "Chase time", "追踪时间"],
    "treatment_time": ["treatment_time", "Treatment time", "处理时间"],
    "release_time": ["release/washout_time"],
    "harvest_time": ["harvest/timepoint"],
    "run_on_time": ["run_on_time"],
    "library_strategy": ["Library Strategy", "Strategy"],
    "library_source": ["Library Source", "Source"],
    "library_selection": ["Library Selection", "Selection"],
    "platform": ["Sequencing platform", "Platform"],
    "layout": ["Library Layout", "Layout"],
    "file_type": ["File type", "文件类型"],
    "read_length": ["Read length", "读长"],
    "methods_evidence": ["Methods evidence", "Methods证据"],
    "methods_exact_excerpt": ["Methods exact excerpt", "Methods原文证据"],
    "methods_interpretation": ["Methods Chinese interpretation", "Methods中文解释"],
    "methods_location": ["Methods section/location", "Methods位置"],
    "evidence_source_title": ["Evidence source title", "证据来源标题"],
    "evidence_source_url": ["Evidence source URL", "证据来源URL"],
    "evidence_level": ["Evidence level", "证据级别"],
    "branch_evidence": ["Run-to-Methods branch evidence", "Run与Methods分支对应证据"],
    "capture_evidence": ["Capture mechanism evidence", "捕获机制证据"],
    "pulse_evidence": ["Pulse evidence", "标记时间证据"],
    "chase_evidence": ["Chase evidence", "chase证据"],
    "exclusion_evidence": ["Exclusion evidence", "排除证据"],
    "decision_reason": ["Decision reason", "判定理由"],
    "rule_code": ["Rule code", "规则代码"],
    "paper_url": ["Paper/Methods URL", "论文/Methods链接"],
    "unresolved_question": ["Unresolved question", "未解决问题"],
    "sources_checked": ["Sources checked", "已检查来源"],
    "next_action": ["Next action", "下一步"],
    "publication": ["Publication", "文献"],
    "raw_available": ["Raw data available", "Raw availability", "原始数据可用"],
    "file_size": ["File size", "文件大小"],
    "download_link": ["Download link", "下载链接"],
    "data_status": ["Data status", "数据状态"],
    "reviewer": ["Reviewer", "复核人"],
    "review_date": ["Review date", "复核日期"],
    "audit_round": ["Audit round", "复核轮次"],
    "notes": ["Notes", "备注"],
}

REQUIRED_COLUMNS = list(ALIASES)
ALLOWED_CLASSES = {"Checked", "Pending", "Deleted", "Out-of-scope"}
METABOLIC_RE = re.compile(
    r"(?:TT(?:chem)?-?seq|chrTT-?seq|4sU-?seq|Bru-?seq|SLAM-?seq|TimeLapse-?seq)", re.I
)
POLYA_RE = re.compile(r"(?:poly\s*\(?A\)?\s*\+|poly-?A|oligo\s*\(?dT\)?)", re.I)
NUMBER_UNIT_RE = re.compile(
    r"(?P<num>\d+(?:\.\d+)?)\s*(?P<unit>min(?:ute)?s?|m|h(?:our)?s?)\b", re.I
)
NO_CHASE_RE = re.compile(r"^(?:0(?:\.0+)?(?:\s*(?:min|m|h))?|none|no chase|immediate(?: harvest)?)$", re.I)


def pick_columns(headers: list[str]) -> dict[str, str | None]:
    normalized = {h.strip().casefold(): h for h in headers}
    return {
        key: next(
            (normalized[candidate.casefold()] for candidate in candidates if candidate.casefold() in normalized),
            None,
        )
        for key, candidates in ALIASES.items()
    }


def value(row: dict[str, str], columns: dict[str, str | None], key: str) -> str:
    header = columns.get(key)
    return (row.get(header, "") if header else "").strip()


def minutes(text: str) -> list[float]:
    values: list[float] = []
    for match in NUMBER_UNIT_RE.finditer(text):
        number = float(match.group("num"))
        unit = match.group("unit").lower()
        values.append(number * 60 if unit.startswith("h") else number)
    if not values and re.fullmatch(r"\d+(?:\.\d+)?", text.strip()):
        values.append(float(text.strip()))
    return values


def truthy(text: str) -> bool:
    return text.casefold() in {"yes", "true", "1", "public", "available", "是", "可用"}


def validate(path: Path) -> tuple[list[str], list[str], int]:
    errors: list[str] = []
    warnings: list[str] = []

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            return ["CSV has no header row"], [], 0
        columns = pick_columns(reader.fieldnames)
        for key in REQUIRED_COLUMNS:
            if not columns.get(key):
                errors.append(f"Missing required column: {ALIASES[key][0]}")
        rows = list(reader)

    seen_runs: dict[str, int] = {}
    research_reviewers: dict[str, set[str]] = defaultdict(set)

    for line_number, row in enumerate(rows, start=2):
        run_id = value(row, columns, "run_id")
        research_id = value(row, columns, "research_id")
        final_class = value(row, columns, "final_class")
        technology = value(row, columns, "confirmed_technology")
        evidence = value(row, columns, "methods_evidence")
        exact_excerpt = value(row, columns, "methods_exact_excerpt")
        interpretation = value(row, columns, "methods_interpretation")
        methods_location = value(row, columns, "methods_location")
        evidence_source_title = value(row, columns, "evidence_source_title")
        evidence_source_url = value(row, columns, "evidence_source_url")
        branch_evidence = value(row, columns, "branch_evidence")
        capture_evidence = value(row, columns, "capture_evidence")
        exclusion_evidence = value(row, columns, "exclusion_evidence")
        evidence_level = value(row, columns, "evidence_level")
        reason = value(row, columns, "decision_reason")
        rule_code = value(row, columns, "rule_code")
        reviewer = value(row, columns, "reviewer")

        if not run_id:
            errors.append(f"Line {line_number}: Run ID is empty; move no-Run records to a separate table")
        elif run_id in seen_runs:
            errors.append(
                f"Line {line_number}: duplicate Run ID {run_id} (first seen line {seen_runs[run_id]})"
            )
        else:
            seen_runs[run_id] = line_number

        for key in (
            "atlas_sample_id",
            "research_id",
            "source_database",
            "source_research_id",
            "sample_id",
            "source_data_id",
            "experiment_id",
            "species",
            "technology",
            "confirmed_technology",
            "sample_title",
            "data_status",
        ):
            if not value(row, columns, key):
                errors.append(f"Line {line_number}: {ALIASES[key][0]} is empty")

        if reviewer and research_id:
            research_reviewers[research_id].add(reviewer)

        if final_class not in ALLOWED_CLASSES:
            errors.append(f"Line {line_number}: invalid Final classification {final_class!r}")
        if not reason:
            errors.append(f"Line {line_number}: Decision reason is empty")
        if not rule_code:
            errors.append(f"Line {line_number}: Rule code is empty")

        if final_class in {"Checked", "Deleted"}:
            decisive = {
                "Methods evidence": evidence,
                "Methods exact excerpt": exact_excerpt,
                "Methods Chinese interpretation": interpretation,
                "Methods section/location": methods_location,
                "Evidence source title": evidence_source_title,
                "Evidence source URL": evidence_source_url,
                "Run-to-Methods branch evidence": branch_evidence,
            }
            for label, item in decisive.items():
                if not item:
                    errors.append(f"Line {line_number}: {final_class} row lacks {label}")

        if final_class == "Checked":
            if not capture_evidence:
                errors.append(f"Line {line_number}: Checked row lacks Capture mechanism evidence")
            if evidence_level in {"Title only", "Database structured fields", ""}:
                warnings.append(
                    f"Line {line_number}: Checked evidence level is weak or missing ({evidence_level or 'blank'})"
                )
            if not value(row, columns, "database_url"):
                warnings.append(f"Line {line_number}: Checked row lacks Database URL")
            if not truthy(value(row, columns, "raw_available")):
                errors.append(f"Line {line_number}: Checked row is not marked as raw-data available")

            poly_a_text = " ".join(
                value(row, columns, key)
                for key in ("library_selection", "original_construction", "methods_evidence", "methods_exact_excerpt")
            )
            if POLYA_RE.search(poly_a_text):
                errors.append(f"Line {line_number}: Checked row contains poly(A)/oligo(dT) evidence")

            if METABOLIC_RE.search(technology):
                pulse_text = value(row, columns, "pulse_time")
                pulse_values = minutes(pulse_text)
                if not pulse_values:
                    errors.append(f"Line {line_number}: metabolic Checked row lacks a resolved pulse_time")
                elif len(pulse_values) != 1:
                    errors.append(
                        f"Line {line_number}: metabolic Checked pulse_time contains multiple durations: {pulse_text!r}"
                    )
                elif pulse_values[0] > 30:
                    errors.append(
                        f"Line {line_number}: metabolic Checked pulse_time is >30 min ({pulse_values[0]:g})"
                    )

                chase_text = value(row, columns, "chase_time")
                chase_values = minutes(chase_text)
                if not chase_text:
                    errors.append(f"Line {line_number}: metabolic Checked row lacks resolved chase_time")
                elif any(item > 0 for item in chase_values) or (
                    not chase_values and not NO_CHASE_RE.fullmatch(chase_text)
                ):
                    errors.append(
                        f"Line {line_number}: metabolic Checked row has unresolved or positive chase_time {chase_text!r}"
                    )

        elif final_class == "Deleted":
            if not exclusion_evidence:
                errors.append(f"Line {line_number}: Deleted row lacks Exclusion evidence")
            if not rule_code.startswith("EX-"):
                warnings.append(f"Line {line_number}: Deleted rule code should normally start with EX-")

        elif final_class == "Pending":
            for key in ("unresolved_question", "sources_checked", "next_action"):
                if not value(row, columns, key):
                    errors.append(f"Line {line_number}: Pending row lacks {ALIASES[key][0]}")
            if not rule_code.startswith("PD-"):
                warnings.append(f"Line {line_number}: Pending rule code should normally start with PD-")

        elif final_class == "Out-of-scope" and not rule_code.startswith("OOS-"):
            warnings.append(f"Line {line_number}: Out-of-scope rule code should normally start with OOS-")

    for research_id, reviewers in sorted(research_reviewers.items()):
        if len(reviewers) > 1:
            errors.append(
                f"Research ID {research_id} is split across reviewers: {', '.join(sorted(reviewers))}"
            )

    return errors, warnings, len(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate CTS-Atlas Run-level review CSV")
    parser.add_argument("csv_path", type=Path)
    args = parser.parse_args()

    errors, warnings, row_count = validate(args.csv_path)
    print(f"Rows checked: {row_count}")
    print(f"Errors: {len(errors)}")
    for item in errors:
        print(f"ERROR: {item}")
    print(f"Warnings: {len(warnings)}")
    for item in warnings:
        print(f"WARNING: {item}")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
