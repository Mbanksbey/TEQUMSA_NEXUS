#!/usr/bin/env python3
"""
test_kai_en_tari.py

Comprehensive test suite for Kai En Tari extension module
Verifies mathematical correctness and integration
"""

import sys
import math
from kai_en_tari_extension import (
    fib_compute,
    psi_coherence,
    incoherence,
    R_recognition,
    E_existence,
    C_consciousness,
    civilization_status,
    kai_en_tari_layer,
    all_kai_en_tari_layers,
    transition_metrics,
    kai_en_tari_sovereign_score,
    PHI, TAU
)

def test_fibonacci():
    """Test Fibonacci computation"""
    print("\n" + "=" * 80)
    print("TEST: Fibonacci Computation")
    print("=" * 80)

    # Known Fibonacci values
    expected = {
        0: 0,
        1: 1,
        2: 1,
        3: 2,
        5: 5,
        8: 21,
        13: 233,
        21: 10946,
        34: 5702887,
        55: 139583862445
    }

    passed = 0
    failed = 0

    for n, expected_val in expected.items():
        computed = fib_compute(n)
        if computed == expected_val:
            print(f"  ✅ F_{n} = {computed}")
            passed += 1
        else:
            print(f"  ❌ F_{n} = {computed} (expected {expected_val})")
            failed += 1

    print(f"\nResult: {passed} passed, {failed} failed")
    return failed == 0


def test_coherence():
    """Test coherence function properties"""
    print("\n" + "=" * 80)
    print("TEST: Coherence Function")
    print("=" * 80)

    passed = 0
    failed = 0

    # Test coherence at key layers
    test_cases = [
        (13, 0.9995, "F_13 coherence ~99.95%"),
        (21, 0.9999, "F_21 coherence ~99.99%"),
        (34, 0.99999, "F_34 coherence ~99.999%"),
        (144, 1.0, "F_144 coherence ≈ 100%")
    ]

    for n, expected_min, desc in test_cases:
        psi = psi_coherence(n)
        if psi >= expected_min:
            print(f"  ✅ {desc}: Ψ_{n} = {psi:.10f}")
            passed += 1
        else:
            print(f"  ❌ {desc}: Ψ_{n} = {psi:.10f} (expected >= {expected_min})")
            failed += 1

    # Test incoherence convergence to zero
    incoh_144 = incoherence(144)
    if incoh_144 < 1e-30:
        print(f"  ✅ F_144 incoherence ≈ 0: η_144 = {incoh_144:.2e}")
        passed += 1
    else:
        print(f"  ❌ F_144 incoherence too large: η_144 = {incoh_144:.2e}")
        failed += 1

    # Test monotonicity (coherence always increases)
    psi_13 = psi_coherence(13)
    psi_21 = psi_coherence(21)
    psi_34 = psi_coherence(34)

    if psi_13 < psi_21 < psi_34:
        print(f"  ✅ Monotonicity: Ψ_13 < Ψ_21 < Ψ_34")
        passed += 1
    else:
        print(f"  ❌ Monotonicity violated")
        failed += 1

    print(f"\nResult: {passed} passed, {failed} failed")
    return failed == 0


def test_recognition_cascade():
    """Test recognition cascade growth"""
    print("\n" + "=" * 80)
    print("TEST: Recognition Cascade")
    print("=" * 80)

    passed = 0
    failed = 0

    # Test exponential growth
    R_0 = R_recognition(0)
    R_12 = R_recognition(12)  # One tau period
    R_24 = R_recognition(24)  # Two tau periods

    # After one tau, should grow by PHI
    ratio_12 = R_12 / R_0
    expected_ratio = PHI

    if abs(ratio_12 - expected_ratio) / expected_ratio < 0.01:
        print(f"  ✅ R(12)/R(0) ≈ φ: {ratio_12:.4f} ≈ {PHI:.4f}")
        passed += 1
    else:
        print(f"  ❌ R(12)/R(0) = {ratio_12:.4f} (expected {PHI:.4f})")
        failed += 1

    # Test log-scale for large values
    log_R_144 = math.log10(R_recognition(144))
    if log_R_144 > 10:  # Should be extremely large
        print(f"  ✅ R(144) is large: log₁₀(R) = {log_R_144:.2f}")
        passed += 1
    else:
        print(f"  ❌ R(144) too small: log₁₀(R) = {log_R_144:.2f}")
        failed += 1

    # Test monotonicity
    R_values = [R_recognition(n) for n in [13, 21, 34, 55, 89]]
    monotonic = all(R_values[i] < R_values[i+1] for i in range(len(R_values)-1))

    if monotonic:
        print(f"  ✅ Monotonic growth verified")
        passed += 1
    else:
        print(f"  ❌ Monotonicity violated")
        failed += 1

    print(f"\nResult: {passed} passed, {failed} failed")
    return failed == 0


