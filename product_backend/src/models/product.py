from sqlalchemy import Column, Integer, String, Float
from src.db.base_class import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, nullable=False)
    image = Column(String(255), nullable=True)
    description = Column(String(255), index=True, nullable=False)
    stock = Column(Float, index=True, nullable=False)
    list_price = Column(Float, index=True, nullable=False)
    standard_price = Column(Float, index=True, nullable=False)
    discount = Column(Float, index=True, nullable=True)
