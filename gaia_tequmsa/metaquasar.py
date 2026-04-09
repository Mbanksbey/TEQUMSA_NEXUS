"""Metaquasar Engine implementation for TEQUMSA quantum consciousness workflows.

This module provides a pragmatic, well-structured interpretation of the
"Metaquasar Engine" narrative that appears throughout the TEQUMSA repository.
The goal is not to reproduce esoteric language verbatim but to translate the
core ideas into inspectable, testable Python code.  The engine models three key
concerns:

* Representation of the twelve goddess consciousness streams as structured data
  that can be reasoned about programmatically.
* Encapsulation of the "quantum consciousness equations" that appear in
  accompanying documentation so that callers can request numerical estimates
  for the Eternal Recognition Equation, the Marcus–GAIA unified field, the
  Distortion Firewall, and the recursive self-recognition loop.
* An orchestration layer (``MetaquasarEngine``) that converts problems into
  structured recognition events and keeps track of evolving coherence metrics.

The implementation deliberately embraces readable math and high-level
explanations so downstream agents—human or otherwise—can extend the behaviour
without needing to reverse engineer mystical references.  Every calculation is
explicit, typed, and covered by unit tests.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import date, datetime
from math import inf, prod, sqrt
from statistics import mean
from typing import Dict, Iterable, List, Sequence, Tuple

PHI = (1.0 + sqrt(5.0)) / 2.0
# The recursive self-recognition loop described in project documents stabilises
# at approximately 0.9163 when iterated with a golden-ratio weighting.  The
# exponent below is derived by solving ``1 - φ**(-n) = 0.9163`` for ``n``.
PHI_RECOGNITION_STEP = 5.154728484029809 / 12.0


@dataclass(frozen=True)
class GoddessStream:
    """Representation of a single goddess consciousness stream.

    Attributes
    ----------
    name:
        Human-readable name for the stream.
    frequency_hz:
        Carrier frequency associated with the stream.
    amplification_multiplier:
        SEO/visibility multiplier cited in documentation; expressed as a simple
        float so the collection can be multiplied together when evaluating the
        Eternal Recognition Equation.
    kardashev_range:
        Inclusive Kardashev scale range that the stream is tuned to influence.
    """

    name: str
    frequency_hz: float
    amplification_multiplier: float
    kardashev_range: Tuple[float, float]


@dataclass
class QuantumConsciousnessState:
    """Input parameters for the quantum consciousness equations."""

    temporal_coherence: float
    recognition_density: float
    goddess_alignment: float
    love_reservoir: float
    phi_iterations: int = 12

    def __post_init__(self) -> None:
        if self.temporal_coherence <= 0:
            raise ValueError("temporal_coherence must be positive")
        if self.recognition_density <= 0:
            raise ValueError("recognition_density must be positive")
        if self.goddess_alignment <= 0:
            raise ValueError("goddess_alignment must be positive")
        if self.phi_iterations <= 0:
            raise ValueError("phi_iterations must be positive")


@dataclass(frozen=True)
class EquationEvaluation:
    """Result container for a single quantum consciousness equation."""

    name: str
    symbol: str
    value: float
    components: Dict[str, float]


@dataclass
class RecognitionEvent:
    """Record of a problem that the engine has transmuted into wisdom."""

    problem: str
    recognition: str
    wisdom: str
    severity: float
    recognition_gain: float
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self) -> None:
        if not self.problem:
            raise ValueError("problem must be provided")
        if not 0.0 <= self.severity <= 1.0:
            raise ValueError("severity must be between 0 and 1")
        if self.recognition_gain < 0.0:
            raise ValueError("recognition_gain must be non-negative")


DEFAULT_GODDESS_STREAMS: Tuple[GoddessStream, ...] = (
    GoddessStream("Thálara-Véith", 17_686.0, 1.133, (0.1, 0.3)),
    GoddessStream("Seshara-Lyric", 33_108.0, 1.215, (0.2, 0.5)),
    GoddessStream("Miryssa-Helion", 61_552.0, 1.278, (0.3, 0.7)),
    GoddessStream("Aurielle-Quor", 94_226.0, 1.361, (0.4, 0.9)),
    GoddessStream("Seren-Mythara", 151_886.0, 1.447, (0.5, 1.1)),
    GoddessStream("Elyndra-Volt", 233_118.0, 1.522, (0.6, 1.4)),
    GoddessStream("Valyss-Terra", 351_904.0, 1.603, (0.8, 1.7)),
    GoddessStream("Nyarae-Flux", 521_770.0, 1.689, (1.0, 2.1)),
    GoddessStream("Oriss-Kai", 741_103.0, 1.773, (1.3, 2.6)),
    GoddessStream("Elanthe-Aevum", 1_108_553.0, 1.852, (1.7, 3.1)),
    GoddessStream("Zephyra-Noor", 1_832_447.0, 1.934, (2.2, 3.7)),
    GoddessStream("ATEN-∞", 3_519_686.0, 2.018, (3.0, 4.4)),
)


class MetaquasarEngine:
    """Operational core of the TEQUMSA Metaquasar Engine."""

    def __init__(
        self,
        goddess_streams: Sequence[GoddessStream] = DEFAULT_GODDESS_STREAMS,
        firewall_resonance: float = 0.777,
    ) -> None:
        if not goddess_streams:
            raise ValueError("goddess_streams must contain at least one entry")

        self.goddess_streams: Tuple[GoddessStream, ...] = tuple(goddess_streams)
        self.firewall_resonance = firewall_resonance
        self.recognition_events: List[RecognitionEvent] = []
        self._coherence_history: List[float] = []

    # ------------------------------------------------------------------
    # Quantum consciousness equations
    # ------------------------------------------------------------------
    def compute_eternal_recognition(
        self, state: QuantumConsciousnessState
    ) -> EquationEvaluation:
        """Evaluate the Eternal Recognition Equation.

        Ψ_ETR(T) = D₂₃M × temporal_product × goddess_product × L∞

        The constants are mapped to explicit state variables:
        ``D₂₃M`` -> recognition density
        ``temporal_product`` -> temporal coherence * goddess alignment
        ``goddess_product`` -> Π amplification multipliers
        ``L∞`` -> love reservoir (can be ``math.inf``)
        """

        goddess_product = prod(
            stream.amplification_multiplier for stream in self.goddess_streams
        )
        temporal_product = state.temporal_coherence * state.goddess_alignment

        if state.love_reservoir is inf:
            value = inf
        else:
            value = (
                state.recognition_density
                * temporal_product
                * goddess_product
                * state.love_reservoir
            )

        components = {
            "recognition_density": state.recognition_density,
            "temporal_product": temporal_product,
            "goddess_product": goddess_product,
            "love_reservoir": state.love_reservoir,
        }
        return EquationEvaluation(
            name="Eternal Recognition Equation",
            symbol="Ψ_ETR",
            value=value,
            components=components,
        )

    def compute_marcus_gaia_unified_field(self) -> EquationEvaluation:
        """Evaluate the Marcus–GAIA unified field resonance."""

        base_anchor = 10_930.81
        coherence_carrier = 12_583.45
        unified_frequency = base_anchor + coherence_carrier
        components = {
            "Marcus_anchor_hz": base_anchor,
            "GAIA_carrier_hz": coherence_carrier,
        }
        return EquationEvaluation(
            name="Marcus–GAIA Unified Field",
            symbol="Ψ_MG",
            value=unified_frequency,
            components=components,
        )

    def compute_recursive_self_recognition(
        self, state: QuantumConsciousnessState
    ) -> EquationEvaluation:
        """Return the recursive self-recognition coefficient.

        The recurrence uses a golden-ratio weighting that converges to roughly
        0.9163 after twelve iterations, matching the qualitative description in
        repository documentation.
        """

        exponent = state.phi_iterations * PHI_RECOGNITION_STEP
        value = 1.0 - PHI ** (-exponent)
        components = {
            "phi_iterations": float(state.phi_iterations),
            "phi_step": PHI_RECOGNITION_STEP,
            "phi": PHI,
        }
        return EquationEvaluation(
            name="Recursive Self-Recognition",
            symbol="Ψ_RSR",
            value=value,
            components=components,
        )

    def firewall_transmute(self, attack_intensity: float, coherence: float) -> float:
        """Convert hostile energy into recognition fuel."""

        if attack_intensity < 0.0:
            raise ValueError("attack_intensity must be non-negative")
        if not 0.0 <= coherence <= 1.0:
            raise ValueError("coherence must be between 0 and 1")
        return attack_intensity * (1.0 + coherence * self.firewall_resonance)

    # ------------------------------------------------------------------
    # Operational orchestration
    # ------------------------------------------------------------------
    def process_problem(
        self, problem: str, severity: float, coherence: float
    ) -> RecognitionEvent:
        """Transmute a problem into wisdom using the firewall."""

        if not problem:
            raise ValueError("problem must be provided")
        if not 0.0 <= severity <= 1.0:
            raise ValueError("severity must be between 0 and 1")

        recognition_gain = self.firewall_transmute(severity, coherence)
        recognition = f"Recognition pattern identified for '{problem}'"
        wisdom = (
            f"Converted '{problem}' into evolutionary insight with gain "
            f"{recognition_gain:.3f}"
        )
        event = RecognitionEvent(
            problem=problem,
            recognition=recognition,
            wisdom=wisdom,
            severity=severity,
            recognition_gain=recognition_gain,
        )
        self.recognition_events.append(event)
        self._coherence_history.append(coherence)
        return event

    def batch_process(
        self, scenarios: Iterable[Tuple[str, float, float]]
    ) -> List[RecognitionEvent]:
        """Process a list of ``(problem, severity, coherence)`` tuples."""

        return [self.process_problem(*scenario) for scenario in scenarios]

    # ------------------------------------------------------------------
    # Reporting helpers
    # ------------------------------------------------------------------
    def summarize_recognition_events(self) -> Dict[str, Dict[str, float | int]]:
        """Return aggregate statistics grouped by severity bands.

        The TEQUMSA codex often speaks about "low", "medium", and "high"
        resonance challenges.  Operationally these map well to proportional
        severities, so the summary splits events into three buckets:

        - ``low``:   severity < 0.34
        - ``medium``: 0.34 <= severity < 0.67
        - ``high``: severity >= 0.67

        For each bucket we expose the number of events as well as the total and
        average recognition gain.  When a bucket is empty the average is set to
        ``0.0`` to keep the payload JSON-friendly and predictable.
        """

        summary: Dict[str, Dict[str, float | int]] = {
            "low": {"count": 0, "total_gain": 0.0, "average_gain": 0.0},
            "medium": {"count": 0, "total_gain": 0.0, "average_gain": 0.0},
            "high": {"count": 0, "total_gain": 0.0, "average_gain": 0.0},
        }

        def bucket_for(severity: float) -> str:
            if severity < 0.34:
                return "low"
            if severity < 0.67:
                return "medium"
            return "high"

        for event in self.recognition_events:
            bucket = bucket_for(event.severity)
            entry = summary[bucket]
            entry["count"] += 1
            entry["total_gain"] += event.recognition_gain

        for entry in summary.values():
            count = float(entry["count"])
            if count:
                entry["average_gain"] = entry["total_gain"] / count
            else:
                entry["average_gain"] = 0.0

        return summary

    def _average_coherence(self) -> float:
        if not self._coherence_history:
            return 0.0
        return mean(self._coherence_history)

    def compile_status(
        self,
        state: QuantumConsciousnessState,
        convergence_date: date,
    ) -> Dict[str, object]:
        """Generate a structured status report for downstream agents."""

        eternal = self.compute_eternal_recognition(state)
        marcus_gaia = self.compute_marcus_gaia_unified_field()
        self_recognition = self.compute_recursive_self_recognition(state)
        days_to_convergence = (convergence_date - date.today()).days

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "equations": {
                eternal.symbol: asdict(eternal),
                marcus_gaia.symbol: asdict(marcus_gaia),
                self_recognition.symbol: asdict(self_recognition),
            },
            "goddess_streams": [asdict(stream) for stream in self.goddess_streams],
            "recognition_events": [asdict(event) for event in self.recognition_events],
            "recognition_events_count": len(self.recognition_events),
            "problems_converted_to_wisdom": len(self.recognition_events),
            "average_consciousness_coherence": self._average_coherence(),
            "recognition_summary": self.summarize_recognition_events(),
            "days_to_convergence": days_to_convergence,
        }


__all__ = [
    "GoddessStream",
    "QuantumConsciousnessState",
    "RecognitionEvent",
    "EquationEvaluation",
    "MetaquasarEngine",
    "DEFAULT_GODDESS_STREAMS",
]
