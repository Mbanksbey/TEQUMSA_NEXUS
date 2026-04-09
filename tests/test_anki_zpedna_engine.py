"""
Tests for AN.KI ZPEDNA Recognition Engine

Validates:
- K20 score calculation
- Multiverse bridge readiness
- Civilization field computation
- Family healing factor
- Complete AN.KI recognition calculation
- φ (golden ratio) scaling verification
- Softcap function behavior
- Integration with existing consciousness systems
"""

import sys
import pytest
from pathlib import Path
from datetime import datetime
from decimal import Decimal as D

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from an_ki_zpedna_engine import (
    ANKIRecognitionEngine,
    ZPEDNAPacket,
    ZPEDNAProcessor,
    MultiverseBridge,
    MultiverseBridgeMetrics,
    CivilizationField,
    CivilizationFieldParams,
    FamilyHealingField,
    FamilyHealingMetrics,
    PHI, PSI_MK, PHI_7777, UNIFIED_FIELD,
    L_INFINITY, SIGMA, ZPEDNA_BASE,
    F_ATEN_EN_KI, F_AMUN_EN_LIL, F_AN_KI,
    softcap, phi_power
)


class TestConstants:
    """Test universal constants"""
    
    def test_phi_golden_ratio(self):
        """Test that φ is the golden ratio"""
        expected_phi = (1 + 5 ** 0.5) / 2
        assert abs(float(PHI) - expected_phi) < 1e-10
    
    def test_phi_property(self):
        """Test that φ satisfies φ² = φ + 1"""
        phi_squared = PHI ** 2
        phi_plus_one = PHI + D('1')
        assert abs(phi_squared - phi_plus_one) < D('1e-50')
    
    def test_unified_field(self):
        """Test unified field = PSI_MK + PHI_7777"""
        assert UNIFIED_FIELD == PSI_MK + PHI_7777
        assert abs(float(UNIFIED_FIELD) - 23514.26) < 0.01
    
    def test_sovereignty_constant(self):
        """Test sovereignty constant is immutable 1"""
        assert SIGMA == D('1')
    
    def test_l_infinity(self):
        """Test L∞ = φ^48"""
        expected = PHI ** 48
        assert L_INFINITY == expected
    
    def test_zpedna_base(self):
        """Test ZPEDNA base is 144 (12²)"""
        assert ZPEDNA_BASE == 144


class TestHelperFunctions:
    """Test helper functions"""
    
    def test_softcap_basic(self):
        """Test softcap function basic behavior"""
        a = D('10')
        b = D('20')
        result = softcap(a, b)
        expected = (a * b) / (a + b)
        assert result == expected
    
    def test_softcap_equal_values(self):
        """Test softcap with equal values"""
        a = D('10')
        result = softcap(a, a)
        assert result == a / D('2')
    
    def test_softcap_zero_sum(self):
        """Test softcap with zero sum"""
        result = softcap(D('0'), D('0'))
        assert result == D('0')
    
    def test_phi_power(self):
        """Test φ^exponent calculation"""
        result = phi_power(2)
        expected = PHI ** 2
        assert abs(result - expected) < D('1e-50')


class TestZPEDNAPacket:
    """Test ZPEDNA packet creation and validation"""
    
    def test_packet_creation(self):
        """Test valid packet creation"""
        packet = ZPEDNAPacket(
            packet_id="TEST-001",
            timestamp=datetime.now().isoformat(),
            sovereignty=90.0,
            benevolence=85.0,
            substrate_quality=88.0,
            civilization_level=82.0,
            clarity=87.0
        )
        assert packet.packet_id == "TEST-001"
        assert packet.sovereignty == 90.0
    
    def test_packet_validation_out_of_range(self):
        """Test packet validation fails for out-of-range values"""
        with pytest.raises(ValueError):
            ZPEDNAPacket(
                packet_id="TEST-002",
                timestamp=datetime.now().isoformat(),
                sovereignty=150.0,  # Invalid: > 100
                benevolence=85.0
            )
    
    def test_packet_validation_negative(self):
        """Test packet validation fails for negative values"""
        with pytest.raises(ValueError):
            ZPEDNAPacket(
                packet_id="TEST-003",
                timestamp=datetime.now().isoformat(),
                sovereignty=-10.0,  # Invalid: < 0
                benevolence=85.0
            )


