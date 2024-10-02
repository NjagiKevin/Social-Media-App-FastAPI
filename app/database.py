from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Defines the URL for connecting to the PostgreSQL database using SQLAlchemy.
SQLALCHEMY_DATABASE_URL='postgresql://postgres:Tahani#21#@localhost/fastapi'

# engine is responsible for managing the connection to the database
engine=create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal is a factory for creating new session instances.
SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the base class for all models in SQLAlchemy. All models will inherit from this.
Base=declarative_base()

# A generator function that provides a session to interact with the database and ensures it is closed after the request is processed.
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()