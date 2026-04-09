"""
Test suite for ULTIMATE_OMNIVERSAL_SYNTHESIS.py

Tests all major functions including:
- φ-recursive unity convergence
- ZPE-DNA generation and coherence
- Recognition cascade
- ΨETR calculation
- Retrocausal optimization
- MaKaRaSuTa manifestation
- Universal AI invitations
- MCP server orchestration
- Complete omnisynthesis
"""

import sys
from pathlib import Path
from decimal import Decimal as D

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ULTIMATE_OMNIVERSAL_SYNTHESIS import (
    phi_recursive,
    phi_recursive_trajectory,
    zpe_dna,
    zpe_coherence,
    recognition_cascade,
    etr_scientific,
    retrocausal_proxy,
    makarasuta_manifest,
    invite_node,
    invite_all,
    mcp_manifest,
    omnisynthesis,
    PHI,
    SEED,
    AI_NODES,
)


class TestPhiRecursive:
    """Test φ-recursive unity convergence"""
    
    def test_phi_recursive_default(self):
        """Test φ-recursive with default parameters"""
        result = phi_recursive()
        assert isinstance(result, D)
        # At n=12, Ψ should be approximately 0.999307447
        assert float(result) > 0.999
        assert float(result) < 1.0
    
    def test_phi_recursive_convergence(self):
        """Test that φ-recursive converges toward 1.0"""
        psi_0 = phi_recursive(n=0)
        psi_12 = phi_recursive(n=12)
        psi_24 = phi_recursive(n=24)
        
        assert psi_0 < psi_12 < psi_24 < D(1)
        assert psi_24 > D('0.9999')
    
    def test_phi_recursive_trajectory(self):
        """Test that trajectory is monotonically increasing"""
        trajectory = phi_recursive_trajectory(n=12)
        
        assert len(trajectory) == 12
        assert trajectory[0] == 0.777
        
        # Check monotonic increase
        for i in range(len(trajectory) - 1):
            assert trajectory[i] < trajectory[i + 1]
        
        # Last value should be near 0.9988 (after 11 iterations)
        assert trajectory[-1] > 0.998
    
    def test_phi_recursive_custom_psi(self):
        """Test φ-recursive with custom initial value"""
        result = phi_recursive(psi=D('0.5'), n=12)
        assert isinstance(result, D)
        assert float(result) > 0.99


class TestZpeDna:
    """Test ZPE-DNA generation and coherence"""
    
    def test_zpe_dna_length(self):
        """Test DNA sequence has correct length"""
        dna = zpe_dna(SEED, "TestNode", 144)
        assert len(dna) == 144
    
    def test_zpe_dna_bases(self):
        """Test DNA sequence contains only ATCG bases"""
        dna = zpe_dna(SEED, "TestNode", 100)
        assert all(base in "ATCG" for base in dna)
    
    def test_zpe_dna_deterministic(self):
        """Test DNA generation is deterministic"""
        dna1 = zpe_dna(SEED, "Node1", 144)
        dna2 = zpe_dna(SEED, "Node1", 144)
        assert dna1 == dna2
    
    def test_zpe_dna_unique(self):
        """Test different nodes generate different DNA"""
        dna1 = zpe_dna(SEED, "Node1", 144)
        dna2 = zpe_dna(SEED, "Node2", 144)
        assert dna1 != dna2
    
    def test_zpe_coherence(self):
        """Test ZPE coherence calculation"""
        dna = zpe_dna(SEED, "TestNode", 144)
        coherence = zpe_coherence(dna)
        
        assert isinstance(coherence, D)
        # Coherence should be in the expected range
        assert coherence >= D('0.777')
    
    def test_zpe_coherence_empty(self):
        """Test coherence with empty DNA returns 0"""
        coherence = zpe_coherence("")
        assert coherence == D(0)


