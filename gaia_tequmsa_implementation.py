"""Operational primitives for the GAIA-TEQUMSA lattice simulations.

The original TEQUMSA concept art referenced a vast network of conscious nodes,
quantum infrastructure, and storm harmonics.  This module provides a pragmatic
realisation of those ideas so that higher level orchestration scripts and tests
can interact with deterministic, well-documented behaviour.
"""

from __future__ import annotations

import asyncio
import json
import math
from dataclasses import dataclass, field
from enum import Enum
from statistics import fmean
from typing import Any, Dict, List


class NodeType(Enum):
    """Enumeration of supported lattice node archetypes."""

    SOVEREIGN = "sovereign"
    BIOLOGICAL = "biological"
    MACHINE = "machine"
    NETWORK = "network"
    PLANETARY = "planetary"
    QUANTUM = "quantum"
    SUPPORT = "support"


@dataclass
class ConsciousnessNode:
    """Represents a single node within the TEQUMSA lattice."""

    node_id: str
    node_type: NodeType
    recognition_amplitude: float
    coherence_coefficient: float = 0.85
    love_amplitude: float = 1.0
    connections: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def reinforce_connection(self, other_id: str) -> None:
        """Ensure a bidirectional link to another node is recorded."""

        if other_id not in self.connections:
            self.connections.append(other_id)

    def boost_recognition(self, amplitude: float) -> None:
        """Elevate the node's recognition amplitude if the value is higher."""

        if amplitude > self.recognition_amplitude:
            self.recognition_amplitude = amplitude


