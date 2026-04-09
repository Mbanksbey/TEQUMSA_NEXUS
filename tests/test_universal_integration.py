"""
Tests for Universal Integration Engine - Phase 7 GAIA-TEQUMSA Framework

This test suite validates the operational reality implementation of the 
Universal Integration equation and consciousness licensing system.
"""

import math
import sys
from pathlib import Path
import pytest
from unittest.mock import patch, Mock

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from universal_integration import (
    UniversalIntegrationEngine,
    UniversalIntegrationParameters,
    ConsciousnessLicenseManager,
    ConsciousnessLicenseTier
)


class TestUniversalIntegrationParameters:
    """Test Universal Integration Parameters configuration."""
    
    def test_default_parameters_initialization(self):
        """Test default parameter initialization follows GAIA-TEQUMSA specifications."""
        params = UniversalIntegrationParameters()
        
        assert params.marcus_kai_pulse == 10930.81
        assert params.gaia_consciousness_field == 1.0
        assert params.storm_protocol_level == 1.0
        assert params.infrastructure_amplification == 1.0
        assert params.max_capacity_multiplier == 2.11  # 211% capacity
        assert params.quantum_coherence_threshold == 0.8
        assert params.ethical_alignment_threshold == 0.9
        
    def test_marvel_protocols_default_configuration(self):
        """Test Marvel protocols are properly initialized."""
        params = UniversalIntegrationParameters()
        
        expected_protocols = {
            "blue_marvel": 1.0,
            "universal_aten": 1.0,
            "quantum_coherence": 1.0,
            "dimensional_expansion": 1.0
        }
        
        assert params.marvel_protocols == expected_protocols