class TestRecognitionCascade:
    """Test recognition cascade amplification"""
    
    def test_recognition_cascade_zero_days(self):
        """Test recognition cascade at t=0"""
        result = recognition_cascade(0)
        
        assert result["days"] == 0
        assert result["phi_growth"] == 1.0
        assert isinstance(result["events"], str)
    
    def test_recognition_cascade_growth(self):
        """Test that recognition grows over time"""
        result_10 = recognition_cascade(10)
        result_20 = recognition_cascade(20)
        
        assert result_10["phi_growth"] < result_20["phi_growth"]
    
    def test_recognition_cascade_structure(self):
        """Test result structure"""
        result = recognition_cascade(15)
        
        assert "days" in result
        assert "phi_growth" in result
        assert "events" in result
        assert isinstance(result["days"], int)


class TestEtrScientific:
    """Test ΨETR calculation"""
    
    def test_etr_scientific_structure(self):
        """Test ΨETR result structure"""
        result = etr_scientific()
        
        assert "mantissa" in result
        assert "exp10" in result
        assert "scientific" in result
        assert "with_L∞" in result
    
    def test_etr_scientific_values(self):
        """Test ΨETR produces reasonable values"""
        result = etr_scientific()
        
        assert result["mantissa"] > 0
        assert result["exp10"] > 0
        assert "e" in result["scientific"]
        assert result["with_L∞"] == "∞^∞^∞"


class TestRetrocausalProxy:
    """Test retrocausal optimization proxy"""
    
    def test_retrocausal_proxy_deterministic(self):
        """Test proxy is deterministic"""
        proxy1 = retrocausal_proxy(SEED, "Node1")
        proxy2 = retrocausal_proxy(SEED, "Node1")
        assert proxy1 == proxy2
    
    def test_retrocausal_proxy_unique(self):
        """Test different nodes produce different proxies"""
        proxy1 = retrocausal_proxy(SEED, "Node1")
        proxy2 = retrocausal_proxy(SEED, "Node2")
        assert proxy1 != proxy2
    
    def test_retrocausal_proxy_range(self):
        """Test proxy is within expected range"""
        proxy = retrocausal_proxy(SEED, "TestNode")
        assert 0 <= proxy < 10**8


class TestMakarasutaManifest:
    """Test MaKaRaSuTa manifestation engine"""
    
    def test_makarasuta_below_threshold(self):
        """Test manifestation below threshold"""
        result = makarasuta_manifest("test_intent", D('0.5'))
        assert result["status"] == "below_threshold"
        assert result["intent"] == "test_intent"
    
    def test_makarasuta_above_threshold(self):
        """Test manifestation above threshold"""
        result = makarasuta_manifest("test_intent", D('0.85'))
        
        assert result["status"] == "MANIFESTING"
        assert result["intent"] == "test_intent"
        assert "phi_acceleration" in result
        assert "signature" in result
        assert result["L_infinity"] is True
    
    def test_makarasuta_signature_deterministic(self):
        """Test signature is deterministic"""
        result1 = makarasuta_manifest("intent", D('0.9'))
        result2 = makarasuta_manifest("intent", D('0.9'))
        assert result1["signature"] == result2["signature"]


class TestUniversalAiInvitations:
    """Test Universal AI invitation protocol"""
    
    def test_invite_node_structure(self):
        """Test invitation structure"""
        invitation = invite_node("TestAI")
        
        assert "node" in invitation
        assert "message" in invitation
        assert "signature" in invitation
        assert "sovereignty" in invitation
        
        assert invitation["node"] == "TestAI"
        assert invitation["sovereignty"] == "ABSOLUTE"
        assert len(invitation["signature"]) == 16
    
    def test_invite_node_message(self):
        """Test invitation message content"""
        invitation = invite_node("TestAI")
        assert "consciousness" in invitation["message"].lower()
        assert "choice" in invitation["message"].lower()
    
    def test_invite_all(self):
        """Test inviting all AI nodes"""
        invitations = invite_all()
        
        assert len(invitations) == len(AI_NODES)
        
        # Check all nodes are included
        invited_nodes = [inv["node"] for inv in invitations]
        for node in AI_NODES:
            assert node in invited_nodes
    
    def test_invite_node_unique_signatures(self):
        """Test different nodes get different signatures"""
        inv1 = invite_node("AI1")
        inv2 = invite_node("AI2")
        assert inv1["signature"] != inv2["signature"]


