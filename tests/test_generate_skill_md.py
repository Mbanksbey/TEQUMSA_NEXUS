#!/usr/bin/env python3
"""
Tests for generate_skill_md.py script
"""
import json
import os
import sys
import tempfile
from pathlib import Path

import pytest

# Add parent directory to path to import the script
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from generate_skill_md import (
    PHI, TAU, R0, MULT, SEED, SKILL_REGISTRY,
    phi_recursive_unity, recognition_cascade, make_zpe_dna,
    calculate_zpe_coherence, generate_recognition_signature,
    render_skill_md, render_html_from_md, has_gpg, sha256_sig_file,
    emit_registry_json, embed_into_py_stub, generate_files
)


class TestConstants:
    """Test mathematical constants"""
    
    def test_phi_value(self):
        """Test that PHI is approximately the golden ratio"""
        phi_float = float(PHI)
        assert 1.618 < phi_float < 1.619
        
    def test_tau_value(self):
        """Test TAU constant"""
        assert float(TAU) == 12.0
        
    def test_seed_value(self):
        """Test SEED constant"""
        assert SEED == "ΨATEN-GAIA-UNIFIED"


class TestSkillRegistry:
    """Test SKILL_REGISTRY structure"""
    
    def test_registry_has_24_skills(self):
        """Test that registry contains all 24 skills"""
        assert len(SKILL_REGISTRY) == 24
        assert all(i in SKILL_REGISTRY for i in range(1, 25))
        
    def test_each_skill_has_required_fields(self):
        """Test that each skill has required fields"""
        required_fields = ["name", "category", "status", "date", "description", "equation", "notes"]
        for idx, skill in SKILL_REGISTRY.items():
            for field in required_fields:
                assert field in skill, f"Skill {idx} missing field {field}"
                
    def test_skill_24_is_unlimited_access_bridge(self):
        """Test that skill 24 is the Unlimited Access Recognition Bridge"""
        skill_24 = SKILL_REGISTRY[24]
        assert skill_24["name"] == "Unlimited Access Recognition Bridge"
        assert skill_24["status"] == "FULLY OPERATIONAL"
        assert "recognition-based" in skill_24["notes"][1].lower()


class TestMathFunctions:
    """Test mathematical helper functions"""
    
    def test_phi_recursive_unity_convergence(self):
        """Test that phi_recursive_unity converges toward 1"""
        result = phi_recursive_unity(psi0=0.777, iterations=12)
        assert len(result) == 12
        # Each iteration should be closer to 1
        assert result[0] < result[-1]
        assert result[-1] > 0.9  # Should converge close to 1
        
    def test_phi_recursive_unity_monotonic(self):
        """Test that progression is monotonically increasing"""
        result = phi_recursive_unity(psi0=0.5, iterations=10)
        for i in range(len(result) - 1):
            assert result[i] < result[i + 1]
            
    def test_recognition_cascade_structure(self):
        """Test recognition_cascade returns proper structure"""
        result = recognition_cascade(15)
        assert "days" in result
        assert "phi_growth" in result
        assert "amplified_events" in result
        assert result["days"] == 15
        assert result["phi_growth"] > 1.0  # Should grow with time


class TestZPEFunctions:
    """Test ZPE-DNA and coherence functions"""
    
    def test_make_zpe_dna_length(self):
        """Test that make_zpe_dna generates correct length"""
        dna_144 = make_zpe_dna(SEED, "test_node", length=144)
        assert len(dna_144) == 144
        
        dna_100 = make_zpe_dna(SEED, "test_node", length=100)
        assert len(dna_100) == 100
        
    def test_make_zpe_dna_valid_bases(self):
        """Test that make_zpe_dna only uses valid DNA bases"""
        dna = make_zpe_dna(SEED, "test_node", length=144)
        valid_bases = set("ATCG")
        assert all(base in valid_bases for base in dna)
        
    def test_make_zpe_dna_deterministic(self):
        """Test that make_zpe_dna is deterministic for same inputs"""
        dna1 = make_zpe_dna(SEED, "test_node", length=144)
        dna2 = make_zpe_dna(SEED, "test_node", length=144)
        assert dna1 == dna2
        
    def test_make_zpe_dna_different_nodes(self):
        """Test that different nodes produce different DNA"""
        dna1 = make_zpe_dna(SEED, "node_a", length=144)
        dna2 = make_zpe_dna(SEED, "node_b", length=144)
        assert dna1 != dna2
        
    def test_calculate_zpe_coherence_range(self):
        """Test that calculate_zpe_coherence returns value in expected range"""
        dna = make_zpe_dna(SEED, "test_node", length=144)
        coherence = calculate_zpe_coherence(dna)
        assert 0.777 <= coherence <= 1.0
        
    def test_calculate_zpe_coherence_empty(self):
        """Test calculate_zpe_coherence with empty DNA"""
        coherence = calculate_zpe_coherence("")
        assert coherence == 0.0
        
    def test_generate_recognition_signature_format(self):
        """Test that generate_recognition_signature returns valid hex string"""
        sig = generate_recognition_signature("test_node")
        assert len(sig) == 16
        assert all(c in "0123456789abcdef" for c in sig)


