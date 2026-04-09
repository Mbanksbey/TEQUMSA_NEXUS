import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from universal_aten import UniversalAten


def test_lift_mass_within_capacity():
    aten = UniversalAten()
    assert aten.lift_mass(99_999)


def test_lift_mass_invalid_negative():
    aten = UniversalAten()
    with pytest.raises(ValueError):
        aten.lift_mass(-1)


def test_survive_explosion_threshold():
    aten = UniversalAten()
    assert aten.survive_explosion(50)
    assert not aten.survive_explosion(51)


def test_survive_explosion_negative():
    aten = UniversalAten()
    with pytest.raises(ValueError):
        aten.survive_explosion(-0.1)


def test_flight_time_to_moon_positive_speed():
    aten = UniversalAten()
    speed = 700_000
    minutes = aten.flight_time_to_moon(speed)
    expected = (238_900 / speed) * 60
    assert math.isclose(minutes, expected, rel_tol=1e-9)


def test_flight_time_to_moon_requires_positive_speed():
    aten = UniversalAten()
    with pytest.raises(ValueError):
        aten.flight_time_to_moon(0)


def test_generate_energy_blast_scaling():
    aten = UniversalAten()
    assert aten.generate_energy_blast(5) == 50


def test_generate_energy_blast_invalid_intensity():
    aten = UniversalAten()
    with pytest.raises(ValueError):
        aten.generate_energy_blast(-1)


def test_stabilize_antimatter_duration():
    aten = UniversalAten()
    assert aten.stabilize_antimatter(300)
    assert not aten.stabilize_antimatter(301)


def test_stabilize_antimatter_invalid():
    aten = UniversalAten()
    with pytest.raises(ValueError):
        aten.stabilize_antimatter(-5)


def test_manipulate_molecules_requires_target_and_control():
    aten = UniversalAten()
    assert "steel beam" in aten.manipulate_molecules("steel beam")
    aten.molecular_control = False
    with pytest.raises(RuntimeError):
        aten.manipulate_molecules("steel beam")


def test_manipulate_molecules_requires_target():
    aten = UniversalAten()
    with pytest.raises(ValueError):
        aten.manipulate_molecules("")


def test_sense_quark_level_and_ageless():
    aten = UniversalAten()
    assert aten.sense_quark_level()
    assert aten.is_ageless()


def test_expand_dimension_filters_intensity():
    aten = UniversalAten()
    result = aten.expand_dimension({"fear": 0.05, "doubt": 0.5})
    assert "fear" not in result
    assert result["doubt"] == "Add dimension: doubt"


def test_resistance_decay_success_and_failure():
    aten = UniversalAten()
    time_to_zero, success = aten.resistance_decay(1.0, 2.0)
    assert not success
    assert time_to_zero == 60
    time_to_zero, success = aten.resistance_decay(1.0, 0.01)
    assert not success
    assert time_to_zero == 60


def test_resistance_decay_invalid_inputs():
    aten = UniversalAten()
    with pytest.raises(ValueError):
        aten.resistance_decay(-1, 1)
    with pytest.raises(ValueError):
        aten.resistance_decay(1, -1)


def test_network_amplification_scaling():
    aten = UniversalAten()
    assert aten.network_amplification(1.0, 1_000, 0.5) == pytest.approx(31.6227766017)


def test_network_amplification_invalid_inputs():
    aten = UniversalAten()
    with pytest.raises(ValueError):
        aten.network_amplification(-1, 10, 0.1)
    with pytest.raises(ValueError):
        aten.network_amplification(1, 0, 0.1)


def test_validate_decision_threshold():
    aten = UniversalAten()
    assert aten.validate_decision({"flow": 0.9, "alignment": 0.8}) == "proceed"
    assert aten.validate_decision({"flow": 0.7, "alignment": 0.8}) == "optimize"


def test_validate_decision_requires_factors():
    aten = UniversalAten()
    with pytest.raises(ValueError):
        aten.validate_decision({})
