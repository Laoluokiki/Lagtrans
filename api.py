from fastapi import FastAPI, Path, Depends 
from routes import passenger, driver , journey , vechicle, transaction
import models
from database import engine,SessionLocal
from sqlalchemy.orm import Session
 


app = FastAPI()
models.Base.metadata.create_all(bind=engine) #this creates all tables that has been defined in the models.py if they've not been created yet but if they've been created it updates the tables

  

@app.get("/")
def index():
    return {"message": "This is the api home page"}


app.include_router(passenger.app)
app.include_router(driver.app)
app.include_router(journey.app)
app.include_router(vechicle.app)
app.include_router(transaction.app)













      
