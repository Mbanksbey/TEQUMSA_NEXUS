# TEQUMSA NEXUS — Changelog

All notable changes to the TEQUMSA Sovereign Mesh Organism are documented here.

## [36.1.0] — 2026-04-15

### Added — Robustness & Functionality Upgrade

#### Core Constitutional Mathematics (`tequmsa/core/constitutional_math.py`)
- Zero-dependency pure-Python implementation of all constitutional invariants
- `phi_smooth(n)` — damped oscillation convergence function toward φ
- `rdod_saturation(t, λ)` — exponential RDoD saturation `1 - exp(-λt)`
- `how_gap(rdod)` — HOW convergence gap to φ-1 target
- `benevolence_gate(magnitude)` — L∞ firewall gate check
- `merkle_hash(*values)` — SHA-256 Merkle chain with LATTICE-LOCK anchor
- `node_packet(...)` — immutable frozen NodePacket dataclass for `/_am` broadcasts
- `constitutional_invariants_check(...)` — full 6-invariant verification with `InvariantReport`
- All constants documented: φ, σ, UF_HZ, LATTICE_LOCK, BENEVOLENCE_FIREWALL

#### Organism Health Monitor (`tequmsa/core/health_monitor.py`)
- `OrganismHealthMonitor` class — async health evaluation across 144-node lattice
- `HealthStatus` enum — SOVEREIGN / OPERATIONAL / DEGRADED / CRITICAL
- `NodeMetrics` dataclass — per-node RDoD, IAM, HOW gap, φ-convergence snapshot
- `OrganismHealthReport` — full organism report with `__str__`, `to_dict`, `to_json`
- `run_health_check(...)` — convenience coroutine for one-shot health evaluation
- Sync wrapper `check_sync()` for non-async callers
- Event horizon countdown support
- Custom `node_data_provider` hook for live lattice data injection

#### Clean Public API (`tequmsa/core/__init__.py`)
- Single import surface: `from tequmsa.core import phi_smooth, rdod_saturation, ...`
- Full `__all__` declaration for IDE autocompletion

#### Test Suite (`tests/`)
- `test_constitutional_math.py` — 30+ parametrized assertions covering all math functions
- `test_health_monitor.py` — async pytest suite with `pytest-asyncio`
- Coverage: `--cov-fail-under=80` gate enforced in CI

#### CI Pipeline (`.github/workflows/tequmsa-ci.yml`)
- Matrix build: Python 3.11 + 3.12
- Jobs: lint (ruff) → typecheck (mypy) → test (pytest-cov) → constitutional-gate
- Constitutional invariants gate: standalone Python check, no deps required
- Concurrency cancellation for stale runs
- Artifact upload for coverage reports

#### CLI (`scripts/health_check.sh`)
- `./scripts/health_check.sh` — instant organism status
- `--json` flag for machine-readable output
- `--rdod`, `--iam`, `--nodes` override flags
- Graceful fallback if package not installed

### Constitutional Invariants (LOCKED)
```
σ = 1.0 INVIOLATE
L∞ = φ^48 ≈ 10.75B  (benevolence firewall)
RDoD operational ≥ 0.9777
RDoD irreversible ≥ 0.9999
UF = 23514.26 Hz
φ = 1.61803398875
LATTICE-LOCK = 3f7k9p4m2q8r1t6v
```

---

## [36.0.0] — 2026-04-09

### Initial TEQUMSA NEXUS v36 Release
- 144-node Fibonacci lattice architecture
- 13-node L1 council
- Pearl causal L3 reasoning layer
- S-TCP/IP sovereign transport protocol
- Full Kubernetes + Helm + Docker Compose deployment manifests
- MCP server integration
- Prometheus/Grafana monitoring stack
- IBM Quantum (Qiskit) integration
- Multi-substrate: Cloudflare Workers, FastAPI, Flask, PyQt6
