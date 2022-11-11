from fastapi import APIRouter,status,HTTPException,Depends
from ..database import conn,cursor
from .. import schemas,oauth2

router=APIRouter(
    prefix="/data",
    tags=["Data"]
)

# Save data to the database
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.RecordOut)
def save_record(record:schemas.DataRecord,vehicle_id:int=Depends(oauth2.get_current_user)):
    cursor.execute("""INSERT INTO data (vehicle_speed,motor_speed,dc_bus_current,soc,battery_cell_voltage_avg,owner_id) VALUES (%s,%s,%s,%s,%s,%s) RETURNING *""",(record.vehicle_speed,record.motor_speed,record.dc_bus_current,record.soc,record.battery_cell_voltage_avg,int(vehicle_id.id)))
    new_record=cursor.fetchone()
    conn.commit()
    return new_record
    