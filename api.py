from fastapi import FastAPI, Path, Depends 
from typing import Optional
from pydantic import BaseModel, Field, EmailStr
import models
from database import engine,SessionLocal
from sqlalchemy.orm import Session
import datetime

app = FastAPI()
models.Base.metadata.create_all(bind=engine) #this creates all tables that has been defined in the models.py if they've not been created yet but if they've been created it updates the tables

def get_db():
    try: #we use try method to connect to DB so it can catch any error,if there one during connection to DB, so that error wont break the entire code,try method can be used for any other operation we are not sure of.
        db = SessionLocal()
        yield db
    finally:
        db.close()    


passengers ={
    1:{
        "name" : "Akintunde",
        "phone_number" : "08151000091",
        "balance":1000,
        "email_address" : "akintunde@gmail.com"
    },
    2:{
        "name" : "Olaoluwa",
        "phone_number" : "08082288420",
        "balance":1000,
        "email_address" : "olaoluwa@gmail.com"

    }, 
    3:{
        "name" : "Adediwura",
        "phone_number" : "08082288421",
        "balance":10000,
        "email_address" : "akin@gmail.com"

    }
}

class Passenger(BaseModel): #this passenger model is created to define the request body from the user of the api 
    name : str = Field(min_lenghts=3)
    phone_number : str = Field(min_lenghts=10, max_lenghts=13)
    balance: float = Field(ge=1000)
    email_address : EmailStr
    status : str = Field(min_lenghts=3)


class UpdatePassenger(BaseModel):
    name : Optional[str] = None
    phone_number : Optional[str] = None
    balance: Optional[float] = None
    email_address : Optional[str] = None
    status : Optional[str] = None

@app.get("/")
def index():
    return {"message": "This is the api home page"}

#@app.get("/journeys")
#def get_all_journeys():
 #   return {"message": "this will return all journeys", "code":"200"}

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

    # for passenger_id in passengers:
    #     if passengers[passenger_id]["name"]==name:
    #        return passengers[passenger_id] 

    # return {"message": "passenger not found"}  


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
        # if passenger_id in passengers:
        #     return {"Error": "passenger exists"}
        # passengers[passenger_id] = passenger    
    passenger_model = models.Passengers()
    passenger_model.name =  passenger.name
    passenger_model.phone_number  = passenger.phone_number
    passenger_model.balance = passenger.balance
    passenger_model.email_address = passenger.email_address
    passenger_model.status = passenger.status
    db.add(passenger_model)
    db.commit()

    # create record of transaction
    trans_model = models.Transactions()
    trans_model.passenger_identification = passenger_model.id
    trans_model.amount = passenger.balance
    trans_model.narration = "opening balance"
    trans_model.date = datetime.datetime.now()
    db.add(trans_model)
    db.commit()

    return passenger

@app.get("/transactions")
def get_all_transactions(db: Session = Depends(get_db)):
    return db.query(models.Transactions).all() # select everything from transactions model

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

vechicles = {}

class Vechicle(BaseModel): #this passenger model is created to define the request body from the user of the api 
    plate_number : str = Field(min_lenghts=3)
    colour : str = Field(min_lenghts=10)
    make : str = Field(min_lenghts=9)
    status : str = Field(min_lenghts=6)    

class UpdateVechicles(BaseModel):
    plate_number : Optional[str] = None
    colour : Optional[str] = None
    make : Optional[str] = None
    status : Optional[str] = None

@app.get("/vechicles")
def get_all_vechicles(db: Session = Depends(get_db)):
    return db.query(models.Vechicles).all()


@app.post("/create-vechicles")
def create_vechicles(vechicle : Vechicle, db: Session = Depends(get_db)):    
           
    vechicle_model = models.Vechicles()
    vechicle_model.plate_number=  vechicle.plate_number
    vechicle_model.colour  = vechicle.colour
    vechicle_model.make = vechicle.make
    vechicle_model.status = vechicle.status
    db.add(vechicle_model)
    db.commit()

    return vechicle


@app.put("/update-vechicles/{vechicle_id}")
def update_vechicles(vechicle_id :int, vechicle : UpdateVechicles, db: Session = Depends(get_db)):    
    vechicle_model =  db.query(models.Vechicles).filter(models.Vechicles.id == vechicle_id).first() 
    
    if vechicle_model is None:
        return {"message": "vechicle does not exit", "code":"404"}
    
    if vechicle.plate_number != None:       
       vechicle_model.plate_number=  vechicle.plate_number

    if vechicle.colour != None:       
       vechicle_model.colour  = vechicle.colour  

    if vechicle.make != None:
        vechicle_model.make = vechicle.make

    if vechicle.status != None:
        vechicle_model.status = vechicle.status    

    db.add(vechicle_model)
    db.commit()
         
    return vechicle 

class Driver(BaseModel): 
    name : str = Field(min_lenghts=3)
    phone_number : str = Field(min_lenghts=10)
    email_address : str = Field(min_lenghts=9)
    date_birth : str = Field(min_lenghts=6) 
    status : str = Field(min_lenghts=6)
    

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

#ceating journey
class Journey(BaseModel): 
    vechicle_identification  : str = Field(min_lenghts=3)
    driver_identification : int = Field(min_lenghts=10)
    starting_point : str = Field(min_lenghts=9)
    ending_point: str = Field(min_lenghts=6) 
    fees : float = Field(min_lenghts=6) 
    status : str = Field(min_lenghts=6)

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


class Journey_Passenger(BaseModel):
    journey_identification : str = Field(min_lenghts=3)
    passenger_identification :str = Field(min_lenghts=3)
    status :str = Field(min_lenghts=3)

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
    trans_model = models.Transactions()
    trans_model.passenger_identification = passenger_model.id
    trans_model.amount = journey_model.fees
    trans_model.narration = "onbaord journey from "+ journey_model.starting_point +" to " + journey_model.ending_point
    trans_model.date = datetime.datetime.now()
    db.add(trans_model)

    

    

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

@app.get("/journey_passenger_transaction/{passenger_id}")
def journey_passenger_transaction_list(passenger_id: int = Path(description= "The List 0f the Passenger transaction on a journey", gt=0, le=10),db: Session = Depends(get_db)):
    journey_passenger_transaction =  db.query(models.Transactions).filter(models.Transactions.passenger_identification == passenger_id).all() # select everything from passanger model, but return only record where pasenger id = to passenger id collect from user  
    
    if journey_passenger_transaction is None:
        return {"message": "Transaction history doe not exit", "code":"404"}
    
    return journey_passenger_transaction        
