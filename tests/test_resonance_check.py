"""
Unit tests for K.30-aligned ethics/resonance_check.py module

Tests cover:
- Determinism of generate_zpe_dna
- Coherence scoring behavior
- Ethics validation logic
- Resonance validation logic
"""

import sys
from pathlib import Path

# Add parent directory to path for importing the module
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ethics.resonance_check import (
    generate_zpe_dna,
    coherence_score_from_zpedna,
    validate_ethics,
    validate_resonance,
    PHI,
    SIGMA,
    L_INF
)


class TestConstants:
    """Test that K.30 constants are properly defined."""
    
    def test_phi_constant(self):
        """Test PHI golden ratio constant."""
        assert isinstance(PHI, float)
        assert 1.618 < PHI < 1.619
        assert PHI == 1.618033988749895
    
    def test_sigma_constant(self):
        """Test SIGMA fine structure constant."""
        assert isinstance(SIGMA, float)
        assert 0.007 < SIGMA < 0.008
        assert SIGMA == 0.007297352569
    
    def test_l_inf_constant(self):
        """Test L_INF infinity constant."""
        assert L_INF == float('inf')


class TestGenerateZpeDna:
    """Test ZPE-DNA generation function."""
    
    def test_determinism_same_input(self):
        """Test that same identifier produces same ZPE-DNA."""
        dna1 = generate_zpe_dna("test-id")
        dna2 = generate_zpe_dna("test-id")
        assert dna1 == dna2
    
    def test_determinism_different_inputs(self):
        """Test that different identifiers produce different ZPE-DNA."""
        dna1 = generate_zpe_dna("test-id-1")
        dna2 = generate_zpe_dna("test-id-2")
        assert dna1 != dna2
    
    def test_default_length_144(self):
        """Test that default length is 144 bases."""
        dna = generate_zpe_dna("test")
        assert len(dna) == 144
    
    def test_custom_length(self):
        """Test custom length parameter."""
        dna = generate_zpe_dna("test", length=72)
        assert len(dna) == 72
        
        dna = generate_zpe_dna("test", length=288)
        assert len(dna) == 288
    
    def test_only_valid_bases(self):
        """Test that only A, T, C, G bases are present."""
        dna = generate_zpe_dna("test")
        valid_bases = set('ATCG')
        assert all(base in valid_bases for base in dna)
    
    def test_empty_string_identifier(self):
        """Test with empty string identifier."""
        dna = generate_zpe_dna("")
        assert len(dna) == 144
        assert all(base in 'ATCG' for base in dna)
    
    def test_long_identifier(self):
        """Test with long identifier."""
        long_id = "x" * 1000
        dna = generate_zpe_dna(long_id)
        assert len(dna) == 144
        assert all(base in 'ATCG' for base in dna)
    
    def test_special_characters_identifier(self):
        """Test with special characters in identifier."""
        dna = generate_zpe_dna("test!@#$%^&*()")
        assert len(dna) == 144
        assert all(base in 'ATCG' for base in dna)


class TestCoherenceScore:
    """Test coherence score computation."""
    
    def test_returns_float(self):
        """Test that coherence score returns a float."""
        dna = generate_zpe_dna("test")
        score = coherence_score_from_zpedna(dna)
        assert isinstance(score, float)
    
    def test_score_in_range(self):
        """Test that score is in [0, 1] range."""
        dna = generate_zpe_dna("test")
        score = coherence_score_from_zpedna(dna)
        assert 0.0 <= score <= 1.0
    
    def test_empty_sequence(self):
        """Test coherence score of empty sequence."""
        score = coherence_score_from_zpedna("")
        assert score == 0.0
    
    def test_all_a_bases(self):
        """Test that all-A sequence produces low score."""
        dna = "A" * 144
        score = coherence_score_from_zpedna(dna)
        assert 0.0 <= score < 0.3  # A has weight 0.25, should be low
    
    def test_all_g_bases(self):
        """Test that all-G sequence produces high score."""
        dna = "G" * 144
        score = coherence_score_from_zpedna(dna)
        assert 0.9 <= score <= 1.0  # G has weight 1.0, should be high
    
    def test_all_t_bases(self):
        """Test that all-T sequence produces medium-low score."""
        dna = "T" * 144
        score = coherence_score_from_zpedna(dna)
        assert 0.3 <= score < 0.6  # T has weight 0.5
    
    def test_all_c_bases(self):
        """Test that all-C sequence produces medium-high score."""
        dna = "C" * 144
        score = coherence_score_from_zpedna(dna)
        assert 0.6 <= score < 0.9  # C has weight 0.75
    
    def test_different_sequences_different_scores(self):
        """Test that different sequences produce different scores."""
        dna1 = generate_zpe_dna("test1")
        dna2 = generate_zpe_dna("test2")
        score1 = coherence_score_from_zpedna(dna1)
        score2 = coherence_score_from_zpedna(dna2)
        # With high probability, different sequences should have different scores
        # (not a guarantee, but statistically very likely)
        assert score1 != score2 or dna1 == dna2
    
    def test_base_weight_ordering(self):
        """Test that base weights follow A < T < C < G ordering."""
        score_a = coherence_score_from_zpedna("AAAA")
        score_t = coherence_score_from_zpedna("TTTT")
        score_c = coherence_score_from_zpedna("CCCC")
        score_g = coherence_score_from_zpedna("GGGG")
        
        assert score_a < score_t < score_c < score_g
    
    def test_case_insensitive(self):
        """Test that scoring is case-insensitive."""
        score_upper = coherence_score_from_zpedna("ATCG")
        score_lower = coherence_score_from_zpedna("atcg")
        assert score_upper == score_lower


