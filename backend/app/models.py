from pydantic import BaseModel, Field

class MachineState(BaseModel):
    water_ml: int = Field(0, ge=0)
    coffee_g: int = Field(0, ge=0)
    water_capacity_ml: int = Field(2000, ge=1)
    coffee_capacity_g: int = Field(500, ge=1)

class BrewRequest(BaseModel):
    type: str

class FillWaterRequest(BaseModel):
    amount_ml: int

class FillCoffeeRequest(BaseModel):
    amount_g: int

class Message(BaseModel):
    message: str
    state: MachineState
