from pydantic import BaseModel, Field, EmailStr
from fastapi import APIRouter,status, HTTPException
from fastapi import FastAPI, Path, Depends 
from helper.helper import get_db
from sqlalchemy.orm import Session
import models
from schema import Driver




app = APIRouter(
    prefix="/api/v1"
)

    

@app.get("/drivers")
def get_all_drivers(db: Session = Depends(get_db)):
    return db.query(models.Drivers).all()

@app.post("/create-drivers")
def create_drivers(driver : Driver, db: Session = Depends(get_db)):    
           
    driver_model = models.Drivers()
    driver_model.name= driver.name
    driver_model.phone_number = driver.phone_number
    driver_model.email_address = driver.email_address
    driver_model.date_birth  = driver.date_birth
    driver_model.status = driver.status
    db.add(driver_model)
    db.commit()

    return driver