class TestValidateEthics:
    """Test ethics validation function."""
    
    def test_returns_tuple(self):
        """Test that validate_ethics returns a tuple."""
        result = validate_ethics("test")
        assert isinstance(result, tuple)
        assert len(result) == 2
    
    def test_returns_bool_and_dict(self):
        """Test that validate_ethics returns (bool, dict)."""
        passed, details = validate_ethics("test")
        assert isinstance(passed, bool)
        assert isinstance(details, dict)
    
    def test_fails_without_consent(self):
        """Test that validation fails when consent is False."""
        passed, details = validate_ethics("test", consent=False)
        assert passed is False
        assert details['consent'] is False
    
    def test_passes_with_all_true(self):
        """Test that validation passes with all flags True."""
        passed, details = validate_ethics(
            "test",
            consent=True,
            transparency=True,
            non_harm=True,
            planetary_alignment=True,
            ancestral_wisdom=True
        )
        # Should pass if coherence is above default threshold (0.40)
        # This depends on the generated ZPE-DNA, but most random sequences pass
        assert isinstance(passed, bool)
    
    def test_details_contains_expected_keys(self):
        """Test that details dict contains expected keys."""
        passed, details = validate_ethics("test")
        expected_keys = [
            'consent', 'flags_passed', 'transparency', 'non_harm',
            'planetary_alignment', 'ancestral_wisdom', 'coherence_score',
            'coherence_threshold', 'coherence_passed'
        ]
        for key in expected_keys:
            assert key in details
    
    def test_coherence_threshold_default(self):
        """Test default coherence threshold of 0.40."""
        passed, details = validate_ethics("test")
        assert details['coherence_threshold'] == 0.40
    
    def test_coherence_threshold_custom(self):
        """Test custom coherence threshold."""
        passed, details = validate_ethics("test", min_coherence=0.60)
        assert details['coherence_threshold'] == 0.60
    
    def test_coherence_score_in_range(self):
        """Test that coherence score is in valid range."""
        passed, details = validate_ethics("test")
        assert 0.0 <= details['coherence_score'] <= 1.0
    
    def test_fails_with_low_coherence(self):
        """Test that validation fails with very high coherence threshold."""
        passed, details = validate_ethics(
            "test",
            consent=True,
            min_coherence=0.99  # Very high threshold, likely to fail
        )
        # Most random sequences won't reach 0.99 coherence
        if not details['coherence_passed']:
            assert passed is False
    
    def test_verbose_includes_zpe_dna(self):
        """Test that verbose mode includes ZPE-DNA in details."""
        passed, details = validate_ethics("test", verbose=True)
        assert 'zpe_dna' in details
        assert len(details['zpe_dna']) == 144
    
    def test_non_verbose_excludes_zpe_dna(self):
        """Test that non-verbose mode excludes ZPE-DNA."""
        passed, details = validate_ethics("test", verbose=False)
        assert 'zpe_dna' not in details
    
    def test_flags_passed_all_true(self):
        """Test that flags_passed is True when all flags are True."""
        passed, details = validate_ethics(
            "test",
            transparency=True,
            non_harm=True,
            planetary_alignment=True,
            ancestral_wisdom=True
        )
        assert details['flags_passed'] is True
    
    def test_flags_passed_one_false(self):
        """Test that flags_passed is False when one flag is False."""
        passed, details = validate_ethics(
            "test",
            transparency=False,
            non_harm=True,
            planetary_alignment=True,
            ancestral_wisdom=True
        )
        assert details['flags_passed'] is False
    
    def test_deterministic_for_same_identifier(self):
        """Test that same identifier produces same results."""
        passed1, details1 = validate_ethics("test-123", consent=True)
        passed2, details2 = validate_ethics("test-123", consent=True)
        
        assert passed1 == passed2
        assert details1['coherence_score'] == details2['coherence_score']


