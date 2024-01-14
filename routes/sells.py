from fastapi import APIRouter, Depends
from sqlmodel import Session

from db import crud
from db.db import get_db
from db.models import Sell, SellCreate, SellRead

router = APIRouter(prefix='/sells')


@router.get('/', response_model=list[SellRead])
async def get_all(db: Session = Depends(get_db)):
    return crud.get_all_sells(db)


@router.get('/{id}', response_model=SellRead)
async def get_one(id: int, db: Session = Depends(get_db)):
    return crud.get_sell(db, id)


@router.post('/new', response_model=Sell)
async def new(sell: SellCreate, db: Session = Depends(get_db)):
    return crud.create_sell(db, sell)
