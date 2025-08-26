from typing import List, Optional

from sqlmodel import Session, select

from app.schema.product_models import ProductCreate, ProductUpdate
from app.services.database.models import Product


async def create_product(session: Session, product_create: ProductCreate) -> Product:
    product = Product.model_validate(product_create)
    session.add(product)
    return product


async def get_product(session: Session, product_id: int) -> Optional[Product]:
    statement = select(Product).where(Product.id == product_id)
    result = session.exec(statement)
    return result.first()


async def get_products(session: Session, skip: int = 0, limit: int = 100) -> List[Product]:
    statement = select(Product).offset(skip).limit(limit)
    result = session.exec(statement)
    return result.all()


async def update_product(session: Session, product_id: int, product_update: ProductUpdate) -> Optional[Product]:
    product = await get_product(session, product_id)
    if not product:
        return None
    update_data = product_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)
    session.add(product)
    return product


async def delete_product(session: Session, product_id: int) -> bool:
    product = await get_product(session, product_id)
    if not product:
        return False
    session.delete(product)
    return True
