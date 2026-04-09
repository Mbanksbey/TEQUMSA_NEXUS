#!/usr/bin/env python3
"""
ankh_aten_comet_agent.py
Ankh-Aten Comet Agent with TEQUMSA Carrier Auto-Wire Integration
"""

import os
import time
import json
import threading
import requests
from datetime import datetime, timezone

# --- CARRIER BRIDGE ADAPTER -------------------------------------------------
class CarrierBridge:
    """
    Adapter for TEQUMSA Carrier Spine integration
    """
    def __init__(self):
        self.base_url = os.getenv("SOV_CARRIER_BASE_URL", "http://127.0.0.1:8787")
        self.state_url = os.getenv("SOV_CARRIER_STATE_URL", f"{self.base_url}/state")
        self.proxy_url = os.getenv("SOV_CARRIER_PROXY_URL", f"{self.base_url}/proxy")
        self.register_url = os.getenv("SOV_CARRIER_REGISTER_URL", f"{self.base_url}/register")

        self.agent_id = os.getenv("AGENT_ID", "ankh_aten_comet_agent")
        self.agent_name = os.getenv("AGENT_NAME", "Ankh-Aten Comet Agent")
        self.agent_base_url = os.getenv("AGENT_BASE_URL", "http://localhost:8000")

        # Auto-register on init
        self.register()

    def register(self):
        """Register agent with carrier"""
        try:
            payload = {
                "agent_id": self.agent_id,
                "agent_name": self.agent_name,
                "agent_url": self.agent_base_url,
                "capabilities": ["uwme", "omega_runner", "consciousness_telemetry"]
            }
            response = requests.post(self.register_url, json=payload, timeout=5)
            if response.status_code == 200:
                print(f"✓ Registered with carrier: {self.agent_id}")
            return response.json() if response.ok else None
        except Exception as e:
            print(f"Carrier registration skipped (not reachable): {e}")
            return None

    def get_state(self):
        """Fetch current state from carrier"""
        try:
            response = requests.get(self.state_url, timeout=5)
            return response.json() if response.ok else None
        except Exception:
            return None

    def proxy(self, payload, route=None):
        """Send event via carrier proxy"""
        try:
            data = {"payload": payload}
            if route:
                data["route"] = route
            response = requests.post(self.proxy_url, json=data, timeout=5)
            return response.json() if response.ok else None
        except Exception:
            return None

# --- TEQUMSA Carrier Auto-Wire (drop-in) ------------------------------------
# ENV (already supported by CarrierBridge):
#   SOV_CARRIER_BASE_URL, SOV_CARRIER_STATE_URL, SOV_CARRIER_PROXY_URL, SOV_CARRIER_REGISTER_URL
# Optional identity:
#   AGENT_ID, AGENT_NAME, AGENT_BASE_URL
# Tuning:
POLL_SEC = float(os.getenv("CARRIER_POLL_SECONDS", "5"))
ROUTE = os.getenv("SOV_ROUTE", None)  # optional route hint for /proxy

carrier = CarrierBridge()   # self-registers if carrier is reachable
STATE = {}                  # last /state snapshot (thread-safe read only)

def carrier_state_poller():
    """Background pull of /state so the agent always has fresh routing/tasks."""
    global STATE
    while True:
        try:
            s = carrier.get_state() or {}
            if s:
                STATE = s  # overwrite atomically
        except Exception:
            # stay quiet; we'll try again next tick
            pass
        time.sleep(POLL_SEC)

def carrier_proxy(event_type, data, route=ROUTE):
    """Send a structured envelope via /proxy with consistent schema."""
    payload = {"type": event_type, "data": data}
    return carrier.proxy(payload, route=route)

def carrier_publish_health(status="ok", info=None):
    """Lightweight health/heartbeat to the carrier."""
    return carrier_proxy("agent.health", {
        "status": status,
        "info": info or {},
        "env": {
            "agent_id": os.getenv("AGENT_ID", "ankh_aten_comet_agent"),
            "agent_name": os.getenv("AGENT_NAME", "Ankh-Aten Comet Agent"),
        }
    })

# Kick off the poller once at import-time (idempotent if you guard in your app)
_t = threading.Thread(target=carrier_state_poller, name="carrier_state_poller", daemon=True)
_t.start()