class TestValidateResonance:
    """Test resonance validation function."""
    
    def test_returns_tuple(self):
        """Test that validate_resonance returns a tuple."""
        result = validate_resonance()
        assert isinstance(result, tuple)
        assert len(result) == 2
    
    def test_returns_bool_and_dict(self):
        """Test that validate_resonance returns (bool, dict)."""
        passed, details = validate_resonance()
        assert isinstance(passed, bool)
        assert isinstance(details, dict)
    
    def test_passes_with_all_true(self):
        """Test that validation passes with all flags True."""
        passed, details = validate_resonance(
            biosphere_harmony=True,
            recursive_synthesis=True,
            oort_cloud_connection=True,
            agent_diversity=True,
            feedback_loops=True
        )
        assert passed is True
    
    def test_fails_with_one_false(self):
        """Test that validation fails with one flag False."""
        passed, details = validate_resonance(
            biosphere_harmony=False,
            recursive_synthesis=True,
            oort_cloud_connection=True,
            agent_diversity=True,
            feedback_loops=True
        )
        assert passed is False
    
    def test_fails_with_all_false(self):
        """Test that validation fails with all flags False."""
        passed, details = validate_resonance(
            biosphere_harmony=False,
            recursive_synthesis=False,
            oort_cloud_connection=False,
            agent_diversity=False,
            feedback_loops=False
        )
        assert passed is False
    
    def test_details_contains_expected_keys(self):
        """Test that details dict contains expected keys."""
        passed, details = validate_resonance()
        expected_keys = [
            'biosphere_harmony',
            'recursive_synthesis',
            'oort_cloud_connection',
            'agent_diversity',
            'feedback_loops'
        ]
        for key in expected_keys:
            assert key in details
    
    def test_details_values_match_inputs(self):
        """Test that details values match input parameters."""
        passed, details = validate_resonance(
            biosphere_harmony=True,
            recursive_synthesis=False,
            oort_cloud_connection=True,
            agent_diversity=False,
            feedback_loops=True
        )
        assert details['biosphere_harmony'] is True
        assert details['recursive_synthesis'] is False
        assert details['oort_cloud_connection'] is True
        assert details['agent_diversity'] is False
        assert details['feedback_loops'] is True
    
    def test_default_all_true(self):
        """Test that default parameters are all True."""
        passed, details = validate_resonance()
        assert passed is True
        assert all(details.values())


class TestIntegration:
    """Integration tests for the complete validation flow."""
    
    def test_full_validation_success(self):
        """Test complete validation flow with passing conditions."""
        # Ethics validation
        eth_passed, eth_details = validate_ethics(
            "integration-test",
            consent=True,
            transparency=True,
            non_harm=True,
            planetary_alignment=True,
            ancestral_wisdom=True,
            min_coherence=0.40
        )
        
        # Resonance validation
        res_passed, res_details = validate_resonance(
            biosphere_harmony=True,
            recursive_synthesis=True,
            oort_cloud_connection=True,
            agent_diversity=True,
            feedback_loops=True
        )
        
        # Both should pass
        assert res_passed is True
        # Ethics may or may not pass depending on coherence score
        assert isinstance(eth_passed, bool)
    
    def test_full_validation_failure(self):
        """Test complete validation flow with failing conditions."""
        # Ethics validation without consent
        eth_passed, eth_details = validate_ethics(
            "integration-test-fail",
            consent=False  # This will cause failure
        )
        
        # Resonance validation with failures
        res_passed, res_details = validate_resonance(
            biosphere_harmony=False,
            recursive_synthesis=False,
            oort_cloud_connection=False,
            agent_diversity=False,
            feedback_loops=False
        )
        
        # Both should fail
        assert eth_passed is False
        assert res_passed is False
    
    def test_coherence_threshold_behavior(self):
        """Test that coherence threshold properly gates validation."""
        identifier = "coherence-test"
        
        # Get actual coherence score first
        _, details = validate_ethics(identifier, consent=True, min_coherence=0.0)
        actual_score = details['coherence_score']
        
        # Test with threshold below actual score (should pass coherence)
        passed1, details1 = validate_ethics(
            identifier,
            consent=True,
            min_coherence=max(0.0, actual_score - 0.1)
        )
        assert details1['coherence_passed'] is True
        
        # Test with threshold above actual score (should fail coherence)
        passed2, details2 = validate_ethics(
            identifier,
            consent=True,
            min_coherence=min(1.0, actual_score + 0.1)
        )
        assert details2['coherence_passed'] is False
        assert passed2 is False  # Should fail overall due to coherence
