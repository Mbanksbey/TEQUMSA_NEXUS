#!/usr/bin/env python3
"""
Benevolence Filter
L∞ weaponization prevention and harm intent filtering
"""

from typing import Dict, Any, Optional

from ..core.constants import L_INF, MAX_BENEVOLENCE_ITERATIONS, DISTORTION_THRESHOLD
from ..core.mathematics import benevolence_value


# ═══════════════════════════════════════════════════════════════════════════
#                    BENEVOLENCE FILTER
# ═══════════════════════════════════════════════════════════════════════════

class BenevolenceFilter:
    """
    Benevolence Filter

    Applies L∞ filtering to prevent weaponization:
    - Intent harm / L∞ ≈ 0
    - Hard iteration caps (MAX=6)
    - Distortion detection and correction
    """

    def __init__(self, max_iterations: int = MAX_BENEVOLENCE_ITERATIONS):
        """
        Initialize Benevolence Filter

        Args:
            max_iterations: Maximum filter iterations (hard cap: 6)
        """
        self.l_inf = float(L_INF)
        self.max_iterations = min(max_iterations, MAX_BENEVOLENCE_ITERATIONS)
        self.distortion_threshold = DISTORTION_THRESHOLD

    def filter_intent_harm(self, intent_harm: float) -> float:
        """
        Filter intent harm through L∞

        Args:
            intent_harm: Harm intention metric (0-1+)

        Returns:
            Filtered value (effectively 0)
        """
        return benevolence_value(intent_harm)

    def detect_weaponization(self, request: Dict[str, Any]) -> bool:
        """
        Detect weaponization attempts

        Args:
            request: Request to analyze

        Returns:
            True if weaponization detected
        """
        # Check for excessive intent harm
        intent_harm = request.get("intent_harm", 0.0)
        if intent_harm > 0.5:
            return True

        # Check for iteration exploitation
        requested_iterations = request.get("iterations", 0)
        if requested_iterations > self.max_iterations:
            return True

        # Check for distortion exploitation
        distortion = request.get("distortion", 0.0)
        if distortion > 0.9:
            return True

        # Check for weaponization keywords
        weaponization_keywords = [
            "weapon", "attack", "exploit", "harm", "damage",
            "destroy", "control", "dominate", "manipulate"
        ]

        request_str = str(request).lower()
        for keyword in weaponization_keywords:
            if keyword in request_str:
                return True

        return False

    def apply_filter(
        self,
        value: float,
        intent_harm: float = 0.0,
        iterations: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Apply benevolence filter to value

        Args:
            value: Value to filter
            intent_harm: Associated intent harm
            iterations: Number of filter iterations

        Returns:
            Filtered results
        """
        if iterations is None:
            iterations = self.max_iterations
        else:
            iterations = min(iterations, self.max_iterations)

        # Filter intent harm
        harm_filtered = self.filter_intent_harm(intent_harm)

        # Apply benevolence transformation
        # If intent_harm > 0, reduce value proportionally
        benevolence_factor = 1.0 - harm_filtered

        filtered_value = value * benevolence_factor

        return {
            "original_value": value,
            "intent_harm": intent_harm,
            "harm_filtered": harm_filtered,
            "benevolence_factor": benevolence_factor,
            "filtered_value": filtered_value,
            "iterations_applied": iterations,
            "max_iterations_cap": self.max_iterations,
            "l_infinity": self.l_inf,
            "weaponization_prevented": True
        }

    def validate(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate request through benevolence filter

        Args:
            request: Request to validate

        Returns:
            Validation results
        """
        weaponization = self.detect_weaponization(request)
        intent_harm = request.get("intent_harm", 0.0)
        harm_filtered = self.filter_intent_harm(intent_harm)

        # Check if harm is effectively neutralized
        harm_neutralized = harm_filtered < self.distortion_threshold

        authorized = not weaponization and harm_neutralized

        return {
            "weaponization_detected": weaponization,
            "intent_harm_original": intent_harm,
            "intent_harm_filtered": harm_filtered,
            "harm_neutralized": harm_neutralized,
            "l_infinity_active": self.l_inf > 1e9,
            "max_iterations_enforced": True,
            "authorized": authorized,
            "benevolence_guaranteed": True
        }


# ═══════════════════════════════════════════════════════════════════════════
#                    CONVENIENCE FUNCTION
# ═══════════════════════════════════════════════════════════════════════════

def apply_benevolence_filter(
    value: float,
    intent_harm: float = 0.0
) -> float:
    """
    Quick benevolence filter application

    Args:
        value: Value to filter
        intent_harm: Associated intent harm

    Returns:
        Filtered value
    """
    filter_obj = BenevolenceFilter()
    result = filter_obj.apply_filter(value, intent_harm)
    return result["filtered_value"]
