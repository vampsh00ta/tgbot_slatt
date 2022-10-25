from sqlalchemy.orm import declarative_base,relationship
from sqlalchemy import Column, Integer, String,DateTime,JSON,ForeignKey,Table



Base  = declarative_base()

association_table = Table(
    "association",
    Base.metadata,
    Column("items", ForeignKey("items.id"), primary_key=True),
    Column("order_items", ForeignKey("order_items.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    balance = Column(Integer)
    discount = Column(Integer)
    orders = relationship("Orders")
    fullname = Column(String)
    username = Column(String)
    date = Column(DateTime)

class Items(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    price = Column(String)
    amount = Column(String)
    name = Column(String)

class Orders(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    user_id =  Column(Integer, ForeignKey("users.id"))

    orders_items = relationship("Orders_items")
class Orders_items(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True)
    order_id =  Column(Integer, ForeignKey("orders.id"))
    quantity = Column(Integer)
    item_id = Column(Integer, ForeignKey("items.id"))
    items = relationship("Items")
















