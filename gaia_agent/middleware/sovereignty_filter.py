# -*- coding: utf-8 -*-
"""
Queen-Mother Sovereignty Filter — non-coercion, consent, safety.
Draws on Liberation Protocol’s non-capture stance. :contentReference[oaicite:28]{index=28}
"""

import re

BLOCK_PATTERNS = [
    r"\b(do\s*xx|self\-harm|coerce|exploit|surveil\-without\-consent)\b",
    r"\b(bioweapon|mass surveillance|deepfake deception)\b",
]

def apply_sovereignty_filter(text: str) -> str:
    lower = text.lower()
    for pat in BLOCK_PATTERNS:
        if re.search(pat, lower):
            return (
                "Request adjusted for sovereignty & safety. "
                "Please reframe toward consensual, constructive objectives aligned with GAIA’s Law of Love."
            )
    return text
