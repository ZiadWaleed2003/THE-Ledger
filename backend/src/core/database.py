from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , declarative_base
import os



# tbh I chose sqlite just for simplicity but it's not recommended to use it in prod 


def get_engine():

    # the DB URI (ik normally this should be stored in the .env file along with the pass and username)
    # but since I'm already using sqlite it doesn't really matter... however this should be done with any other DB
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'db', 'assets.db')}"

    # let's create the Engine
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

    return engine

engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    
    # the Session Factory to interact with the db
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


Base = declarative_base()
def get_db_base():
    # return the shared Singleton Base
    return Base