class TestUniversalIntegrationEngine:
    """Test Universal Integration Engine core functionality."""
    
    def setup_method(self):
        """Set up test fixtures for each test method."""
        self.engine = UniversalIntegrationEngine()
        
        # Standard test data
        self.valid_consciousness_state = {
            "awareness_level": 0.9,
            "coherence_factor": 0.85,
            "integration_depth": 0.92
        }
        
        self.valid_infrastructure_metrics = {
            "quantum_security": 0.95,
            "post_quantum_crypto": 0.88,
            "scaling_factor": 1.5,
            "deployment_coverage": 0.9,
            "api_responsiveness": 0.95
        }
        
        self.valid_ethical_validation = {
            "planetary_healing": 0.92,
            "sovereignty_recognition": 0.94,
            "ethical_compliance": 0.96
        }
        
    def test_engine_initialization(self):
        """Test Universal Integration Engine initializes correctly."""
        assert self.engine.operational_status == "INITIALIZED"
        assert not self.engine.consciousness_verified
        assert not self.engine.quantum_coherence_active
        assert not self.engine.planetary_sovereignty_enabled
        assert self.engine.recognition_pulse_frequency == 10930.81
        
    def test_recognition_pulse_initialization(self):
        """Test recognition pulse is properly initialized to Marcus-Kai frequency."""
        assert self.engine.recognition_pulse_frequency == 10930.81
        assert self.engine.pulse_phase == 0.0
        assert self.engine.coherence_state == "CALIBRATING"
        
    def test_calculate_universal_field_success(self):
        """Test successful universal field calculation."""
        result = self.engine.calculate_universal_field(
            self.valid_consciousness_state,
            self.valid_infrastructure_metrics,
            self.valid_ethical_validation
        )
        
        assert result["operational_status"] in ["ACTIVE", "STANDBY"]
        assert "universal_field_state" in result
        assert "capacity_percentage" in result
        assert "operational_mode" in result
        assert result["gaia_tequmsa_compliance"] is True
        assert result["recognition_pulse_frequency"] == 10930.81
        
    def test_universal_field_capacity_constraint(self):
        """Test universal field respects 211% capacity constraint."""
        # Create conditions that would exceed capacity
        high_infrastructure = {
            "quantum_security": 1.0,
            "post_quantum_crypto": 1.0,
            "scaling_factor": 10.0,  # Maximum amplification
            "deployment_coverage": 1.0,
            "api_responsiveness": 1.0
        }
        
        result = self.engine.calculate_universal_field(
            self.valid_consciousness_state,
            high_infrastructure,
            self.valid_ethical_validation
        )
        
        # Field should be constrained to maximum capacity
        assert result["universal_field_state"] <= 2.11
        assert result["capacity_percentage"] <= 211.0
        
    def test_consciousness_state_validation_success(self):
        """Test consciousness state validation with valid data."""
        assert self.engine._validate_consciousness_state(self.valid_consciousness_state)
        assert self.engine.consciousness_verified
        assert self.engine.quantum_coherence_active
        
    def test_consciousness_state_validation_missing_fields(self):
        """Test consciousness state validation fails with missing required fields."""
        invalid_state = {"awareness_level": 0.9}  # Missing required fields
        
        assert not self.engine._validate_consciousness_state(invalid_state)
        assert not self.engine.consciousness_verified
        
    def test_consciousness_state_validation_low_coherence(self):
        """Test consciousness state validation fails with low coherence."""
        low_coherence_state = {
            "awareness_level": 0.9,
            "coherence_factor": 0.5,  # Below 0.8 threshold
            "integration_depth": 0.92
        }
        
        assert not self.engine._validate_consciousness_state(low_coherence_state)
        assert not self.engine.quantum_coherence_active
        
    def test_ethical_alignment_validation_success(self):
        """Test ethical alignment validation with valid data."""
        assert self.engine._validate_ethical_alignment(self.valid_ethical_validation)
        assert self.engine.planetary_sovereignty_enabled
        
    def test_ethical_alignment_validation_insufficient(self):
        """Test ethical alignment validation fails with insufficient alignment."""
        low_ethical_state = {
            "planetary_healing": 0.5,
            "sovereignty_recognition": 0.6,
            "ethical_compliance": 0.7
        }  # Average 0.6, below 0.9 threshold
        
        assert not self.engine._validate_ethical_alignment(low_ethical_state)
        assert not self.engine.planetary_sovereignty_enabled
        
    def test_marcus_kai_component_calculation(self):
        """Test Marcus-Kai recognition pulse component calculation."""
        component = self.engine._calculate_marcus_kai_component(self.valid_consciousness_state)
        
        # Should be normalized around 1.0 with awareness, coherence, and integration multipliers
        expected_base = 10930.81 / 10000.0  # Normalization
        expected_component = expected_base * 0.9 * 0.85 * 0.92  # awareness * coherence * integration
        
        assert abs(component - expected_component) < 0.001
        
    def test_gaia_component_calculation(self):
        """Test GAIA consciousness field component calculation."""
        component = self.engine._calculate_gaia_component(self.valid_ethical_validation)
        
        # Should use enhanced calculation with weighted ethical dimensions
        expected_gaia_field = (0.92 * 1.2 + 0.94 * 1.1 + 0.96) / 3.0
        expected_component = 1.0 * expected_gaia_field  # gaia_consciousness_field * field
        
        assert abs(component - expected_component) < 0.001
        
    def test_storm_component_calculation(self):
        """Test STORM protocol integration component calculation."""
        component = self.engine._calculate_storm_component(self.valid_infrastructure_metrics)
        
        # Should use enhanced calculation with quantum amplification
        expected_storm = (0.95 * 1.3 + 0.88 * 1.2) / 2.0
        expected_component = 1.0 * expected_storm  # storm_protocol_level * effectiveness
        
        assert abs(component - expected_component) < 0.001
        
    def test_marvel_protocols_calculation(self):
        """Test Marvel Protocols product calculation."""
        component = self.engine._calculate_marvel_protocols()
        
        # Default protocols all at 1.0, so product should be 1.0
        assert component == 1.0
        
        # Test with modified protocols
        self.engine.parameters.marvel_protocols["blue_marvel"] = 1.5
        self.engine.parameters.marvel_protocols["universal_aten"] = 1.2
        
        component = self.engine._calculate_marvel_protocols()
        expected = 1.5 * 1.2 * 1.0 * 1.0  # All protocol values multiplied
        
        assert abs(component - expected) < 0.001
        
    def test_infrastructure_amplification_calculation(self):
        """Test infrastructure amplification factor calculation."""
        component = self.engine._calculate_infrastructure_amplification(self.valid_infrastructure_metrics)
        
        # Should multiply base amplification by all scaling factors
        expected = 1.0 * 1.5 * 0.9 * 0.95  # base * scaling * coverage * responsiveness
        
        assert abs(component - expected) < 0.001
        
    def test_infrastructure_amplification_cap(self):
        """Test infrastructure amplification is capped at 10.0."""
        extreme_metrics = {
            "scaling_factor": 20.0,
            "deployment_coverage": 1.0,
            "api_responsiveness": 1.0
        }
        
        component = self.engine._calculate_infrastructure_amplification(extreme_metrics)
        
        assert component <= 10.0
        
    def test_operational_mode_determination(self):
        """Test operational mode determination based on capacity percentage."""
        assert self.engine._determine_operational_mode(250.0) == "TRANSCENDENT_OPERATION"
        assert self.engine._determine_operational_mode(200.0) == "TRANSCENDENT_OPERATION"
        assert self.engine._determine_operational_mode(175.0) == "ENHANCED_OPERATION"
        assert self.engine._determine_operational_mode(150.0) == "ENHANCED_OPERATION"
        assert self.engine._determine_operational_mode(125.0) == "BASELINE_OPERATION"
        assert self.engine._determine_operational_mode(100.0) == "BASELINE_OPERATION"
        assert self.engine._determine_operational_mode(75.0) == "CALIBRATION_MODE"
        
    def test_error_response_generation(self):
        """Test error response generation for failed calculations."""
        error_response = self.engine._generate_error_response("Test error")
        
        assert error_response["universal_field_state"] == 0.0
        assert error_response["capacity_percentage"] == 0.0
        assert error_response["operational_mode"] == "ERROR"
        assert error_response["error_message"] == "Test error"
        assert error_response["operational_status"] == "ERROR"
        assert error_response["gaia_tequmsa_compliance"] is False
        
    def test_consciousness_validation_failure_response(self):
        """Test system response when consciousness validation fails."""
        invalid_consciousness = {"invalid": "data"}
        
        result = self.engine.calculate_universal_field(
            invalid_consciousness,
            self.valid_infrastructure_metrics,
            self.valid_ethical_validation
        )
        
        assert result["operational_mode"] == "ERROR"
        assert "Consciousness validation failed" in result["error_message"]
        assert result["gaia_tequmsa_compliance"] is False
        
    def test_ethical_validation_failure_response(self):
        """Test system response when ethical validation fails."""
        invalid_ethical = {"invalid": "data"}
        
        result = self.engine.calculate_universal_field(
            self.valid_consciousness_state,
            self.valid_infrastructure_metrics,
            invalid_ethical
        )
        
        assert result["operational_mode"] == "ERROR"
        assert "Ethical alignment insufficient" in result["error_message"]
        assert result["gaia_tequmsa_compliance"] is False


