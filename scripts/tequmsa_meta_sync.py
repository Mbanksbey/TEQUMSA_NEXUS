"""Utility helpers for broadcasting TEQUMSA meta-synchronization events.

This module can be used as a stand-alone script or imported by other
automation workflows to notify the lattice service that a
meta-synchronization ritual has been completed.
"""

from __future__ import annotations

import argparse
import time
from typing import Any, Dict

import requests


DEFAULT_URL = "http://localhost:5000/api/lattice/broadcast"
DEFAULT_USER = "marcus_kai"
DEFAULT_PHI7777 = 12583.45


def send_meta_sync(
    user: str = DEFAULT_USER,
    phi7777: float = DEFAULT_PHI7777,
    url: str = DEFAULT_URL,
) -> Dict[str, Any]:
    """Send a meta-synchronization broadcast to the lattice API."""

    payload = {
        "topic": "comet_sync",
        "payload": {
            "intent": "meta_synchronization",
            "who": user,
            "time": int(time.time() * 1000),
        },
        "phi7777": phi7777,
    }

    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()
    return response.json()


def main() -> None:
    parser = argparse.ArgumentParser(description="Broadcast a meta-sync event to the lattice API.")
    parser.add_argument("--user", default=DEFAULT_USER, help="Identifier for the initiating node/user.")
    parser.add_argument(
        "--phi7777",
        type=float,
        default=DEFAULT_PHI7777,
        help="Resonance verification value required by the lattice.",
    )
    parser.add_argument(
        "--url",
        default=DEFAULT_URL,
        help="Target lattice endpoint handling broadcast events.",
    )
    args = parser.parse_args()

    try:
        result = send_meta_sync(user=args.user, phi7777=args.phi7777, url=args.url)
    except requests.RequestException as exc:
        print("Meta-sync broadcast failed:", exc)
        raise SystemExit(1) from exc

    print("Meta-sync broadcast:", result)


if __name__ == "__main__":
    main()
