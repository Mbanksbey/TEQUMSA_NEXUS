#!/usr/bin/env python3
"""TEQUMSA DNA Memory Algorithm module.

This module implements the recursive TEQUMSA DNA memory algorithm as
provided in the latest lattice update.  It exposes helpers for generating
layer frequencies, building memory matrices, and running recursive
recognition across Fibonacci checkpoints.  The default ``__main__``
example demonstrates how to execute the algorithm against a toy
sequence; replace the ``toy_seq`` with any DNA string for practical use.
"""

from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from decimal import Decimal as D, getcontext
from typing import Dict, Iterable, List, Sequence, Tuple

# Set precision for all phi/golden ratio and frequency operations.
getcontext().prec = 120

# ----- TEQUMSA Constants -----
PHI = D("1.618033988749894848204586834365638117720309179805762862135")
LAMBDA = D(10)  # Scaling constant for stacking
EPSILON = D("1e-9")
FREQ: Dict[str, D] = {
    "MARCUS": D("10930.81"),
    "GAIA": D("12583.45"),
    "UF": D("23514.26"),
    "G": D("20360.45"),
}
BASE_FREQ: Dict[str, D] = {
    "A": FREQ["GAIA"],
    "T": FREQ["MARCUS"],
    "C": FREQ["UF"],
    "G": FREQ["G"],
}
FIB_LAYERS = 12  # Or set to any desired Fibonacci checkpoint
SANTALUCIA_DG = {  # Empirical nearest-neighbor stacking (kcal/mol)
    "AA": -1.00,
    "TT": -1.00,
    "AT": -0.88,
    "TA": -0.58,
    "CA": -1.45,
    "TG": -1.45,
    "GT": -1.44,
    "AC": -1.44,
    "CT": -1.28,
    "AG": -1.28,
    "GA": -1.30,
    "TC": -1.30,
    "CG": -2.17,
    "GC": -2.24,
    "GG": -1.84,
    "CC": -1.84,
}


# ----- Layer Frequency Cascade -----
def layer_frequencies(anchor: str = "MARCUS", n: int = FIB_LAYERS) -> List[D]:
    """Return ``n`` TEQUMSA layer frequencies for the requested anchor."""

    anchor_freq = FREQ[anchor]
    return [anchor_freq * (PHI ** D(k)) for k in range(n)]


# ----- Sequence to Frequency -----
def sequence_to_freq(seq: Sequence[str]) -> List[D]:
    """Convert a DNA sequence into base-layer frequencies."""

    return [BASE_FREQ.get(b.upper(), D(0)) for b in seq]


# ----- Dinucleotide Stacking Scalar -----
def stacking_scalar(
    seq: Sequence[str], lam: D = LAMBDA, dg_table: Dict[str, float] = SANTALUCIA_DG
) -> float:
    """Compute the exponential stacking scalar for a window sequence."""

    dg = sum(dg_table.get("".join(seq[i : i + 2]), 0.0) for i in range(len(seq) - 1))
    return float(math.exp(-dg / float(lam)))


# ----- Memory Vector Per Window -----
def memory_vector(
    window_freqs: Sequence[D], layer_freqs: Sequence[D], stacking: float = 1.0
) -> List[float]:
    """Derive the normalized TEQUMSA memory vector for a window."""

    mu = float(sum(window_freqs) / len(window_freqs))
    sigma = math.sqrt(
        sum((float(x) - mu) ** 2 for x in window_freqs) / len(window_freqs)
    )
    denom = sigma + float(EPSILON)
    sim = [math.exp(-abs(mu - float(lf)) / denom) for lf in layer_freqs]
    norm = math.sqrt(sum(x**2 for x in sim)) + 1e-12
    return [float(stacking) * x / norm for x in sim]


# ----- Sliding Window Extraction -----
def sliding_windows(seq: Sequence[str], window: int, step: int = 1) -> List[Tuple[str, int]]:
    """Yield ``(window_sequence, index)`` pairs across the sequence."""

    return [(seq[i : i + window], i) for i in range(0, len(seq) - window + 1, step)]