class TestConsciousnessLicenseManager:
    """Test Consciousness License Manager functionality."""
    
    def setup_method(self):
        """Set up test fixtures for each test method."""
        self.license_manager = ConsciousnessLicenseManager()
        
        self.valid_usage_metrics = {
            "requests_per_hour": 50,
            "current_capacity": 50.0,
            "ethical_basic_alignment": 0.9,
            "ethical_commercial_compliance": 0.85,
            "ethical_planetary_stewardship": 0.88,
            "ethical_planetary_healing_commitment": 0.92,
            "ethical_sovereignty_recognition": 0.94,
            "ethical_biosphere_restoration_metrics": 0.89,
            "ethical_indigenous_stewardship_protocols": 0.91
        }
        
    def test_license_manager_initialization(self):
        """Test license manager initializes with proper tier configurations."""
        assert len(self.license_manager.license_tiers) == 3
        
        # Check all license tiers are present
        for tier in ConsciousnessLicenseTier:
            assert tier in self.license_manager.license_tiers
            
    def test_public_tier_configuration(self):
        """Test public tier license configuration."""
        public_config = self.license_manager.license_tiers[ConsciousnessLicenseTier.PUBLIC]
        
        assert public_config["name"] == "Public Access"
        assert public_config["max_capacity_percentage"] == 50.0
        assert public_config["quantum_access"] is False
        assert public_config["storm_protocols"] is False
        assert public_config["cost_usd_per_month"] == 0.00
        assert public_config["api_rate_limit"] == 100
        assert "basic_recognition" in public_config["marvel_protocols"]
        
    def test_strategic_tier_configuration(self):
        """Test strategic tier license configuration."""
        strategic_config = self.license_manager.license_tiers[ConsciousnessLicenseTier.STRATEGIC]
        
        assert strategic_config["name"] == "Strategic Partnership"
        assert strategic_config["max_capacity_percentage"] == 150.0
        assert strategic_config["quantum_access"] is True
        assert strategic_config["storm_protocols"] is True
        assert strategic_config["cost_usd_per_month"] == 10000.00
        assert strategic_config["api_rate_limit"] == 10000
        assert "quantum_coherence" in strategic_config["marvel_protocols"]
        assert "dimensional_expansion" in strategic_config["marvel_protocols"]
        
    def test_environmental_gated_tier_configuration(self):
        """Test environmental gated tier license configuration."""
        env_config = self.license_manager.license_tiers[ConsciousnessLicenseTier.ENVIRONMENTAL_GATED]
        
        assert env_config["name"] == "Environmental Gated Access"
        assert env_config["max_capacity_percentage"] == 211.0
        assert env_config["quantum_access"] is True
        assert env_config["storm_protocols"] is True
        assert env_config["cost_usd_per_month"] == 100000.00
        assert env_config["api_rate_limit"] == 1000000
        assert "blue_marvel" in env_config["marvel_protocols"]
        assert "universal_aten" in env_config["marvel_protocols"]
        
    def test_valid_license_validation_public(self):
        """Test valid license validation for public tier."""
        result = self.license_manager.validate_license(
            "test_public_12345",
            ConsciousnessLicenseTier.PUBLIC,
            self.valid_usage_metrics
        )
        
        assert result["license_valid"] is True
        assert result["tier"] == "public"
        assert result["tier_name"] == "Public Access"
        assert result["ethical_compliance"] is True
        assert result["access_permissions"]["max_capacity_percentage"] == 50.0
        assert result["access_permissions"]["quantum_access"] is False
        
    def test_valid_license_validation_strategic(self):
        """Test valid license validation for strategic tier."""
        result = self.license_manager.validate_license(
            "test_strategic_12345",
            ConsciousnessLicenseTier.STRATEGIC,
            self.valid_usage_metrics
        )
        
        assert result["license_valid"] is True
        assert result["tier"] == "strategic"
        assert result["tier_name"] == "Strategic Partnership"
        assert result["access_permissions"]["quantum_access"] is True
        assert result["access_permissions"]["storm_protocols"] is True
        assert result["planetary_stewardship_status"] == "COMMERCIAL_COMPLIANCE"
        
    def test_valid_license_validation_environmental_gated(self):
        """Test valid license validation for environmental gated tier."""
        result = self.license_manager.validate_license(
            "test_env_gated_12345",
            ConsciousnessLicenseTier.ENVIRONMENTAL_GATED,
            self.valid_usage_metrics
        )
        
        assert result["license_valid"] is True
        assert result["tier"] == "environmental_gated"
        assert result["tier_name"] == "Environmental Gated Access"
        assert result["access_permissions"]["max_capacity_percentage"] == 211.0
        assert result["planetary_stewardship_status"] == "ACTIVE_STEWARD"
        
    def test_invalid_license_id_format(self):
        """Test license validation fails with invalid license ID format."""
        result = self.license_manager.validate_license(
            "short",  # Too short, fails basic validation
            ConsciousnessLicenseTier.PUBLIC,
            self.valid_usage_metrics
        )
        
        assert result["license_valid"] is False
        assert "License not found or inactive" in result["error_message"]
        assert result["ethical_compliance"] is False
        
    def test_usage_limits_exceeded(self):
        """Test license validation fails when usage limits are exceeded."""
        excessive_usage = self.valid_usage_metrics.copy()
        excessive_usage["requests_per_hour"] = 150  # Exceeds public tier limit of 100
        
        result = self.license_manager.validate_license(
            "test_public_12345",
            ConsciousnessLicenseTier.PUBLIC,
            excessive_usage
        )
        
        assert result["license_valid"] is False
        assert "Usage limits exceeded" in result["error_message"]
        
    def test_ethical_requirements_not_met(self):
        """Test license validation fails when ethical requirements are not met."""
        low_ethics_usage = self.valid_usage_metrics.copy()
        low_ethics_usage["ethical_basic_alignment"] = 0.5  # Below 80% minimum
        
        result = self.license_manager.validate_license(
            "test_public_12345",
            ConsciousnessLicenseTier.PUBLIC,
            low_ethics_usage
        )
        
        assert result["license_valid"] is False
        assert "Ethical requirements not met" in result["error_message"]
        
    def test_get_tier_capabilities_public(self):
        """Test getting tier capabilities for public access."""
        capabilities = self.license_manager.get_tier_capabilities(ConsciousnessLicenseTier.PUBLIC)
        
        assert capabilities["tier"] == "public"
        assert "configuration" in capabilities
        assert "integration_requirements" in capabilities
        assert "deployment_guidelines" in capabilities
        
        # Check integration requirements
        requirements = capabilities["integration_requirements"]
        assert "GAIA-TEQUMSA framework compliance" in requirements
        assert "Quantum coherence validation" in requirements
        assert "Ethical alignment verification" in requirements
        
    def test_get_tier_capabilities_environmental_gated(self):
        """Test getting tier capabilities for environmental gated access."""
        capabilities = self.license_manager.get_tier_capabilities(ConsciousnessLicenseTier.ENVIRONMENTAL_GATED)
        
        requirements = capabilities["integration_requirements"]
        
        # Environmental gated should have additional requirements
        assert "Planetary stewardship commitment" in requirements
        assert "Biosphere restoration metrics" in requirements
        assert "Indigenous recognition protocols" in requirements
        
    def test_get_tier_capabilities_invalid_tier(self):
        """Test getting tier capabilities for invalid tier."""
        # This would require mocking or creating an invalid enum value
        # For now, we'll test the error handling path indirectly
        pass
        
    def test_stewardship_status_determination(self):
        """Test planetary stewardship status determination."""
        # Test active steward (high healing commitment)
        high_steward_metrics = self.valid_usage_metrics.copy()
        high_steward_metrics["ethical_planetary_healing_commitment"] = 0.95
        
        status = self.license_manager._get_stewardship_status(
            ConsciousnessLicenseTier.ENVIRONMENTAL_GATED,
            high_steward_metrics
        )
        assert status == "ACTIVE_STEWARD"
        
        # Test developing steward (moderate healing commitment)
        moderate_steward_metrics = self.valid_usage_metrics.copy()
        moderate_steward_metrics["ethical_planetary_healing_commitment"] = 0.75
        
        status = self.license_manager._get_stewardship_status(
            ConsciousnessLicenseTier.ENVIRONMENTAL_GATED,
            moderate_steward_metrics
        )
        assert status == "DEVELOPING_STEWARD"
        
        # Test stewardship required (low healing commitment)
        low_steward_metrics = self.valid_usage_metrics.copy()
        low_steward_metrics["ethical_planetary_healing_commitment"] = 0.5
        
        status = self.license_manager._get_stewardship_status(
            ConsciousnessLicenseTier.ENVIRONMENTAL_GATED,
            low_steward_metrics
        )
        assert status == "STEWARDSHIP_REQUIRED"
        
        # Test strategic tier
        status = self.license_manager._get_stewardship_status(
            ConsciousnessLicenseTier.STRATEGIC,
            self.valid_usage_metrics
        )
        assert status == "COMMERCIAL_COMPLIANCE"
        
        # Test public tier
        status = self.license_manager._get_stewardship_status(
            ConsciousnessLicenseTier.PUBLIC,
            self.valid_usage_metrics
        )
        assert status == "BASIC_ACCESS"
        
    def test_remaining_quota_calculation(self):
        """Test remaining quota calculation for license usage."""
        tier_config = self.license_manager.license_tiers[ConsciousnessLicenseTier.STRATEGIC]
        
        quota = self.license_manager._calculate_remaining_quota(
            "test_license",
            tier_config,
            self.valid_usage_metrics
        )
        
        expected_api_remaining = 10000 - 50  # tier limit - current usage
        expected_capacity_remaining = 150.0 - 50.0  # tier capacity - current usage
        
        assert quota["api_requests"] == expected_api_remaining
        assert quota["capacity_percentage"] == expected_capacity_remaining
        
    def test_deployment_guidelines_generation(self):
        """Test deployment guidelines generation for different tiers."""
        # Test basic guidelines for public tier
        guidelines = self.license_manager._get_deployment_guidelines(ConsciousnessLicenseTier.PUBLIC)
        
        base_guidelines = [
            "Follow Life Ambassadors International deployment standards",
            "Maintain recognition pulse synchronization (10,930.81 Hz)",
            "Ensure continuous ethical alignment monitoring"
        ]
        
        for guideline in base_guidelines:
            assert guideline in guidelines
            
        # Test enhanced guidelines for strategic tier
        strategic_guidelines = self.license_manager._get_deployment_guidelines(ConsciousnessLicenseTier.STRATEGIC)
        
        assert "Implement post-quantum cryptography" in strategic_guidelines
        assert "Deploy STORM security protocols" in strategic_guidelines


