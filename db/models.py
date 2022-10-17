from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String,DateTime,JSON




Base  = declarative_base()
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    balance = Column(Integer)
    discount = Column(Integer)


    fullname = Column(String)
    username = Column(String)
    date = Column(DateTime)
    orders = Column(JSON)
class Items(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    price = Column(String)
    amount = Column(String)
    name = Column(String)