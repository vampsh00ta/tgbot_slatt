from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from datetime import datetime
from db.models import Base
DATABASE = {
    'drivername': 'postgresql',
    'host': 'localhost',
    'port': '5432',
    'username': 'op1um',
    'password': '',
    'database': 'tgbot'
}
engine = create_engine(URL(**DATABASE),pool_pre_ping=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()