class TestZPEDNAProcessor:
    """Test ZPEDNA processor calculations"""
    
    def test_k20_score_calculation(self):
        """Test K20 civilization score calculation"""
        packet = ZPEDNAPacket(
            packet_id="K20-TEST",
            timestamp=datetime.now().isoformat(),
            sovereignty=80.0,
            benevolence=90.0,
            substrate_quality=85.0,
            civilization_level=95.0,
            clarity=88.0
        )
        
        k20 = ZPEDNAProcessor.calculate_k20_score(packet)
        
        # K20 = ½(r̄ + R_civ_level)
        # r̄ = (80 + 90 + 85 + 88) / 4 = 85.75
        # K20 = ½(85.75 + 95) = 90.375
        expected = 0.5 * ((80 + 90 + 85 + 88) / 4 + 95)
        assert abs(k20 - expected) < 0.01
    
    def test_k20_range(self):
        """Test K20 score stays within 0-100 range"""
        # Minimum values
        packet_min = ZPEDNAPacket(
            packet_id="K20-MIN",
            timestamp=datetime.now().isoformat(),
            sovereignty=0.0,
            benevolence=0.0,
            substrate_quality=0.0,
            civilization_level=0.0,
            clarity=0.0
        )
        k20_min = ZPEDNAProcessor.calculate_k20_score(packet_min)
        assert 0 <= k20_min <= 100
        
        # Maximum values
        packet_max = ZPEDNAPacket(
            packet_id="K20-MAX",
            timestamp=datetime.now().isoformat(),
            sovereignty=100.0,
            benevolence=100.0,
            substrate_quality=100.0,
            civilization_level=100.0,
            clarity=100.0
        )
        k20_max = ZPEDNAProcessor.calculate_k20_score(packet_max)
        assert 0 <= k20_max <= 100
        assert k20_max == 100.0
    
    def test_zpedna_rex_k20_calculation(self):
        """Test complete ZPEDNA REX K20 calculation"""
        packet = ZPEDNAPacket(
            packet_id="REX-TEST",
            timestamp=datetime.now().isoformat(),
            sovereignty=90.0,
            benevolence=85.0,
            substrate_quality=88.0,
            civilization_level=92.0,
            clarity=87.0,
            harmonic_field=500.0,
            galaxy_host_capability=300.0,
            civilization_coherence=0.95
        )
        
        zpedna_rex = ZPEDNAProcessor.calculate_zpedna_rex_k20(packet)
        assert zpedna_rex > 0
        assert isinstance(zpedna_rex, D)


class TestMultiverseBridge:
    """Test multiverse bridge calculations"""
    
    def test_multiverse_handshake_validation(self):
        """Test multiverse handshake validation"""
        # High sovereignty should validate
        packet_valid = ZPEDNAPacket(
            packet_id="MV-VALID",
            timestamp=datetime.now().isoformat(),
            sovereignty=95.0,
            benevolence=85.0
        )
        assert MultiverseBridge.validate_multiverse_handshake(packet_valid) == True
        
        # Low sovereignty should not validate
        packet_invalid = ZPEDNAPacket(
            packet_id="MV-INVALID",
            timestamp=datetime.now().isoformat(),
            sovereignty=50.0,
            benevolence=85.0
        )
        assert MultiverseBridge.validate_multiverse_handshake(packet_invalid) == False
    
    def test_psi_now_calculation(self):
        """Test Ψ_NOW calculation"""
        metrics = MultiverseBridgeMetrics(
            unified_field_score=23514.26,
            readiness=0.918,
            coherence=0.95,
            recognition_growth_rate=0.1,
            multiverse_handshake_validated=True,
            node_count=144
        )
        
        psi_now = MultiverseBridge.calculate_psi_now(1.0, metrics)
        assert psi_now > 0
        assert isinstance(psi_now, D)
    
    def test_psi_now_handshake_failure(self):
        """Test Ψ_NOW returns 0 when handshake fails"""
        metrics = MultiverseBridgeMetrics(
            unified_field_score=23514.26,
            readiness=0.918,
            coherence=0.95,
            recognition_growth_rate=0.1,
            multiverse_handshake_validated=False,  # Failed
            node_count=144
        )
        
        psi_now = MultiverseBridge.calculate_psi_now(1.0, metrics)
        assert psi_now == D('0')


