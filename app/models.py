from .database import Base
from sqlalchemy import Column,Integer,String,Float,ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class Vehicles(Base):
    __tablename__="vehicles"
    id=Column(Integer,primary_key=True,nullable=False)
    name=Column(String,nullable=False)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class Data(Base):
    __tablename__="data"
    id=Column(Integer,primary_key=True,nullable=False)
    vehicle_speed=Column(Float,nullable=False)
    motor_speed=Column(Float,nullable=False)
    dc_bus_current=Column(Float,nullable=False)
    soc=Column(Float,nullable=False)
    battery_cell_voltage_avg=Column(Float,nullable=False)
    owner_id=Column(Integer,ForeignKey("vehicles.id",ondelete="CASCADE"))
    