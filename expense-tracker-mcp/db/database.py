from sqlalchemy import create_engine, engine
from sqlalchemy.orm import sessionmaker
from db.model import Base



engine=create_engine("sqlite:///expense_tracker.db")
Session=sessionmaker(bind=engine)



def init_db(): 
    Base.metadata.create_all(engine)

def get_session():
    return Session()
