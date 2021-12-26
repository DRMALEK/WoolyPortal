import datetime

from sqlalchemy import Column, String, Integer, Date
from database.base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column("name", String)
    brand = Column("brand", String)
    price = Column("price", String)  # In Euro
    composition = Column("composition", String)
    needle_size = Column("needle_size", String)  # In m.m
    deliver_time = Column("delivery_time", Date)
    creation_time = Column("creation_time", Date, default=datetime.datetime.utcnow())
    last_update = Column("last_update", Date, default=datetime.datetime.utcnow())


    def __init__(self, name, brand, price, composition, needle_size, deliver_time):
        self.name = name
        self.brand = brand
        self.price = price
        self.composition = composition
        self.needle_size = needle_size
        self.deliver_time = deliver_time
