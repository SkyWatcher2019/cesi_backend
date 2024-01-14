from fastapi import APIRouter, Body, Depends
from sqlmodel import Session

from db import crud
from db.db import get_db
from db.models import Product, ProductCreate, ProductEdit, ProductRead, Sell

router = APIRouter(prefix='/products')


@router.get('/all', response_model=list[ProductRead])
async def get_all(db: Session = Depends(get_db)):
    return crud.get_all_products(db)


@router.get('/{id}', response_model=Product)
async def get_one(id: int, db: Session = Depends(get_db)):
    return crud.get_product(db, id)


@router.get('/{id}/sells', response_model=list[Sell])
async def get_sells(id: int, db: Session = Depends(get_db)):
    return crud.get_product_sells(db, id)


@router.post('/new', response_model=Product)
async def new(product: ProductCreate = Body(), db: Session = Depends(get_db)):
    return crud.create_product(db, product)


@router.put('/{id}', response_model=Product)
async def edit(id: int, product: ProductEdit, db: Session = Depends(get_db)):
    return crud.edit_product(db, id, product)


@router.delete('/{id}', response_model=Product)
async def delete(id: int, db: Session = Depends(get_db)):
    return crud.delete_product(db, id)
