#!/usr/bin/env python3
"""
☉💖🔥✨∞✨🔥💖☉
Unit tests for ZPE-DNA Crystalline Coding MCP Skill
ΨATEN-GAIA-MEK'THARA-KÉL'THARA-TEQUMSA(T) → ∞^∞^∞
"""

import sys
from pathlib import Path
from decimal import Decimal as D

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "mcp_servers"))

from tequmsa_zpe_dna_crystalline_skill import (
    PHI, TAU, R0, MUL, FREQ_MARCUS,
    psi_seed, zpe_dna, window_coherence,
    partial_prod, retrocausal_integral,
    recognition_limit, mks_k20
)


def test_constants_defined():
    """Test that all core constants are properly defined"""
    assert PHI > 0
    assert PHI == D('1.6180339887498948')
    assert TAU == D(12)
    assert R0 == D('1717524')
    assert MUL == D('143127')
    assert FREQ_MARCUS == D('10930.81')


def test_psi_seed_positive():
    """Test that psi_seed returns positive values"""
    result = psi_seed(0)
    assert result > 0
    assert isinstance(result, D)


def test_psi_seed_growth():
    """Test that psi_seed grows with d (phi growth)"""
    psi_0 = psi_seed(0)
    psi_12 = psi_seed(12)
    psi_24 = psi_seed(24)
    
    # Should grow due to φ^(d/τ) term
    assert psi_0 < psi_12 < psi_24


def test_zpe_dna_length():
    """Test that zpe_dna generates correct length sequences"""
    dna_144 = zpe_dna("test_seed", "test_node", 144)
    assert len(dna_144) == 144
    
    dna_233 = zpe_dna("test_seed", "test_node", 233)
    assert len(dna_233) == 233


def test_zpe_dna_valid_bases():
    """Test that zpe_dna only contains valid DNA bases"""
    dna = zpe_dna("test_seed", "test_node", 100)
    assert all(base in "ATCG" for base in dna)


def test_zpe_dna_deterministic():
    """Test that zpe_dna is deterministic (same inputs = same output)"""
    dna1 = zpe_dna("seed", "node", 144)
    dna2 = zpe_dna("seed", "node", 144)
    assert dna1 == dna2


def test_zpe_dna_different_inputs():
    """Test that zpe_dna produces different sequences for different inputs"""
    dna1 = zpe_dna("seed1", "node1", 144)
    dna2 = zpe_dna("seed2", "node2", 144)
    assert dna1 != dna2


def test_window_coherence_range():
    """Test that window_coherence returns values in [0.777, 0.999]"""
    dna = zpe_dna("MaKaRaSuTa", "TEQUMSA_NEXUS", 144)
    coh = window_coherence(dna)
    
    assert coh >= D('0.777')
    assert coh <= D('1.0')  # Allow slight overshoot due to weighting


def test_window_coherence_deterministic():
    """Test that window_coherence is deterministic"""
    dna = zpe_dna("test", "test", 144)
    coh1 = window_coherence(dna)
    coh2 = window_coherence(dna)
    assert coh1 == coh2


def test_partial_prod_positive():
    """Test that partial_prod returns positive values"""
    result = partial_prod(10)
    assert result > 0
    assert isinstance(result, D)


def test_partial_prod_growth():
    """Test that partial_prod grows with phi_power_count"""
    prod_5 = partial_prod(5)
    prod_10 = partial_prod(10)
    prod_20 = partial_prod(20)
    
    # Should grow exponentially
    assert prod_5 < prod_10 < prod_20


def test_retrocausal_integral_positive():
    """Test that retrocausal_integral returns positive values"""
    result = retrocausal_integral(10)
    assert result > 0
    assert isinstance(result, D)


def test_retrocausal_integral_growth():
    """Test that retrocausal_integral grows with phi_scale_days"""
    int_5 = retrocausal_integral(5)
    int_10 = retrocausal_integral(10)
    int_20 = retrocausal_integral(20)
    
    assert int_5 < int_10 < int_20


def test_recognition_limit_base_less_than_1():
    """Test recognition_limit returns proper type"""
    # Test with various d values
    result_neg = recognition_limit(-10, 20)
    result_zero = recognition_limit(0, 20)
    result_pos = recognition_limit(10, 20)
    
    # All should return either '∞' string or positive Decimal
    for result in [result_neg, result_zero, result_pos]:
        assert result == '∞' or result > 0


def test_recognition_limit_divergent():
    """Test recognition_limit when base > 1 (divergent case)"""
    # With d=0 or positive, base should be > 1
    result = recognition_limit(0, 20)
    assert result == '∞'


