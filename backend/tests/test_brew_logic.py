import pytest
from app.models import MachineState
from app.domain import brew, fill_water, fill_coffee

def test_brew_success():
    st = MachineState(water_ml=1000, coffee_g=100)
    st2 = brew(st, "espresso")
    assert st2.water_ml == 976
    assert st2.coffee_g == 92

def test_not_enough_water():
    st = MachineState(water_ml=10, coffee_g=100)
    with pytest.raises(Exception) as e:
        brew(st, "espresso")
    assert "Not enough water" in str(e.value)

def test_fill_overflow_water():
    st = MachineState(water_ml=1990, coffee_g=0)
    with pytest.raises(Exception) as e:
        fill_water(st, 20)
    assert "overflow" in str(e.value)

def test_fill_coffee_ok():
    st = MachineState(water_ml=0, coffee_g=400)
    st2 = fill_coffee(st, 50)
    assert st2.coffee_g == 450
