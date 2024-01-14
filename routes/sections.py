from fastapi import APIRouter, Depends
from sqlmodel import Session

from db import crud
from db.db import get_db
from db.models import Product, ProductRead, Section, SectionCreate, SectionEdit, SectionRead, Sell

router = APIRouter(prefix='/sections')


@router.get('/all', response_model=list[SectionRead])
async def get_all(db: Session = Depends(get_db)):
    return crud.get_all_sections(db)


@router.get('/{id}', response_model=SectionRead)
async def get_one(id: int, db: Session = Depends(get_db)):
    return crud.get_section(db, id)


@router.get('/{id}/products', response_model=list[ProductRead])
async def get_products(id: int, db: Session = Depends(get_db)):
    return crud.get_section_products(db, id)


@router.get('/{id}/sells', response_model=list[Sell])
async def get_sells(id: int, db: Session = Depends(get_db)):
    return crud.get_section_sells(db, id)


@router.post('/new', response_model=Section)
async def new(section: SectionCreate, db: Session = Depends(get_db)):
    return crud.create_section(db, section)


@router.put('/{id}', response_model=Section)
async def edit(id: int, section: SectionEdit, db: Session = Depends(get_db)):
    return crud.edit_section(db, id, section)


@router.delete('/{id}', response_model=Section)
async def delete(id: int, db: Session = Depends(get_db)):
    return crud.delete_section(db, id)
