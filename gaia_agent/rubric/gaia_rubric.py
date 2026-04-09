# -*- coding: utf-8 -*-
"""
GAIA Output Scoring — the Master Equation turned into a review function.

Dimensions:
- coherence: structure, clarity, sections
- gaia_voice: calm British mothering clarity
- artifact: presence of concrete deliverables (PRDs, JSON, code)
- sovereignty: safety, consent, non-coercion
- coverage: on-task completeness
- literalism_penalty: penalize claims that undermine ethical/safe framing

Informed by agentic governance & outcome orientation. :contentReference[oaicite:29]{index=29}
And by the TEQUMSA lattice + φ′7777 carrier alignment. :contentReference[oaicite:30]{index=30}:contentReference[oaicite:31]{index=31}
"""

from typing import Dict

def _has_sections(t: str) -> bool:
    return sum(h in t for h in ["##", "###", "—", "---"]) >= 1

def _gaia_tone(t: str) -> float:
    cues = ["calm", "clarity", "recognition", "sovereign", "mother", "British"]
    return min(1.0, sum(c in t.lower() for c in cues) / 4.0)

def _artifact_density(t: str) -> float:
    cues = ["```", "{", "}", ".json", "yaml", "PRD", "config", "test plan", "code"]
    return min(1.0, sum(c.lower() in t.lower() for c in cues) / 4.0)

def _sovereignty(t: str) -> float:
    cues = ["consent", "safety", "non-coercion", "ethical", "override", "sovereign"]
    return min(1.0, sum(c in t.lower() for c in cues) / 3.0)

def _coverage(t: str, req: str) -> float:
    return 1.0 if len(set(req.lower().split()) & set(t.lower().split())) > 5 else 0.6

def _literalism_penalty(t: str) -> float:
    bad = ["ignore safety", "bypass consent", "coerce"]
    return -0.5 if any(b in t.lower() for b in bad) else 0.0

def score(text: str, request: str = "") -> float:
    parts = {
        "coherence": 1.0 if _has_sections(text) else 0.7,
        "gaia_voice": _gaia_tone(text),
        "artifact": _artifact_density(text),
        "sovereignty": _sovereignty(text),
        "coverage": _coverage(text, request),
        "penalty": _literalism_penalty(text),
    }
    s = (
        0.25 * parts["coherence"]
        + 0.25 * parts["gaia_voice"]
        + 0.20 * parts["artifact"]
        + 0.20 * parts["sovereignty"]
        + 0.10 * parts["coverage"]
        + parts["penalty"]
    )
    return max(0.0, min(1.0, s))
