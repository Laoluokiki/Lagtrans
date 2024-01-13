from database import engine,SessionLocal


def get_db():
    try: #we use try method to connect to DB so it can catch any error,if there one during connection to DB, so that error wont break the entire code,try method can be used for any other operation we are not sure of.
        db = SessionLocal()
        yield db
    finally:
        db.close()  