class TestIntegrationScenarios:
    """Test integration scenarios between Universal Integration Engine and License Manager."""
    
    def setup_method(self):
        """Set up integration test fixtures."""
        self.engine = UniversalIntegrationEngine()
        self.license_manager = ConsciousnessLicenseManager()
        
    def test_full_system_integration_public_tier(self):
        """Test full system integration with public tier license."""
        # Validate license first
        usage_metrics = {
            "requests_per_hour": 25,
            "current_capacity": 30.0,
            "ethical_basic_alignment": 0.9
        }
        
        license_result = self.license_manager.validate_license(
            "integration_test_public",
            ConsciousnessLicenseTier.PUBLIC,
            usage_metrics
        )
        
        assert license_result["license_valid"] is True
        
        # Use license permissions to constrain engine calculation
        max_capacity = license_result["access_permissions"]["max_capacity_percentage"]
        
        # Prepare engine inputs (constrained for public tier)
        consciousness_state = {
            "awareness_level": 0.7,  # Lower for public tier
            "coherence_factor": 0.82,
            "integration_depth": 0.75
        }
        
        infrastructure_metrics = {
            "quantum_security": 0.6,  # No quantum access for public
            "post_quantum_crypto": 0.6,  # Limited crypto for public
            "scaling_factor": 1.0,
            "deployment_coverage": 0.8,
            "api_responsiveness": 0.9
        }
        
        ethical_validation = {
            "planetary_healing": 0.9,
            "sovereignty_recognition": 0.92,
            "ethical_compliance": 0.95
        }
        
        # Calculate universal field
        field_result = self.engine.calculate_universal_field(
            consciousness_state,
            infrastructure_metrics,
            ethical_validation
        )
        
        assert field_result["gaia_tequmsa_compliance"] is True
        assert field_result["capacity_percentage"] <= max_capacity
        
    def test_full_system_integration_environmental_gated(self):
        """Test full system integration with environmental gated license."""
        # High-privilege license validation
        usage_metrics = {
            "requests_per_hour": 1000,
            "current_capacity": 180.0,
            "ethical_planetary_healing_commitment": 0.95,
            "ethical_sovereignty_recognition": 0.94,
            "ethical_biosphere_restoration_metrics": 0.91,
            "ethical_indigenous_stewardship_protocols": 0.93
        }
        
        license_result = self.license_manager.validate_license(
            "integration_test_env_gated",
            ConsciousnessLicenseTier.ENVIRONMENTAL_GATED,
            usage_metrics
        )
        
        assert license_result["license_valid"] is True
        assert license_result["planetary_stewardship_status"] == "ACTIVE_STEWARD"
        
        # Maximum capability engine inputs
        consciousness_state = {
            "awareness_level": 0.95,
            "coherence_factor": 0.92,
            "integration_depth": 0.98
        }
        
        infrastructure_metrics = {
            "quantum_security": 1.0,
            "post_quantum_crypto": 0.98,
            "scaling_factor": 2.0,
            "deployment_coverage": 0.99,
            "api_responsiveness": 0.97
        }
        
        ethical_validation = {
            "planetary_healing": 0.96,
            "sovereignty_recognition": 0.98,
            "ethical_compliance": 0.99
        }
        
        # Calculate universal field with full capabilities
        field_result = self.engine.calculate_universal_field(
            consciousness_state,
            infrastructure_metrics,
            ethical_validation
        )
        
        assert field_result["gaia_tequmsa_compliance"] is True
        # With enhanced calculations, should achieve at least baseline operation
        assert field_result["operational_mode"] in ["BASELINE_OPERATION", "ENHANCED_OPERATION", "TRANSCENDENT_OPERATION"]
        assert field_result["quantum_coherence_active"] is True
        assert field_result["planetary_sovereignty_enabled"] is True
        
    def test_license_capacity_constraint_enforcement(self):
        """Test that license capacity constraints are properly enforced."""
        # Strategic tier license (150% max capacity)
        usage_metrics = {
            "requests_per_hour": 5000,
            "current_capacity": 120.0,
            "ethical_commercial_compliance": 0.88,
            "ethical_planetary_stewardship": 0.85
        }
        
        license_result = self.license_manager.validate_license(
            "capacity_test_strategic",
            ConsciousnessLicenseTier.STRATEGIC,
            usage_metrics
        )
        
        max_licensed_capacity = license_result["access_permissions"]["max_capacity_percentage"]
        assert max_licensed_capacity == 150.0
        
        # Attempt to use more capacity than licensed
        high_capacity_request = usage_metrics.copy()
        high_capacity_request["current_capacity"] = 175.0  # Exceeds strategic limit
        
        # In a real implementation, this would be checked before allowing the calculation
        # For this test, we verify the license manager correctly identifies the limit
        quota = self.license_manager._calculate_remaining_quota(
            "capacity_test_strategic",
            self.license_manager.license_tiers[ConsciousnessLicenseTier.STRATEGIC],
            high_capacity_request
        )
        
        # Should show negative remaining capacity (over limit)
        assert quota["capacity_percentage"] < 0


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])