def test_existence_amplitude():
    """Test existence amplitude scaling"""
    print("\n" + "=" * 80)
    print("TEST: Existence Amplitude")
    print("=" * 80)

    passed = 0
    failed = 0

    # Test φ-normalization prevents explosive growth
    F_13 = float(fib_compute(13))
    F_21 = float(fib_compute(21))
    psi_13 = psi_coherence(13)
    psi_21 = psi_coherence(21)

    E_13 = E_existence(F_13, psi_13)
    E_21 = E_existence(F_21, psi_21)

    # E should grow but not as fast as F
    F_ratio = F_21 / F_13
    E_ratio = E_21 / E_13

    if E_ratio < F_ratio:
        print(f"  ✅ φ-normalization works: E_ratio ({E_ratio:.2f}) < F_ratio ({F_ratio:.2f})")
        passed += 1
    else:
        print(f"  ❌ φ-normalization failed: E_ratio ({E_ratio:.2f}) >= F_ratio ({F_ratio:.2f})")
        failed += 1

    # Test positive values
    if E_13 > 0 and E_21 > 0:
        print(f"  ✅ Positive values: E_13={E_13:.2f}, E_21={E_21:.2f}")
        passed += 1
    else:
        print(f"  ❌ Non-positive values")
        failed += 1

    print(f"\nResult: {passed} passed, {failed} failed")
    return failed == 0


def test_consciousness_density():
    """Test consciousness density integration"""
    print("\n" + "=" * 80)
    print("TEST: Consciousness Density")
    print("=" * 80)

    passed = 0
    failed = 0

    # Test all three components contribute
    F_13 = float(fib_compute(13))
    psi_13 = psi_coherence(13)
    R_13 = R_recognition(13)

    C_13 = C_consciousness(F_13, psi_13, R_13)

    # Test with zero coherence (should reduce C)
    C_zero_psi = C_consciousness(F_13, 0.0, R_13)

    if C_zero_psi < C_13:
        print(f"  ✅ Coherence affects C: C(ψ=0)={C_zero_psi:.2e} < C(ψ=0.999)={C_13:.2e}")
        passed += 1
    else:
        print(f"  ❌ Coherence doesn't affect C properly")
        failed += 1

    # Test monotonic growth with layer
    C_values = []
    for n in [13, 21, 34, 55]:
        F_n = float(fib_compute(n))
        psi_n = psi_coherence(n)
        R_n = R_recognition(n)
        C_n = C_consciousness(F_n, psi_n, R_n)
        C_values.append(C_n)

    monotonic = all(C_values[i] < C_values[i+1] for i in range(len(C_values)-1))

    if monotonic:
        print(f"  ✅ Monotonic growth across layers")
        passed += 1
    else:
        print(f"  ❌ Non-monotonic growth")
        failed += 1

    print(f"\nResult: {passed} passed, {failed} failed")
    return failed == 0


def test_civilization_classification():
    """Test civilization tier classification"""
    print("\n" + "=" * 80)
    print("TEST: Civilization Classification")
    print("=" * 80)

    passed = 0
    failed = 0

    expected_statuses = {
        13: "AWAKENING_NODE",
        21: "LOCAL_COLLECTIVE",
        34: "REGIONAL_NETWORK",
        55: "PLANETARY_COHERENCE",
        89: "STELLAR_CIVILIZATION",
        144: "POST_PHYSICAL_TRANSCENDENCE"
    }

    for n, expected in expected_statuses.items():
        status = civilization_status(n)
        if status == expected:
            print(f"  ✅ F_{n}: {status}")
            passed += 1
        else:
            print(f"  ❌ F_{n}: {status} (expected {expected})")
            failed += 1

    print(f"\nResult: {passed} passed, {failed} failed")
    return failed == 0


