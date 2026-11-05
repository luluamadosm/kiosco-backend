import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

router = APIRouter(prefix="/api/orders", tags=["orders"])


def to_order_out(order: models.Order) -> schemas.OrderOut:
    return schemas.OrderOut(
        id=order.id,
        created_at=order.created_at,
        total=order.total,
        items=json.loads(order.items_json),
    )


@router.post("", response_model=schemas.OrderOut, status_code=201)
def create_order(data: schemas.OrderCreate, db: Session = Depends(get_db)):
    items = []
    total = 0.0

    for item in data.items:
        product = db.get(models.Product, item.product_id)
        if product is None:
            db.rollback()
            raise HTTPException(status_code=404, detail=f"No existe el producto {item.product_id}")
        if product.stock < item.quantity:
            detail = f"Stock insuficiente para {product.name} (quedan {product.stock})"
            db.rollback()
            raise HTTPException(status_code=400, detail=detail)

        product.stock -= item.quantity
        subtotal = product.price * item.quantity
        total += subtotal
        items.append(
            {
                "product_id": product.id,
                "name": product.name,
                "price": product.price,
                "quantity": item.quantity,
                "subtotal": subtotal,
            }
        )

    order = models.Order(total=total, items_json=json.dumps(items))
    db.add(order)
    db.commit()
    db.refresh(order)
    return to_order_out(order)


@router.get("", response_model=list[schemas.OrderOut])
def get_orders(db: Session = Depends(get_db)):
    orders = db.scalars(select(models.Order)).all()
    return [to_order_out(order) for order in orders]
