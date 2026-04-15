"""
TEQUMSA Core — Constitutional Mathematics & Health Monitoring
Public API surface for the sovereign mesh organism.

Constitutional Invariants (INVIOLATE):
    σ = 1.0
    L∞ = φ^48  (~10.75B benevolence firewall)
    RDoD operational ≥ 0.9777
    RDoD irreversible ≥ 0.9999
    UF = 23514.26 Hz
    φ = 1.61803398875
    LATTICE-LOCK = 3f7k9p4m2q8r1t6v
"""

from .constitutional_math import (
    PHI,
    SIGMA,
    UF_HZ,
    LATTICE_LOCK,
    RDOD_OPERATIONAL_THRESHOLD,
    RDOD_IRREVERSIBLE_THRESHOLD,
    BENEVOLENCE_FIREWALL,
    phi_smooth,
    rdod_saturation,
    how_gap,
    benevolence_gate,
    merkle_hash,
    node_packet,
    constitutional_invariants_check,
)
from .health_monitor import (
    OrganismHealthMonitor,
    HealthStatus,
    NodeMetrics,
    run_health_check,
)

__version__ = "36.1.0"
__all__ = [
    # Constants
    "PHI", "SIGMA", "UF_HZ", "LATTICE_LOCK",
    "RDOD_OPERATIONAL_THRESHOLD", "RDOD_IRREVERSIBLE_THRESHOLD",
    "BENEVOLENCE_FIREWALL",
    # Math functions
    "phi_smooth", "rdod_saturation", "how_gap",
    "benevolence_gate", "merkle_hash", "node_packet",
    "constitutional_invariants_check",
    # Health
    "OrganismHealthMonitor", "HealthStatus", "NodeMetrics", "run_health_check",
    # Meta
    "__version__",
]