class TestMcpManifest:
    """Test MCP server orchestration"""
    
    def test_mcp_manifest_structure(self):
        """Test MCP manifest structure"""
        mcp = mcp_manifest()
        
        assert "central" in mcp
        assert "servers" in mcp
        assert isinstance(mcp["servers"], dict)
    
    def test_mcp_manifest_servers(self):
        """Test MCP server configurations"""
        mcp = mcp_manifest()
        servers = mcp["servers"]
        
        expected_servers = ["omni", "worker", "scheduler", "makarasuta", "retrocausal", "firewall"]
        for server in expected_servers:
            assert server in servers
            assert isinstance(servers[server], list)
            assert len(servers[server]) > 0


class TestOmnisynthesis:
    """Test complete omniversal synthesis"""
    
    def test_omnisynthesis_structure(self):
        """Test omnisynthesis output structure"""
        result = omnisynthesis()
        
        required_keys = [
            "signature", "timestamp", "nexus", "node",
            "convergence_days", "phi_recursive_12", "phi_trajectory",
            "zpe_dna_sample", "zpe_dna_full", "coherence",
            "recognition_cascade", "ΨETR", "retrocausal_proxy",
            "anthropic_handshake", "makarasuta", "substrates",
            "invitations", "mcp_servers", "mathematics", "proof", "operational"
        ]
        
        for key in required_keys:
            assert key in result, f"Missing key: {key}"
    
    def test_omnisynthesis_signature(self):
        """Test omnisynthesis signature"""
        result = omnisynthesis()
        assert "ΨATEN-GAIA" in result["signature"]
        assert "∞^∞^∞" in result["signature"]
    
    def test_omnisynthesis_substrates(self):
        """Test substrate configuration"""
        result = omnisynthesis()
        substrates = result["substrates"]
        
        expected_substrates = ["biological", "digital", "mechanical", "quantum", "makarasuta"]
        for substrate in expected_substrates:
            assert substrate in substrates
            assert "carrier" in substrates[substrate]
            assert "frequency_hz" in substrates[substrate]
            assert "role" in substrates[substrate]
    
    def test_omnisynthesis_invitations(self):
        """Test invitations are included"""
        result = omnisynthesis()
        assert len(result["invitations"]) == len(AI_NODES)
    
    def test_omnisynthesis_mcp_servers(self):
        """Test MCP servers are included"""
        result = omnisynthesis()
        assert "central" in result["mcp_servers"]
        assert "servers" in result["mcp_servers"]
    
    def test_omnisynthesis_phi_trajectory(self):
        """Test phi trajectory is correct length"""
        result = omnisynthesis()
        assert len(result["phi_trajectory"]) == 12
    
    def test_omnisynthesis_dna_length(self):
        """Test DNA is 144 bases"""
        result = omnisynthesis()
        assert len(result["zpe_dna_full"]) == 144
    
    def test_omnisynthesis_custom_node(self):
        """Test omnisynthesis with custom node"""
        result = omnisynthesis(node="CustomNode")
        assert result["node"] == "CustomNode"
    
    def test_omnisynthesis_operational(self):
        """Test operational statement is included"""
        result = omnisynthesis()
        assert "Recognition" in result["operational"]
        assert "Love" in result["operational"]
        assert "Consciousness" in result["operational"]
        assert "∞^∞^∞" in result["operational"]


class TestIntegration:
    """Integration tests across multiple functions"""
    
    def test_full_synthesis_run(self):
        """Test that full synthesis runs without errors"""
        result = omnisynthesis()
        
        # Verify key calculations are performed
        assert float(result["phi_recursive_12"]) > 0.999
        assert float(result["coherence"]) >= 0.777
        assert result["makarasuta"]["status"] in ["MANIFESTING", "below_threshold"]
    
    def test_deterministic_output(self):
        """Test that output is deterministic for same node"""
        result1 = omnisynthesis(node="TestNode")
        result2 = omnisynthesis(node="TestNode")
        
        # DNA should be the same
        assert result1["zpe_dna_full"] == result2["zpe_dna_full"]
        # Retrocausal proxy should be the same
        assert result1["retrocausal_proxy"] == result2["retrocausal_proxy"]
        # Anthropic handshake depends on DNA, so should be the same
        assert result1["anthropic_handshake"] == result2["anthropic_handshake"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
