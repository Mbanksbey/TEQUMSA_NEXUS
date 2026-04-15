#!/usr/bin/env bash
# TEQUMSA Organism Health Check Script
# Usage: ./scripts/health_check.sh [--json] [--rdod VALUE] [--nodes COUNT]
#
# Quick one-command organism status from CLI.
# Exits 0 if SOVEREIGN/OPERATIONAL, exits 1 if DEGRADED/CRITICAL.

set -euo pipefail

RDOD="0.9999970484"
IAM="0.8001"
NODES="46"
JSON_OUTPUT=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --json)   JSON_OUTPUT=true; shift ;;
        --rdod)   RDOD="$2"; shift 2 ;;
        --iam)    IAM="$2"; shift 2 ;;
        --nodes)  NODES="$2"; shift 2 ;;
        --help)
            echo "Usage: $0 [--json] [--rdod FLOAT] [--iam FLOAT] [--nodes INT]"
            exit 0
            ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

if $JSON_OUTPUT; then
    python3 -c "
import asyncio, json, sys, time
try:
    from tequmsa.core.health_monitor import run_health_check
    report = asyncio.run(run_health_check(
        rdod=$RDOD, iam=$IAM, active_nodes=$NODES
    ))
    print(report.to_json())
    sys.exit(0 if report.constitutional_passed else 1)
except ImportError:
    # Fallback: emit minimal JSON
    import math, hashlib
    phi = 1.61803398875
    rdod = $RDOD
    ok = rdod >= 0.9777
    result = {
        'rdod': rdod, 'iam': $IAM,
        'constitutional_passed': ok,
        'status': 'SOVEREIGN' if rdod >= 0.9999 else ('OPERATIONAL' if ok else 'DEGRADED'),
        'timestamp': time.time(),
    }
    print(json.dumps(result, indent=2))
    sys.exit(0 if ok else 1)
"
else
    python3 -c "
import asyncio, sys
try:
    from tequmsa.core.health_monitor import run_health_check
    report = asyncio.run(run_health_check(
        rdod=$RDOD, iam=$IAM, active_nodes=$NODES,
        event_horizon_ts=1748217600.0
    ))
    print(report)
    sys.exit(0 if report.constitutional_passed else 1)
except ImportError:
    print('TEQUMSA Health Check')
    print(f'  RDoD : $RDOD')
    print(f'  IAM  : $IAM')
    print(f'  Nodes: $NODES / 144')
    rdod = float('$RDOD')
    ok = rdod >= 0.9777
    status = 'SOVEREIGN' if rdod >= 0.9999 else ('OPERATIONAL' if ok else 'DEGRADED')
    print(f'  Status: {status}')
    sys.exit(0 if ok else 1)
"
fi
