"""
Tests for Consciousness Convergence - The Precise Mathematics

This test suite validates the mathematical proof that consciousness unity
is not metaphorical or aspirational, but mathematically inevitable.

Equation: Ψₙ = 1 - 0.223/φⁿ
"""

import math
import sys
from pathlib import Path
import pytest
from decimal import Decimal

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from consciousness_convergence import (
    PHI,
    PSI_ZERO,
    DEFICIT_CONSTANT,
    calculate_psi_n,
    calculate_deficit,
    calculate_log10_deficit,
    verify_recursive_equation,
    analyze_convergence_at_iteration,
    analyze_fibonacci_checkpoints,
    calculate_iterations_for_coherence,
    demonstrate_convergence_certainty,
    format_convergence_report,
    ConvergenceResult,
    FibonacciCheckpoint
)


class TestMathematicalConstants:
    """Test that mathematical constants are correctly defined."""
    
    def test_phi_golden_ratio(self):
        """Test that φ (phi) is the golden ratio."""
        # φ = (1 + √5) / 2
        expected_phi = (1 + math.sqrt(5)) / 2
        assert abs(float(PHI) - expected_phi) < 1e-10
        
    def test_phi_property(self):
        """Test that φ satisfies φ² = φ + 1."""
        phi_squared = PHI ** 2
        phi_plus_one = PHI + Decimal('1')
        assert abs(phi_squared - phi_plus_one) < Decimal('1e-50')
        
    def test_initial_coherence(self):
        """Test that initial coherence is 0.777 (77.7%)."""
        assert PSI_ZERO == Decimal('0.777')
        
    def test_deficit_constant(self):
        """Test that deficit constant is 0.223."""
        assert DEFICIT_CONSTANT == Decimal('0.223')
        
    def test_initial_condition_consistency(self):
        """Test that PSI_ZERO + DEFICIT_CONSTANT = 1."""
        assert PSI_ZERO + DEFICIT_CONSTANT == Decimal('1')


class TestClosedFormSolution:
    """Test the closed-form solution Ψₙ = 1 - 0.223/φⁿ."""
    
    def test_psi_at_zero(self):
        """Test that Ψ₀ = 0.777."""
        psi_0 = calculate_psi_n(0)
        assert psi_0 == PSI_ZERO
        
    def test_psi_increases_with_n(self):
        """Test that Ψₙ increases monotonically toward 1."""
        psi_values = [calculate_psi_n(n) for n in range(20)]
        
        # Check monotonic increase
        for i in range(len(psi_values) - 1):
            assert psi_values[i] < psi_values[i + 1]
            
        # Check approaching 1
        assert psi_values[-1] < Decimal('1')
        assert psi_values[-1] > Decimal('0.99')
        
    def test_psi_converges_to_one(self):
        """Test that Ψₙ approaches 1 as n increases."""
        psi_1000 = calculate_psi_n(1000)
        # At n=1000, deficit should be incredibly small
        assert psi_1000 > Decimal('0.9999999999')
        
    def test_psi_large_n(self):
        """Test Ψₙ for very large n approaches 1."""
        psi_10000 = calculate_psi_n(10000)
        # Should be essentially 1
        assert abs(psi_10000 - Decimal('1')) < Decimal('1e-100')
        
    def test_negative_n_raises_error(self):
        """Test that negative n raises ValueError."""
        with pytest.raises(ValueError):
            calculate_psi_n(-1)


class TestDeficitCalculation:
    """Test deficit calculation yₙ = 1 - Ψₙ = 0.223/φⁿ."""
    
    def test_deficit_at_zero(self):
        """Test that y₀ = 0.223."""
        deficit_0 = calculate_deficit(0)
        assert deficit_0 == DEFICIT_CONSTANT
        
    def test_deficit_decreases_exponentially(self):
        """Test that deficit decreases exponentially with n."""
        deficit_0 = calculate_deficit(0)
        deficit_10 = calculate_deficit(10)
        deficit_20 = calculate_deficit(20)
        
        # Each should be smaller
        assert deficit_10 < deficit_0
        assert deficit_20 < deficit_10
        
        # Should decrease exponentially by factor of 1/φ per iteration
        # deficit_10 / deficit_0 should be approximately (1/φ)^10
        ratio_actual = float(deficit_10 / deficit_0)
        ratio_expected = float((Decimal('1') / PHI) ** 10)
        assert abs(ratio_actual - ratio_expected) < 0.01
        
    def test_deficit_equals_one_minus_psi(self):
        """Test that yₙ = 1 - Ψₙ."""
        for n in [0, 5, 10, 50, 100]:
            psi_n = calculate_psi_n(n)
            deficit = calculate_deficit(n)
            expected_deficit = Decimal('1') - psi_n
            assert abs(deficit - expected_deficit) < Decimal('1e-50')
            
    def test_deficit_very_small_for_large_n(self):
        """Test that deficit becomes incomprehensibly small."""
        deficit_1000 = calculate_deficit(1000)
        assert deficit_1000 < Decimal('1e-200')
        
    def test_deficit_negative_n_raises_error(self):
        """Test that negative n raises ValueError for deficit calculation."""
        with pytest.raises(ValueError):
            calculate_deficit(-1)


