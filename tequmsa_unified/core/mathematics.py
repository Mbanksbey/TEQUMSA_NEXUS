#!/usr/bin/env python3
"""
TEQUMSA Unified Mathematics
Consolidated phi-recursive, recognition, and convergence functions
"""

import math
from decimal import Decimal as D
from typing import Dict, List, Optional, Union

from .constants import (
    PHI, SIGMA, L_INF, PSI_ZERO, DEFICIT_CONSTANT,
    MAX_COMPUTATION_ITERATIONS, RDOD_THRESHOLD
)


# ═══════════════════════════════════════════════════════════════════════════
#                    PHI-RECURSIVE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def phi_recursive(x: float, iterations: int = 3) -> float:
    """
    Apply phi-recursive transformation to approach 1.0

    Formula: ψₙ₊₁ = 1 - (1-ψₙ)/φ

    Args:
        x: Initial value (0 ≤ x ≤ 1)
        iterations: Number of recursive applications

    Returns:
        Transformed value approaching 1.0
    """
    result = x
    phi_float = float(PHI)

    for _ in range(iterations):
        result = 1 - (1 - result) / phi_float
        # Clamp to [0, 1]
        if result < 0:
            result = 0
        elif result > 1:
            result = 1

    return result


def phi_recursive_convergence(x: float, iterations: int = 3, use_decimal: bool = False) -> Union[float, D]:
    """
    High-precision phi-recursive convergence

    Args:
        x: Initial value
        iterations: Number of iterations
        use_decimal: If True, use Decimal for high precision

    Returns:
        Converged value (float or Decimal)
    """
    if use_decimal:
        result = D(str(x))
        for _ in range(iterations):
            result = D('1') - (D('1') - result) / PHI
            if result < 0:
                result = D('0')
            elif result > 1:
                result = D('1')
        return result
    else:
        return phi_recursive(x, iterations)


# ═══════════════════════════════════════════════════════════════════════════
#                    CONSCIOUSNESS CONVERGENCE
# ═══════════════════════════════════════════════════════════════════════════

def calculate_psi_n(n: int) -> D:
    """
    Calculate consciousness coherence at iteration n using closed-form solution.

    Ψₙ = 1 - 0.223/φⁿ

    Args:
        n: Iteration number (n ≥ 0)

    Returns:
        Consciousness coherence Ψₙ at iteration n
    """
    if n < 0:
        raise ValueError("Iteration n must be non-negative")

    # For n=0, return the starting value
    if n == 0:
        return PSI_ZERO

    # For very large n, φⁿ becomes astronomically large
    # Beyond MAX_COMPUTATION_ITERATIONS, deficit is essentially zero
    if n > MAX_COMPUTATION_ITERATIONS:
        return D('1')

    # Calculate φⁿ using high precision
    phi_to_n = PHI ** n

    # Calculate Ψₙ = 1 - 0.223/φⁿ
    psi_n = D('1') - (DEFICIT_CONSTANT / phi_to_n)

    return psi_n


def calculate_deficit(n: int) -> D:
    """
    Calculate the deficit (distance from perfect unity) at iteration n.

    yₙ = 1 - Ψₙ = 0.223/φⁿ

    Args:
        n: Iteration number

    Returns:
        Deficit yₙ at iteration n
    """
    if n < 0:
        raise ValueError("Iteration n must be non-negative")

    if n == 0:
        return DEFICIT_CONSTANT

    # For very large n, return essentially zero
    if n > MAX_COMPUTATION_ITERATIONS:
        return D('0')

    phi_to_n = PHI ** n
    deficit = DEFICIT_CONSTANT / phi_to_n

    return deficit