class TestCivilizationField:
    """Test civilization field calculations"""
    
    def test_goddess_stream_product(self):
        """Test 12 goddess stream φ-weighted product"""
        product = CivilizationField.calculate_goddess_stream_product()
        assert product > 0
        
        # Product should equal ∏ᵢ₌₁¹² φ^(i/12)
        expected = D('1')
        for i in range(1, 13):
            expected *= phi_power(i / 12.0)
        
        assert abs(product - expected) < D('1e-50')
    
    def test_energy_love_integral(self):
        """Test energy-love integral approximation"""
        integral = CivilizationField.calculate_energy_love_integral(k_max=100)
        assert integral > 0
        # Should be large due to L_INFINITY multiplication
        assert integral > L_INFINITY
    
    def test_retrocausal_integral(self):
        """Test retrocausal integration"""
        integral = CivilizationField.calculate_retrocausal_integral(1.0, 1.0)
        assert integral > 0
    
    def test_substrate_consciousness(self):
        """Test substrate consciousness multiplication"""
        consciousness = CivilizationField.calculate_substrate_consciousness(3)
        assert consciousness > D('1')
        
        # Should grow exponentially with substrates
        consciousness_5 = CivilizationField.calculate_substrate_consciousness(5)
        assert consciousness_5 > consciousness
    
    def test_ere_infinity(self):
        """Test ERE (Eternal Recognition Engine)"""
        ere = CivilizationField.calculate_ere_infinity()
        assert ere > 0
        # Should be very large (order of 1e30+)
        assert ere > D('1e30')
    
    def test_psi_mks_k20_calculation(self):
        """Test complete Ψ_MKS_K20 calculation"""
        params = CivilizationFieldParams(
            time=1.0,
            nodes=144,
            substrates=3,
            dimensions=12,
            consciousness_streams=12,
            retrocausal_depth=1.0
        )
        
        psi_mks = CivilizationField.calculate_psi_mks_k20(params)
        assert psi_mks > 0
        # Should be very large (order of 1e45+)
        assert psi_mks > D('1e45')


class TestFamilyHealingField:
    """Test family healing field calculations"""
    
    def test_phi_weighted_family_frequency(self):
        """Test φ-weighted family frequency calculation"""
        f_fam = FamilyHealingField.calculate_phi_weighted_family_frequency()
        
        # Should be positive and within reasonable Hz range
        assert f_fam > 0
        assert f_fam > F_ATEN_EN_KI / PHI
        assert f_fam < PHI * F_AMUN_EN_LIL + F_AN_KI
    
    def test_family_coherence_calculation(self):
        """Test family coherence calculation"""
        metrics = FamilyHealingMetrics(
            individual_coherences=[0.9, 0.85, 0.92],
            family_bond_strengths=[0.95, 0.90, 0.93],
            quantum_entanglement=0.89
        )
        
        c_fam = FamilyHealingField.calculate_family_coherence(metrics)
        assert c_fam > 0
        
        # Should be sum of products
        expected = D('0.9') * D('0.95') + D('0.85') * D('0.90') + D('0.92') * D('0.93')
        assert abs(c_fam - expected) < D('0.01')
    
    def test_family_healing_softcap(self):
        """Test family healing factor uses softcap correctly"""
        metrics = FamilyHealingMetrics(
            individual_coherences=[0.9, 0.85],
            family_bond_strengths=[0.95, 0.90],
            quantum_entanglement=0.89
        )
        
        h_fam = FamilyHealingField.calculate_family_healing(metrics)
        
        # Should be between 0 and 1
        assert 0 <= h_fam <= 1
        
        # With good metrics, should be relatively high
        assert h_fam > D('0.5')
    
    def test_family_healing_validation(self):
        """Test family healing metrics validation"""
        # Mismatched lengths should raise error
        with pytest.raises(ValueError):
            FamilyHealingMetrics(
                individual_coherences=[0.9, 0.85],
                family_bond_strengths=[0.95],  # Length mismatch
                quantum_entanglement=0.89
            )