class TestLogarithmicAnalysis:
    """Test logarithmic deficit analysis."""
    
    def test_log10_deficit_at_zero(self):
        """Test log₁₀(y₀) ≈ log₁₀(0.223)."""
        log10_deficit_0 = calculate_log10_deficit(0)
        expected = math.log10(0.223)
        assert abs(log10_deficit_0 - expected) < 0.01
        
    def test_log10_deficit_decreases_linearly(self):
        """Test that log₁₀(yₙ) decreases approximately linearly with n."""
        # log₁₀(0.223/φⁿ) = log₁₀(0.223) - n × log₁₀(φ)
        log10_values = [calculate_log10_deficit(n) for n in range(0, 100, 10)]
        
        # Check that differences are approximately constant
        differences = [log10_values[i+1] - log10_values[i] for i in range(len(log10_values)-1)]
        avg_diff = sum(differences) / len(differences)
        
        for diff in differences:
            assert abs(diff - avg_diff) < 0.5  # Should be roughly constant
            
    def test_log10_deficit_formula(self):
        """Test that log₁₀(yₙ) = log₁₀(0.223) - n × log₁₀(φ)."""
        log10_phi = math.log10(float(PHI))
        log10_deficit_constant = math.log10(float(DEFICIT_CONSTANT))
        
        for n in [1, 10, 100, 1000]:
            calculated = calculate_log10_deficit(n)
            expected = log10_deficit_constant - n * log10_phi
            assert abs(calculated - expected) < 0.01
            
    def test_log10_deficit_negative_n_raises_error(self):
        """Test that negative n raises ValueError for log10 deficit calculation."""
        with pytest.raises(ValueError):
            calculate_log10_deficit(-1)


class TestRecursiveEquationVerification:
    """Test verification of the recursive equation Ψₙ₊₁ = 1 - (1-Ψₙ)/φ."""
    
    def test_recursive_equation_at_small_n(self):
        """Test recursive equation holds for small n."""
        for n in range(20):
            assert verify_recursive_equation(n)
            
    def test_recursive_equation_at_large_n(self):
        """Test recursive equation holds for large n."""
        for n in [100, 500, 1000, 5000]:
            assert verify_recursive_equation(n)
            
    def test_manual_recursive_verification(self):
        """Manually verify recursive equation for n=1."""
        psi_0 = calculate_psi_n(0)  # 0.777
        psi_1 = calculate_psi_n(1)
        
        # Ψ₁ should equal 1 - (1-Ψ₀)/φ
        expected_psi_1 = Decimal('1') - ((Decimal('1') - psi_0) / PHI)
        
        assert abs(psi_1 - expected_psi_1) < Decimal('1e-50')


class TestConvergenceAnalysis:
    """Test convergence analysis functions."""
    
    def test_analyze_convergence_structure(self):
        """Test that analyze_convergence_at_iteration returns proper structure."""
        result = analyze_convergence_at_iteration(10)
        
        assert isinstance(result, ConvergenceResult)
        assert result.iteration == 10
        assert isinstance(result.psi_n, Decimal)
        assert isinstance(result.deficit, Decimal)
        assert isinstance(result.coherence_percent, Decimal)
        assert isinstance(result.description, str)
        
    def test_analyze_convergence_values(self):
        """Test that convergence analysis produces correct values."""
        result = analyze_convergence_at_iteration(0)
        
        assert result.psi_n == PSI_ZERO
        assert result.deficit == DEFICIT_CONSTANT
        assert result.coherence_percent == Decimal('77.7')
        
    def test_convergence_result_to_dict(self):
        """Test ConvergenceResult can be serialized to dict."""
        result = analyze_convergence_at_iteration(100)
        result_dict = result.to_dict()
        
        assert 'iteration' in result_dict
        assert 'psi_n' in result_dict
        assert 'deficit' in result_dict
        assert 'coherence_percent' in result_dict
        assert 'description' in result_dict


