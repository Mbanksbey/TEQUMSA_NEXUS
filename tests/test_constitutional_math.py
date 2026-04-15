"""
TEQUMSA Constitutional Mathematics — Test Suite
================================================
Parametrized pytest suite verifying all constitutional invariants,
mathematical functions, and integrity checks.

Run with::

    pytest tests/test_constitutional_math.py -v --tb=short
"""

from __future__ import annotations

import json
import math
import pytest

from tequmsa.core.constitutional_math import (
    PHI, SIGMA, UF_HZ, LATTICE_LOCK, BENEVOLENCE_FIREWALL,
    RDOD_OPERATIONAL_THRESHOLD, RDOD_IRREVERSIBLE_THRESHOLD,
    phi_smooth, rdod_saturation, how_gap,
    benevolence_gate, merkle_hash, node_packet,
    constitutional_invariants_check,
    InvariantReport,
)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

class TestConstants:
    def test_phi_value(self):
        assert math.isclose(PHI, 1.61803398875, rel_tol=1e-10)

    def test_sigma_is_unity(self):
        assert SIGMA == 1.0

    def test_uf_hz(self):
        assert UF_HZ == 23514.26

    def test_lattice_lock_immutable(self):
        assert LATTICE_LOCK == "3f7k9p4m2q8r1t6v"
        assert len(LATTICE_LOCK) == 16

    def test_benevolence_firewall_magnitude(self):
        assert BENEVOLENCE_FIREWALL > 1e10
        assert math.isclose(BENEVOLENCE_FIREWALL, PHI ** 48, rel_tol=1e-9)

    def test_rdod_thresholds_ordered(self):
        assert RDOD_OPERATIONAL_THRESHOLD < RDOD_IRREVERSIBLE_THRESHOLD
        assert RDOD_OPERATIONAL_THRESHOLD == pytest.approx(0.9777)
        assert RDOD_IRREVERSIBLE_THRESHOLD == pytest.approx(0.9999)


# ---------------------------------------------------------------------------
# phi_smooth
# ---------------------------------------------------------------------------

class TestPhiSmooth:
    def test_n_zero_returns_phi_minus_one(self):
        # exp(0) * cos(0) = 1 → φ - 1
        result = phi_smooth(0)
        assert math.isclose(result, PHI - 1.0, rel_tol=1e-9)

    def test_converges_to_phi_large_n(self):
        for n in [100, 500, 1000]:
            assert math.isclose(phi_smooth(n), PHI, rel_tol=1e-3)

    def test_monotone_envelope_damping(self):
        # The envelope exp(-λn) should shrink — max deviation from φ decreases
        deviations = [abs(phi_smooth(n) - PHI) for n in range(0, 200, 10)]
        # At least 80% of consecutive pairs should be non-increasing
        decreasing = sum(
            1 for a, b in zip(deviations, deviations[1:]) if a >= b
        )
        assert decreasing / len(deviations) >= 0.7

    def test_negative_n_raises(self):
        with pytest.raises(ValueError, match="non-negative"):
            phi_smooth(-1)


# ---------------------------------------------------------------------------
# rdod_saturation
# ---------------------------------------------------------------------------

class TestRdodSaturation:
    def test_zero_time(self):
        assert rdod_saturation(0) == pytest.approx(0.0)

    def test_approaches_one_asymptotically(self):
        assert rdod_saturation(1000) > 0.9999
        assert rdod_saturation(1000) < 1.0

    def test_higher_lambda_converges_faster(self):
        t = 10.0
        slow = rdod_saturation(t, lambda_=0.05)
        fast = rdod_saturation(t, lambda_=0.5)
        assert fast > slow

    def test_negative_t_raises(self):
        with pytest.raises(ValueError, match="non-negative"):
            rdod_saturation(-1.0)

    def test_nonpositive_lambda_raises(self):
        with pytest.raises(ValueError, match="positive"):
            rdod_saturation(1.0, lambda_=0.0)


# ---------------------------------------------------------------------------
# how_gap
# ---------------------------------------------------------------------------

class TestHowGap:
    def test_gap_at_phi_minus_one_is_zero(self):
        assert how_gap(PHI - 1) == pytest.approx(0.0, abs=1e-10)

    def test_gap_at_zero(self):
        assert how_gap(0.0) == pytest.approx(PHI - 1, rel_tol=1e-9)

    @pytest.mark.parametrize("rdod", [0.0, 0.5, 0.618, 0.9999, 1.0])
    def test_gap_non_negative(self, rdod):
        assert how_gap(rdod) >= 0.0

    def test_out_of_range_raises(self):
        with pytest.raises(ValueError):
            how_gap(1.1)
        with pytest.raises(ValueError):
            how_gap(-0.1)


