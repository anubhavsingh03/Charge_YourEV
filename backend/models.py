from sqlalchemy import Column, Integer, String, Float
from database import Base

class Station(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False, index=True)
    address = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    connectors = Column(String, nullable=False)
    price = Column(Float, nullable=True)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=True)
