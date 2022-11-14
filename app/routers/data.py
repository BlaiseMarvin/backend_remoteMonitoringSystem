from fastapi import APIRouter,status,HTTPException,Depends
from ..database import conn,cursor
from .. import schemas,oauth2
from typing import List

router=APIRouter(
    prefix="/data",
    tags=["Data"]
)

# Get all the data stored within a particular timeframe
@router.get("/",status_code=status.HTTP_200_OK,response_model=List[schemas.MultipleRecordOut])
def get_all_records(vehicle_id:int=Depends(oauth2.get_current_user),t1:str='2018-01-01',t2:str='2022-12-31',limit=50,offset:int=0):
    cursor.execute("""SELECT v.name AS vehicle_name,d.id AS record_id,d.vehicle_speed AS vehicle_speed,d.motor_speed AS motor_speed,d.dc_bus_current AS dc_bus_current,d.soc AS soc,d.battery_cell_voltage_avg AS battery_cell_voltage_avg,d.created_at AS time_stored FROM vehicles v LEFT OUTER JOIN data d ON v.id=d.owner_id WHERE d.created_at BETWEEN %s AND %s  LIMIT %s OFFSET %s""",(t1,t2,limit,offset))
    records=cursor.fetchall()
    if not records:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No data found")
    return records

# Save data to the database
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.RecordOut)
def save_record(record:schemas.DataRecord,vehicle_id:int=Depends(oauth2.get_current_user)):
    cursor.execute("""INSERT INTO data (vehicle_speed,motor_speed,dc_bus_current,soc,battery_cell_voltage_avg,owner_id) VALUES (%s,%s,%s,%s,%s,%s) RETURNING *""",(record.vehicle_speed,record.motor_speed,record.dc_bus_current,record.soc,record.battery_cell_voltage_avg,int(vehicle_id.id)))
    new_record=cursor.fetchone()
    conn.commit()
    return new_record

# Extract a summary of a particular vehicle's data
@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=List[schemas.MultipleRecordOut])
def get_vehicle_data(id:int,vehicle_id:int=Depends(oauth2.get_current_user),limit:int=50,t1:str='2018-01-01',t2:str='2022-12-31',offset:int=0):
    cursor.execute("""SELECT v.name AS vehicle_name,d.id AS record_id,d.vehicle_speed AS vehicle_speed,d.motor_speed AS motor_speed,d.dc_bus_current AS dc_bus_current,d.soc AS soc,d.battery_cell_voltage_avg AS battery_cell_voltage_avg,d.created_at AS time_stored FROM vehicles v LEFT OUTER JOIN data d ON v.id=d.owner_id WHERE (d.created_at BETWEEN %s AND %s) AND d.owner_id=%s LIMIT %s OFFSET %s""",(t1,t2,id,limit,offset))
    records=cursor.fetchall()
    if not records:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No data found")
    return records


# delete a record
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_record(id:int,vehicle_id:int=Depends(oauth2.get_current_user)):
    cursor.execute("""SELECT * FROM data WHERE id=%s""",(id,))
    record=cursor.fetchone()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="record not found")
    elif record['owner_id']==int(vehicle_id.id):
        cursor.execute("""DELETE FROM data WHERE id=%s""",(id,))
        conn.commit()
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You can not delete a record you did not create")


# update a record
@router.put("/{id_}",response_model=schemas.RecordOut)
def update_record(record:schemas.DataRecord,id_:int,vehicle_id:int=Depends(oauth2.get_current_user)):
    cursor.execute("""SELECT * FROM data WHERE id=%s""",(id_,))
    record_=cursor.fetchone()
    if not record_:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail="Record not found")
    elif record_['owner_id']==int(vehicle_id.id):
        cursor.execute("""UPDATE data SET vehicle_speed=%s,motor_speed=%s,dc_bus_current=%s,soc=%s,battery_cell_voltage_avg=%s,owner_id=%s WHERE id=%s RETURNING *""",(record.vehicle_speed,record.motor_speed,record.dc_bus_current,record.soc,record.battery_cell_voltage_avg,int(vehicle_id.id),id_))
        record__=cursor.fetchone()
        conn.commit()
        return record__
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You do not own this record")

