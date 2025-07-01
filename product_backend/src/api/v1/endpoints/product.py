from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.schemas import product as product_schema
from src.crud import product as crud_product
from src.db.session import get_db

router = APIRouter()

@router.post("/", response_model=product_schema.ProductRead)
def create_product(product_in: product_schema.ProductCreate, db: Session = Depends(get_db)):
    return crud_product.create_product(db, product_in)

@router.get("/", response_model=List[product_schema.ProductRead])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud_product.get_products(db, skip=skip, limit=limit)
    return products

@router.get("/{product_id}", response_model=product_schema.ProductRead)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = crud_product.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

@router.get("/name/{product_name}", response_model=product_schema.ProductRead)
def read_product_by_name(product_name: str, db: Session = Depends(get_db)):
    product = crud_product.get_product_by_name(db, product_name)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

@router.put("/{product_name}", response_model=product_schema.ProductRead)
def update_product(product_name: str, product_in: product_schema.ProductUpdate, db: Session = Depends(get_db)
):
    updated_product = crud_product.update_product(db, product_name, product_in)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return updated_product


