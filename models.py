from sqlalchemy import Column, Integer, String, Float
from database import Base

class Passengers(Base): #this model passengers is declared to tell the DB to create table passenger with the below fields
   __tablename__ = "passengers"
   id = Column(Integer, primary_key=True, index=True)
   name = Column(String)
   phone_number  = Column(String)
   balance = Column(Float)
   email_address = Column(String)
   status = Column(String)

# create models for the rest of the tables
class Drivers(Base):
   __tablename__ = "drivers"
   id = Column(Integer, primary_key=True, index=True)
   name = Column(String)
   phone_number  = Column(String)
   email_address = Column(String)
   date_birth = Column(String)
   status = Column(String)

class Vechicles(Base):
   __tablename__ = "vechicles"
   id = Column(Integer, primary_key=True, index=True)
   plate_number = Column(String)
   colour = Column(String)
   make = Column(String)
   status = Column(String)

class Journeys(Base):
   __tablename__ = "journeys"
   id = Column(Integer, primary_key=True, index=True)
   vechicle_identification = Column(String)
   driver_identification = Column(Integer)
   starting_point = Column(String)
   ending_point = Column(String)
   fees = Column(Float)
   status = Column(String)

class Transactions(Base):
   __tablename__ = "transactions"
   id = Column(Integer, primary_key=True, index=True)
   passenger_identification= Column(Integer)
   amount = Column(Float)
   narration = Column(String)
   date= Column(String)
   
class  Journey_Passengers(Base):
   __tablename__ = "journey_passenger"
   id = Column(Integer, primary_key=True, index=True)
   journey_identification = Column(Integer)
   passenger_identification = Column(Integer)
   status= Column(String)