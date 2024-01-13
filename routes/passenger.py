
from pydantic import BaseModel, Field, EmailStr
from fastapi import FastAPI, Path, Depends 
import models
from sqlalchemy.orm import Session
from fastapi import APIRouter,status, HTTPException
from helper.helper import get_db
from schema import Passenger, UpdatePassenger
from typing import Optional
from .transaction import saveTransaction



app = APIRouter(
    prefix="/api/v1"
)

@app.get("/passengers")
def get_all_passengers(db: Session = Depends(get_db)):
    return db.query(models.Passengers).all() # select everything from passanger model

@app.get("/get-passenger/{passenger_id}")
def get_passenger(passenger_id: int = Path(description= "The ID 0f the Passenger", gt=0, le=10),db: Session = Depends(get_db)):
    passenger_model =  db.query(models.Passengers).filter(models.Passengers.id == passenger_id).first() # select everything from passanger model, but return only record where pasenger id = to passenger id collect from user  
    
    if passenger_model is None:
        return {"message": "Passenger not exit", "code":"404"}
    
    return passenger_model

@app.get("/get-passenger-by-name")
def get_passenger(name: str,db: Session = Depends(get_db)):
    passenger_model =  db.query(models.Passengers).filter(models.Passengers.name == name).first()

    if passenger_model is None:
        return {"message": "Name does not exit"}
    
    return passenger_model



@app.get("/get-passenger-by-phone/{passenger_phone}")
def get_passenger_by_phone(passenger_phone: str):
    for passenger_id in passengers:
        if passengers[passenger_id]["phone_number"]==passenger_phone:
           return passengers[passenger_id]  

    return {"message": "passenger with phone not found"}  

@app.get("/get-passenger-by-email/{passenger_email}")
def get_passenger_by_email(passenger_email: Optional[str] = None):
    for passenger_id in passengers:
        if passengers[passenger_id]["email_address"]==passenger_email:
           return passengers[passenger_id]  

    return {"message": "passenger with email not found"}  

@app.post("/create-passenger")
def create_passenger(passenger : Passenger, db: Session = Depends(get_db)):    

    passenger_model = models.Passengers()
    passenger_model.name =  passenger.name
    passenger_model.phone_number  = passenger.phone_number
    passenger_model.balance = passenger.balance
    passenger_model.email_address = passenger.email_address
    passenger_model.status = passenger.status
    db.add(passenger_model)
    db.commit()

    # create record of transaction
    naration = "opening balance"
    saveTransaction(passenger_model.id,passenger.balance,naration, db)
    return passenger

@app.put("/update-passenger/{passenger_id}")
def update_passenger(passenger_id :int, passenger : UpdatePassenger, db: Session = Depends(get_db)):    
    passenger_model =  db.query(models.Passengers).filter(models.Passengers.id == passenger_id).first() # select everything from passanger model, but return only record where pasenger id = to passenger id collect from user  
    
    if passenger_model is None:
        return {"message": "Passenger not exit", "code":"404"}

    if passenger.name != None:       
        # passengers[passenger_id]["name"] = passenger.name  
        passenger_model.name =  passenger.name

    if  passenger.phone_number != None:       
        # passengers[passenger_id]["phone_number"] = passenger.phone_number
        passenger_model.phone_number  = passenger.phone_number

    if passenger.email_address != None:       
        # passengers[passenger_id]["email_address"] = passenger.email_address
        passenger_model.email_address = passenger.email_address

    if  passenger. balance != None:       
        passenger_model.balance = passenger.balance
    
    db.add(passenger_model)
    db.commit()
         
    return passenger    

@app.get("/journey_passenger_transaction/{passenger_id}")
def journey_passenger_transaction_list(passenger_id: int = Path(description= "The List 0f the Passenger transaction", gt=0, le=10000),db: Session = Depends(get_db)):
    journey_passenger_transaction =  db.query(models.Transactions).filter(models.Transactions.passenger_identification == passenger_id).all() # select everything from passanger model, but return only record where pasenger id = to passenger id collect from user  
    
    if journey_passenger_transaction is None:
        return {"message": "Transaction history doe not exit", "code":"404"}
    
    return journey_passenger_transaction  

