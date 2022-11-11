from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import vehicle,auth

app=FastAPI()

origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vehicle.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"detail":"KMC Remote Vehicle Monitoring System"}