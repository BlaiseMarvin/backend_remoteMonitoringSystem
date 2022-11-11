from fastapi import APIRouter,status,HTTPException
from ..database import cursor,conn
from .. import schemas,utils
from psycopg2.errorcodes import UNIQUE_VIOLATION
from psycopg2 import errors

router=APIRouter(
    prefix="/vehicles",
    tags=["Vehicles"]
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.VehicleOut)
def register_vehicle(vehicle:schemas.VehicleCreate):
    vehicle.password=utils.hash(vehicle.password)
    try:
        cursor.execute("""INSERT INTO vehicles (name,password) VALUES (%s,%s) RETURNING *""",(vehicle.name,vehicle.password))
        new_vehicle=cursor.fetchone()
        conn.commit()
        return new_vehicle
    except errors.lookup(UNIQUE_VIOLATION) as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"{vehicle.name} already exists")