from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , declarative_base

from src.core.config import CONFIG

# tbh I chose sqlite just for simplicity but it's not recommended to use it in prod 

# the db URL
SQLALCHEMY_DATABASE_URL = CONFIG['DATABASE_URL']

# let's create the Engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

#the Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base class
base = declarative_base()

