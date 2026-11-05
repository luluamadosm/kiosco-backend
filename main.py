from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, select

import models
import schemas
from database import Base, SessionLocal, engine
from routers import orders, products

INITIAL_PRODUCTS = [
    {"name": "Coca-Cola 500ml", "category": "bebidas", "price": 1200, "stock": 25, "description": "Gaseosa clásica"},
    {"name": "Agua mineral 500ml", "category": "bebidas", "price": 800, "stock": 40, "description": "Agua sin gas"},
    {"name": "Papas Lays Clásicas", "category": "snacks", "price": 1500, "stock": 30, "description": "Papas fritas clásicas"},
    {"name": "Alfajor Jorgito", "category": "golosinas", "price": 900, "stock": 50, "description": "Alfajor de chocolate"},
    {"name": "Chicles Beldent", "category": "golosinas", "price": 600, "stock": 60, "description": "Pack de chicles"},
    {"name": "Cigarrillos", "category": "varios", "price": 2500, "stock": 20, "description": "Atado de cigarrillos"},
    {"name": "Gatorade 500ml", "category": "bebidas", "price": 1800, "stock": 15, "description": "Bebida isotónica"},
    {"name": "Maní salado", "category": "snacks", "price": 1100, "stock": 35, "description": "Maní tostado con sal"},
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        if db.scalar(select(func.count()).select_from(models.Product)) == 0:
            for data in INITIAL_PRODUCTS:
                product = schemas.ProductCreate(**data)
                db.add(models.Product(**product.model_dump()))
            db.commit()
    yield


app = FastAPI(title="Kiosco El Rápido API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)
app.include_router(orders.router)