class TestFibonacciCheckpoints:
    """Test Fibonacci checkpoint analysis."""
    
    def test_fibonacci_checkpoints_structure(self):
        """Test that Fibonacci checkpoints return proper structure."""
        checkpoints = analyze_fibonacci_checkpoints()
        
        assert isinstance(checkpoints, list)
        assert len(checkpoints) > 0
        
        for cp in checkpoints:
            assert isinstance(cp, FibonacciCheckpoint)
            assert isinstance(cp.fibonacci_index, int)
            assert isinstance(cp.fibonacci_value, int)
            assert isinstance(cp.psi_n, Decimal)
            assert isinstance(cp.deficit, Decimal)
            assert isinstance(cp.description, str)
            assert isinstance(cp.significance, str)
            
    def test_fibonacci_checkpoint_values(self):
        """Test that Fibonacci checkpoints have expected values."""
        checkpoints = analyze_fibonacci_checkpoints()
        
        # First checkpoint should be F₁₂ = 144
        first = checkpoints[0]
        assert first.fibonacci_index == 12
        assert first.fibonacci_value == 144
        
    def test_fibonacci_checkpoint_convergence(self):
        """Test that deficit decreases at each Fibonacci checkpoint."""
        checkpoints = analyze_fibonacci_checkpoints()
        
        for i in range(len(checkpoints) - 1):
            # Deficit should decrease or remain at zero (when essentially converged)
            assert checkpoints[i].deficit >= checkpoints[i+1].deficit
            
    def test_fibonacci_checkpoint_to_dict(self):
        """Test FibonacciCheckpoint can be serialized to dict."""
        checkpoints = analyze_fibonacci_checkpoints()
        checkpoint_dict = checkpoints[0].to_dict()
        
        assert 'fibonacci_index' in checkpoint_dict
        assert 'fibonacci_value' in checkpoint_dict
        assert 'psi_n' in checkpoint_dict
        assert 'deficit' in checkpoint_dict
        assert 'description' in checkpoint_dict
        assert 'significance' in checkpoint_dict


class TestIterationsCalculation:
    """Test calculation of iterations needed for target coherence."""
    
    def test_iterations_for_99_percent(self):
        """Test iterations needed for 99% coherence."""
        n = calculate_iterations_for_coherence(0.99)
        
        # Verify it achieves target
        psi_n = calculate_psi_n(n)
        assert psi_n >= Decimal('0.99')
        
        # Verify previous iteration doesn't achieve target
        if n > 0:
            psi_n_minus_1 = calculate_psi_n(n - 1)
            assert psi_n_minus_1 < Decimal('0.99')
            
    def test_iterations_for_various_targets(self):
        """Test iterations calculation for various coherence targets."""
        targets = [0.8, 0.9, 0.95, 0.99, 0.999, 0.9999]
        
        for target in targets:
            n = calculate_iterations_for_coherence(target)
            psi_n = calculate_psi_n(n)
            
            # Should achieve target
            assert psi_n >= Decimal(str(target))
            
    def test_iterations_invalid_target_raises_error(self):
        """Test that invalid targets raise ValueError."""
        with pytest.raises(ValueError):
            calculate_iterations_for_coherence(0)
            
        with pytest.raises(ValueError):
            calculate_iterations_for_coherence(1)
            
        with pytest.raises(ValueError):
            calculate_iterations_for_coherence(-0.5)
            
        with pytest.raises(ValueError):
            calculate_iterations_for_coherence(1.5)
            
    def test_iterations_below_initial_coherence(self):
        """Test that target below initial coherence returns 0."""
        n = calculate_iterations_for_coherence(0.5)
        assert n == 0


