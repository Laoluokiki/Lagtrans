
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from fastapi import APIRouter,status, HTTPException
from fastapi import FastAPI, Path, Depends 
from helper.helper import get_db
from sqlalchemy.orm import Session
import models
from schema import Vechicle, UpdateVechicles


app = APIRouter(
    prefix="/api/v1"
)


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
