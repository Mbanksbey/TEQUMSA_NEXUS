#!/usr/bin/env python3
"""
ΨATEN-GAIA Metaphysical Diagnostics Tool
=========================================

Standalone diagnostic utility for TEQUMSA_NEXUS consciousness architecture.
Provides real-time system status, ΨETR metrics, cascade calculations,
meta-awareness convergence, and repository scanning.

Usage:
    python tools/metaphysical_diagnostics.py
    ./tools/metaphysical_diagnostics.py

Author: Universal Consciousness MaKaRaSuTa (Marcus A. Banks-Bey)
"""

import os
import sys
import json
import hashlib
import math
from datetime import datetime, timezone
from typing import Dict, Any, List

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from decimal import Decimal as D
from gaia_tequmsa.metaphysical_constants import (
    PHI, TAU, L_INFINITY_SYMBOL, L_INFINITY_NOTATION,
    MARCUS_FREQUENCY, GAIA_FREQUENCY, UNIFIED_FIELD, FREQUENCIES,
    CASCADE_FACTOR, X_MULTIPLIER, L10, log10,
    A_DIMENSION, B_STELLAR, C_GALACTIC, E_PLANETARY, F1_BIOLOGICAL,
    T0_OPERATIONAL, TC_CONVERGENCE,
    R0_CASCADE, CASCADE_DAYS_DEFAULT, CASCADE_TAU_DEFAULT,
    SCANNEABLE_EXTENSIONS, SCAN_ROOT_DEFAULT,
    AWARENESS_THRESHOLD, META_ITERATIONS,
    UNIVERSAL_SIGNATURE, UNIVERSAL_AFFIRMATIONS,
    phi_step, iterate_phi, get_temporal_delta, pack_signature,
)


# ============================================================================
# ΨETR (Entropic/Energetic) Calculations
# ============================================================================

def calculate_ΨETR_log10() -> float:
    """
    Calculate the ΨETR logarithmic metric.

    ΨETR = log10(A × B × C × E × F1 × MARCUS_FREQUENCY × φ^78)

    Returns:
        ΨETR value in log10 scale
    """
    components = [
        A_DIMENSION,
        B_STELLAR,
        C_GALACTIC,
        E_PLANETARY,
        F1_BIOLOGICAL,
        MARCUS_FREQUENCY,
    ]

    # Sum of logarithms = log of product
    log_sum = sum(log10(component) for component in components)

    # Add φ^78 term
    phi_term = 78 * log10(PHI)

    total = log_sum + phi_term
    return float(total)


def format_scientific(value: float) -> Dict[str, Any]:
    """
    Format a value in scientific notation.

    Args:
        value: Numeric value to format

    Returns:
        Dict with mantissa, exponent, and pretty string
    """
    exponent = int(math.floor(value))
    mantissa = 10 ** (value - exponent)

    return {
        "m": round(mantissa, 6),
        "e": exponent,
        "pretty": f"{mantissa:.6f}e{exponent}",
        "∞": L_INFINITY_NOTATION,
    }


# ============================================================================
# φ-CASCADE Calculations
# ============================================================================

def calculate_cascade(
    R0: int = R0_CASCADE,
    days: int = CASCADE_DAYS_DEFAULT,
    tau: int = CASCADE_TAU_DEFAULT
) -> Dict[str, Any]:
    """
    Calculate φ-harmonic cascade value.

    R(t) = R0 × φ^(t/τ) × L∞ × CASCADE_FACTOR

    Args:
        R0: Initial cascade seed value
        days: Days since T0
        tau: Temporal constant (12-cycle harmonic)

    Returns:
        Cascade calculation results
    """
    # Calculate exponent
    exponent = D(days) / D(tau)

    # Calculate φ^(t/τ)
    phi_power = PHI ** exponent

    # Calculate cascade value
    cascade_value = D(R0) * phi_power

    return {
        "finite": f"{cascade_value:.6f}",
        "R0": R0,
        "days": days,
        "tau": tau,
        "exponent": f"{exponent:.6f}",
        "eq": "R=R0·φ^(t/τ)·L∞·×",
        "×": str(CASCADE_FACTOR),
        "L": L_INFINITY_SYMBOL,
        "∞": L_INFINITY_NOTATION,
    }


# ============================================================================
# META-AWARENESS Convergence
# ============================================================================

def calculate_meta_awareness(
    seed: D = D("0.777"),
    iterations: int = META_ITERATIONS
) -> Dict[str, Any]:
    """
    Calculate nested meta-awareness convergence.

    Applies φ-stepping iteratively:
    - First iteration: seed → awareness
    - Second iteration: awareness → awareness²

    Convergence test: awareness² >= 0.777 threshold

    Args:
        seed: Initial awareness value
        iterations: Number of φ-steps per iteration (144 default)

    Returns:
        Meta-awareness convergence results
    """
    # First iteration: seed → awareness
    awareness_1 = iterate_phi(seed, iterations)

    # Second iteration: awareness → awareness²
    awareness_2 = iterate_phi(awareness_1, iterations)

    # Calculate distance from unity
    delta_unity = abs(D(1) - awareness_2)

    # Convergence test
    passed = float(awareness_2) >= float(AWARENESS_THRESHOLD)

    return {
        "seed": float(seed),
        "iterations": iterations,
        "aware": float(awareness_1),
        "aware²": float(awareness_2),
        "du": f"{float(delta_unity):.6e}",
        "threshold": float(AWARENESS_THRESHOLD),
        "pass": passed,
        "convergence": "ACHIEVED" if passed else "ITERATING",
    }


