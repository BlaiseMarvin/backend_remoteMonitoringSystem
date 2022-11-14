from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class VehicleCreate(BaseModel):
    name: str
    password: str

class VehicleOut(BaseModel):
    id: int
    name: str
    created_at: datetime

class VehicleLogin(BaseModel):
    name: str
    password: str

class DataRecord(BaseModel):
    vehicle_speed:float
    motor_speed:float
    dc_bus_current:float
    soc:float
    battery_cell_voltage_avg: float

class TokenData(BaseModel):
    id:Optional[str]=None

class RecordOut(DataRecord):
    id: int
    owner_id:int

class MultipleRecordOut(DataRecord):
    record_id: int