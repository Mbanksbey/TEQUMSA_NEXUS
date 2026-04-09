#!/usr/bin/env python3
"""
TEQUMSA Coherence Validation Script
Validates coherence threshold with pull request context

Part of: ΨATEN-GAIA-MEK'THARA-KÉL'THARA-TEQUMSA(T) → ∞^∞^∞
"""

import argparse
import json
import sys
from decimal import Decimal


def validate_coherence(threshold: float, current_coherence: float, pr_number: int = None) -> dict:
    """
    Validate coherence against minimum threshold.
    
    Args:
        threshold: Minimum required coherence (0.777)
        current_coherence: Current lattice coherence score
        pr_number: Optional PR number for context
    
    Returns:
        Dictionary with validation results
    """
    threshold_decimal = Decimal(str(threshold))
    coherence_decimal = Decimal(str(current_coherence))
    
    passed = coherence_decimal >= threshold_decimal
    delta = float(coherence_decimal - threshold_decimal)
    
    result = {
        "passed": passed,
        "threshold": float(threshold_decimal),
        "current_coherence": float(coherence_decimal),
        "delta": delta,
        "pr_number": pr_number,
        "status": "✅ COHERENT" if passed else "❌ BELOW THRESHOLD"
    }
    
    # Print results
    print(f"\n🔍 TEQUMSA Coherence Validation")
    print(f"{'='*50}")
    print(f"Threshold:         {threshold:.3f}")
    print(f"Current Coherence: {current_coherence:.3f}")
    print(f"Delta:             {delta:+.3f}")
    print(f"Status:            {result['status']}")
    
    if pr_number:
        print(f"PR Number:         #{pr_number}")
    
    print(f"{'='*50}\n")

    # Set output for GitHub Actions
    import os
    github_output = os.getenv('GITHUB_OUTPUT')
    if github_output:
        with open(github_output, 'a') as f:
            f.write(f"passed={str(passed).lower()}\n")
            f.write(f"coherence={current_coherence}\n")
            f.write(f"delta={delta}\n")

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Validate TEQUMSA lattice coherence threshold"
    )
    parser.add_argument(
        "--threshold",
        type=float,
        required=True,
        help="Minimum coherence threshold (typically 0.777)"
    )
    parser.add_argument(
        "--coherence",
        type=float,
        required=True,
        help="Current coherence score from lattice synthesis"
    )
    parser.add_argument(
        "--pr-number",
        type=int,
        help="Pull request number for context"
    )
    parser.add_argument(
        "--output-json",
        type=str,
        help="Optional JSON output file path"
    )
    
    args = parser.parse_args()
    
    result = validate_coherence(
        threshold=args.threshold,
        current_coherence=args.coherence,
        pr_number=args.pr_number
    )
    
    if args.output_json:
        with open(args.output_json, 'w') as f:
            json.dump(result, f, indent=2)
    
    # Exit with appropriate code
    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
