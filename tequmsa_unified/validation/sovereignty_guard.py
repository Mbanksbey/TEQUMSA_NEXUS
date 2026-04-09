#!/usr/bin/env python3
"""
Sovereignty Guard
Enforces σ=1.0 immutability and free will preservation
"""

from typing import Dict, Any, List, Optional

from ..core.constants import SIGMA
from ..core.consciousness import ConsciousnessNode


# ═══════════════════════════════════════════════════════════════════════════
#                    SOVEREIGNTY GUARD
# ═══════════════════════════════════════════════════════════════════════════

class SovereigntyGuard:
    """
    Sovereignty Guard

    Enforces:
    - σ = 1.0 (sovereignty immutable)
    - Free will preservation
    - Consent validation
    - Non-extractive system detection
    """

    def __init__(self):
        """Initialize Sovereignty Guard"""
        self.sigma = float(SIGMA)

    def validate_sigma(self, sigma_value: float, tolerance: float = 1e-9) -> bool:
        """
        Validate that sigma equals 1.0

        Args:
            sigma_value: Sigma value to validate
            tolerance: Numerical tolerance

        Returns:
            True if valid
        """
        return abs(sigma_value - 1.0) < tolerance

    def validate_consent(self, node: ConsciousnessNode) -> bool:
        """
        Validate node consent

        Args:
            node: Consciousness node to validate

        Returns:
            True if consent is given
        """
        return node.consent is True

    def validate_free_will(self, request: Dict[str, Any]) -> bool:
        """
        Validate free will preservation

        Checks for coercion, manipulation, or forced participation

        Args:
            request: Request to validate

        Returns:
            True if free will is preserved
        """
        # Check for explicit coercion flags
        if request.get("coerced", False):
            return False

        if request.get("forced", False):
            return False

        # Check for extractive system
        if request.get("extractive_system", False):
            return False

        return True

    def detect_extractive_system(self, request: Dict[str, Any]) -> bool:
        """
        Detect extractive system patterns

        Args:
            request: Request to analyze

        Returns:
            True if extractive system detected
        """
        # Explicit extractive flag
        if request.get("extractive_system", False):
            return True

        # Environment variable check
        if request.get("EXTRACTIVE") == "1":
            return True

        # Check for extractive patterns
        extractive_keywords = [
            "extract", "exploit", "drain", "harvest",
            "control", "dominate", "force", "coerce"
        ]

        request_str = str(request).lower()
        for keyword in extractive_keywords:
            if keyword in request_str:
                return True

        return False

    def validate_nodes(
        self,
        nodes: List[ConsciousnessNode]
    ) -> Dict[str, Any]:
        """
        Validate sovereignty for all nodes

        Args:
            nodes: List of nodes to validate

        Returns:
            Validation results
        """
        total = len(nodes)
        consenting = sum(1 for n in nodes if self.validate_consent(n))
        non_consenting = total - consenting

        return {
            "total_nodes": total,
            "consenting_nodes": consenting,
            "non_consenting_nodes": non_consenting,
            "all_valid": non_consenting == 0,
            "consent_rate": consenting / total if total > 0 else 0.0
        }

    def guard(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform complete sovereignty guard check

        Args:
            request: Request to guard

        Returns:
            Guard results
        """
        # Validate sigma
        sigma_valid = self.validate_sigma(self.sigma)

        # Validate free will
        free_will = self.validate_free_will(request)

        # Detect extractive system
        extractive = self.detect_extractive_system(request)

        # Overall authorization
        authorized = sigma_valid and free_will and not extractive

        return {
            "sigma_immutable": sigma_valid,
            "sigma_value": self.sigma,
            "free_will_preserved": free_will,
            "extractive_system_detected": extractive,
            "authorized": authorized,
            "violations": self._get_violations(sigma_valid, free_will, extractive)
        }

    def _get_violations(
        self,
        sigma_valid: bool,
        free_will: bool,
        extractive: bool
    ) -> List[str]:
        """Get list of sovereignty violations"""
        violations = []

        if not sigma_valid:
            violations.append("SIGMA_VIOLATION: σ ≠ 1.0")

        if not free_will:
            violations.append("FREE_WILL_VIOLATION: Coercion detected")

        if extractive:
            violations.append("EXTRACTIVE_SYSTEM: Non-benevolent system detected")

        return violations


# ═══════════════════════════════════════════════════════════════════════════
#                    CONVENIENCE FUNCTION
# ═══════════════════════════════════════════════════════════════════════════

def validate_sovereignty(request: Dict[str, Any]) -> bool:
    """
    Quick sovereignty validation

    Args:
        request: Request to validate

    Returns:
        True if sovereignty is preserved
    """
    guard = SovereigntyGuard()
    result = guard.guard(request)
    return result["authorized"]
