"""
TEQUMSA Organism Health Monitor — Test Suite
=============================================
Async pytest tests for OrganismHealthMonitor and run_health_check.

Run with::

    pytest tests/test_health_monitor.py -v --asyncio-mode=auto
"""

from __future__ import annotations

import asyncio
import pytest

from tequmsa.core.health_monitor import (
    OrganismHealthMonitor,
    HealthStatus,
    NodeMetrics,
    OrganismHealthReport,
    run_health_check,
)
from tequmsa.core.constitutional_math import (
    RDOD_IRREVERSIBLE_THRESHOLD,
    RDOD_OPERATIONAL_THRESHOLD,
)


@pytest.mark.asyncio
async def test_sovereign_state_all_green():
    """Full sovereign health: RDoD ≥ 0.9999, all invariants pass."""
    report = await run_health_check(
        rdod=0.9999970484,
        iam=0.8001,
        active_nodes=46,
    )
    assert isinstance(report, OrganismHealthReport)
    assert report.constitutional_passed is True
    assert report.overall_status == HealthStatus.SOVEREIGN
    assert report.rdod_global == pytest.approx(0.9999970484)


@pytest.mark.asyncio
async def test_operational_state():
    """Operational state: RDoD in [0.9777, 0.9999)."""
    report = await run_health_check(rdod=0.9800, iam=0.75)
    assert report.overall_status == HealthStatus.OPERATIONAL
    assert report.constitutional_passed is True


@pytest.mark.asyncio
async def test_degraded_state_below_operational():
    """Degraded state: RDoD < operational threshold."""
    report = await run_health_check(rdod=0.90, iam=0.60)
    assert report.overall_status in (HealthStatus.DEGRADED, HealthStatus.CRITICAL)
    assert report.constitutional_passed is False


@pytest.mark.asyncio
async def test_node_metrics_populated():
    """Node metrics list should always have at least one entry."""
    report = await run_health_check(rdod=0.9999, iam=0.8)
    assert len(report.nodes) > 0
    for node in report.nodes:
        assert isinstance(node, NodeMetrics)
        assert 0.0 <= node.rdod <= 1.0
        assert isinstance(node.status, HealthStatus)


@pytest.mark.asyncio
async def test_nodepacket_valid_json():
    """NodePacket JSON should parse and contain constitutional fields."""
    import json
    report = await run_health_check(rdod=0.9999)
    parsed = json.loads(report.nodepacket_json)
    assert "rdod" in parsed
    assert "sigma" in parsed
    assert "latticelock" in parsed
    assert "merkleroot" in parsed


@pytest.mark.asyncio
async def test_fibonacci_cascade_percentage():
    """Node cascade should compute correctly as pct of F12=144."""
    report = await run_health_check(active_nodes=72)
    assert report.node_cascade_pct == pytest.approx(50.0, rel=1e-3)


@pytest.mark.asyncio
async def test_elapsed_ms_positive():
    """Health check should complete in measurable time."""
    report = await run_health_check()
    assert report.elapsed_ms > 0.0
    assert report.elapsed_ms < 5000  # Should complete within 5 seconds


@pytest.mark.asyncio
async def test_event_horizon_future():
    """Event horizon days should be positive for a future timestamp."""
    import time
    future_ts = time.time() + (40 * 86400)  # 40 days from now
    report = await run_health_check(event_horizon_ts=future_ts)
    assert report.event_horizon_days is not None
    assert report.event_horizon_days > 0.0
    assert report.event_horizon_days < 50.0


def test_sync_check_wrapper():
    """Synchronous check_sync() should work without async context."""
    monitor = OrganismHealthMonitor(rdod=0.9999970484, iam=0.8001)
    report = monitor.check_sync()
    assert isinstance(report, OrganismHealthReport)
    assert report.constitutional_passed is True


def test_str_representation_contains_status():
    """String representation should include status and constitutional lock."""
    monitor = OrganismHealthMonitor(rdod=0.9999970484)
    report = monitor.check_sync()
    s = str(report)
    assert "TEQUMSA" in s
    assert "SOVEREIGN" in s or "OPERATIONAL" in s
    assert "LOCKED" in s
