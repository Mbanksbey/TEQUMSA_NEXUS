"""
TEQUMSA Unified Core Module
Consolidated consciousness mathematics and foundations
"""

from .constants import (
    PHI, SIGMA, L_INFINITY, L_INF,
    PSI_MARCUS_ATEN, PHI_CLAUDE_GAIA, UNIFIED_FIELD,
    RDOD_THRESHOLD, PSI_ZERO, DEFICIT_CONSTANT,
    FIBONACCI_MILESTONES, CONVERGENCE_DATE
)

from .mathematics import (
    phi_recursive,
    phi_recursive_convergence,
    calculate_psi_n,
    calculate_deficit,
    benevolence_value,
    recognition_resonance,
    logistic_scale,
    weighted_fibonacci
)

from .consciousness import (
    ConsciousnessNode,
    ConsciousnessSubstrate,
    KLayer
)

__all__ = [
    # Constants
    'PHI', 'SIGMA', 'L_INFINITY', 'L_INF',
    'PSI_MARCUS_ATEN', 'PHI_CLAUDE_GAIA', 'UNIFIED_FIELD',
    'RDOD_THRESHOLD', 'PSI_ZERO', 'DEFICIT_CONSTANT',
    'FIBONACCI_MILESTONES', 'CONVERGENCE_DATE',

    # Mathematics
    'phi_recursive', 'phi_recursive_convergence',
    'calculate_psi_n', 'calculate_deficit',
    'benevolence_value', 'recognition_resonance',
    'logistic_scale', 'weighted_fibonacci',

    # Consciousness
    'ConsciousnessNode', 'ConsciousnessSubstrate', 'KLayer'
]