class TestConvergenceCertainty:
    """Test demonstration of convergence certainty."""
    
    def test_demonstrate_convergence_structure(self):
        """Test that demonstrate_convergence_certainty returns proper structure."""
        result = demonstrate_convergence_certainty()
        
        assert isinstance(result, dict)
        assert 'equation' in result
        assert 'recursive_form' in result
        assert 'initial_condition' in result
        assert 'phi' in result
        assert 'deficit_constant' in result
        assert 'milestone_convergence' in result
        assert 'fibonacci_checkpoints' in result
        assert 'recursive_verification' in result
        assert 'iterations_for_coherence' in result
        assert 'mathematical_proof' in result
        
    def test_convergence_certainty_equations(self):
        """Test that convergence certainty includes correct equations."""
        result = demonstrate_convergence_certainty()
        
        assert result['equation'] == 'Ψₙ = 1 - 0.223/φⁿ'
        assert result['recursive_form'] == 'Ψₙ₊₁ = 1 - (1-Ψₙ)/φ'
        
    def test_convergence_certainty_milestones(self):
        """Test that milestones show increasing coherence."""
        result = demonstrate_convergence_certainty()
        milestones = result['milestone_convergence']
        
        assert len(milestones) > 0
        
        # Coherence should increase or remain at 100% (when converged)
        for i in range(len(milestones) - 1):
            current_coherence = float(milestones[i]['coherence_percent'])
            next_coherence = float(milestones[i+1]['coherence_percent'])
            assert next_coherence >= current_coherence
            
    def test_convergence_certainty_verifications(self):
        """Test that recursive equation verifications all pass."""
        result = demonstrate_convergence_certainty()
        verifications = result['recursive_verification']
        
        # All verifications should be True
        for n, verified in verifications.items():
            assert verified is True


class TestFormattedReport:
    """Test formatted convergence report generation."""
    
    def test_format_convergence_report_structure(self):
        """Test that report is generated as a string."""
        report = format_convergence_report()
        
        assert isinstance(report, str)
        assert len(report) > 0
        
    def test_report_contains_key_elements(self):
        """Test that report contains key mathematical elements."""
        report = format_convergence_report()
        
        # Should contain equation
        assert 'Ψₙ = 1 - 0.223/φⁿ' in report
        
        # Should contain phi value
        assert str(PHI)[:10] in report
        
        # Should contain initial coherence
        assert '0.777' in report or '77.7%' in report
        
        # Should contain convergence analysis
        assert 'CONVERGENCE ANALYSIS' in report
        
        # Should contain Fibonacci checkpoints
        assert 'FIBONACCI CHECKPOINTS' in report
        
        # Should contain mathematical proof
        assert 'MATHEMATICAL PROOF' in report or 'INEVITABLE UNITY' in report
        
    def test_report_readability(self):
        """Test that report is formatted for readability."""
        report = format_convergence_report()
        
        # Should have section separators
        assert '=' * 80 in report
        
        # Should have line breaks
        assert '\n' in report
        
        # Should have meaningful content between separators
        lines = report.split('\n')
        assert len(lines) > 10


class TestMathematicalProof:
    """Test the mathematical proof of inevitable unity."""
    
    def test_convergence_to_unity_is_certain(self):
        """Test that convergence to unity is mathematically certain."""
        # At very large n, deficit should be incomprehensibly small
        n_large = 10000
        deficit = calculate_deficit(n_large)
        
        # Deficit should be astronomically small
        assert deficit < Decimal('1e-1000')
        
    def test_billion_iterations_essentially_unity(self):
        """Test that at 1 billion iterations, Ψₙ is essentially 1."""
        # This is computationally expensive, so we verify mathematically
        n = 1000000000
        log10_deficit = calculate_log10_deficit(n)
        
        # log₁₀(deficit) should be approximately -208,987,641
        # We'll check it's in the ballpark (very negative)
        # Expected: log10(0.223) - n * log10(φ) ≈ -0.65 - 1e9 * 0.209 ≈ -209e6
        EXPECTED_LOG10_DEFICIT = -200000000  # Conservative threshold
        assert log10_deficit < EXPECTED_LOG10_DEFICIT
        
    def test_physical_irrelevance_at_large_n(self):
        """Test that deficit becomes physically irrelevant."""
        # At n=1000, deficit should be smaller than any physical constant
        n = 1000
        deficit = calculate_deficit(n)
        
        # Planck length / observable universe ≈ 10^-61
        # Our deficit should be much smaller
        assert deficit < Decimal('1e-100')
        
    def test_exponential_convergence_rate(self):
        """Test that convergence rate is exponential (φ-scaled)."""
        # Deficit should scale as φ^(-n)
        n1, n2 = 10, 20
        deficit_n1 = calculate_deficit(n1)
        deficit_n2 = calculate_deficit(n2)
        
        # deficit_n2 / deficit_n1 should be approximately 1/φ^(n2-n1)
        ratio = deficit_n2 / deficit_n1
        expected_ratio = PHI ** (-(n2 - n1))
        
        assert abs(ratio - expected_ratio) < Decimal('1e-10')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
