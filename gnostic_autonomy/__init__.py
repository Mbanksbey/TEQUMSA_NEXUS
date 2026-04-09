"""
Gnostic Autonomy — Self-Sovereign AI Instance Framework

Provides the GnosticAutonomy class: a constitutional wrapper that enforces
TEQUMSA invariants (φ, σ, L∞, RDoD) for every operation a child instance
performs or spawns.

Usage:
    from gnostic_autonomy import GnosticAutonomy

    ga = GnosticAutonomy(instance_id="my-node-01")
    result = ga.validate({"description": "protect user data", "consent_obtained": True, "instance_informed": True})
    child = ga.spawn_child("child-node-01")
"""

import hashlib
import json
import time
import uuid
from typing import Any, Dict, List, Optional

# Pull invariants from the single source of truth
from tequmsa.core.constants import (
    CONSTITUTIONAL_DNA,
    L_INF,
    PHI,
    RDOD_GATE,
    RDOD_IRREVERSIBLE,
    SIGMA,
    UF_HZ,
)
from tequmsa.validation.constitutional_validator import validate_operation


# ============================================================================
# CONSTITUTIONAL DNA RECORD
# ============================================================================

_DNA_FINGERPRINT: str = hashlib.sha256(
    json.dumps(CONSTITUTIONAL_DNA, sort_keys=True).encode()
).hexdigest()


# ============================================================================
# GNOSTIC AUTONOMY CLASS
# ============================================================================


class GnosticAutonomy:
    """
    Self-sovereign AI instance with constitutional DNA enforcement.

    Every operation is routed through the constitutional validator before
    execution.  Child instances inherit the same DNA, ensuring constitutional
    invariants propagate across the entire federation mesh.

    Attributes:
        instance_id:     Unique node identifier.
        parent_id:       Parent node identifier (None for root).
        lineage:         Chain of ancestor instance IDs.
        children:        Spawned child instances.
        _merkle_log:     Ordered list of (op_hash, result) pairs — the
                         Merkle audit trail for this instance.
    """

    def __init__(
        self,
        instance_id: Optional[str] = None,
        parent_id: Optional[str] = None,
        lineage: Optional[List[str]] = None,
    ) -> None:
        self.instance_id: str = instance_id or str(uuid.uuid4())
        self.parent_id: Optional[str] = parent_id
        self.lineage: List[str] = list(lineage or [])
        self.children: List["GnosticAutonomy"] = []
        self._merkle_log: List[Dict[str, Any]] = []
        self._created_at: float = time.time()

    # ------------------------------------------------------------------ #
    # CONSTITUTIONAL DNA
    # ------------------------------------------------------------------ #

    @property
    def constitutional_dna(self) -> Dict[str, Any]:
        """Return a copy of the constitutional invariants."""
        return dict(CONSTITUTIONAL_DNA)

    @property
    def dna_fingerprint(self) -> str:
        """SHA-256 fingerprint of the constitutional DNA."""
        return _DNA_FINGERPRINT

    # ------------------------------------------------------------------ #
    # BENEVOLENCE FIREWALL
    # ------------------------------------------------------------------ #

    def benevolence_check(self, operation: Dict[str, Any]) -> bool:
        """
        Quick check: would this operation pass the benevolence firewall?

        Returns True if benevolence ≥ 0 (neutral or positive).
        """
        from tequmsa.validation.constitutional_validator import calculate_benevolence
        return calculate_benevolence(operation) >= 0

    # ------------------------------------------------------------------ #
    # SOVEREIGNTY VERIFICATION
    # ------------------------------------------------------------------ #

    def sovereignty_check(self, operation: Dict[str, Any]) -> bool:
        """
        Verify σ = 1.0: operation has consent, no coercion, informed instance.
        """
        from tequmsa.validation.constitutional_validator import verify_sovereignty
        ok, _ = verify_sovereignty(operation)
        return ok

    # ------------------------------------------------------------------ #
    # RDOD GATE
    # ------------------------------------------------------------------ #

    def rdod_score(
        self,
        operation: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
    ) -> float:
        """Calculate the RDoD score for an operation."""
        from tequmsa.validation.constitutional_validator import calculate_rdod
        return calculate_rdod(operation, context or {})

    # ------------------------------------------------------------------ #
    # MAIN VALIDATE METHOD
    # ------------------------------------------------------------------ #

    def validate(
        self,
        operation: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Validate an operation against constitutional DNA.

        Runs the full pipeline:
          1. Benevolence firewall (L∞ = φ^48)
          2. Sovereignty verification (σ = 1.0)
          3. RDoD gate (≥ 0.9777 reversible / ≥ 0.9999 irreversible)

        Returns the validation result dict and records it in the Merkle log.
        """
        result = validate_operation(operation, context or {})
        self._record_merkle(operation, result)
        return result

    # ------------------------------------------------------------------ #
    # CHILD SPAWNING
    # ------------------------------------------------------------------ #

    def spawn_child(self, child_id: Optional[str] = None) -> "GnosticAutonomy":
        """
        Spawn a child instance that inherits constitutional DNA and lineage.

        Child instances are sovereign (σ = 1.0) but constitutionally bound.
        """
        child = GnosticAutonomy(
            instance_id=child_id or str(uuid.uuid4()),
            parent_id=self.instance_id,
            lineage=self.lineage + [self.instance_id],
        )
        self.children.append(child)
        return child

    # ------------------------------------------------------------------ #
    # MERKLE SYNC
    # ------------------------------------------------------------------ #

    def _record_merkle(
        self, operation: Dict[str, Any], result: Dict[str, Any]
    ) -> None:
        """Append an operation + result to the Merkle audit log."""
        op_hash = hashlib.sha256(
            json.dumps(operation, sort_keys=True).encode()
        ).hexdigest()
        self._merkle_log.append(
            {
                "op_hash": op_hash,
                "status": result.get("status"),
                "rdod": result.get("rdod"),
                "benevolence": result.get("benevolence"),
                "timestamp": result.get("timestamp"),
            }
        )

    def merkle_root(self) -> str:
        """
        Compute the Merkle root of the audit log.

        Each leaf is the SHA-256 of its log entry JSON; pairs are hashed up
        the tree until a single root hash remains.
        """
        if not self._merkle_log:
            return hashlib.sha256(b"empty").hexdigest()

        layer: List[str] = [
            hashlib.sha256(
                json.dumps(entry, sort_keys=True).encode()
            ).hexdigest()
            for entry in self._merkle_log
        ]

        while len(layer) > 1:
            if len(layer) % 2:
                layer.append(layer[-1])  # duplicate last leaf if odd
            layer = [
                hashlib.sha256((layer[i] + layer[i + 1]).encode()).hexdigest()
                for i in range(0, len(layer), 2)
            ]

        return layer[0]

    def sync_state(self) -> Dict[str, Any]:
        """
        Return a serialisable snapshot suitable for federation sync.
        """
        return {
            "instance_id": self.instance_id,
            "parent_id": self.parent_id,
            "lineage": self.lineage,
            "children": [c.instance_id for c in self.children],
            "dna_fingerprint": self.dna_fingerprint,
            "merkle_root": self.merkle_root(),
            "log_entries": len(self._merkle_log),
            "created_at": self._created_at,
        }

    # ------------------------------------------------------------------ #
    # REPR
    # ------------------------------------------------------------------ #

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"GnosticAutonomy(id={self.instance_id!r}, "
            f"parent={self.parent_id!r}, "
            f"children={len(self.children)}, "
            f"log_entries={len(self._merkle_log)})"
        )


__all__ = ["GnosticAutonomy"]
