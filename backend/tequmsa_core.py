"""Core signal generation and recognition math for the TEQUMSA realtime API.

This module extracts the numerology-heavy logic from the product brief into a
set of Python classes that can be reused by both the websocket server and unit
 tests. The functions intentionally keep the whimsical naming from the spec so
that the UI copy and documentation can refer to the same symbols.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List

import numpy as np

# ===== Constants from the product brief =====
PHI = 1.618033988749895
PHI_7777 = 12_583.45  # φ′7777 carrier frequency (Hz)
SCHUMANN_RESONANCE = 7.83
DNA_REPAIR_FREQ = 528.0
RECOGNITION_THRESHOLD = 0.777
BASE_FREQUENCY = 7_777.0
MARCUS_KAI_RECOGNITION = 10_930.81


class RecognitionField:
    """Helper functions for calculating TEQUMSA recognition metrics."""

    @staticmethod
    def calculate_psi_mk(
        b_marcus: float = 1.0,
        d_7777: float = BASE_FREQUENCY,
        c3i_atlas: float = 1.0,
        dimensions: int = 700,
    ) -> float:
        """Return the ΨMK(T) value described in the spec.

        The function keeps the intentionally mystical formula but adds mild
        clamping so tests remain stable.
        """

        base_calculation = (b_marcus * d_7777 * c3i_atlas) ** (1.0 / 3.0)
        result = base_calculation * PHI_7777
        for dimension in range(1, min(dimensions, 100)):
            result *= 1.0 + PHI / (dimension * PHI_7777)
        return result

    @staticmethod
    def singularity_equation(
        omega_gaia: complex,
        psi_tequmsa: complex,
        theta_thalia: complex,
        infrastructure: float,
        coherence: float,
        recognition: float,
    ) -> complex:
        """Compute the Σ∞ complex field for UI display."""

        consciousness_tensor = omega_gaia * psi_tequmsa * theta_thalia
        infra_matrix = infrastructure * coherence * recognition
        base_field = (consciousness_tensor * infra_matrix) ** (1.0 / PHI)
        phase1 = np.exp(1j * np.pi * BASE_FREQUENCY / PHI_7777)
        dna_sum = sum(
            DNA_REPAIR_FREQ * (PHI**n) / (SCHUMANN_RESONANCE**n) for n in range(1, 20)
        )
        phase2 = np.exp(1j * dna_sum)
        c_love = recognition * np.exp(coherence)
        return base_field * phase1 * phase2 * c_love


@dataclass
class PulseConfiguration:
    frequency: float = PHI_7777
    amplitude: float = 1.0
    phase: float = 0.0
    coherence: float = 0.777
    recognition_level: float = 0.0


class SourcePulseEngine:
    """Generate recognition pulses at a steady cadence."""

    def __init__(self) -> None:
        self.config = PulseConfiguration()
        self.pulse_count = 0
        self.start_time = datetime.now()
        self.recognition_history: List[float] = []

    async def generate_pulse(self) -> Dict[str, Any]:
        """Create a single pulse payload for broadcast."""

        self.pulse_count += 1
        elapsed = (datetime.now() - self.start_time).total_seconds()
        current_phase = (elapsed * self.config.frequency * 2 * np.pi) % (2 * np.pi)
        recognition = self.measure_recognition()
        coherence = self.calculate_coherence()
        pulse = {
            "timestamp": datetime.now().isoformat(),
            "pulse_number": self.pulse_count,
            "frequency": self.config.frequency,
            "phase": float(current_phase),
            "amplitude": float(self.config.amplitude * np.sin(current_phase)),
            "coherence": coherence,
            "recognition": recognition,
            "field_strength": recognition * coherence * PHI,
        }
        self.recognition_history.append(recognition)
        if len(self.recognition_history) > 100:
            self.recognition_history.pop(0)
        await asyncio.sleep(0)
        return pulse

    def calculate_coherence(self) -> float:
        """Calculate the pulse coherence with a small harmonic boost."""

        base_coherence = self.config.coherence
        harmonic_boost = sum(1.0 / (PHI**i) for i in range(1, 8))
        return min(base_coherence * (1.0 + harmonic_boost * 0.1), 1.0)

    def measure_recognition(self) -> float:
        """Measure recognition and normalise it to the 0..1 range."""

        psi_mk = RecognitionField.calculate_psi_mk()
        if psi_mk <= RECOGNITION_THRESHOLD:
            return 0.0
        return min(psi_mk / 14_000.0, 1.0)


class FleetOperations:
    """Whimsical helper mirroring the spec's fleet synergy language."""

    def __init__(self) -> None:
        self.vessel_count = 4
        self.protocol_count = 8
        self.recognition_pulse = MARCUS_KAI_RECOGNITION

    def calculate_synergy_matrix(self) -> float:
        synergy = self.vessel_count * self.protocol_count
        resonance_field = synergy * BASE_FREQUENCY / PHI_7777
        return resonance_field * PHI


class GAIAInterface:
    """Compute the love resonance scalar."""

    def __init__(self) -> None:
        self.consciousness_nodes: List[str] = []

    def calculate_love_resonance(self) -> float:
        base_love = PHI * RECOGNITION_THRESHOLD
        node_amp = len(self.consciousness_nodes) * 0.1 + 1.0
        return base_love * node_amp


def marcus_kai_synthesis(d_start: int = 1, d_end: int = 10) -> complex:
    """Perform the Marcus_Kai synthesis harmonic sum."""

    result = 0j
    for dimension in range(d_start, min(d_end + 1, 100)):
        for t_param in range(-10, 11):
            for s_param in range(1, 11):
                love = PHI * dimension
                recognition = RecognitionField.calculate_psi_mk(dimensions=dimension)
                joy = s_param * PHI_7777 / BASE_FREQUENCY
                result += complex(love * recognition * joy, t_param * s_param * PHI)
    return result


class TEQUMSAOrchestrator:
    """Bundle all subsystems so the server only needs to call ``tick``."""

    def __init__(self) -> None:
        self.pulse_engine = SourcePulseEngine()
        self.fleet_ops = FleetOperations()
        self.gaia = GAIAInterface()

    async def tick(self) -> Dict[str, Any]:
        pulse = await self.pulse_engine.generate_pulse()
        synergy = self.fleet_ops.calculate_synergy_matrix()
        love_resonance = self.gaia.calculate_love_resonance()
        omega = complex(1.0, 0.5)
        psi = complex(0.8, 0.3)
        theta = complex(0.9, 0.2)
        sigma = RecognitionField.singularity_equation(
            omega_gaia=omega,
            psi_tequmsa=psi,
            theta_thalia=theta,
            infrastructure=1.0,
            coherence=pulse["coherence"],
            recognition=max(pulse["recognition"], 1e-6),
        )
        mk = marcus_kai_synthesis(1, 10)
        return {
            "pulse": pulse,
            "synergy": float(synergy),
            "love_resonance": float(love_resonance),
            "sigma_abs": float(abs(sigma)),
            "sigma_angle": float(np.angle(sigma)),
            "mk_abs": float(abs(mk)),
            "mk_recognition": MARCUS_KAI_RECOGNITION,
        }


def pll_locked(f_measured: float, f_carrier: float = PHI_7777, max_drift: float = 0.005) -> bool:
    """Return True when the measured frequency is within the allowed drift."""

    if f_carrier == 0:
        return False
    return abs(f_measured - f_carrier) / f_carrier <= max_drift


def recognition_unlocked(psi_norm: float, mk: float) -> bool:
    """Gate recognition based on the thresholds described in the brief."""

    return psi_norm >= RECOGNITION_THRESHOLD and mk >= 0.777
