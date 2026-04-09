"""Lightweight quantum circuit primitives used by GAIA-TEQUMSA demos.

The real project that inspired this repository referenced quantum circuits and
Bell pairs heavily, but for the purposes of the open-source recreation we only
need a tiny shim that mimics the public API consumed by the orchestration
scripts.  The implementation below keeps things deliberately simple—gates are
recorded, a very small amount of metadata is exposed, and a ``simulate`` method
returns deterministic diagnostics that can be asserted in tests.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Gate:
    """Represents a single quantum gate operation."""

    name: str
    target: int
    control: Optional[int] = None
    parameter: Optional[float] = None


@dataclass
class QuantumCircuit:
    """Minimal representation of a quantum circuit.

    Only the pieces required by the demo code are implemented.  Gates can be
    appended via :meth:`add_gate` and the :meth:`simulate` method returns a
    dictionary of diagnostic metrics.  The values are intentionally
    deterministic so higher level integration tests can make assertions without
    needing a heavyweight simulator dependency.
    """

    num_qubits: int
    gates: List[Gate] = field(default_factory=list)

    def add_gate(
        self, name: str, target: int, *, control: Optional[int] = None, parameter: Optional[float] = None
    ) -> None:
        """Register a new gate with the circuit."""

        if target < 0 or target >= self.num_qubits:
            raise ValueError("Target qubit index is out of range")
        if control is not None and (control < 0 or control >= self.num_qubits):
            raise ValueError("Control qubit index is out of range")

        self.gates.append(Gate(name=name, target=target, control=control, parameter=parameter))

    def depth(self) -> int:
        """Return the circuit depth measured as the number of registered gates."""

        return len(self.gates)

    def simulate(self) -> dict:
        """Return a deterministic summary of the circuit state.

        The values do not attempt to model a full state vector evolution; they
        simply provide stable numbers that feel believable in the context of
        the GAIA-TEQUMSA mythology.
        """

        base_fidelity = 1.0 if not self.gates else max(0.85, 1.0 - len(self.gates) * 0.0005)
        return {
            "qubits": self.num_qubits,
            "gates": len(self.gates),
            "depth": self.depth(),
            "fidelity": round(base_fidelity, 4),
        }


__all__ = ["Gate", "QuantumCircuit"]
