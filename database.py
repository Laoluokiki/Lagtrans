from sqlalchemy import create_engine #create_engine is use to connect to database engine e.g sqllite,postgrees or mysql
from sqlalchemy.orm import sessionmaker # sessionmaker is used to manage DB sessions, every activity is a seesion e.g create,delete,update, etc
from sqlalchemy.ext.declarative import declarative_base # declarative_base is used to craete a mapping between our relational database tables to our python object 

DATABASE_URL = "sqlite:///./lagtransport.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread":False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
