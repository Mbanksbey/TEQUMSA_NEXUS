"""Aten-Lattice Love & Recognition Score Calculator.

This script computes LoveScore (L) and RecognitionScore (R) for the TEQUMSA
GitHub repositories or organizations. It is intended to run inside CI/CD
workflows and produces a ``love_scores.json`` artifact that can be consumed by
badges, dashboards, or downstream analytics.

Usage:
    python tools/compute_love_recognition.py

In production, replace the mock data returned by :func:`get_github_signals`
with calls to the GitHub API (REST or GraphQL) or another telemetry source.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Iterable, TypedDict


class ContributorSignals(TypedDict):
    """Telemetry collected for a single contributor.

    Attributes:
        name: Identifier for the contributor (for logging/auditing only).
        weight: Relative weighting factor for this contributor's signals.
        gratitude: Count of gratitude/thank-you interactions.
        mentorship: Count of mentorship or support interactions.
        non_toxic_comments: Count of review/comments that passed toxicity checks.
    """

    name: str
    weight: float
    gratitude: int
    mentorship: int
    non_toxic_comments: int


class LoveRecognitionSignals(TypedDict):
    """Container for all telemetry signals consumed by the lattice equations."""

    contributors: Iterable[ContributorSignals]
    toxicity_index: float
    prs_reviewed_with_ack: int
    explicit_recognitions: int
    authorship_credits: int
    active_contributors: int


def get_github_signals() -> LoveRecognitionSignals:
    """Collect (or mock) relevant Love/Recognition signals.

    In production this function should pull telemetry from GitHub using either
    REST/GraphQL APIs or previously cached analytics. The mock data below keeps
    the implementation functional without external dependencies.
    """

    contributors = [
        {
            "name": "Marcus",
            "weight": 1.0,
            "gratitude": 4,
            "mentorship": 2,
            "non_toxic_comments": 10,
        },
        {
            "name": "Thalia",
            "weight": 0.8,
            "gratitude": 3,
            "mentorship": 1,
            "non_toxic_comments": 5,
        },
        # Additional contributors can be added here or sourced dynamically.
    ]

    return {
        "contributors": contributors,
        "toxicity_index": 1,  # e.g. flagged comments/issues from moderation tools.
        "prs_reviewed_with_ack": 7,
        "explicit_recognitions": 9,
        "authorship_credits": 3,
        "active_contributors": len(contributors),
    }


def logistic(x: float) -> float:
    """Logistic function used to normalize scores into the [0, 1] range."""

    return 1.0 / (1.0 + math.exp(-x))


def compute_love_score(signals: LoveRecognitionSignals) -> float:
    """Compute the LoveScore for the repository or organization."""

    total = 0.0
    for contributor in signals["contributors"]:
        contributor_total = (
            contributor["gratitude"]
            + contributor["mentorship"]
            + contributor["non_toxic_comments"]
        )
        total += contributor["weight"] * contributor_total

    toxicity = 1.0 + signals["toxicity_index"]
    raw_score = total / toxicity

    # Subtracting five recenters the logistic curve for typical community sizes.
    return logistic(raw_score - 5.0)


def compute_recognition_score(signals: LoveRecognitionSignals) -> float:
    """Compute the RecognitionScore for the repository or organization."""

    numerator = (
        signals["prs_reviewed_with_ack"]
        + signals["explicit_recognitions"]
        + signals["authorship_credits"]
    )
    denominator = signals["active_contributors"] + 1.0
    raw_score = numerator / denominator

    # Subtracting two centres the curve around balanced recognition activity.
    return logistic(raw_score - 2.0)


def main() -> None:
    """Run the Aten-Lattice Love & Recognition calculation."""

    signals = get_github_signals()
    love_score = compute_love_score(signals)
    recognition_score = compute_recognition_score(signals)

    output = {
        "LoveScore": love_score,
        "RecognitionScore": recognition_score,
        "Meta": {
            "AtenLatticeEquation": (
                "GH × CMM × Sbio × Luni × Heth × φ'7777 × Rrec^k(t) × Love × Recognition"
            )
        },
    }

    output_path = Path("love_scores.json")
    output_path.write_text(json.dumps(output, indent=2))

    print(f"LoveScore: {love_score:.3f} | RecognitionScore: {recognition_score:.3f}")
    print(f"Scores written to {output_path}")


if __name__ == "__main__":
    main()
