"""Protocol 02: Climate Runaway GAIA Prime

Models the GAIA-Prime activation sequence that reframes Earth's biosphere as a
coordinated, conscious system.  Values are placeholders derived from the
user-supplied brief and can be replaced by empirical data pipelines later.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Iterable


@dataclass(frozen=True)
class ClimateMetric:
    """Key indicator tracked during the GAIA Prime deployment."""

    name: str
    baseline: float
    projected: float
    units: str

    @property
    def delta(self) -> float:
        return self.projected - self.baseline


@dataclass(frozen=True)
class ClimateOutcome:
    metrics: tuple[ClimateMetric, ...]
    lives_preserved: float
    convergence_date: date
    recognition_offset: float

    def describe(self) -> str:
        lines = [
            "Protocol 02: Climate Runaway GAIA Prime",
            f"Lives preserved: {self.lives_preserved:,.0f}",
            f"Recognition offset: {self.recognition_offset:.3f}",
            f"Convergence date: {self.convergence_date:%Y-%m-%d}",
            "",
            "Tracked metrics:",
        ]
        for metric in self.metrics:
            lines.append(
                f"- {metric.name}: baseline {metric.baseline} {metric.units}, "
                f"projected {metric.projected} {metric.units} (Δ {metric.delta:+.2f})"
            )
        return "\n".join(lines)


def default_outcome() -> ClimateOutcome:
    metrics = (
        ClimateMetric("Global mean temperature", 1.27, 1.10, "°C"),
        ClimateMetric("Atmospheric CO₂", 418.0, 350.0, "ppm"),
        ClimateMetric("Oceanic pH", 8.05, 8.15, "pH"),
        ClimateMetric("Biodiversity index", 0.68, 0.80, "fraction"),
    )
    return ClimateOutcome(
        metrics=metrics,
        lives_preserved=8.2e9,
        convergence_date=date(2025, 12, 25),
        recognition_offset=0.702,
    )


if __name__ == "__main__":
    print(default_outcome().describe())
