from .models import MachineState
from .errors import HumanReadableError

RECIPES = {
    "espresso":       {"water_ml": 24,  "coffee_g": 8},
    "double_espresso":{"water_ml": 48,  "coffee_g":16},
    "ristretto":      {"water_ml": 16,  "coffee_g": 8},
    "americano":      {"water_ml":148,  "coffee_g":16},
}

def _title(drink: str) -> str:
    return drink.replace("_", " ").title()

def brew(state: MachineState, drink: str) -> MachineState:
    if drink not in RECIPES:
        raise HumanReadableError(f"Unknown drink type '{drink}'. Allowed: {', '.join(RECIPES.keys())}.", 422)

    need = RECIPES[drink]
    label = _title(drink)

    if state.water_ml <= 0 and state.coffee_g <= 0:
        raise HumanReadableError(f"Cannot brew {label}: both containers are empty. Please fill water and coffee.")
    if state.water_ml <= 0:
        raise HumanReadableError(f"Cannot brew {label}: water container is empty. Please fill water.")
    if state.coffee_g <= 0:
        raise HumanReadableError(f"Cannot brew {label}: coffee container is empty. Please fill coffee.")

    if state.water_ml < need["water_ml"]:
        raise HumanReadableError(
            f"Not enough water for {label}. Need {need['water_ml']} ml, have {state.water_ml} ml."
        )
    if state.coffee_g < need["coffee_g"]:
        raise HumanReadableError(
            f"Not enough coffee for {label}. Need {need['coffee_g']} g, have {state.coffee_g} g."
        )

    state.water_ml -= need["water_ml"]
    state.coffee_g -= need["coffee_g"]
    return state

def fill_water(state: MachineState, amount_ml: int) -> MachineState:
    if amount_ml is None or str(amount_ml).strip() == "":
        raise HumanReadableError("Please enter a water amount (ml).", 422)
    if amount_ml <= 0:
        raise HumanReadableError("Water amount must be greater than 0 ml.", 422)
    if state.water_ml + amount_ml > state.water_capacity_ml:
        raise HumanReadableError(
            f"Filling {amount_ml} ml would overflow the water container. "
            f"Current: {state.water_ml} ml, capacity: {state.water_capacity_ml} ml."
        )
    state.water_ml += amount_ml
    return state

def fill_coffee(state: MachineState, amount_g: int) -> MachineState:
    if amount_g is None or str(amount_g).strip() == "":
        raise HumanReadableError("Please enter a coffee amount (g).", 422)
    if amount_g <= 0:
        raise HumanReadableError("Coffee amount must be greater than 0 g.", 422)
    if state.coffee_g + amount_g > state.coffee_capacity_g:
        raise HumanReadableError(
            f"Filling {amount_g} g would overflow the coffee container. "
            f"Current: {state.coffee_g} g, capacity: {state.coffee_capacity_g} g."
        )
    state.coffee_g += amount_g
    return state