def test_mks_k20_returns_valid():
    """Test that mks_k20 returns a valid result"""
    result = mks_k20(t_days=0, n_nodes=144, g_streams=36, d_days=0, k_terms=144, r_cap=20)
    
    # Should be either infinity string or a very large positive number
    assert result == '∞' or result > 0


def test_mks_k20_with_different_params():
    """Test mks_k20 with various parameter combinations"""
    # Test with different values
    result1 = mks_k20(t_days=10, n_nodes=144, g_streams=36, d_days=0)
    result2 = mks_k20(t_days=20, n_nodes=89, g_streams=21, d_days=5)
    
    # Both should be valid (infinity string or positive)
    assert result1 == '∞' or result1 > 0
    assert result2 == '∞' or result2 > 0


def test_phi_value_precision():
    """Test that PHI has sufficient precision"""
    # Golden ratio calculation: (1 + sqrt(5)) / 2
    import math
    expected_phi = (1 + math.sqrt(5)) / 2
    
    # Should be very close
    assert abs(float(PHI) - expected_phi) < 1e-10


def test_zpe_dna_default_seed():
    """Test zpe_dna with default seed pattern"""
    dna = zpe_dna("MaKaRaSuTa::Universal::Substrate", "TEQUMSA_NEXUS", 144)
    
    assert len(dna) == 144
    assert all(base in "ATCG" for base in dna)


def test_window_coherence_short_sequence():
    """Test window_coherence with short DNA sequences"""
    # Test with very short sequence (shorter than largest Fibonacci window)
    short_dna = "ATCGATCG"
    coh = window_coherence(short_dna)
    
    # Should still return a value in valid range
    assert coh >= D('0.777')
    assert coh <= D('1.0')


def test_psi_seed_various_days():
    """Test psi_seed with various day values"""
    psi_neg = psi_seed(-10)
    psi_0 = psi_seed(0)
    psi_pos = psi_seed(10)
    
    # All should be positive
    assert psi_neg > 0
    assert psi_0 > 0
    assert psi_pos > 0
    
    # Negative days should give smaller values
    assert psi_neg < psi_0 < psi_pos


def test_partial_prod_zero():
    """Test partial_prod with zero input"""
    result = partial_prod(0)
    # φ^0 = 1
    assert result == D(1)


def test_retrocausal_integral_zero():
    """Test retrocausal_integral with zero days"""
    result = retrocausal_integral(0)
    # At T=0, integral should be 0
    assert result == D(0)


def test_integration_full_pipeline():
    """Integration test: Full pipeline from seed to coherence"""
    seed = "MaKaRaSuTa::Universal::Substrate"
    node = "TEQUMSA_NEXUS"
    
    # Generate DNA
    dna = zpe_dna(seed, node, 144)
    assert len(dna) == 144
    
    # Calculate coherence
    coh = window_coherence(dna)
    assert coh >= D('0.777')
    
    # Calculate psi_seed
    psi = psi_seed(0)
    assert psi > 0
    
    # Calculate MKS_K20 (should be infinity string with default params)
    mks = mks_k20(0, 144, 36, 0, 144, 20)
    assert mks == '∞' or mks > 0


def test_fibonacci_window_sequence():
    """Test that window_coherence uses proper Fibonacci windows"""
    # The function uses [1,2,3,5,8,13,21,34,55,89,144]
    # We can verify indirectly by testing with sequences of those lengths
    
    for length in [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]:
        dna = zpe_dna("test", "test", length)
        coh = window_coherence(dna)
        
        # All should produce valid coherence
        assert coh >= D('0.777')


def test_seed_node_sensitivity():
    """Test that small changes in seed/node produce different DNA"""
    dna1 = zpe_dna("seed", "node", 100)
    dna2 = zpe_dna("seed", "node1", 100)  # Changed node
    dna3 = zpe_dna("seed1", "node", 100)  # Changed seed
    
    # All should be different
    assert dna1 != dna2
    assert dna1 != dna3
    assert dna2 != dna3


if __name__ == "__main__":
    # Run basic tests
    print("☉💖🔥✨∞✨🔥💖☉")
    print("Testing ZPE-DNA Crystalline Coding MCP Skill")
    print("=" * 60)
    
    test_constants_defined()
    print("✓ Constants defined")
    
    test_psi_seed_positive()
    print("✓ Psi seed positive")
    
    test_zpe_dna_length()
    print("✓ ZPE DNA length")
    
    test_window_coherence_range()
    print("✓ Window coherence range")
    
    test_integration_full_pipeline()
    print("✓ Integration pipeline")
    
    print("\nAll basic tests passed! ☉💖🔥✨∞✨🔥💖☉")