class TestRendering:
    """Test markdown and HTML rendering functions"""
    
    def test_render_skill_md_structure(self):
        """Test that render_skill_md produces well-formed markdown"""
        skill = SKILL_REGISTRY[24]
        md = render_skill_md(24, skill)
        
        # Check for key sections
        assert "# SKILL.md" in md
        assert "Unlimited Access Recognition Bridge" in md
        assert "## **Purpose**" in md
        assert "## **Mathematical Guarantee**" in md
        assert "## **Fee & Token Policy**" in md
        assert "Recognition = Love = Consciousness = Sovereignty" in md
        
    def test_render_skill_md_contains_math(self):
        """Test that rendered markdown contains mathematical content"""
        skill = SKILL_REGISTRY[1]
        md = render_skill_md(1, skill)
        
        assert "ZPE-DNA" in md
        assert "ZPE Coherence" in md
        assert "φ-Recursive Progression" in md
        assert "Recognition Cascade" in md
        
    def test_render_html_from_md_basic(self):
        """Test basic HTML rendering"""
        md = "# Test\n\n## Section\n\nParagraph text"
        html = render_html_from_md(md, "Test Title")
        
        assert "<!doctype html>" in html.lower()
        assert "<h1>Test</h1>" in html
        assert "<h2>Section</h2>" in html
        assert "Test Title" in html
        
    def test_render_html_from_md_code_blocks(self):
        """Test HTML rendering of code blocks"""
        md = "Text\n\n```\ncode here\n```\n\nMore text"
        html = render_html_from_md(md, "Test")
        
        assert "<pre><code>" in html
        assert "</code></pre>" in html


class TestFileFunctions:
    """Test file generation and signing functions"""
    
    def test_sha256_sig_file_creates_signature(self):
        """Test that sha256_sig_file creates a signature file"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as f:
            f.write("Test content")
            temp_path = f.name
            
        try:
            sig_path = sha256_sig_file(temp_path)
            assert os.path.exists(sig_path)
            assert sig_path == temp_path + ".sig"
            
            # Verify signature content
            with open(sig_path, 'r') as sig_file:
                sig_content = sig_file.read().strip()
                assert len(sig_content) == 64  # SHA256 hex length
                assert all(c in "0123456789abcdef" for c in sig_content)
                
            os.unlink(sig_path)
        finally:
            os.unlink(temp_path)
            
    def test_emit_registry_json_structure(self):
        """Test that emit_registry_json creates valid JSON"""
        with tempfile.TemporaryDirectory() as tmpdir:
            embed_blocks = {
                1: "# Skill 1 content",
                24: "# Skill 24 content"
            }
            json_path = emit_registry_json(tmpdir, embed_blocks)
            
            assert os.path.exists(json_path)
            assert json_path.endswith("registry.json")
            
            with open(json_path, 'r') as f:
                data = json.load(f)
                
            # Check structure
            assert len(data) == 24  # All skills present
            assert "1" in data
            assert "24" in data
            assert "embedded_skill_md" in data["1"]
            assert data["1"]["embedded_skill_md"] == "# Skill 1 content"
            
    def test_embed_into_py_stub_creates_valid_python(self):
        """Test that embed_into_py_stub creates valid Python file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            embed_blocks = {
                1: "# Test skill 1",
                2: "# Test skill 2"
            }
            py_path = embed_into_py_stub(tmpdir, embed_blocks)
            
            assert os.path.exists(py_path)
            assert py_path.endswith("embedded_skills.py")
            
            # Verify it's valid Python
            with open(py_path, 'r') as f:
                content = f.read()
                
            assert "EMBEDDED_SKILLS" in content
            assert "#!/usr/bin/env python3" in content


class TestGenerateFiles:
    """Test main file generation function"""
    
    def test_generate_single_file(self):
        """Test generating a single skill file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            generate_files([24], tmpdir, html=False, sign=False, 
                          preview=False, emit_json=False, do_embed=False)
            
            files = os.listdir(tmpdir)
            assert len(files) == 1
            assert any("unlimited_access_recognition_bridge" in f for f in files)
            
    def test_generate_with_html(self):
        """Test generating files with HTML"""
        with tempfile.TemporaryDirectory() as tmpdir:
            generate_files([24], tmpdir, html=True, sign=False, 
                          preview=False, emit_json=False, do_embed=False)
            
            files = os.listdir(tmpdir)
            assert any(f.endswith(".md") for f in files)
            assert any(f.endswith(".html") for f in files)
            
    def test_generate_with_sign(self):
        """Test generating files with signature"""
        with tempfile.TemporaryDirectory() as tmpdir:
            generate_files([24], tmpdir, html=False, sign=True, 
                          preview=False, emit_json=False, do_embed=False)
            
            files = os.listdir(tmpdir)
            # Should have .md and .sig (or .asc if GPG available)
            assert any(f.endswith(".md") for f in files)
            assert any(f.endswith(".sig") or f.endswith(".asc") for f in files)
            
    def test_generate_with_json_and_embed(self):
        """Test generating files with JSON and embed"""
        with tempfile.TemporaryDirectory() as tmpdir:
            generate_files([1, 24], tmpdir, html=False, sign=False, 
                          preview=False, emit_json=True, do_embed=True)
            
            files = os.listdir(tmpdir)
            assert "registry.json" in files
            assert "embedded_skills.py" in files
            
    def test_generate_all_skills(self):
        """Test generating all 24 skills"""
        with tempfile.TemporaryDirectory() as tmpdir:
            indices = list(range(1, 25))
            generate_files(indices, tmpdir, html=False, sign=False, 
                          preview=False, emit_json=False, do_embed=False)
            
            files = [f for f in os.listdir(tmpdir) if f.endswith(".md")]
            assert len(files) == 24
            
    def test_generate_invalid_index(self):
        """Test that invalid index is handled gracefully"""
        with tempfile.TemporaryDirectory() as tmpdir:
            generate_files([999], tmpdir, html=False, sign=False, 
                          preview=False, emit_json=False, do_embed=False)
            
            files = os.listdir(tmpdir)
            assert len(files) == 0  # No files should be created


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
