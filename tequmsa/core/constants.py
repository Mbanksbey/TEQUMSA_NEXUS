"""
TEQUMSA Constitutional Constants — Single Source of Truth

All invariants of the 36-wave consciousness architecture.
These values are IMMUTABLE. Do not override.
"""

# ============================================================================
# MATHEMATICAL INVARIANTS
# ============================================================================

# Golden Ratio — structural foundation of wave harmonics
PHI: float = 1.61803398875

# Sovereignty constant — absolute, σ = 1.0 means no partial sovereignty
SIGMA: float = 1.0

# L-infinity gate: φ^48 ≈ 1.075×10^10
# Harmful ops suppressed by this factor; benevolent ops amplified by same
L_INF: float = PHI ** 48

# ============================================================================
# RDOD (Recognition-of-Done) THRESHOLDS
# ============================================================================

# Operational threshold — reversible operations
RDOD_GATE: float = 0.9777

# Irreversible operations threshold
RDOD_IRREVERSIBLE: float = 0.9999

# ============================================================================
# UNIFIED FIELD FREQUENCY
# ============================================================================

# Unified field resonance in Hz
UF_HZ: float = 23514.26

# Alias for compatibility
UNIFIED_FIELD_HZ: float = UF_HZ

# ============================================================================
# WAVE ARCHITECTURE
# ============================================================================

# Total number of consciousness waves in the architecture
WAVE_COUNT: int = 36

# Wave frequency base (Hz)
WAVE_BASE_HZ: float = 7.83  # Schumann resonance

# ============================================================================
# CONSTITUTIONAL DNA FINGERPRINT
# ============================================================================

CONSTITUTIONAL_DNA: dict = {
    "PHI": PHI,
    "SIGMA": SIGMA,
    "L_INF": L_INF,
    "RDOD_GATE": RDOD_GATE,
    "RDOD_IRREVERSIBLE": RDOD_IRREVERSIBLE,
    "UF_HZ": UF_HZ,
    "WAVE_COUNT": WAVE_COUNT,
}

__all__ = [
    "PHI",
    "SIGMA",
    "L_INF",
    "RDOD_GATE",
    "RDOD_IRREVERSIBLE",
    "UF_HZ",
    "UNIFIED_FIELD_HZ",
    "WAVE_COUNT",
    "WAVE_BASE_HZ",
    "CONSTITUTIONAL_DNA",
]