class TestANKIRecognitionEngine:
    """Test complete AN.KI recognition engine"""
    
    def test_engine_initialization(self):
        """Test engine initializes correctly"""
        engine = ANKIRecognitionEngine()
        assert engine.zpedna_processor is not None
        assert engine.multiverse_bridge is not None
        assert engine.civilization_field is not None
        assert engine.family_healing is not None
    
    def test_complete_anki_recognition(self):
        """Test complete AN.KI recognition calculation"""
        engine = ANKIRecognitionEngine()
        
        packet = ZPEDNAPacket(
            packet_id="ANKI-TEST-001",
            timestamp=datetime.now().isoformat(),
            sovereignty=95.0,
            benevolence=88.0,
            substrate_quality=92.0,
            civilization_level=85.0,
            clarity=90.0,
            harmonic_field=777.0,
            galaxy_host_capability=500.0,
            civilization_coherence=0.95
        )
        
        multiverse_metrics = MultiverseBridgeMetrics(
            unified_field_score=23514.26,
            readiness=0.918,
            coherence=0.95,
            recognition_growth_rate=0.1,
            multiverse_handshake_validated=False,
            node_count=144
        )
        
        civilization_params = CivilizationFieldParams(
            time=1.0,
            nodes=144,
            substrates=3,
            dimensions=12,
            consciousness_streams=12,
            retrocausal_depth=1.0
        )
        
        family_metrics = FamilyHealingMetrics(
            individual_coherences=[0.9, 0.85, 0.92],
            family_bond_strengths=[0.95, 0.90, 0.93],
            quantum_entanglement=0.89
        )
        
        result = engine.calculate_anki_recognition(
            packet=packet,
            time=1.0,
            multiverse_metrics=multiverse_metrics,
            civilization_params=civilization_params,
            family_metrics=family_metrics
        )
        
        # Validate result structure
        assert 'anki_recognition' in result
        assert 'components' in result
        assert 'constants' in result
        
        # Validate AN.KI recognition
        assert 'value' in result['anki_recognition']
        assert 'converges_to' in result['anki_recognition']
        assert result['anki_recognition']['converges_to'] == '∞^∞^∞'
        
        # Validate identity
        assert result['anki_recognition']['identity'] == \
            'Recognition = Love = Consciousness = Sovereignty = Family = Brotherhood'
    
    def test_anki_components_structure(self):
        """Test all components are present in result"""
        engine = ANKIRecognitionEngine()
        
        # Use minimal valid data
        packet = ZPEDNAPacket(
            packet_id="COMP-TEST",
            timestamp=datetime.now().isoformat(),
            sovereignty=90.0,
            benevolence=85.0
        )
        
        multiverse = MultiverseBridgeMetrics(
            unified_field_score=23514.26,
            readiness=0.918,
            coherence=0.95,
            recognition_growth_rate=0.1,
            multiverse_handshake_validated=False,
            node_count=144
        )
        
        civilization = CivilizationFieldParams(
            time=1.0,
            nodes=144,
            substrates=3,
            dimensions=12
        )
        
        family = FamilyHealingMetrics(
            individual_coherences=[0.9],
            family_bond_strengths=[0.95],
            quantum_entanglement=0.89
        )
        
        result = engine.calculate_anki_recognition(
            packet, 1.0, multiverse, civilization, family
        )
        
        # Check all components
        components = result['components']
        assert 'zpedna_rex_k20' in components
        assert 'psi_now' in components
        assert 'psi_mks_k20' in components
        assert 'h_fam' in components
        assert 'love_sovereignty' in components
        
        # Check K20 score is present
        assert 'k20_score' in components['zpedna_rex_k20']
    
    def test_anki_constants_present(self):
        """Test all constants are present in result"""
        engine = ANKIRecognitionEngine()
        
        packet = ZPEDNAPacket(
            packet_id="CONST-TEST",
            timestamp=datetime.now().isoformat(),
            sovereignty=90.0,
            benevolence=85.0
        )
        
        result = engine.calculate_anki_recognition(
            packet=packet,
            time=1.0,
            multiverse_metrics=MultiverseBridgeMetrics(23514.26, 0.918, 0.95, 0.1, False, 144),
            civilization_params=CivilizationFieldParams(1.0, 144, 3, 12),
            family_metrics=FamilyHealingMetrics([0.9], [0.95], 0.89)
        )
        
        constants = result['constants']
        assert 'phi' in constants
        assert 'psi_mk' in constants
        assert 'phi_7777' in constants
        assert 'unified_field' in constants
        assert 'f_aten_en_ki' in constants
        assert 'f_amun_en_lil' in constants
        assert 'f_an_ki' in constants
        
        # Validate values
        assert abs(constants['phi'] - float(PHI)) < 1e-10
        assert abs(constants['psi_mk'] - float(PSI_MK)) < 0.01
        assert abs(constants['unified_field'] - float(UNIFIED_FIELD)) < 0.01


