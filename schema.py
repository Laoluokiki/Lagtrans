from pydantic import BaseModel, Field, EmailStr
from typing import Optional



class Journey(BaseModel): 
    vechicle_identification  : str = Field(min_lenghts=3)
    driver_identification : int = Field(min_lenghts=10)
    starting_point : str = Field(min_lenghts=9)
    ending_point: str = Field(min_lenghts=6) 
    fees : float = Field(min_lenghts=6) 
    status : str = Field(min_lenghts=6)

class Journey_Passenger(BaseModel):
    journey_identification : str = Field(min_lenghts=3)
    passenger_identification :str = Field(min_lenghts=3)
    status :str = Field(min_lenghts=3)


class Driver(BaseModel): 
    name : str = Field(min_lenghts=3)
    phone_number : str = Field(min_lenghts=10)
    email_address : str = Field(min_lenghts=9)
    date_birth : str = Field(min_lenghts=6) 
    status : str = Field(min_lenghts=6)



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