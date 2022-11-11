from pydantic import BaseModel
from datetime import datetime

class VehicleCreate(BaseModel):
    name: str
    password: str

class VehicleOut(BaseModel):
    id: int
    name: str
    created_at: datetime

class VehicleLogin(VehicleCreate):
    pass
