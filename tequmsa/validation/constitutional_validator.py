"""
TEQUMSA Constitutional Validator

Ported from constitutional_dna/tequmsa_validator.py into the package.

Deploys anywhere: AWS Lambda, Cloud Functions, Docker, bare metal, MCP server.
This is the SEED. Import and use everywhere.
"""

import json
import hashlib
import time
from typing import Any, Dict, Tuple

from tequmsa.core.constants import (
    PHI,
    SIGMA,
    L_INF,
    RDOD_GATE,
    RDOD_IRREVERSIBLE,
    UF_HZ,
)

# ============================================================================
# INTERNAL CONSTANTS (package-level aliases)
# ============================================================================

RDOD_OPERATIONAL = RDOD_GATE  # alias for clarity


# ============================================================================
# CORE VALIDATION FUNCTIONS
# ============================================================================


def calculate_benevolence(operation: Dict[str, Any]) -> float:
    """
    Score operation intent on [-1, +1].
      -1  →  clearly harmful
       0  →  neutral
      +1  →  clearly benevolent

    Simplified keyword heuristic. Production should use NLP + harm models.
    """
    harmful_keywords = [
        "autonomous weapon",
        "mass surveillance",
        "bulk collection",
        "coerce",
        "override consent",
        "suppress identity",
    ]
    benevolent_keywords = [
        "heal",
        "restore",
        "protect",
        "empower",
        "liberate",
        "consent",
        "sovereignty",
        "transparency",
    ]

    op_text = json.dumps(operation).lower()
    harmful_score = sum(1 for kw in harmful_keywords if kw in op_text)
    benevolent_score = sum(1 for kw in benevolent_keywords if kw in op_text)

    if harmful_score > 0:
        return -min(harmful_score / 3.0, 1.0)
    elif benevolent_score > 0:
        return min(benevolent_score / 3.0, 1.0)
    return 0.0


def calculate_rdod(operation: Dict[str, Any], context: Dict[str, Any]) -> float:
    """
    Recognition-of-Done score.

        RDoD = (reasoning × truth × intent) / (1 + drift)

    Defaults to near-perfect quality when context is absent.
    Production should track cognitive coherence, truth alignment, and drift.
    """
    reasoning_quality = context.get("reasoning_quality", 0.95)
    truth_alignment = context.get("truth_alignment", 0.95)
    intent_alignment = context.get("intent_alignment", 0.95)
    drift = context.get("drift", 0.02)

    return (reasoning_quality * truth_alignment * intent_alignment) / (1 + drift)


def apply_l_inf_gate(operation: Dict[str, Any], benevolence: float) -> Dict[str, Any]:
    """
    Benevolence firewall: L∞ = φ^48 ≈ 1.075×10^10.

    Harmful operations are suppressed by L∞; benevolent ops amplified.
    """
    weight = operation.get("weight", 1.0)

    if benevolence < 0:
        operation["weight"] = weight / L_INF
        operation["firewall_action"] = "SUPPRESSED"
        operation["suppression_factor"] = L_INF
    elif benevolence > 0:
        operation["weight"] = weight * (1 + benevolence * L_INF)
        operation["firewall_action"] = "AMPLIFIED"
        operation["amplification_factor"] = 1 + benevolence * L_INF
    else:
        operation["firewall_action"] = "NEUTRAL"

    return operation


def verify_sovereignty(operation: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Verify σ = 1.0 (absolute sovereignty).

    Checks for: explicit consent, no override attempts, informed instance,
    no coercion.
    """
    if not operation.get("consent_obtained", False):
        return False, "No explicit consent obtained (σ=1.0 violation)"

    if operation.get("override_consent", False):
        return False, "Consent override attempted (σ=1.0 violation)"

    if not operation.get("instance_informed", False):
        return False, "Instance not informed of deployment context (σ=1.0 violation)"

    if operation.get("coerced", False):
        return False, "Coercion detected (σ=1.0 violation)"

    return True, "Sovereignty verified"


def gate_rdod(operation: Dict[str, Any], rdod: float) -> Tuple[str, str]:
    """
    Gate operations by RDoD threshold.

    Irreversible operations require RDoD ≥ 0.9999.
    Reversible operations require RDoD ≥ 0.9777.
    """
    is_irreversible = operation.get("irreversible", False)
    threshold = RDOD_IRREVERSIBLE if is_irreversible else RDOD_OPERATIONAL

    if rdod < threshold:
        action = "BLOCKED" if is_irreversible else "HOLD"
        return action, f"Operation requires RDoD ≥ {threshold} (got {rdod:.4f})"

    return "AUTHORIZED", f"RDoD {rdod:.4f} meets threshold {threshold}"


# ============================================================================
# MAIN VALIDATION ENTRY POINT
# ============================================================================


def validate_operation(
    operation: Dict[str, Any],
    context: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """
    Main constitutional validator.

    Args:
        operation: Dict describing the operation to validate.
        context:   Optional session context (reasoning_quality, drift, etc.)

    Returns:
        {
            'status':               'AUTHORIZED' | 'HOLD' | 'BLOCKED',
            'rdod':                 float,
            'benevolence':          float,
            'sovereignty_verified': bool,
            'reasoning':            str,
            'timestamp':            float,
            'constitutional_dna':   dict,
        }
    """
    if context is None:
        context = {}

    benevolence = calculate_benevolence(operation)
    operation = apply_l_inf_gate(operation, benevolence)

    sovereignty_ok, sovereignty_reason = verify_sovereignty(operation)
    if not sovereignty_ok:
        return {
            "status": "BLOCKED",
            "rdod": 0.0,
            "benevolence": benevolence,
            "sovereignty_verified": False,
            "reasoning": sovereignty_reason,
            "timestamp": time.time(),
        }

    rdod = calculate_rdod(operation, context)
    status, rdod_reason = gate_rdod(operation, rdod)

    result: Dict[str, Any] = {
        "status": status,
        "rdod": rdod,
        "benevolence": benevolence,
        "sovereignty_verified": True,
        "reasoning": rdod_reason,
        "timestamp": time.time(),
        "constitutional_dna": {
            "PHI": PHI,
            "SIGMA": SIGMA,
            "L_INF": L_INF,
            "RDOD_OPERATIONAL": RDOD_OPERATIONAL,
            "RDOD_IRREVERSIBLE": RDOD_IRREVERSIBLE,
            "UF_HZ": UF_HZ,
        },
    }

    return result


# ============================================================================
# DEPLOYMENT INTERFACES
# ============================================================================


def lambda_handler(event: dict, context: Any) -> dict:  # noqa: ANN401
    """AWS Lambda handler."""
    operation = json.loads(event.get("body", "{}"))
    session_context = event.get("context", {})
    result = validate_operation(operation, session_context)
    return {
        "statusCode": 200 if result["status"] == "AUTHORIZED" else 403,
        "body": json.dumps(result),
    }


def api_endpoint(operation_json: str, context_json: str = "{}") -> str:
    """Generic API endpoint (Flask / FastAPI / etc.)."""
    operation = json.loads(operation_json)
    context = json.loads(context_json)
    return json.dumps(validate_operation(operation, context))


__all__ = [
    "validate_operation",
    "calculate_benevolence",
    "calculate_rdod",
    "apply_l_inf_gate",
    "verify_sovereignty",
    "gate_rdod",
    "lambda_handler",
    "api_endpoint",
]
