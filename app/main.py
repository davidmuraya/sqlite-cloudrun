from typing import List

from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from sqlmodel import Session
from starlette.middleware.base import BaseHTTPMiddleware

from app.config.events import on_shutdown, on_start_up
from app.logging.logging_config import setup_logging
from app.middleware.process_time_middleware import add_process_time_header
from app.schema.product_models import ProductCreate, ProductRead, ProductUpdate
from app.services.database.crud_product import (
    create_product,
    delete_product,
    get_product,
    get_products,
    update_product,
)
from app.services.database.database import get_db

setup_logging()

app = FastAPI(on_shutdown=[on_shutdown], on_startup=[on_start_up])


app.add_middleware(BaseHTTPMiddleware, dispatch=add_process_time_header)


@app.post("/products/", response_model=ProductRead)
async def create_product_endpoint(product: ProductCreate, db: Session = Depends(get_db)):
    result = await create_product(db, product)
    # Commit handled in route handler
    db.commit()
    db.refresh(result)
    return result


@app.get("/products/{product_id}", response_model=ProductRead)
async def read_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    result = await get_product(db, product_id)
    if not result:
        raise HTTPException(status_code=404, detail="Product not found")
    return result


@app.get("/products/", response_model=List[ProductRead])
async def read_products_endpoint(
    skip: int = Query(0, alias="skip", ge=0),
    limit: int = Query(100, alias="limit", ge=1),
    db: Session = Depends(get_db),
):
    return await get_products(db, skip=skip, limit=limit)


@app.patch("/products/{product_id}", response_model=ProductRead)
async def update_product_endpoint(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = await update_product(db, product_id, product)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.commit()
    db.refresh(db_product)
    return db_product


@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    deleted = await delete_product(db, product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