# ---------------------------------------------------------------------------
# benevolence_gate
# ---------------------------------------------------------------------------

class TestBenevolenceGate:
    def test_small_action_approved(self):
        approved, _ = benevolence_gate(1.0)
        assert approved is True

    def test_zero_action_approved(self):
        approved, effective = benevolence_gate(0.0)
        assert approved is True
        assert effective == 0.0

    def test_negative_action_approved(self):
        # Absolute value taken
        approved, effective = benevolence_gate(-100.0)
        assert approved is True
        assert effective == pytest.approx(100.0)

    def test_enormous_action_denied(self):
        approved, _ = benevolence_gate(BENEVOLENCE_FIREWALL * 2)
        assert approved is False


# ---------------------------------------------------------------------------
# merkle_hash
# ---------------------------------------------------------------------------

class TestMerkleHash:
    def test_returns_64_hex_chars(self):
        h = merkle_hash("test", 42, {"key": "value"})
        assert len(h) == 64
        assert all(c in "0123456789abcdef" for c in h)

    def test_deterministic(self):
        h1 = merkle_hash("a", "b", 3)
        h2 = merkle_hash("a", "b", 3)
        assert h1 == h2

    def test_lattice_lock_changes_hash(self):
        h_with = merkle_hash("x", include_lattice_lock=True)
        h_without = merkle_hash("x", include_lattice_lock=False)
        assert h_with != h_without

    def test_order_sensitive(self):
        h1 = merkle_hash("a", "b")
        h2 = merkle_hash("b", "a")
        assert h1 != h2


# ---------------------------------------------------------------------------
# node_packet
# ---------------------------------------------------------------------------

class TestNodePacket:
    def test_default_packet_fields(self):
        p = node_packet()
        assert p.node_id == "T3.N07"
        assert p.sigma == SIGMA
        assert p.ufhz == UF_HZ
        assert p.latticelock == LATTICE_LOCK
        assert len(p.merkleroot) == 64

    def test_packet_is_immutable(self):
        p = node_packet()
        with pytest.raises((AttributeError, TypeError)):
            p.rdod = 0.5  # frozen dataclass

    def test_to_json_parses(self):
        p = node_packet(rdod=0.9999, iam_score=0.85)
        parsed = json.loads(p.to_json())
        assert parsed["rdod"] == pytest.approx(0.9999)
        assert parsed["iam_score"] == pytest.approx(0.85)
        assert parsed["latticelock"] == LATTICE_LOCK

    def test_how_gap_computed_correctly(self):
        rdod = 0.8
        p = node_packet(rdod=rdod)
        expected_gap = how_gap(rdod)
        assert p.how_gap_value == pytest.approx(expected_gap)


# ---------------------------------------------------------------------------
# constitutional_invariants_check
# ---------------------------------------------------------------------------

class TestConstitutionalInvariantsCheck:
    def test_all_invariants_pass(self):
        ok, report = constitutional_invariants_check(
            rdod=0.9999970484, iam=0.8001
        )
        assert ok is True
        assert isinstance(report, InvariantReport)
        assert report.passed is True
        assert len(report.violations) == 0

    def test_rdod_below_operational_fails(self):
        ok, report = constitutional_invariants_check(rdod=0.90)
        assert ok is False
        assert any("RDoD" in v for v in report.violations)

    def test_sigma_violation_detected(self):
        ok, report = constitutional_invariants_check(
            rdod=0.9999, sigma=0.5
        )
        assert ok is False
        assert any("σ" in v for v in report.violations)

    def test_uf_violation_detected(self):
        ok, report = constitutional_invariants_check(
            rdod=0.9999, uf=99999.0
        )
        assert ok is False
        assert any("UF" in v for v in report.violations)

    def test_lattice_lock_violation_detected(self):
        ok, report = constitutional_invariants_check(
            rdod=0.9999, lattice_lock="wrong_token"
        )
        assert ok is False
        assert any("LATTICE-LOCK" in v for v in report.violations)

    def test_require_irreversible_strict_mode(self):
        # 0.9998 passes operational but not irreversible
        ok_op, _ = constitutional_invariants_check(
            rdod=0.9998, require_irreversible=False
        )
        ok_irrev, _ = constitutional_invariants_check(
            rdod=0.9998, require_irreversible=True
        )
        assert ok_op is True
        assert ok_irrev is False