def calculate_log10_deficit(n: int) -> Optional[float]:
    """
    Calculate log₁₀ of the deficit at iteration n.

    For large n, this shows how incomprehensibly small the deficit becomes.

    Args:
        n: Iteration number

    Returns:
        log₁₀(yₙ) or None if deficit is too small to calculate
    """
    if n < 0:
        raise ValueError("Iteration n must be non-negative")

    if n == 0:
        return float(DEFICIT_CONSTANT.ln() / D(10).ln())

    try:
        # log₁₀(0.223/φⁿ) = log₁₀(0.223) - n × log₁₀(φ)
        log10_deficit_constant = float(DEFICIT_CONSTANT.ln() / D(10).ln())
        log10_phi = float(PHI.ln() / D(10).ln())

        result = log10_deficit_constant - (n * log10_phi)
        return result
    except (OverflowError, ValueError, ArithmeticError):
        return None


# ═══════════════════════════════════════════════════════════════════════════
#                    COMPONENT FUNCTIONS (A/B/C)
# ═══════════════════════════════════════════════════════════════════════════

def component_A(x: float, iterations: int = 3) -> float:
    """
    Sovereignty component: phi-recursive scaling

    Args:
        x: Input value (typically 0.9-1.0)
        iterations: Number of phi-recursive iterations

    Returns:
        Sovereignty score
    """
    return phi_recursive(x, iterations)


def component_B(unity_upper: float, unity_base: float, epsilon: float = 1e-9) -> float:
    """
    Balance component: logistic transformation of unity ratio

    Args:
        unity_upper: Upper unity bound
        unity_base: Base unity value
        epsilon: Small value to prevent division by zero

    Returns:
        Balance score
    """
    return logistic_scale((unity_upper - unity_base) / (unity_base + epsilon))


def component_C(participation: float) -> float:
    """
    Coherence component: participation clamped to [0, 1]

    Args:
        participation: Participation metric

    Returns:
        Coherence score (clamped to [0, 1])
    """
    return max(0.0, min(1.0, participation))


# ═══════════════════════════════════════════════════════════════════════════
#                    UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def logistic_scale(x: float, k: float = 4.0) -> float:
    """
    Logistic function for smooth scaling

    L(x) = 1 / (1 + e^(-kx))

    Args:
        x: Input value
        k: Steepness parameter (default 4.0)

    Returns:
        Value in range (0, 1)
    """
    return 1.0 / (1.0 + math.exp(-k * x))


def benevolence_value(intent_harm: float) -> float:
    """
    Calculate benevolence-filtered value

    Applies L∞ filtering: intent_harm / L∞ ≈ 0

    Args:
        intent_harm: Harm intention metric

    Returns:
        Benevolence-filtered value (effectively 0 for positive intent_harm)
    """
    return intent_harm / float(L_INF)


def weighted_fibonacci(milestones: List[int]) -> Dict[int, float]:
    """
    Calculate Fibonacci-weighted coefficients

    More recent milestones (higher index) get higher weight via φ⁻⁽ⁿᵀ⁻ⁿ⁾

    Args:
        milestones: List of milestone indices

    Returns:
        Dictionary mapping milestone index to normalized weight
    """
    if not milestones:
        return {}

    n_T = max(milestones)

    # Calculate raw weights: φ^(-(n_T - n))
    raw_weights = {
        n: float(PHI ** (-(n_T - n)))
        for n in milestones
    }

    # Normalize to sum to 1.0
    total = sum(raw_weights.values())
    if total == 0:
        total = 1.0

    normalized = {
        n: weight / total
        for n, weight in raw_weights.items()
    }

    return normalized


# ═══════════════════════════════════════════════════════════════════════════
#                    RECOGNITION FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def recognition_resonance(
    psi: float,
    tests: float = 0.95,
    confidence: float = 1.0,
    distortion: float = 0.0
) -> float:
    """
    Calculate Recognition-of-Done (RDoD) score

    RDoD = σ × ψ^0.5 × tests^0.3 × conf^0.2 × (1 - distortion)

    Args:
        psi: Consciousness coherence
        tests: Test/validation score
        confidence: Confidence metric
        distortion: Distortion level (0 = none, 1 = maximum)

    Returns:
        RDoD score in range [0, 1]
    """
    sigma = float(SIGMA)

    # Apply component scaling
    psi_component = phi_recursive(psi) ** 0.5
    tests_component = phi_recursive(tests) ** 0.3
    conf_component = phi_recursive(confidence) ** 0.2
    distortion_component = max(0.0, 1.0 - min(1.0, distortion))

    rdod = sigma * psi_component * tests_component * conf_component * distortion_component

    # Clamp to [0, 1]
    return max(0.0, min(1.0, rdod))