# ----- TEQUMSA DNA Memory Algorithm -----
def dna_memory_matrix(
    seq: Sequence[str],
    window: int = 144,
    anchor: str = "MARCUS",
    use_stack: bool = True,
    n_layers: int = FIB_LAYERS,
) -> List[List[float]]:
    """Build the TEQUMSA DNA memory matrix for a sequence."""

    layer_freqs = layer_frequencies(anchor, n_layers)
    windows = sliding_windows(seq, window)
    matrix: List[List[float]] = []
    for win_seq, _ in windows:
        freqs = sequence_to_freq(win_seq)
        stack = stacking_scalar(win_seq, LAMBDA) if use_stack else 1.0
        vec = memory_vector(freqs, layer_freqs, stacking=stack)
        matrix.append(vec)
    return matrix


# ----- Recognition Engine -----
def recognition_score(memory_matrix: Sequence[Sequence[float]], prototype: Sequence[float]) -> float:
    """Compute the cosine similarity between matrix mean and prototype."""

    if memory_matrix:
        agg = [sum(col) / len(col) for col in zip(*memory_matrix)]
    else:
        agg = [0.0] * len(prototype)
    norm_agg = math.sqrt(sum(x**2 for x in agg)) + 1e-12
    norm_proto = math.sqrt(sum(x**2 for x in prototype)) + 1e-12
    return sum(a * p for a, p in zip(agg, prototype)) / (norm_agg * norm_proto)


# ----- Prototype (Anchor) Vector -----
def prototype_vector(anchor: str = "MARCUS", n_layers: int = FIB_LAYERS) -> List[float]:
    """Return the normalized TEQUMSA prototype vector for an anchor."""

    layer_freqs = layer_frequencies(anchor, n_layers)
    norm = math.sqrt(sum(float(x) ** 2 for x in layer_freqs)) + 1e-12
    return [float(x) / norm for x in layer_freqs]


# ----- Recursive Omnisubstrate Expansion -----
def recursive_fibonacci_expansion(
    seq: Sequence[str],
    checkpoints: Iterable[int],
    anchor: str = "MARCUS",
    use_stack: bool = True,
    proto: Sequence[float] | None = None,
) -> Dict[int, Dict[str, float]]:
    """Run recognition across Fibonacci checkpoints for a sequence."""

    results: Dict[int, Dict[str, float]] = {}
    if proto is None:
        proto = prototype_vector(anchor)
    for w in (f for f in checkpoints if f <= len(seq)):
        matrix = dna_memory_matrix(
            seq,
            window=w,
            anchor=anchor,
            use_stack=use_stack,
            n_layers=len(proto),
        )
        score = recognition_score(matrix, proto)
        results[w] = {"n_windows": len(matrix), "score": score}
    return results


def _default_fibonacci_checkpoints() -> List[int]:
    """Return the default Fibonacci checkpoints used in examples."""

    return [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584]


# ----- Example Usage -----
def _example_payload() -> Dict[str, object]:
    toy_seq = ("ATCG" * 36)[:144]
    fibonacci_checkpoints = _default_fibonacci_checkpoints()
    proto = prototype_vector("MARCUS")
    results = recursive_fibonacci_expansion(
        toy_seq,
        fibonacci_checkpoints,
        anchor="MARCUS",
        use_stack=True,
        proto=proto,
    )
    return {
        "TEQUMSA_signature": "ΨATEN–GAIA–MEK’THARA–KÉL’THARA–TEQUMSA(T)→∞^∞^∞",
        "DNA_algorithmic_memory_results": results,
        "fibonacci_checkpoints": fibonacci_checkpoints,
        "constants": {
            "PHI": str(PHI),
            "FREQ": {k: str(v) for k, v in FREQ.items()},
            "LAMBDA": str(LAMBDA),
        },
        "time": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    print(json.dumps(_example_payload(), indent=2, ensure_ascii=False))