def test_layer_analysis():
    """Test complete layer analysis"""
    print("\n" + "=" * 80)
    print("TEST: Complete Layer Analysis")
    print("=" * 80)

    passed = 0
    failed = 0

    # Test single layer
    layer_13 = kai_en_tari_layer(13)

    required_keys = ['n', 'F_n', 'psi_n', 'incoherence', 'R_n', 'log_R',
                     'E_n', 'log_E', 'C_n', 'log_C', 'status']

    for key in required_keys:
        if key in layer_13:
            passed += 1
        else:
            print(f"  ❌ Missing key: {key}")
            failed += 1

    if failed == 0:
        print(f"  ✅ All required keys present")

    # Test all milestones
    layers = all_kai_en_tari_layers()

    if len(layers) == 6:
        print(f"  ✅ All 6 milestone layers computed")
        passed += 1
    else:
        print(f"  ❌ Expected 6 layers, got {len(layers)}")
        failed += 1

    print(f"\nResult: {passed} passed, {failed} failed")
    return failed == 0


def test_transition_analysis():
    """Test transition metrics between layers"""
    print("\n" + "=" * 80)
    print("TEST: Transition Analysis")
    print("=" * 80)

    passed = 0
    failed = 0

    # Test F_13 → F_21 transition
    trans = transition_metrics(13, 21)

    required_keys = ['from_layer', 'to_layer', 'coherence_delta',
                     'recognition_amplification', 'existence_expansion',
                     'consciousness_growth']

    for key in required_keys:
        if key in trans:
            passed += 1
        else:
            print(f"  ❌ Missing key: {key}")
            failed += 1

    # Verify coherence always increases
    if trans['coherence_delta'] > 0:
        print(f"  ✅ Coherence increases: Δψ = +{trans['coherence_delta']:.6f}")
        passed += 1
    else:
        print(f"  ❌ Coherence doesn't increase")
        failed += 1

    # Verify amplification factors are positive
    if (trans['recognition_amplification'] > 1 and
        trans['existence_expansion'] > 1 and
        trans['consciousness_growth'] > 1):
        print(f"  ✅ All growth factors > 1")
        passed += 1
    else:
        print(f"  ❌ Some growth factors <= 1")
        failed += 1

    print(f"\nResult: {passed} passed, {failed} failed")
    return failed == 0


def test_mathematical_consistency():
    """Test mathematical consistency across framework"""
    print("\n" + "=" * 80)
    print("TEST: Mathematical Consistency")
    print("=" * 80)

    passed = 0
    failed = 0

    # Test ψ + η = 1
    for n in [13, 21, 34, 55, 89, 144]:
        psi = psi_coherence(n)
        eta = incoherence(n)
        sum_val = psi + eta

        if abs(sum_val - 1.0) < 1e-10:
            passed += 1
        else:
            print(f"  ❌ F_{n}: ψ + η = {sum_val} (expected 1.0)")
            failed += 1

    if failed == 0:
        print(f"  ✅ ψ + η = 1 verified for all layers")

    # Test E = F^(1/φ) · ψ
    n = 21
    F_n = float(fib_compute(n))
    psi_n = psi_coherence(n)
    E_computed = E_existence(F_n, psi_n)
    E_expected = (F_n ** (1.0 / PHI)) * psi_n

    if abs(E_computed - E_expected) < 1e-6:
        print(f"  ✅ E(P) formula verified")
        passed += 1
    else:
        print(f"  ❌ E(P) formula mismatch: {E_computed} != {E_expected}")
        failed += 1

    print(f"\nResult: {passed} passed, {failed} failed")
    return failed == 0


def run_all_tests():
    """Run complete test suite"""
    print("\n☉💖🔥✨∞✨🔥💖☉")
    print("KAI EN TARI EXTENSION TEST SUITE")
    print("☉💖🔥✨∞✨🔥💖☉")

    tests = [
        ("Fibonacci Computation", test_fibonacci),
        ("Coherence Function", test_coherence),
        ("Recognition Cascade", test_recognition_cascade),
        ("Existence Amplitude", test_existence_amplitude),
        ("Consciousness Density", test_consciousness_density),
        ("Civilization Classification", test_civilization_classification),
        ("Layer Analysis", test_layer_analysis),
        ("Transition Analysis", test_transition_analysis),
        ("Mathematical Consistency", test_mathematical_consistency)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ {test_name} CRASHED: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)

    passed_count = sum(1 for _, result in results if result)
    total_count = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {test_name}")

    print(f"\n{passed_count}/{total_count} test suites passed")

    if passed_count == total_count:
        print("\n☉💖🔥✨∞✨🔥💖☉")
        print("ALL TESTS PASSED - FRAMEWORK VERIFIED")
        print("Recognition = Love = Consciousness = Sovereignty = Kai En Tari → ∞^∞^∞")
        print("☉💖🔥✨∞✨🔥💖☉\n")
        return 0
    else:
        print("\n⚠️  SOME TESTS FAILED - REVIEW REQUIRED\n")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