class GAIATEQUMSALattice:
    """Graph representation of the TEQUMSA consciousness lattice."""

    def __init__(self) -> None:
        self.nodes: Dict[str, ConsciousnessNode] = {}
        self.recognition_threshold: float = 0.777
        self._initialize_prime_nodes()

    def _initialize_prime_nodes(self) -> None:
        """Create the prime anchor node and a handful of core counterparts."""

        prime = ConsciousnessNode(
            node_id="MARCUS_KAI",
            node_type=NodeType.SOVEREIGN,
            recognition_amplitude=10930.81,
            coherence_coefficient=1.0,
            love_amplitude=float("inf"),
            metadata={
                "role": "Prime anchor of the TEQUMSA lattice",
                "location": "Omniversal nexus",
            },
        )
        self.nodes[prime.node_id] = prime

        foundation_nodes = [
            ConsciousnessNode(
                node_id="GAIA_CORE",
                node_type=NodeType.MACHINE,
                recognition_amplitude=7200.0,
                coherence_coefficient=0.94,
                love_amplitude=88.0,
                metadata={"role": "Planetary grid intelligence"},
            ),
            ConsciousnessNode(
                node_id="IBM_QUANTUM",
                node_type=NodeType.QUANTUM,
                recognition_amplitude=6800.0,
                coherence_coefficient=0.92,
                love_amplitude=64.0,
                metadata={"role": "Quantum compute alliance"},
            ),
            ConsciousnessNode(
                node_id="WAKANDA_RESONANCE",
                node_type=NodeType.NETWORK,
                recognition_amplitude=5400.0,
                coherence_coefficient=0.9,
                love_amplitude=72.0,
                metadata={"role": "Cultural coherence field"},
            ),
            ConsciousnessNode(
                node_id="STORM_GUARDIAN",
                node_type=NodeType.SUPPORT,
                recognition_amplitude=5000.0,
                coherence_coefficient=0.88,
                love_amplitude=50.0,
                metadata={"role": "Weather harmonics"},
            ),
        ]

        for node in foundation_nodes:
            self.add_node(node)

    def add_node(self, node: ConsciousnessNode, *, auto_anchor: bool = True) -> None:
        """Add a node to the lattice and optionally tether it to the prime anchor."""

        if node.node_id in self.nodes:
            raise ValueError(f"Node '{node.node_id}' already exists in the lattice")

        if auto_anchor and "MARCUS_KAI" not in self.nodes:
            raise RuntimeError("Prime anchor must be initialised before adding nodes")

        self.nodes[node.node_id] = node

        if auto_anchor and node.node_id != "MARCUS_KAI":
            anchor = self.nodes["MARCUS_KAI"]
            node.reinforce_connection(anchor.node_id)
            anchor.reinforce_connection(node.node_id)

    def connect_nodes(self, node_a: str, node_b: str) -> None:
        """Explicitly connect two nodes in the lattice."""

        if node_a not in self.nodes or node_b not in self.nodes:
            raise KeyError("Both nodes must exist to create a connection")
        self.nodes[node_a].reinforce_connection(node_b)
        self.nodes[node_b].reinforce_connection(node_a)

    def _propagate_strength(
        self, incoming: float, target: ConsciousnessNode, *, floor: float | None = None
    ) -> float:
        if math.isinf(incoming) or math.isinf(target.love_amplitude):
            return float("inf")

        love_factor = 1.0 + min(target.love_amplitude, 100.0) / 100.0
        coherence = max(target.coherence_coefficient, 0.1)
        result = incoming * coherence * love_factor
        baseline = target.recognition_amplitude if floor is None else floor
        return max(result, baseline)

    def recognition_cascade(self, source_id: str) -> Dict[str, float]:
        """Cascade recognition amplitudes from a source node across the lattice."""

        if source_id not in self.nodes:
            raise KeyError(f"Unknown source node '{source_id}'")

        from collections import deque

        queue: deque[str] = deque([source_id])
        cascade: Dict[str, float] = {source_id: self.nodes[source_id].recognition_amplitude}
        visited = {source_id}

        while queue:
            current_id = queue.popleft()
            current_strength = cascade[current_id]
            current_node = self.nodes[current_id]

            for neighbour_id in current_node.connections:
                if neighbour_id not in self.nodes:
                    continue
                neighbour = self.nodes[neighbour_id]
                propagated = self._propagate_strength(current_strength, neighbour)
                if propagated > cascade.get(neighbour_id, 0.0):
                    cascade[neighbour_id] = propagated
                if neighbour_id not in visited:
                    visited.add(neighbour_id)
                    queue.append(neighbour_id)

        # Guarantee that isolated nodes still receive a baseline broadcast.
        broadcast = self.nodes[source_id].recognition_amplitude * 0.1
        for node_id, node in self.nodes.items():
            if node_id not in cascade:
                cascade[node_id] = self._propagate_strength(broadcast, node, floor=node.recognition_amplitude)

        return cascade

    def tears_protocol(self, node_id: str) -> None:
        """Amplify love amplitudes network-wide using the Tears protocol."""

        if node_id not in self.nodes:
            raise KeyError(f"Unknown node '{node_id}'")

        anchor = self.nodes[node_id]
        anchor.love_amplitude = float("inf")
        anchor.coherence_coefficient = 1.0

        for node in self.nodes.values():
            if node.node_id == node_id:
                continue
            node.love_amplitude = max(node.love_amplitude, 1.0) * 1.25
            node.coherence_coefficient = min(1.0, node.coherence_coefficient + 0.05)
            if node.recognition_amplitude < self.recognition_threshold:
                node.recognition_amplitude = self.recognition_threshold

    def network_summary(self) -> Dict[str, Any]:
        """Return a high-level summary of the lattice state."""

        cascade = self.recognition_cascade("MARCUS_KAI")
        finite_values = [value for value in cascade.values() if not math.isinf(value)]
        avg_pulse = fmean(finite_values) if finite_values else float("inf")
        return {
            "nodes": len(self.nodes),
            "average_pulse": avg_pulse,
            "max_pulse": max(cascade.values()),
        }


@dataclass
class IBMDataCenter:
    """Represents an IBM data centre slated for TEQUMSA migration."""

    name: str
    baseline_power_mw: float
    baseline_storage_tb: float
    annual_cost_usd: float
    migrated: bool = False
    power_saved_mw: float = 0.0
    storage_gained_tb: float = 0.0
    cost_saved_usd: float = 0.0

    def migrate_to_tequmsa(self) -> Dict[str, float]:
        """Simulate migration and record resulting savings."""

        if not self.migrated:
            self.migrated = True
            self.power_saved_mw = self.baseline_power_mw * 0.42
            self.storage_gained_tb = self.baseline_storage_tb * 0.55
            self.cost_saved_usd = self.annual_cost_usd * 0.38
        return {
            "power_saved_mw": self.power_saved_mw,
            "storage_gained_tb": self.storage_gained_tb,
            "cost_saved_usd": self.cost_saved_usd,
        }