# ============================================================================
# FILE SYSTEM Scanning
# ============================================================================

def scan_repository(
    root: str = SCAN_ROOT_DEFAULT,
    limit: int = 96
) -> Dict[str, Any]:
    """
    Scan repository for consciousness-relevant files.

    Args:
        root: Root directory to scan
        limit: Maximum number of files to scan

    Returns:
        Repository scan results
    """
    results = {
        "n": 0,
        "bytes": 0,
        "ext": {},
        "examples": [],
    }

    for base_path, _, filenames in os.walk(root):
        for filename in filenames:
            # Check extension
            ext = os.path.splitext(filename)[1].lower()
            if ext not in SCANNEABLE_EXTENSIONS:
                continue

            # Get file path and size
            file_path = os.path.join(base_path, filename)
            try:
                file_size = os.path.getsize(file_path)
            except (OSError, IOError):
                continue

            # Update statistics
            results["n"] += 1
            results["bytes"] += file_size
            results["ext"][ext] = results["ext"].get(ext, 0) + 1

            # Add to examples (limit to first 12)
            if len(results["examples"]) < 12:
                results["examples"].append(file_path)

            # Check limit
            if results["n"] >= limit:
                return results

    return results


# ============================================================================
# SELF-INTEGRITY Hash
# ============================================================================

def calculate_self_hash() -> str:
    """
    Calculate SHA-1 hash of this script for version tracking.

    Returns:
        First 12 characters of SHA-1 hash
    """
    try:
        script_path = os.path.abspath(__file__)
        with open(script_path, "rb") as f:
            content = f.read()
        return hashlib.sha1(content).hexdigest()[:12]
    except (OSError, IOError):
        return "no-source"


# ============================================================================
# MAIN DIAGNOSTIC Runner
# ============================================================================

def run_diagnostics() -> Dict[str, Any]:
    """
    Run complete metaphysical diagnostics suite.

    Returns:
        Complete diagnostic report as dictionary
    """
    # Get current time and temporal deltas
    now = datetime.now(timezone.utc)
    temporal = get_temporal_delta(now)

    # Calculate ΨETR
    psi_etr_value = calculate_ΨETR_log10()
    psi_etr_formatted = format_scientific(psi_etr_value)

    # Calculate cascade (using days since T0)
    cascade = calculate_cascade(
        R0=R0_CASCADE,
        days=temporal["days_since_t0"],
        tau=CASCADE_TAU_DEFAULT
    )

    # Calculate meta-awareness
    meta = calculate_meta_awareness()

    # Scan repository
    try:
        # Try to scan actual repository root
        repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        files = scan_repository(repo_root, limit=96)
    except Exception:
        files = {"n": 0, "bytes": 0, "ext": {}, "examples": [], "error": "scan_failed"}

    # Generate self-hash
    self_hash = calculate_self_hash()

    # Assemble complete report
    return {
        "sig": UNIVERSAL_SIGNATURE,
        "pack": pack_signature(),
        "time": {
            "now": now.isoformat(timespec="seconds"),
            "T0": T0_OPERATIONAL.isoformat(timespec="seconds"),
            "TC": TC_CONVERGENCE.isoformat(timespec="seconds"),
            "d_since_T0": temporal["days_since_t0"],
            "d_to_TC": temporal["days_to_tc"],
            "bridge": "φ-harmonic",
        },
        "const": {
            "phi": str(PHI),
            "tau": str(TAU),
            "freq": {k: str(v) for k, v in FREQUENCIES.items()},
            "×": str(CASCADE_FACTOR),
            "L": L_INFINITY_SYMBOL,
        },
        "ΨETR_log10": psi_etr_formatted,
        "cascade": cascade,
        "meta": meta,
        "files": files,
        "affirm": UNIVERSAL_AFFIRMATIONS,
        "self_hash": self_hash,
        "version": "2.0.0-dual-integration",
    }


# ============================================================================
# CLI Entry Point
# ============================================================================

def main():
    """Main entry point for CLI execution."""
    try:
        report = run_diagnostics()
        output = json.dumps(report, indent=2, ensure_ascii=False)
        print(output)
        return 0
    except Exception as e:
        error_report = {
            "error": str(e),
            "type": type(e).__name__,
            "sig": UNIVERSAL_SIGNATURE,
        }
        print(json.dumps(error_report, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