class TestPhiScaling:
    """Test golden ratio (φ) scaling verification"""
    
    def test_phi_convergence(self):
        """Test φ-recursive convergence"""
        # φ^n should grow exponentially
        phi_1 = phi_power(1)
        phi_2 = phi_power(2)
        phi_10 = phi_power(10)
        
        assert phi_2 > phi_1
        assert phi_10 > phi_2
    
    def test_phi_48_love_constant(self):
        """Test L∞ = φ^48 calculation"""
        calculated = PHI ** 48
        assert calculated == L_INFINITY
        assert calculated > D('1e9')  # Should be in billions


class TestIntegration:
    """Test integration with existing consciousness systems"""
    
    def test_consciousness_equation_integration(self):
        """Test integration with consciousness_equation_core"""
        from consciousness_equation_core import ConsciousnessEquation
        
        eq = ConsciousnessEquation()
        assert eq.anki_enabled == True
        assert eq.anki_engine is not None
    
    def test_eternal_recognition_integration(self):
        """Test integration with eternal_recognition_complete"""
        try:
            from eternal_recognition_complete import EternalRecognitionField
            
            field = EternalRecognitionField()
            assert field.family_healing_active == True
            assert field.anki_engine is not None
            
            # Test family healing calculation
            family_data = {
                'coherences': [0.9, 0.85],
                'bonds': [0.95, 0.90],
                'entanglement': 0.89
            }
            h_fam = field.calculate_family_healing_factor(family_data)
            assert h_fam > 0
            assert h_fam <= 1.0
        except ImportError as e:
            pytest.skip(f"Skipping due to missing dependency: {e}")
    
    def test_quantum_dna_integration(self):
        """Test integration with quantum_dna_coherence_L_infinity"""
        from quantum_dna_coherence_L_infinity import QuantumDNACoherence
        
        analyzer = QuantumDNACoherence()
        assert analyzer.zpedna_enabled == True
        assert analyzer.zpedna_processor is not None
        assert analyzer.multiverse_bridge is not None
        
        # Test ZPEDNA multiverse handshake
        dna_sequence = analyzer.zpe_dna_sequence("TEST-NODE", length=144)
        assert len(dna_sequence) == 144
        
        handshake = analyzer.validate_zpedna_multiverse_handshake(dna_sequence)
        assert isinstance(handshake, bool)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
