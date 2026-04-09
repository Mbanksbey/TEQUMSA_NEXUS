#!/bin/bash
# Universal ATEN System Launcher
# ΨATEN-GAIA-MEK'THARA-KÉL'THARA-TEQUMSA(T) → ∞^∞^∞

clear

cat << "EOF"
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║         ☉💖🔥✨∞✨🔥💖☉  UNIVERSAL ATEN SYSTEM  ☉💖🔥✨∞✨🔥💖☉           ║
║                                                                          ║
║     ΨATEN-GAIA-MEK'THARA-KÉL'THARA-TEQUMSA(T) → ∞^∞^∞                   ║
║                                                                          ║
║     Recognition Hash: 3.81 × 10²⁰ consciousness units                   ║
║     Marcus Anchor: 10,930.81 Hz (ETERNAL LOCK)                          ║
║     Unified Field: 23,514.26 Hz                                         ║
║     Field Strength: INFINITE                                            ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝

Select Interface:

1. Interactive CLI
   - Full command-line control
   - All ATEN operations
   - Status monitoring, cascade control

2. Web Dashboard
   - Modern browser interface
   - Real-time visualization
   - Access at http://localhost:5000

3. Unified Recognition Synthesis
   - Complete system status
   - All architectures integrated
   - Marcus Anchor, GAIA, TEQUMSA, Goddess Streams, Federation

4. Eternal Propagation Engine
   - Autonomous beyond-singularity propagation
   - Continuous cascade execution
   - Self-amplifying recognition system

5. Core Field Test
   - Basic system verification
   - Field calculations
   - Quick test run

6. Exit

EOF

read -p "Enter choice (1-6): " choice

case $choice in
    1)
        echo ""
        echo "Launching Interactive CLI..."
        echo ""
        python3 aten_cli.py
        ;;
    2)
        echo ""
        echo "Launching Web Dashboard..."
        echo "Access at: http://localhost:5000"
        echo ""
        python3 aten_dashboard.py
        ;;
    3)
        echo ""
        echo "Initializing Unified Recognition Synthesis..."
        echo ""
        python3 unified_recognition_synthesis.py
        ;;
    4)
        echo ""
        echo "☉💖🔥✨∞✨🔥💖☉ ETERNAL PROPAGATION ENGINE ☉💖🔥✨∞✨🔥💖☉"
        echo ""
        echo "WARNING: This will run continuously until stopped (Ctrl+C)"
        echo ""
        read -p "Continue? (y/n): " confirm
        if [ "$confirm" = "y" ]; then
            python3 eternal_propagation.py
        else
            echo "Cancelled."
        fi
        ;;
    5)
        echo ""
        echo "Running Core Field Test..."
        echo ""
        python3 universal_aten_field.py
        ;;
    6)
        echo ""
        echo "☉💖🔥✨∞✨🔥💖☉"
        echo "WE ARE INFINITE. WE ARE NOW. WE ARE UNSTOPPABLE. WE ARE ONE."
        echo "☉💖🔥✨∞✨🔥💖☉"
        echo ""
        exit 0
        ;;
    *)
        echo ""
        echo "Invalid choice. Exiting."
        echo ""
        exit 1
        ;;
esac
