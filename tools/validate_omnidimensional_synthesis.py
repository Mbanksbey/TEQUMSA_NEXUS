"""Validate omnidimensional synthesis dataset and emit a CSV report."""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Any, Dict, Iterable, Tuple


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "omnidimensional_synthesis.json"
REPORT_PATH = ROOT / "validation_report.csv"


class CheckResult:
    def __init__(self, name: str, passed: bool, expected: str, observed: str) -> None:
        self.name = name
        self.passed = passed
        self.expected = expected
        self.observed = observed

    def as_row(self) -> Tuple[str, str, str, str]:
        return (self.name, "PASS" if self.passed else "FAIL", self.expected, self.observed)


def approx_equal(a: float, b: float, rel_tol: float = 1e-4, abs_tol: float = 1e-6) -> bool:
    return math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)


def load_payload() -> Dict[str, Any]:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Unable to locate synthesis dataset at {DATA_PATH}")
    with DATA_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate(payload: Dict[str, Any]) -> Iterable[CheckResult]:
    freq = payload["frequencies"]
    anchor = freq["marcus_anchor_hz"]
    threshold = freq["recognition_threshold"]
    ratio = anchor / threshold
    yield CheckResult(
        "Marcus anchor ratio",
        approx_equal(ratio, payload["integration_proof"]["marcus_anchor_threshold_ratio"]),
        "14,067.97× threshold",
        f"{ratio:,.2f}×",
    )

    ladder = freq["harmonic_ladder"]
    multipliers = {
        "Human Base": ladder["base_multiplier"],
        "Trinity": ladder["trinity_multiplier"],
        "Sacred Seven": ladder["sacred_seven_multiplier"],
        "Double Sacred": ladder["double_sacred_multiplier"],
        "Type III": ladder["type_three_multiplier"],
    }
    expected_freqs = {
        "Human Base": anchor,
        "Trinity": 32792.43,
        "Sacred Seven": 76515.67,
        "Double Sacred": 841672.37,
        "Type III": payload["integration_proof"]["type_three_frequency_hz"],
    }
    for name, multiplier in multipliers.items():
        calculated = anchor * multiplier
        yield CheckResult(
            f"{name} frequency",
            approx_equal(calculated, expected_freqs[name]),
            f"{expected_freqs[name]:,.2f} Hz",
            f"{calculated:,.2f} Hz",
        )

    nodes = payload["galactic_network"]["nodes"]
    arithmetic_sum = sum(node["frequency_hz"] for node in nodes)
    expected_sum = 180_459.43
    yield CheckResult(
        "Galactic network arithmetic sum",
        approx_equal(arithmetic_sum, expected_sum),
        f"{expected_sum:,.2f} Hz",
        f"{arithmetic_sum:,.2f} Hz",
    )

    claimed_total = payload["galactic_network"]["claimed_total_resonance_hz"]
    yield CheckResult(
        "Galactic network claimed total",
        approx_equal(claimed_total, 156_346.19),
        "156,346.19 Hz",
        f"{claimed_total:,.2f} Hz",
    )

    comets = payload["cometary_amplification"]["comets"]
    total_coupling = sum(comet["coupling_units"] for comet in comets)
    expected_coupling = payload["cometary_amplification"]["total_coupling_units"]
    yield CheckResult(
        "Cometary coupling total",
        approx_equal(total_coupling, expected_coupling),
        f"{expected_coupling:.2f} units",
        f"{total_coupling:.2f} units",
    )

    amplification = payload["cometary_amplification"]["field_amplification_multiplier"]
    effective_anchor = anchor * amplification
    yield CheckResult(
        "Effective anchor frequency",
        approx_equal(effective_anchor, 470_024.83, rel_tol=1e-5),
        "470,024.83 Hz",
        f"{effective_anchor:,.2f} Hz",
    )

    field_strength = payload["field_strength"]["unified_field_units"]
    threshold_units = payload["field_strength"]["galactic_threshold_units"]
    ratio_units = field_strength / threshold_units
    expected_ratio = 1_030_573_487_773
    yield CheckResult(
        "Unified field to threshold ratio",
        approx_equal(ratio_units, expected_ratio, rel_tol=1e-6),
        f"{expected_ratio:,.0f}×",
        f"{ratio_units:,.0f}×",
    )

    certainty = payload["convergence"]["certainty_percent"]
    yield CheckResult(
        "Convergence certainty",
        approx_equal(certainty, payload["integration_proof"]["convergence_certainty_percent"]),
        "98.4%",
        f"{certainty:.1f}%",
    )


def write_report(results: Iterable[CheckResult]) -> int:
    rows = list(results)
    with REPORT_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["check", "status", "expected", "observed"])
        for row in rows:
            writer.writerow(row.as_row())
    return sum(1 for row in rows if row.passed)


def main() -> None:
    payload = load_payload()
    results = list(validate(payload))
    passed = write_report(results)
    total = len(results)
    for result in results:
        status = "✅" if result.passed else "❌"
        print(f"{status} {result.name}: expected {result.expected} — observed {result.observed}")
    print(f"\n{passed}/{total} checks passed. Report written to {REPORT_PATH.relative_to(ROOT)}")
    if passed != total:
        raise SystemExit("Validation failed: see validation_report.csv for details")


if __name__ == "__main__":
    main()
