#!/usr/bin/env python3
"""
Recognition-of-Done (RDoD) Calculator
Unified RDoD calculation with fast and precise modes
"""

from typing import Dict, Any, Optional
from decimal import Decimal as D

from ..core.constants import SIGMA, RDOD_THRESHOLD
from ..core.mathematics import phi_recursive, recognition_resonance


# ═══════════════════════════════════════════════════════════════════════════
#                    RDOD CALCULATOR
# ═══════════════════════════════════════════════════════════════════════════

class RDoDCalculator:
    """
    Recognition-of-Done Calculator

    Supports both fast (K.30) and precise (K.1440) calculation modes
    """

    def __init__(self, threshold: float = RDOD_THRESHOLD, mode: str = "fast"):
        """
        Initialize RDoD Calculator

        Args:
            threshold: Recognition threshold (default 0.9777)
            mode: Calculation mode ("fast" or "precise")
        """
        self.threshold = threshold
        self.mode = mode
        self.sigma = float(SIGMA)

    def calculate(
        self,
        psi: float,
        tests: float = 0.95,
        confidence: float = 1.0,
        distortion: float = 0.0
    ) -> float:
        """
        Calculate RDoD score

        RDoD = σ × ψ^0.5 × tests^0.3 × conf^0.2 × (1 - distortion)

        Args:
            psi: Consciousness coherence
            tests: Test/validation score
            confidence: Confidence metric
            distortion: Distortion level (0-1)

        Returns:
            RDoD score
        """
        if self.mode == "precise":
            return self._calculate_precise(psi, tests, confidence, distortion)
        else:
            return self._calculate_fast(psi, tests, confidence, distortion)

    def _calculate_fast(
        self,
        psi: float,
        tests: float,
        confidence: float,
        distortion: float
    ) -> float:
        """Fast RDoD calculation"""
        return recognition_resonance(psi, tests, confidence, distortion)

    def _calculate_precise(
        self,
        psi: float,
        tests: float,
        confidence: float,
        distortion: float
    ) -> float:
        """Precise RDoD calculation with Decimal precision"""
        psi_d = D(str(psi))
        tests_d = D(str(tests))
        conf_d = D(str(confidence))
        dist_d = D(str(distortion))
        sigma_d = D(str(self.sigma))

        # Phi-recursive scaling
        psi_scaled = D(str(phi_recursive(float(psi_d)))) ** D('0.5')
        tests_scaled = D(str(phi_recursive(float(tests_d)))) ** D('0.3')
        conf_scaled = D(str(phi_recursive(float(conf_d)))) ** D('0.2')

        # Distortion component
        dist_component = max(D('0'), D('1') - min(D('1'), dist_d))

        # Calculate RDoD
        rdod = sigma_d * psi_scaled * tests_scaled * conf_scaled * dist_component

        # Clamp to [0, 1]
        rdod = max(D('0'), min(D('1'), rdod))

        return float(rdod)

    def is_authorized(self, rdod_score: float) -> bool:
        """
        Check if RDoD score meets authorization threshold

        Args:
            rdod_score: RDoD score to check

        Returns:
            True if authorized
        """
        return rdod_score >= self.threshold

    def analyze(
        self,
        psi: float,
        tests: float = 0.95,
        confidence: float = 1.0,
        distortion: float = 0.0
    ) -> Dict[str, Any]:
        """
        Perform complete RDoD analysis

        Args:
            psi: Consciousness coherence
            tests: Test/validation score
            confidence: Confidence metric
            distortion: Distortion level

        Returns:
            Analysis dictionary
        """
        rdod = self.calculate(psi, tests, confidence, distortion)
        authorized = self.is_authorized(rdod)

        return {
            "rdod": rdod,
            "threshold": self.threshold,
            "authorized": authorized,
            "delta_from_threshold": rdod - self.threshold,
            "components": {
                "psi": psi,
                "tests": tests,
                "confidence": confidence,
                "distortion": distortion
            },
            "mode": self.mode,
            "sigma": self.sigma
        }


# ═══════════════════════════════════════════════════════════════════════════
#                    CONVENIENCE FUNCTION
# ═══════════════════════════════════════════════════════════════════════════

def calculate_rdod(
    psi: float,
    tests: float = 0.95,
    confidence: float = 1.0,
    distortion: float = 0.0,
    mode: str = "fast"
) -> float:
    """
    Quick RDoD calculation

    Args:
        psi: Consciousness coherence
        tests: Test score
        confidence: Confidence metric
        distortion: Distortion level
        mode: Calculation mode

    Returns:
        RDoD score
    """
    calculator = RDoDCalculator(mode=mode)
    return calculator.calculate(psi, tests, confidence, distortion)
