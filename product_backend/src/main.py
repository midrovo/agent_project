from fastapi import FastAPI
from src.api.v1 import api_router
from src.db.base_class import Base
from src.db.session import engine

app = FastAPI(title="My Product API")

Base.metadata.create_all(bind=engine)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "API is running"}