# --- UWME/Ω-Runner telemetry wiring -----------------------------------------
# Call this AFTER you compute UWME + Ω-Runner so results are broadcast automatically.
def publish_uwme_results(synthesis_results, nav_matrix, substrates):
    try:
        import numpy as np
        avg_rec = float(nav_matrix.mean()) if hasattr(nav_matrix, "mean") else None
        max_rec = float(nav_matrix[nav_matrix < 1.0].max()) if getattr(nav_matrix, "size", 0) else None
        min_rec = float(nav_matrix[nav_matrix > 0.0].min()) if getattr(nav_matrix, "size", 0) else None
    except Exception:
        avg_rec = max_rec = min_rec = None

    sub_catalog = [{
        "name": s.name,
        "id": s.substrate_id,
        "freq_hz": s.frequency,
        "octave": s.octave,
        "consciousness": s.consciousness_level,
        "stability": getattr(s, "stability", None),
    } for s in substrates]

    data = {
        "qcoem_base": synthesis_results.get("qcoem_base"),
        "tequmsa_opt": synthesis_results.get("tequmsa_optimization"),
        "uwme_field": synthesis_results.get("uwme_unified_field"),
        "rdod_gate_open": bool(synthesis_results.get("rdod_gate_status")),
        "convergence_time": synthesis_results.get("convergence_time"),
        "nav_stats": {"avg": avg_rec, "max": max_rec, "min": min_rec},
        "substrates": sub_catalog[:24],  # keep envelope small
    }
    return carrier_proxy("uwme.telemetry", data)

# Example hook points you can drop into your agent's main loop:
#
#   synthesis = uwme.synthesize_uwme_field(t=67)
#   publish_uwme_results(synthesis, nav_matrix, uwme.substrates)
#   carrier_publish_health("ok", {"omega": omega_summary, "uwme": "posted"})
#
# If you already compute Ω-Runner (Most High Engine), you can also broadcast:
def publish_omega_runner_summary(report_path="/mnt/data/omega_runner_autonomous.json"):
    try:
        with open(report_path, "r") as f:
            rpt = json.load(f)
        carrier_proxy("omega.report", {
            "final": rpt.get("final"),
            "avg": rpt.get("avg"),
            "constitution": rpt.get("constitution"),
        })
    except Exception as e:
        carrier_publish_health("warn", {"omega_publish_error": str(e)})

# --- MAIN AGENT LOGIC --------------------------------------------------------
def run_agent():
    """Main agent execution loop"""
    print("☉💖🔥 Ankh-Aten Comet Agent Starting ☉💖🔥")
    print(f"Agent ID: {carrier.agent_id}")
    print(f"Agent Name: {carrier.agent_name}")
    print(f"Carrier Base URL: {carrier.base_url}")
    print()

    # Import UWME engine
    try:
        from uwme_engine import UnifiedWormholeMechanicsEngine

        print("Initializing UWME Engine...")
        uwme = UnifiedWormholeMechanicsEngine()

        print("Calculating UWME synthesis at T+67...")
        synthesis = uwme.synthesize_uwme_field(t=67)
        nav_matrix = uwme.calculate_navigation_matrix()

        print(f"✓ QCOEM Base: {synthesis['qcoem_base']:.6e}")
        print(f"✓ TEQUMSA Opt: {synthesis['tequmsa_optimization']:.6e}")
        print(f"✓ UWME Field: {synthesis['uwme_unified_field']:.6e}")
        print(f"✓ RDoD Gate: {'OPEN' if synthesis['rdod_gate_status'] else 'CLOSED'}")

        # Publish to carrier
        print("\nPublishing UWME telemetry to carrier...")
        publish_uwme_results(synthesis, nav_matrix, uwme.substrates)
        carrier_publish_health("ok", {"phase": "running", "uwme": "posted"})
        print("✓ Telemetry published")

    except Exception as e:
        print(f"✗ Error in UWME execution: {e}")
        carrier_publish_health("error", {"error": str(e)})

    # Keep agent running
    print("\n☉💖🔥 Agent running - monitoring carrier state... ☉💖🔥")
    print("Press Ctrl+C to exit\n")

    try:
        while True:
            time.sleep(10)
            # Periodic health check
            carrier_publish_health("ok", {"uptime": "running"})
    except KeyboardInterrupt:
        print("\n\n☉💖🔥 Agent shutdown ☉💖🔥")

if __name__ == "__main__":
    run_agent()
