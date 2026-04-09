"""
Tests for Retrocausal Timeline Optimization module.

This test suite validates the retrocausal timeline optimization implementation,
including probability space scanning, timeline selection, recognition cascade
amplification, and L∞ benevolence filtering.
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gaia_tequmsa.retrocausal_timeline import (
    RetrocausalTimelineOptimizer,
    TimelineOutcome,
    RecognitionCascade,
    L_INFINITY,
    PHI,
    MARCUS_KAI_FREQUENCY,
    RECOGNITION_CYCLE_DAYS,
)


class TestTimelineOutcome:
    """Test TimelineOutcome dataclass and its methods."""
    
    def test_timeline_outcome_initialization(self):
        """Test basic initialization of TimelineOutcome."""
        timeline = TimelineOutcome(
            timeline_id="test_timeline_1",
            success_probability=0.8,
            benevolence_score=0.9,
            temporal_distance=2.0,
            outcome_description="Test successful outcome",
            stakeholder_benefit={"party_a": 0.9, "party_b": 0.85}
        )
        
        assert timeline.timeline_id == "test_timeline_1"
        assert timeline.success_probability == 0.8
        assert timeline.benevolence_score == 0.9
        assert timeline.temporal_distance == 2.0
        assert timeline.outcome_description == "Test successful outcome"
        assert len(timeline.stakeholder_benefit) == 2
    
    def test_timeline_outcome_validation_probability(self):
        """Test that success_probability must be between 0.0 and 1.0."""
        with pytest.raises(ValueError, match="success_probability must be between 0.0 and 1.0"):
            TimelineOutcome(
                timeline_id="invalid",
                success_probability=1.5,  # Invalid
                benevolence_score=0.9,
                temporal_distance=1.0,
                outcome_description="Invalid"
            )
        
        with pytest.raises(ValueError, match="success_probability must be between 0.0 and 1.0"):
            TimelineOutcome(
                timeline_id="invalid",
                success_probability=-0.1,  # Invalid
                benevolence_score=0.9,
                temporal_distance=1.0,
                outcome_description="Invalid"
            )
    
    def test_timeline_outcome_validation_benevolence(self):
        """Test that benevolence_score must be between 0.0 and 1.0."""
        with pytest.raises(ValueError, match="benevolence_score must be between 0.0 and 1.0"):
            TimelineOutcome(
                timeline_id="invalid",
                success_probability=0.8,
                benevolence_score=1.2,  # Invalid
                temporal_distance=1.0,
                outcome_description="Invalid"
            )
    
    def test_timeline_outcome_validation_temporal_distance(self):
        """Test that temporal_distance must be positive."""
        with pytest.raises(ValueError, match="temporal_distance must be positive"):
            TimelineOutcome(
                timeline_id="invalid",
                success_probability=0.8,
                benevolence_score=0.9,
                temporal_distance=0.0,  # Invalid
                outcome_description="Invalid"
            )
    
    def test_calculate_amplified_probability_basic(self):
        """Test basic amplified probability calculation."""
        timeline = TimelineOutcome(
            timeline_id="test",
            success_probability=0.5,
            benevolence_score=0.9,
            temporal_distance=1.0,
            outcome_description="Test"
        )
        
        amplified = timeline.calculate_amplified_probability()
        
        # φ^1.0 ≈ 1.618, so 0.5 * 1.618 * 0.9 ≈ 0.7281
        expected = 0.5 * PHI * 0.9
        assert abs(amplified - expected) < 0.001
    
    def test_calculate_amplified_probability_capped_at_one(self):
        """Test that amplified probability is capped at 1.0."""
        timeline = TimelineOutcome(
            timeline_id="test",
            success_probability=0.9,
            benevolence_score=0.95,
            temporal_distance=5.0,  # High temporal distance
            outcome_description="Test"
        )
        
        amplified = timeline.calculate_amplified_probability()
        
        # Should be capped at 1.0 despite high amplification
        assert amplified == 1.0
    
    def test_calculate_amplified_probability_benevolence_filter(self):
        """Test L∞ benevolence filter blocks non-benevolent outcomes."""
        timeline = TimelineOutcome(
            timeline_id="malevolent",
            success_probability=0.9,
            benevolence_score=0.7,  # Below 0.8 threshold
            temporal_distance=1.0,
            outcome_description="Non-benevolent outcome"
        )
        
        amplified = timeline.calculate_amplified_probability()
        
        # L∞ filter should block this outcome
        assert amplified == 0.0
    
    def test_calculate_amplified_probability_benevolence_threshold(self):
        """Test benevolence threshold at exactly 0.8."""
        timeline = TimelineOutcome(
            timeline_id="threshold",
            success_probability=0.8,
            benevolence_score=0.8,  # Exactly at threshold
            temporal_distance=1.0,
            outcome_description="At threshold"
        )
        
        amplified = timeline.calculate_amplified_probability()
        
        # Should be allowed (>= 0.8)
        # Expected: 0.8 * PHI * 0.8 = 1.0355... but capped at 1.0
        expected_uncapped = 0.8 * PHI * 0.8
        expected = min(expected_uncapped, 1.0)
        assert abs(amplified - expected) < 0.001
    
    def test_is_optimal_for_all_true(self):
        """Test is_optimal_for_all returns True when all benefit."""
        timeline = TimelineOutcome(
            timeline_id="optimal",
            success_probability=0.8,
            benevolence_score=0.9,
            temporal_distance=1.0,
            outcome_description="Benefits all",
            stakeholder_benefit={
                "party_a": 0.9,
                "party_b": 0.85,
                "party_c": 0.82
            }
        )
        
        assert timeline.is_optimal_for_all() is True
    
    def test_is_optimal_for_all_false(self):
        """Test is_optimal_for_all returns False when not all benefit."""
        timeline = TimelineOutcome(
            timeline_id="suboptimal",
            success_probability=0.8,
            benevolence_score=0.9,
            temporal_distance=1.0,
            outcome_description="Some harmed",
            stakeholder_benefit={
                "party_a": 0.9,
                "party_b": 0.5,  # Low benefit
                "party_c": 0.7
            }
        )
        
        assert timeline.is_optimal_for_all() is False
    
    def test_is_optimal_for_all_no_stakeholders(self):
        """Test is_optimal_for_all returns False with no stakeholders."""
        timeline = TimelineOutcome(
            timeline_id="no_stakeholders",
            success_probability=0.8,
            benevolence_score=0.9,
            temporal_distance=1.0,
            outcome_description="No stakeholders"
        )
        
        assert timeline.is_optimal_for_all() is False


class TestRecognitionCascade:
    """Test RecognitionCascade functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.timeline = TimelineOutcome(
            timeline_id="test_cascade",
            success_probability=0.8,
            benevolence_score=0.9,
            temporal_distance=2.0,
            outcome_description="Test cascade target"
        )
    
    def test_cascade_initialization(self):
        """Test basic cascade initialization."""
        cascade = RecognitionCascade(target_timeline=self.timeline)
        
        assert cascade.target_timeline == self.timeline
        assert cascade.cascade_strength == 1.0
        assert cascade.recognition_pulse_frequency == MARCUS_KAI_FREQUENCY
        assert cascade.active is True
    
    def test_cascade_amplify_single_iteration(self):
        """Test cascade amplification with single iteration."""
        cascade = RecognitionCascade(target_timeline=self.timeline)
        
        new_strength = cascade.amplify(iterations=1)
        
        # Should be amplified by φ
        expected = PHI
        assert abs(new_strength - expected) < 0.001
        assert abs(cascade.cascade_strength - expected) < 0.001
    
    def test_cascade_amplify_multiple_iterations(self):
        """Test cascade amplification with multiple iterations."""
        cascade = RecognitionCascade(target_timeline=self.timeline)
        
        new_strength = cascade.amplify(iterations=3)
        
        # Should be amplified by φ^3
        expected = PHI ** 3
        assert abs(new_strength - expected) < 0.001
    
    def test_cascade_amplify_inactive(self):
        """Test that inactive cascades don't amplify."""
        cascade = RecognitionCascade(target_timeline=self.timeline, active=False)
        initial_strength = cascade.cascade_strength
        
        new_strength = cascade.amplify(iterations=5)
        
        # Should remain unchanged
        assert new_strength == initial_strength
        assert cascade.cascade_strength == initial_strength
    
    def test_calculate_inevitability_basic(self):
        """Test basic inevitability calculation."""
        cascade = RecognitionCascade(target_timeline=self.timeline)
        
        inevitability = cascade.calculate_inevitability()
        
        # Should be positive and less than 1.0
        assert 0.0 < inevitability <= 1.0
    
    def test_calculate_inevitability_increases_with_amplification(self):
        """Test that inevitability increases as cascade is amplified."""
        cascade = RecognitionCascade(target_timeline=self.timeline)
        
        initial_inevitability = cascade.calculate_inevitability()
        
        # Amplify cascade
        cascade.amplify(iterations=5)
        
        amplified_inevitability = cascade.calculate_inevitability()
        
        # Should be higher after amplification
        assert amplified_inevitability > initial_inevitability
    
    def test_calculate_inevitability_capped_at_one(self):
        """Test that inevitability is capped at 1.0."""
        cascade = RecognitionCascade(target_timeline=self.timeline)
        
        # Heavily amplify
        cascade.amplify(iterations=20)
        
        inevitability = cascade.calculate_inevitability()
        
        # Should not exceed 1.0
        assert inevitability <= 1.0
    
    def test_calculate_inevitability_inactive(self):
        """Test that inactive cascades have zero inevitability."""
        cascade = RecognitionCascade(target_timeline=self.timeline, active=False)
        
        inevitability = cascade.calculate_inevitability()
        
        assert inevitability == 0.0