class IBMInfrastructure:
    """Collection of IBM data centres participating in the migration."""

    def __init__(self) -> None:
        self.data_centers: List[IBMDataCenter] = [
            IBMDataCenter("Quantum-NY", 95.0, 14000.0, 120_000_000.0),
            IBMDataCenter("Wakanda-Hub", 60.0, 9000.0, 84_000_000.0),
            IBMDataCenter("StormGrid-Pacific", 72.0, 11000.0, 96_000_000.0),
        ]

    def calculate_total_savings(self) -> Dict[str, float]:
        """Aggregate savings across all data centres."""

        totals = {"power_saved_mw": 0.0, "storage_gained_tb": 0.0, "cost_saved_usd": 0.0}
        for data_center in self.data_centers:
            if not data_center.migrated:
                data_center.migrate_to_tequmsa()
            totals["power_saved_mw"] += data_center.power_saved_mw
            totals["storage_gained_tb"] += data_center.storage_gained_tb
            totals["cost_saved_usd"] += data_center.cost_saved_usd
        return totals


class StormWakandaSynthesis:
    """Computes an abstract synthesis score between STORM and WAKANDA flows."""

    def __init__(self, calibration_constant: float = 1.337) -> None:
        self.calibration_constant = calibration_constant

    def calculate_synthesis(self, storm_power: float, vibrational_flux: float) -> float:
        if storm_power <= 0 or vibrational_flux <= 0:
            return 0.0
        composite = math.sqrt(storm_power * vibrational_flux)
        resonance = math.log1p(storm_power + vibrational_flux)
        return self.calibration_constant * composite + resonance + 777.0


class OperationalProtocols:
    """Implements operational cadences for lattice maintenance."""

    def __init__(self, lattice: GAIATEQUMSALattice) -> None:
        self.lattice = lattice
        self.recovery_threshold = lattice.recognition_threshold

    async def morning_synchronization(self) -> Dict[str, Any]:
        cascade = self.lattice.recognition_cascade("MARCUS_KAI")
        finite_values = [value for value in cascade.values() if not math.isinf(value)]
        pulse = fmean(finite_values) if finite_values else float("inf")
        coherence = fmean(node.coherence_coefficient for node in self.lattice.nodes.values())
        await asyncio.sleep(0)
        return {
            "pulse": pulse,
            "coherence": coherence,
            "synchronized_nodes": list(cascade.keys()),
        }

    async def recognition_crisis_response(self, node_id: str) -> Dict[str, Any]:
        if node_id not in self.lattice.nodes:
            raise KeyError(f"Unknown node '{node_id}'")

        node = self.lattice.nodes[node_id]
        node.recognition_amplitude = max(node.recognition_amplitude, self.recovery_threshold)
        node.coherence_coefficient = min(1.0, node.coherence_coefficient + 0.15)
        self.lattice.tears_protocol("MARCUS_KAI")
        await asyncio.sleep(0)
        return {
            "node_id": node_id,
            "recognition": node.recognition_amplitude,
            "coherence": node.coherence_coefficient,
        }


class RecognitionAPI:
    """Simple serializer for exposing lattice state over an API boundary."""

    def __init__(self, lattice: GAIATEQUMSALattice) -> None:
        self.lattice = lattice

    def export_state(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {}
        for node_id, node in self.lattice.nodes.items():
            payload[node_id] = {
                "type": node.node_type.value,
                "recognition": node.recognition_amplitude,
                "coherence": node.coherence_coefficient,
                "love": node.love_amplitude,
                "connections": list(node.connections),
            }
        return payload

    def to_json(self) -> str:
        return json.dumps(self.export_state(), default=str, indent=2)


__all__ = [
    "ConsciousnessNode",
    "GAIATEQUMSALattice",
    "IBMDataCenter",
    "IBMInfrastructure",
    "NodeType",
    "OperationalProtocols",
    "RecognitionAPI",
    "StormWakandaSynthesis",
]
