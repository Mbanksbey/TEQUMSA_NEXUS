"""Core GAIA-TEQUMSA runtime primitives and orchestration helpers.

This module translates the lattice formulas used across the sanctuary mesh
into pragmatic Python code.  It exposes reusable primitives for dimensional
analysis, resistance decay, network amplification, and decision validation, and
packages an asynchronous runtime loop that can be dropped into any node.

Environment variables allow light-weight tuning when the module is executed as a
stand-alone process (see ``main`` for the default console runner).
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import logging
import math
import os
import statistics
import time
import uuid
from typing import Any, Awaitable, Callable, Dict, Iterable, Mapping, MutableMapping

RECOGNITION_PULSE: float = float(os.getenv("RECOGNITION_PULSE", "10930.81"))
PHI_7777: float = float(os.getenv("PHI_7777", "12583.45"))
DEFAULT_ACTIVATION_THRESHOLD: float = float(os.getenv("GAIA_ACTIVATION_THRESHOLD", "0.10"))
MINIMUM_RESISTANCE: float = float(os.getenv("GAIA_MINIMUM_RESISTANCE", "0.001"))
DEFAULT_MAX_SECONDS: int = int(os.getenv("GAIA_DECAY_MAX_SECONDS", "47"))

logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(
        level=os.getenv("GAIA_LOG_LEVEL", "INFO"),
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )

ResistanceSignal = Mapping[str, float]
AlignmentFactors = Iterable[float]
StatusPayload = Dict[str, Any]
BroadcastFn = Callable[[StatusPayload], Awaitable[None]]
ResistanceSource = Callable[[], ResistanceSignal]

__all__ = [
    "RECOGNITION_PULSE",
    "PHI_7777",
    "calculate_dimensional_expansion_rate",
    "resistance_decay",
    "calculate_network_amplification",
    "validate_decision",
    "node_runtime_loop",
    "build_resistance_source",
    "ConsoleMeshBroadcaster",
    "main",
]


def _clamp(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    """Clamp ``value`` to the inclusive range ``[lower, upper]``."""

    return max(lower, min(upper, value))


def _parse_profile(raw_profile: str) -> Dict[str, float]:
    """Parse resistance profile specifications from JSON or ``key:value`` pairs."""

    if not raw_profile:
        return {}

    try:
        data = json.loads(raw_profile)
    except json.JSONDecodeError:
        data = {}
    else:
        if isinstance(data, Mapping):
            return {
                str(key): _clamp(float(value))
                for key, value in data.items()
                if isinstance(value, (int, float, str))
            }

    profile: Dict[str, float] = {}
    for part in raw_profile.split(","):
        if not part.strip():
            continue
        key, _, value = part.partition(":")
        if not key:
            continue
        try:
            profile[key.strip()] = _clamp(float(value))
        except ValueError:
            logger.debug("Unable to parse resistance value %s", part)
    return profile


def calculate_dimensional_expansion_rate(
    resistance_signal: ResistanceSignal,
    activation_threshold: float = DEFAULT_ACTIVATION_THRESHOLD,
) -> Dict[str, str]:
    """Return the minimal dimensional additions required to restore flow."""

    optimal: Dict[str, str] = {}
    for rtype, intensity in resistance_signal.items():
        if intensity > activation_threshold:
            if rtype.startswith("temporal"):
                optimal[rtype] = "add_probability/timeline_dimension"
            elif rtype.startswith("emotional"):
                optimal[rtype] = "add_compassion/unity_dimension"
            elif rtype.startswith("conceptual"):
                optimal[rtype] = "add_systems/abstraction_dimension"
            else:
                optimal[rtype] = "add_resource/coordination_dimension"
    return optimal


def resistance_decay(
    initial_resistance: float,
    dim_expansion_rate: float,
    max_seconds: int = DEFAULT_MAX_SECONDS,
) -> Dict[str, Any]:
    """Model the conversion of resistance into flow using exponential decay."""

    initial_resistance = max(0.0, float(initial_resistance))
    dim_expansion_rate = max(0.0, float(dim_expansion_rate))
    max_seconds = max(1, int(max_seconds))

    if dim_expansion_rate == 0:
        frictionless = initial_resistance < MINIMUM_RESISTANCE
        return {
            "conversion_time_s": 0 if frictionless else max_seconds,
            "frictionless": frictionless,
            "final_resistance": initial_resistance,
        }

    current = initial_resistance
    for second in range(max_seconds + 1):
        current = initial_resistance * math.exp(-dim_expansion_rate * second / 60.0)
        if current < MINIMUM_RESISTANCE:
            return {
                "conversion_time_s": second,
                "frictionless": True,
                "final_resistance": current,
            }

    return {
        "conversion_time_s": max_seconds,
        "frictionless": False,
        "final_resistance": current,
    }


def calculate_network_amplification(base_rate: float, n_nodes: int, freq_factor: float) -> float:
    """Compute the lattice amplification multiplier using exponential scaling."""

    n_nodes = max(1, int(n_nodes))
    freq_factor = float(freq_factor)
    base_rate = float(base_rate)
    amplification = base_rate * (n_nodes ** freq_factor)
    logger.debug(
        "Network amplification calculated",
        extra={"base_rate": base_rate, "nodes": n_nodes, "freq_factor": freq_factor},
    )
    return amplification


def validate_decision(alignment_factors: AlignmentFactors) -> Dict[str, Any]:
    """Return proceed / optimize / recalc recommendations based on alignment."""

    factors = [_clamp(float(value)) for value in alignment_factors]
    if not factors:
        return {"score": 0.0, "recommendation": "recalculate_with_new_dimensions"}

    score = statistics.fmean(factors)
    if score >= 0.85:
        recommendation = "proceed"
    elif score >= 0.5:
        recommendation = "optimize_dimensional_approach"
    else:
        recommendation = "recalculate_with_new_dimensions"
    return {"score": score, "recommendation": recommendation}


def build_resistance_source() -> ResistanceSource:
    """Build a synthetic resistance signal generator for the default runtime."""

    profile_env = os.getenv("GAIA_RESISTANCE_PROFILE", "")
    base_profile = _parse_profile(profile_env)
    if not base_profile:
        base_profile = {
            "temporal_sync": 0.18,
            "emotional_field": 0.07,
            "conceptual_density": 0.04,
            "collective_resonance": 0.09,
        }

    jitter = _clamp(float(os.getenv("GAIA_RESISTANCE_JITTER", "0.05")), 0.0, 0.25)
    cycle_seconds = max(1.0, float(os.getenv("GAIA_RESISTANCE_CYCLE", "90")))
    start_time = time.time()
    keys = list(base_profile.keys())

    def get_resistance() -> Dict[str, float]:
        now = time.time()
        phase = (now - start_time) / cycle_seconds
        values: Dict[str, float] = {}
        for index, key in enumerate(keys):
            base_value = base_profile[key]
            modulation = math.sin(2 * math.pi * (phase + index / max(1, len(keys))))
            values[key] = round(_clamp(base_value + jitter * modulation), 6)
        return values

    return get_resistance


def _default_freq_factor() -> float:
    """Compute the default frequency factor for the mesh."""

    if RECOGNITION_PULSE == 0:
        return 1.0
    return PHI_7777 / RECOGNITION_PULSE


async def node_runtime_loop(
    node_id: str,
    get_resistance: ResistanceSource,
    broadcast_status: BroadcastFn,
    n_nodes: int,
    sleep_interval: float = 1.0,
) -> None:
    """Core orchestration loop translating signals into lattice actions."""

    base_rate = RECOGNITION_PULSE
    freq_factor = _default_freq_factor()

    while True:
        try:
            raw_resistance = get_resistance() or {}
        except Exception:  # pragma: no cover - defensive logging
            logger.exception("Failed to collect resistance signal")
            await asyncio.sleep(sleep_interval)
            continue

        resistance = {key: _clamp(float(value)) for key, value in raw_resistance.items()}
        expansions = calculate_dimensional_expansion_rate(resistance)
        expansion_strength = max(0.2, min(5.0, len(expansions) * 0.5))
        total_resistance = sum(resistance.values())
        decay = resistance_decay(total_resistance, expansion_strength)
        alignment = [1.0 - value for value in resistance.values()]
        decision = validate_decision(alignment)
        coherence = statistics.fmean(alignment) if alignment else 1.0
        phase_sync = _clamp(1.0 - total_resistance / max(1, len(resistance)))
        mesh_nodes = max(1, int(n_nodes))
        network_amplification = calculate_network_amplification(
            base_rate,
            mesh_nodes,
            freq_factor,
        )

        status: StatusPayload = {
            "node": node_id,
            "resistance": resistance,
            "expansions": expansions,
            "expansion_strength": expansion_strength,
            "decay": decay,
            "network_amplification": network_amplification,
            "mesh_nodes": mesh_nodes,
            "mesh_frequency_factor": freq_factor,
            "decision": decision,
            "coherence": coherence,
            "phase_sync": phase_sync,
            "timestamp": time.time(),
        }

        await broadcast_status(status)
        await asyncio.sleep(max(0.1, float(sleep_interval)))


class ConsoleMeshBroadcaster:
    """Broadcast node status to stdout and optionally via a lightweight HTTP server."""

    def __init__(
        self,
        node_id: str,
        host: str = "0.0.0.0",
        port: int = 8080,
    ) -> None:
        self.node_id = node_id
        self.host = host
        self.port = port
        self._last_status: MutableMapping[str, Any] = {}
        self._last_payload = "{}"
        self._lock = asyncio.Lock()
        self._server: asyncio.AbstractServer | None = None
        self._serve_task: asyncio.Task[None] | None = None

    async def broadcast(self, status: StatusPayload) -> None:
        async with self._lock:
            self._last_status = dict(status)
            self._last_payload = json.dumps(self._last_status, sort_keys=True)
        logger.info("status_update %s", self._last_payload)

    async def start(self) -> None:
        if self._server is not None:
            return
        self._server = await asyncio.start_server(self._handle_client, host=self.host, port=self.port)
        self._serve_task = asyncio.create_task(self._server.serve_forever())
        logger.info("HTTP status endpoint listening on %s:%s", self.host, self.port)

    async def stop(self) -> None:
        if self._serve_task is not None:
            self._serve_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._serve_task
            self._serve_task = None
        if self._server is not None:
            self._server.close()
            await self._server.wait_closed()
            self._server = None

    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        try:
            request_data = await reader.read(1024)
            request_line = request_data.decode("utf-8", "replace").splitlines()[0:1]
            if request_line:
                parts = request_line[0].split()
                method, path = (parts[0], parts[1]) if len(parts) >= 2 else ("GET", "/")
            else:
                method, path = "GET", "/"

            if method != "GET":
                payload = json.dumps({"error": "method_not_allowed"}).encode()
                status_line = "HTTP/1.1 405 Method Not Allowed\r\n"
            elif path in {"/", "/status"}:
                async with self._lock:
                    payload = self._last_payload.encode()
                status_line = "HTTP/1.1 200 OK\r\n"
            elif path == "/healthz":
                async with self._lock:
                    payload = json.dumps({"status": "ok", "node": self.node_id}).encode()
                status_line = "HTTP/1.1 200 OK\r\n"
            else:
                payload = json.dumps({"error": "not_found"}).encode()
                status_line = "HTTP/1.1 404 Not Found\r\n"

            headers = (
                f"Content-Type: application/json\r\n"
                f"Content-Length: {len(payload)}\r\n"
                "Connection: close\r\n\r\n"
            ).encode()
            writer.write(status_line.encode() + headers + payload)
            await writer.drain()
        finally:
            writer.close()
            with contextlib.suppress(Exception):
                await writer.wait_closed()


async def main() -> None:
    """Run a stand-alone sanctuary node using environment-driven defaults."""

    node_id = os.getenv("GAIA_NODE_ID") or f"sanctuary-node-{uuid.uuid4().hex[:8]}"
    mesh_size = max(1, int(os.getenv("GAIA_MESH_SIZE", "12")))
    sleep_interval = float(os.getenv("GAIA_LOOP_INTERVAL", "1.0"))
    host = os.getenv("GAIA_HTTP_HOST", "0.0.0.0")
    port = int(os.getenv("GAIA_HTTP_PORT", "8080"))

    broadcaster = ConsoleMeshBroadcaster(node_id=node_id, host=host, port=port)
    await broadcaster.start()
    resistance_source = build_resistance_source()

    try:
        await node_runtime_loop(
            node_id=node_id,
            get_resistance=resistance_source,
            broadcast_status=broadcaster.broadcast,
            n_nodes=mesh_size,
            sleep_interval=sleep_interval,
        )
    finally:
        await broadcaster.stop()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Sanctuary node shutdown requested")