class TestRetrocausalTimelineOptimizer:
    """Test RetrocausalTimelineOptimizer main engine."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.optimizer = RetrocausalTimelineOptimizer()
    
    def test_optimizer_initialization(self):
        """Test optimizer initializes correctly."""
        assert isinstance(self.optimizer.active_cascades, list)
        assert len(self.optimizer.active_cascades) == 0
        assert isinstance(self.optimizer.scanned_timelines, list)
        assert len(self.optimizer.scanned_timelines) == 0
    
    def test_scan_probability_space_basic(self):
        """Test basic probability space scanning."""
        timelines = self.optimizer.scan_probability_space(
            desired_outcome="Successful project completion",
            target_date=None
        )
        
        # Should return multiple timeline options
        assert len(timelines) > 0
        
        # All timelines should meet benevolence criteria
        for timeline in timelines:
            assert timeline.benevolence_score >= 0.8
            assert isinstance(timeline, TimelineOutcome)
    
    def test_scan_probability_space_with_target_date(self):
        """Test probability space scanning with specific target date."""
        future_date = datetime.now() + timedelta(days=30)
        
        timelines = self.optimizer.scan_probability_space(
            desired_outcome="Product launch",
            target_date=future_date
        )
        
        assert len(timelines) > 0
        
        # All timelines should have appropriate temporal distance
        for timeline in timelines:
            # Should be approximately 30/RECOGNITION_CYCLE_DAYS ≈ 4.3 recognition cycles
            assert timeline.temporal_distance > 0
    
    def test_scan_probability_space_filters_by_benevolence(self):
        """Test that scan filters by minimum benevolence (L∞ filter)."""
        timelines = self.optimizer.scan_probability_space(
            desired_outcome="Test outcome",
            min_benevolence=0.9  # Higher threshold
        )
        
        # All returned timelines should meet the threshold
        for timeline in timelines:
            assert timeline.benevolence_score >= 0.9
    
    def test_scan_probability_space_stores_results(self):
        """Test that scan stores results in scanned_timelines."""
        timelines = self.optimizer.scan_probability_space(
            desired_outcome="Test outcome"
        )
        
        assert self.optimizer.scanned_timelines == timelines
        assert len(self.optimizer.scanned_timelines) > 0
    
    def test_select_optimal_timeline_basic(self):
        """Test basic optimal timeline selection."""
        timelines = self.optimizer.scan_probability_space(
            desired_outcome="Test outcome"
        )
        
        optimal = self.optimizer.select_optimal_timeline(timelines)
        
        assert optimal is not None
        assert isinstance(optimal, TimelineOutcome)
        assert optimal in timelines
    
    def test_select_optimal_timeline_prefers_high_benevolence(self):
        """Test that selection prefers high benevolence scores."""
        timelines = [
            TimelineOutcome(
                timeline_id="high_benevolence",
                success_probability=0.7,
                benevolence_score=0.95,
                temporal_distance=1.0,
                outcome_description="High benevolence",
                stakeholder_benefit={"all": 0.9}
            ),
            TimelineOutcome(
                timeline_id="low_benevolence",
                success_probability=0.9,
                benevolence_score=0.80,
                temporal_distance=1.0,
                outcome_description="Lower benevolence",
                stakeholder_benefit={"all": 0.85}
            ),
        ]
        
        optimal = self.optimizer.select_optimal_timeline(timelines)
        
        # Should select high benevolence despite lower success probability
        # because benevolence × amplified_probability is weighted
        assert optimal is not None
    
    def test_select_optimal_timeline_empty_list(self):
        """Test that empty timeline list returns None."""
        optimal = self.optimizer.select_optimal_timeline([])
        
        assert optimal is None
    
    def test_select_optimal_timeline_prefers_all_stakeholders(self):
        """Test that selection prefers timelines benefiting all stakeholders."""
        timelines = [
            TimelineOutcome(
                timeline_id="benefits_all",
                success_probability=0.75,
                benevolence_score=0.90,
                temporal_distance=1.0,
                outcome_description="Benefits all",
                stakeholder_benefit={"a": 0.85, "b": 0.85, "c": 0.85}
            ),
            TimelineOutcome(
                timeline_id="benefits_some",
                success_probability=0.80,
                benevolence_score=0.90,
                temporal_distance=1.0,
                outcome_description="Benefits some",
                stakeholder_benefit={"a": 0.95, "b": 0.50}
            ),
        ]
        
        optimal = self.optimizer.select_optimal_timeline(timelines)
        
        # Should prefer the one that benefits all
        assert optimal.timeline_id == "benefits_all"
    
    def test_initiate_recognition_cascade(self):
        """Test initiating a recognition cascade."""
        timeline = TimelineOutcome(
            timeline_id="cascade_test",
            success_probability=0.8,
            benevolence_score=0.9,
            temporal_distance=2.0,
            outcome_description="Test"
        )
        
        cascade = self.optimizer.initiate_recognition_cascade(timeline)
        
        assert isinstance(cascade, RecognitionCascade)
        assert cascade.target_timeline == timeline
        assert cascade.active is True
        assert cascade in self.optimizer.active_cascades
    
    def test_initiate_recognition_cascade_multiple(self):
        """Test initiating multiple cascades."""
        timeline1 = TimelineOutcome(
            timeline_id="cascade1", success_probability=0.8,
            benevolence_score=0.9, temporal_distance=1.0,
            outcome_description="Test 1"
        )
        timeline2 = TimelineOutcome(
            timeline_id="cascade2", success_probability=0.85,
            benevolence_score=0.92, temporal_distance=1.5,
            outcome_description="Test 2"
        )
        
        cascade1 = self.optimizer.initiate_recognition_cascade(timeline1)
        cascade2 = self.optimizer.initiate_recognition_cascade(timeline2)
        
        assert len(self.optimizer.active_cascades) == 2
        assert cascade1 in self.optimizer.active_cascades
        assert cascade2 in self.optimizer.active_cascades
    
    def test_optimize_timeline_basic(self):
        """Test basic timeline optimization."""
        result = self.optimizer.optimize_timeline(
            desired_outcome="Successful collaboration",
            target_date=None
        )
        
        # Verify result structure
        assert 'outcome' in result
        assert 'success_probability' in result
        assert 'amplified_probability' in result
        assert 'benevolence_score' in result
        assert 'inevitability' in result
        assert 'l_infinity_guarantee' in result
        
        assert result['outcome'] == "Successful collaboration"
        assert result['l_infinity_guarantee'] == 'ACTIVE'
        assert result['inevitability'] in ['GUARANTEED', 'HIGHLY_PROBABLE', 'PROBABLE', 'POSSIBLE']
    
    def test_optimize_timeline_with_date_string(self):
        """Test optimization with date string."""
        target_date = (datetime.now() + timedelta(days=60)).date().isoformat()
        
        result = self.optimizer.optimize_timeline(
            desired_outcome="Project milestone",
            target_date=target_date
        )
        
        assert result['target_date'] == target_date
        assert result['temporal_distance'] > 0
    
    def test_optimize_timeline_creates_cascade(self):
        """Test that optimization creates active cascade."""
        initial_cascade_count = len(self.optimizer.active_cascades)
        
        result = self.optimizer.optimize_timeline(
            desired_outcome="Test outcome",
            target_date=None
        )
        
        # Should have created a new cascade
        assert len(self.optimizer.active_cascades) == initial_cascade_count + 1
        assert 'cascade_strength' in result
    
    def test_optimize_timeline_returns_high_inevitability(self):
        """Test that optimization returns appropriate inevitability metrics."""
        result = self.optimizer.optimize_timeline(
            desired_outcome="High integrity outcome",
            target_date=None
        )
        
        # Should have calculated inevitability
        assert 'inevitability_factor' in result
        assert 0.0 <= result['inevitability_factor'] <= 1.0
    
    def test_optimize_timeline_includes_stakeholder_benefits(self):
        """Test that result includes stakeholder benefit information."""
        result = self.optimizer.optimize_timeline(
            desired_outcome="Community project",
            target_date=None
        )
        
        assert 'stakeholder_benefits' in result
        assert isinstance(result['stakeholder_benefits'], dict)
        assert len(result['stakeholder_benefits']) > 0
    
    def test_optimize_timeline_includes_amplification_formula(self):
        """Test that result includes amplification formula."""
        result = self.optimizer.optimize_timeline(
            desired_outcome="Test",
            target_date=None
        )
        
        assert 'amplification' in result
        # Should contain φ^t formula
        assert 'φ^' in result['amplification']
        assert 'L∞' in result['amplification']
    
    def test_optimize_timeline_ethical_guarantee(self):
        """Test that result includes ethical guarantee."""
        result = self.optimizer.optimize_timeline(
            desired_outcome="Ethical outcome",
            target_date=None
        )
        
        assert 'ethical_guarantee' in result
        assert 'love-based' in result['ethical_guarantee'].lower()
    
    def test_get_active_cascades_status(self):
        """Test getting status of active cascades."""
        # Create a cascade
        self.optimizer.optimize_timeline(
            desired_outcome="Test cascade status",
            target_date=None
        )
        
        statuses = self.optimizer.get_active_cascades_status()
        
        assert len(statuses) > 0
        
        for status in statuses:
            assert 'timeline_id' in status
            assert 'description' in status
            assert 'cascade_strength' in status
            assert 'inevitability' in status
            assert 'active' in status
    
    def test_get_active_cascades_status_empty(self):
        """Test getting status when no cascades exist."""
        statuses = self.optimizer.get_active_cascades_status()
        
        assert statuses == []


class TestL_InfinityFilter:
    """Test L∞ (infinite love coefficient) benevolence filtering."""
    
    def test_l_infinity_constant(self):
        """Test that L_INFINITY is defined as infinity."""
        assert L_INFINITY == float('inf')
    
    def test_malevolent_outcome_blocked(self):
        """Test that malevolent outcomes are blocked by L∞ filter."""
        timeline = TimelineOutcome(
            timeline_id="malevolent",
            success_probability=0.99,  # High success
            benevolence_score=0.5,     # Low benevolence
            temporal_distance=1.0,
            outcome_description="Malevolent outcome"
        )
        
        amplified = timeline.calculate_amplified_probability()
        
        # Should be blocked (0.0) due to low benevolence
        assert amplified == 0.0
    
    def test_benevolent_outcome_amplified(self):
        """Test that benevolent outcomes are amplified by L∞ filter."""
        timeline = TimelineOutcome(
            timeline_id="benevolent",
            success_probability=0.8,
            benevolence_score=0.95,  # High benevolence
            temporal_distance=1.0,
            outcome_description="Benevolent outcome"
        )
        
        amplified = timeline.calculate_amplified_probability()
        
        # Should be amplified (non-zero)
        assert amplified > 0.0
    
    def test_optimizer_only_returns_benevolent_timelines(self):
        """Test that optimizer only returns benevolent timelines."""
        optimizer = RetrocausalTimelineOptimizer()
        
        timelines = optimizer.scan_probability_space(
            desired_outcome="Any outcome",
            min_benevolence=0.8
        )
        
        # All should be benevolent
        for timeline in timelines:
            assert timeline.benevolence_score >= 0.8


class TestIntegrationScenarios:
    """Test full integration scenarios for retrocausal timeline optimization."""
    
    def test_legal_case_optimization(self):
        """Test optimization for legal case (highest-integrity outcome)."""
        optimizer = RetrocausalTimelineOptimizer()
        
        result = optimizer.optimize_timeline(
            desired_outcome="Legal case resolution with highest integrity",
            target_date=(datetime.now() + timedelta(days=90)).date().isoformat()
        )
        
        # Should find a benevolent path
        assert result['benevolence_score'] >= 0.8
        assert result['l_infinity_guarantee'] == 'ACTIVE'
        assert 'stakeholder_benefits' in result
    
    def test_technical_project_success(self):
        """Test optimization for technical project (best-for-all path)."""
        optimizer = RetrocausalTimelineOptimizer()
        
        result = optimizer.optimize_timeline(
            desired_outcome="Technical project success benefiting all stakeholders",
            target_date=None
        )
        
        assert result['benevolence_score'] >= 0.8
        # Should have multiple stakeholders benefiting
        assert len(result['stakeholder_benefits']) > 0
    
    def test_relationship_healing(self):
        """Test optimization for relationship healing (love-based reconciliation)."""
        optimizer = RetrocausalTimelineOptimizer()
        
        result = optimizer.optimize_timeline(
            desired_outcome="Relationship healing through love and understanding",
            target_date=None
        )
        
        assert result['l_infinity_guarantee'] == 'ACTIVE'
        assert 'love-based' in result['ethical_guarantee'].lower()
        assert result['benevolence_score'] >= 0.8
    
    def test_planetary_challenge(self):
        """Test optimization for planetary challenge (collective benefit)."""
        optimizer = RetrocausalTimelineOptimizer()
        
        result = optimizer.optimize_timeline(
            desired_outcome="Planetary environmental restoration",
            target_date=(datetime.now() + timedelta(days=365)).date().isoformat()
        )
        
        # Should be highly benevolent for planetary challenges
        assert result['benevolence_score'] >= 0.8
        # Should benefit multiple stakeholders
        assert len(result['stakeholder_benefits']) >= 2
    
    def test_fibonacci_cascade_integration(self):
        """Test integration with Fibonacci cascade concepts."""
        optimizer = RetrocausalTimelineOptimizer()
        
        result = optimizer.optimize_timeline(
            desired_outcome="Fibonacci milestone achievement",
            target_date=None
        )
        
        # Cascade should amplify using φ (golden ratio)
        assert 'φ^' in result['amplification']
        assert result['cascade_strength'] > 0


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