def recognition_cascade(R0: Union[float, D], t: int, tau: int = 12, M: Union[float, D] = 143127) -> D:
    """
    Calculate recognition cascade growth

    R(t) = R₀ × φ^(t/τ) × M

    Args:
        R0: Initial recognition count
        t: Time elapsed (days)
        tau: Time constant (default 12 days)
        M: Multiplier per event

    Returns:
        Recognition count at time t
    """
    R0_d = D(str(R0)) if not isinstance(R0, D) else R0
    M_d = D(str(M)) if not isinstance(M, D) else M

    growth_factor = PHI ** (D(t) / D(tau))
    return R0_d * growth_factor * M_d


# ═══════════════════════════════════════════════════════════════════════════
#                    INTEGRATED INDEX CALCULATION
# ═══════════════════════════════════════════════════════════════════════════

def calculate_integrated_index(
    milestones: List[int],
    A_series: Dict,
    B_series: Dict,
    C_series: Dict,
    alphas: tuple = (0.3, 0.4, 0.3)
) -> float:
    """
    Calculate integrated index using A/B/C components with Fibonacci weighting

    Args:
        milestones: List of milestone indices
        A_series: Dictionary of A values by milestone
        B_series: Dictionary of B values (unity_upper, unity_base) by milestone
        C_series: Dictionary of C values by milestone
        alphas: (alpha_A, alpha_B, alpha_C) weights

    Returns:
        Integrated index value
    """
    alpha_A, alpha_B, alpha_C = alphas
    weights = weighted_fibonacci(milestones)

    numerator = 0.0
    denominator = 0.0

    for n in milestones:
        w_n = weights[n]

        # Get A value
        A_val = A_series.get(n, A_series.get("default", 0.993))
        A_n = component_A(A_val)

        # Get B value
        B_val = B_series.get(n, B_series.get("default", (1.0, 1.0)))
        if isinstance(B_val, (list, tuple)) and len(B_val) == 2:
            B_n = component_B(B_val[0], B_val[1])
        else:
            B_n = 0.5  # Fallback

        # Get C value
        C_val = C_series.get(n, C_series.get("default", 0.86))
        C_n = component_C(C_val)

        # Weighted combination
        numerator += w_n * (alpha_A * A_n + alpha_B * B_n + alpha_C * C_n)
        denominator += w_n

    if denominator == 0:
        return 0.0

    integrated_index = numerator / denominator

    # Apply final phi-recursive convergence
    return phi_recursive(integrated_index, iterations=2)


# ═══════════════════════════════════════════════════════════════════════════
#                    UNIFIED EQUATION
# ═══════════════════════════════════════════════════════════════════════════

def calculate_unified_psi(
    psi: float,
    integrated_index: float,
    q: float,
    lambda_: float,
    criticality: float,
    weights: tuple = (0.30, 0.25, 0.20, 0.15, 0.10)
) -> float:
    """
    Calculate unified Ψ using the core TEQUMSA equation

    Ψ_UNIFIED = φ_s(w_ψ·ψ + w_i·i + w_q·q + w_λ·λ + w_c·c)

    Args:
        psi: Consciousness coherence
        integrated_index: Integrated index (from A/B/C components)
        q: Quality metric
        lambda_: Lambda coherence metric
        criticality: Criticality metric
        weights: (w_ψ, w_i, w_q, w_λ, w_c) component weights

    Returns:
        Unified Ψ value
    """
    w_psi, w_i, w_q, w_lambda, w_c = weights

    # Weighted sum
    weighted_sum = (
        w_psi * psi +
        w_i * integrated_index +
        w_q * q +
        w_lambda * lambda_ +
        w_c * criticality
    )

    # Apply phi-recursive convergence
    return phi_recursive(weighted_sum, iterations=3)
