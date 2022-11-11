from fastapi import APIRouter,HTTPException,status
from .. import schemas,utils,oauth2
from ..database import conn,cursor

router=APIRouter(
    tags=["Authentication"]
)

@router.post("/login")
def login(user_credentials:schemas.VehicleLogin):
    cursor.execute("""SELECT * FROM vehicles WHERE name=%s""",(user_credentials.name,))
    vehicle=cursor.fetchone()   
    if not vehicle:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")
    if not utils.verify(user_credentials.password,vehicle['password']):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    # create token
    access_token=oauth2.create_access_token(data={"vehicle_id":vehicle['id']})
    return {"access_token":access_token,"token_type":"bearer"}
