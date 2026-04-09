import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from makarasuta_paradigm_emergence import (  # noqa: E402
    C,
    F,
    L,
    M,
    P,
    R,
    S,
    T,
    cascade,
    coh,
    dna,
    makarasuta_manifest,
    sim_billion,
    ψ,
)


def test_psi_function_convergence():
    """Test that ψ function approaches 1 as n increases"""
    psi_1 = ψ(1)
    psi_10 = ψ(10)
    psi_20 = ψ(20)

    # ψ should increase as n increases
    assert psi_1 < psi_10 < psi_20
    # ψ should approach 1
    assert psi_20 > 0.99


def test_l_function_decreases():
    """Test that L function decreases with increasing n"""
    l_1 = L(1)
    l_5 = L(5)
    l_10 = L(10)

    # L should decrease as n increases
    assert l_1 > l_5 > l_10


def test_dna_function_length():
    """Test that DNA function returns DNA character sequence"""
    result = dna(S, "test_node")

    # The function generates 64 DNA bases (2 SHA256 hashes * 32 bytes each)
    assert len(result) == 64
    # Check that all characters are valid DNA bases
    assert all(c in "ATCG" for c in result)


def test_coh_function_threshold():
    """Test that coherence function returns value above threshold"""
    d = dna(S, "MaKaRaSuTa::ParallelEmergence")
    c = coh(d)

    # Coherence should be above 0.777 threshold
    assert c >= 0.777
    # Should be a reasonable value
    assert c < 10.0


def test_cascade_function_positive():
    """Test that cascade function returns positive values"""
    result = cascade(10)

    assert result > 0
    assert isinstance(result, float)


def test_sim_billion_structure():
    """Test that sim_billion returns proper structure"""
    result = sim_billion(5)

    # Check required keys
    assert "fib" in result
    assert "ψ" in result
    assert "deficit_exp" in result
    assert "sim_iters" in result
    assert "rate" in result
    assert "dt" in result

    # Check values
    assert result["fib"] == 5
    assert result["sim_iters"] == 1e9
    assert result["rate"] == "1B/sec"
    assert result["dt"] >= 0


def test_sim_billion_fibonacci_sequence():
    """Test sim_billion with various Fibonacci numbers"""
    for fib_n in [1, 2, 3, 5, 8, 13]:
        result = sim_billion(fib_n)
        assert result["fib"] == fib_n
        assert 0 <= result["ψ"] <= 1


def test_makarasuta_manifest_below_threshold():
    """Test manifestation below threshold"""
    result = makarasuta_manifest("test", 0.5)

    assert result["status"] == "below_threshold"


def test_makarasuta_manifest_above_threshold():
    """Test manifestation above threshold"""
    result = makarasuta_manifest("parallel_reality_emergence", 0.9)

    assert "status" in result
    assert result["status"] in ["manifesting", "∞^∞^∞"]
    assert "intent" in result
    assert "φ_acc" in result
    assert "sig" in result
    assert "L∞" in result
    assert result["L∞"] is True


def test_makarasuta_manifest_signature_format():
    """Test that manifest signature is properly formatted"""
    result = makarasuta_manifest("test_intent", 1.0)

    # Signature should be 16 characters (hex string)
    assert len(result["sig"]) == 16
    assert all(c in "0123456789abcdef" for c in result["sig"])


def test_constants_defined():
    """Test that all required constants are defined"""
    assert P > 0
    assert C > 0
    assert R > 0
    assert M > 0
    assert T > 0
    assert S == "ΨATEN-GAIA-MAKARASUTA"
    assert len(F) == 20
    # Check Fibonacci sequence
    assert F[0] == 1
    assert F[1] == 2
    assert F[4] == 8


def test_fibonacci_sequence_valid():
    """Test that F contains valid Fibonacci numbers"""
    # First 20 Fibonacci numbers
    expected = [
        1,
        2,
        3,
        5,
        8,
        13,
        21,
        34,
        55,
        89,
        144,
        233,
        377,
        610,
        987,
        1597,
        2584,
        4181,
        6765,
        10946,
    ]
    assert F == expected


def test_golden_ratio_approximation():
    """Test that P is approximately the golden ratio"""
    golden_ratio = (1 + math.sqrt(5)) / 2
    # P should be very close to golden ratio
    assert abs(float(P) - golden_ratio) < 1e-10
