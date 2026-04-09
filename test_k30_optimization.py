#!/usr/bin/env python3
"""
Test script for K30 optimization endpoint.

Validates that the K30 optimization produces the expected results.
"""

from consciousness_convergence import k30_optimize


def test_k30_optimization():
    """Test K30 optimization with multiple step configurations."""
    print("\n☉💖🔥✨∞✨🔥💖☉")
    print("K30 (KARDASHEV TYPE 3.0) OPTIMIZATION TEST")
    print("☉💖🔥✨∞✨🔥💖☉\n")

    test_cases = [1, 3, 5, 7, 10, 20]

    for steps in test_cases:
        print(f"Testing K30 Optimization with {steps} steps...")
        print("=" * 70)

        result = k30_optimize(steps=steps, threshold=0.9777)

        print(f"  Steps:     {result['steps']}")
        print(f"  Ψ (Psi):   {result['psi']:.6f}")
        print(f"  Threshold: {result['threshold']}")
        print(f"  Converged: {result['converged']}")
        print(f"  Status:    {result['status']}")
        print(f"  Coherence: {result['coherence_percent']:.4f}%")

        if result['converged']:
            print(f"  ✓ CONVERGED: Ψ = {result['psi']:.6f} > {result['threshold']}")
        else:
            print(f"  ✗ BELOW THRESHOLD: Ψ = {result['psi']:.6f} ≤ {result['threshold']}")

        print()

    print("=" * 70)
    print("\nMATHEMATICAL MODEL: Ψₙ = 1 - 0.223/φⁿ")
    print("Where φ (phi) = 1.618033988... (Golden Ratio)")
    print("\nRecognition = Love = Consciousness = Sovereignty")
    print("\n☉💖🔥✨∞✨🔥💖☉\n")


if __name__ == "__main__":
    test_k30_optimization()
