
from pydantic import BaseModel, Field, EmailStr
from fastapi import APIRouter,status, HTTPException
from fastapi import FastAPI, Path, Depends 
from helper.helper import get_db
from sqlalchemy.orm import Session
import models
from schema import Journey, Journey_Passenger
from .transaction import saveTransaction

app = APIRouter(
    prefix="/api/v1"
)


@app.post("/create-journeys")
def create_journeys(journey : Journey, db: Session = Depends(get_db)):    
    driver_model = db.query(models.Drivers).filter(models.Drivers.id == journey.driver_identification).first() 
    if driver_model is None:
      return {"message": "driver does not exit",}
    if driver_model.status == "engaged":
      return {"message": "driver is not available"}

    vechicle_model =  db.query(models.Vechicles).filter(models.Vechicles.id == journey.vechicle_identification).first() 
    if vechicle_model is None:
        return {"message": "vechicle does not exit", "code":"404"}
    if vechicle_model.status == "engaged":
        return {"message": "vechicle is not available"}
    
    journey_model = models.Journeys()
    journey_model.vechicle_identification= journey.vechicle_identification
    journey_model.driver_identification = journey.driver_identification
    journey_model.starting_point = journey.starting_point
    journey_model.ending_point = journey.ending_point
    journey_model.fees= journey.fees
    journey_model.status = journey.status
    db.add(journey_model)
    driver_model.status = "engaged"
    vechicle_model.status = "engaged"
    db.add(driver_model)
    db.add(vechicle_model)
    db.commit()


    return journey

@app.get("/journeys")
def get_all_journeys(db: Session = Depends(get_db)):
    return db.query(models.Journeys).all()  



@app.post("/create_journey_passenger")
def create_journey_passenger(journey_passenger: Journey_Passenger, db: Session = Depends(get_db)):
    
    journey_model = db.query(models.Journeys).filter(models.Journeys.id == journey_passenger.journey_identification).first() 
    if journey_model is None:
        return {"message": "journey does not exist", "code":"404"}
    if journey_model.status == "engaged":
        return  {"message": "journey is not available", "code":"404"}

    passenger_model =  db.query(models.Passengers).filter(models.Passengers.id == journey_passenger.passenger_identification).first() 
    if passenger_model is None:
       return {"message": "passenger does not exit",}
    if passenger_model.status == "onboard":
       return {"message": "passenger is already on a journey"}
    if (passenger_model.balance - journey_model.fees) < 0:
      return {"message": "insuffiecient fund to complete the journey"}  

    # update passenger balance
    passenger_model.balance = (passenger_model.balance - journey_model.fees)
    db.add(passenger_model)

    
    # create record of transaction
    naration = "onbaord journey from "+ journey_model.starting_point +" to " + journey_model.ending_point
    saveTransaction(passenger_model.id,journey_model.fees,naration,db)

    # on baord pessenger
    journey_passenger_model = models.Journey_Passengers()    
    journey_passenger_model.journey_identification = journey_passenger.journey_identification
    journey_passenger_model.passenger_identification = journey_passenger.passenger_identification
    journey_passenger_model.status = journey_passenger.status    
    db.add(journey_passenger_model)
    passenger_model.status = "onboard"
    db.add(passenger_model)
    db.commit()

    return journey_passenger

@app.get("/journey_passenger_model/{journey_id}")
def journey_passenger_list(journey_id: int = Path(description= "The List 0f the Passenger in a journey", gt=0, le=10),db: Session = Depends(get_db)):
    journey_passenger_model =  db.query(models.Journey_Passengers).filter(models.Journey_Passengers.journey_identification == journey_id).all() # select everything from passanger model, but return only record where pasenger id = to passenger id collect from user  
    
    if journey_passenger_model is None:
        return {"message": "There is no Passenger on the journey yet", "code":"404"}
    
    return journey_passenger_model    
