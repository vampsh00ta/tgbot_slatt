from sqlalchemy import Integer,String,Column,Boolean,Date,MetaData,Table
from sqlalchemy.orm import declarative_base,mapper,relationship,sessionmaker
from sqlalchemy import create_engine

engine =  create_engine("postgresql://op1um:@localhost/tgbot")
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True)
    username  = Column(String(30))
    fullname = Column(String(30))
    payment = Column(Boolean(30))
    date  = Column(Date)

Base.metadata.creata_all(engine)