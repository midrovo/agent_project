from fastapi import APIRouter
from src.api.v1.endpoints import product, webhook

api_router = APIRouter()
api_router.include_router(product.router, prefix="/products", tags=["products"])
api_router.include_router(webhook.router)
