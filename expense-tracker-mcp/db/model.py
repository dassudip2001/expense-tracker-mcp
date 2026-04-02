from sqlalchemy import Column, Integer, Float, String, Date, DateTime
from datetime import datetime
from sqlalchemy.orm import declarative_base

Base=declarative_base()


class Expense(Base):
    __tablename__="expenses"


    id=Column(Integer, primary_key=True, index=True)
    amount=Column(Float, nullable=False)
    category=Column(String, nullable=False)
    description=Column(String, nullable=False)
    date=Column(Date, nullable=False)
    created_at=Column(DateTime, default=datetime.now)
    updated_at=Column(DateTime, default=datetime.now, onupdate=datetime.now)

class Budget(Base):
    __tablename__="budgets"

    id       = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False)
    amount   = Column(Float, nullable=False)
    month    = Column(Integer, nullable=False)
    year     = Column(Integer, nullable=False)