
from fastapi import APIRouter,status, HTTPException
from fastapi import FastAPI, Path, Depends 
import models
from sqlalchemy.orm import Session
from helper.helper import get_db
import datetime


app = APIRouter(
    prefix="/api/v1"
)

@app.get("/transactions")
def get_all_transactions(db: Session = Depends(get_db)):
    return db.query(models.Transactions).all() # select everything from transactions model

def saveTransaction (pid:str, amount: float, narration: str, db):
    # create record of transaction
    trans_model = models.Transactions()
    trans_model.passenger_identification = pid
    trans_model.amount = amount
    trans_model.narration = narration
    trans_model.date = datetime.datetime.now()
    db.add(trans_model)
    db.commit()