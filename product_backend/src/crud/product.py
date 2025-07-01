# src/crud/product.py
from sqlalchemy.orm import Session
from src.models.product import Product
from src.schemas import product as product_schema

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def get_product_by_name(db: Session, product_name: str):
    return db.query(Product).filter(Product.name.ilike(f"%{product_name}%")).first()

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()

def create_product(db: Session, product_in: product_schema.ProductCreate):
    db_product = Product(**product_in.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_name: str, product_in: product_schema.ProductUpdate):
    product = get_product_by_name(db, product_name)
    if not product:
        return None

    # Actualizar campos
    product.name=  product_in.name
    product.description = product_in.description
    product.stock = product_in.stock
    product.list_price = product_in.list_price
    product.standard_price = product_in.standard_price
    product.discount = product_in.discount

    if product_in.image is not None:
        product.image = product_in.image

    db.commit()
    db.refresh(product)
    return product

