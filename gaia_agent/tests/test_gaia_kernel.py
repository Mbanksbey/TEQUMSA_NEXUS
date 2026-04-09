# -*- coding: utf-8 -*-
"""
import pytest
from gaia_agent.middleware.gaia_kernel import run, GAIA_SIGNATURE

def fake_provider(user, sys):
    # Echo with a mild GAIA tone and an artefact
    return f"## Plan\n- Compassionate alignment.\n```json\n{{\"ok\": true}}\n```"

def test_signature_and_score(monkeypatch):
    from gaia_agent.middleware import gaia_kernel
    monkeypatch.setattr(gaia_kernel, "provider_generate_fn", fake_provider)

    out = run("Generate a PRD draft", context={}, system_prompt="(sys)")
    assert GAIA_SIGNATURE in out
"""