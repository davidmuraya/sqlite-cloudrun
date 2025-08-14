from typing import Optional

from sqlmodel import SQLModel


class ProductBase(SQLModel):
    name: str
    price: float
    description: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int


class ProductUpdate(SQLModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None


class ProductDelete(SQLModel):
    id: int
