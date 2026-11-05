from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Category = Literal["bebidas", "snacks", "golosinas", "varios"]


class ProductBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1)
    category: Category
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    description: str | None = None


class ProductCreate(ProductBase):
    pass


class ProductOut(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class OrderItemIn(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class OrderCreate(BaseModel):
    items: list[OrderItemIn] = Field(min_length=1)


class OrderItemOut(BaseModel):
    product_id: int
    name: str
    price: float
    quantity: int
    subtotal: float


class OrderOut(BaseModel):
    id: int
    created_at: datetime
    total: float
    items: list[OrderItemOut]
