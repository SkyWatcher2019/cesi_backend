from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session

import utils
from db import crud
from db.db import get_db
from db.models import Product, Section

router = APIRouter(prefix='/reports')


class SellsResponse(BaseModel):
    top_section: Optional[Section] = None
    netop_section: Optional[Section] = None
    top_product: Optional[Product] = None


@router.get('/stock', response_model=dict[int, bool])
async def stock(db: Session = Depends(get_db)):
    db_products = crud.get_all_products(db)
    result = {}
    for product in db_products:
        result[product.id] = product.amount != 0

    return result


@router.get('/sells', response_model=SellsResponse)
async def sells(db: Session = Depends(get_db)):
    db_sells = crud.get_all_sells(db)
    section_sells: dict[int, float] = {}
    top_product = None
    top_price = 0
    for sell in db_sells:
        if sell.section_id in section_sells:
            section_sells[sell.section_id] += sell.price
        else:
            section_sells[sell.section_id] = sell.price
        if sell.price > top_price:
            top_price = sell.price
            top_product = sell.product

    sorted_sells = sorted(section_sells.items(), key=lambda item: item[1], reverse=True)

    top_section = utils.get(db_sells, id=sorted_sells[0][0]).section if sorted_sells else None
    netop_section = utils.get(db_sells, id=sorted_sells[-1][0]).section if sorted_sells else None

    return SellsResponse(
        top_section=top_section,
        netop_section=netop_section,
        top_product=top_product
    )
