from fastapi import HTTPException
from sqlmodel import SQLModel, Session

from db.models import Product, ProductCreate, ProductEdit, Section, SectionCreate, SectionEdit, Sell, SellCreate


def _update_attrs(db_model: SQLModel, model: SQLModel) -> SQLModel:
    data = model.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(db_model, key, value)
    return db_model


def get_all_products(session: Session) -> list[Product]:
    return session.query(Product).all()


def get_product(session: Session, id: int) -> Product:
    product = session.get(Product, id)
    if not product:
        raise HTTPException(status_code=404, detail=f'Продукт #{id} не найден!')
    return product


def get_product_sells(session: Session, id: int) -> list[Sell]:
    db_product = get_product(session, id)
    return db_product.sells


def create_product(session: Session, product: ProductCreate) -> Product:
    db_product = Product.model_validate(product)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


def edit_product(session: Session, id: int, product: ProductEdit) -> Product:
    db_product = _update_attrs(get_product(session, id), product)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


def delete_product(session: Session, id: int) -> Product:
    db_product = get_product(session, id)
    session.delete(db_product)
    session.commit()
    return db_product


def get_all_sections(session: Session) -> list[Section]:
    return session.query(Section).all()


def get_section(session: Session, id: int) -> Section:
    db_section = session.get(Section, id)
    if not db_section:
        raise HTTPException(status_code=404, detail=f'Отдел #{id} не найден')
    return db_section


def get_section_products(session: Session, id: int) -> list[Product]:
    db_section = get_section(session, id)
    return db_section.products


def get_section_sells(session: Session, id: int) -> list[Sell]:
    db_section = get_section(session, id)
    return db_section.sells


def create_section(session: Session, section: SectionCreate) -> Section:
    db_section = Section.model_validate(section)
    session.add(db_section)
    session.commit()
    session.refresh(db_section)
    return db_section


def edit_section(session: Session, id: int, section: SectionEdit) -> Section:
    db_section = _update_attrs(get_section(session, id), section)
    session.add(db_section)
    session.commit()
    return db_section


def delete_section(session: Session, id: int) -> Section:
    db_section = get_section(session, id)
    session.delete(db_section)
    session.commit()
    return db_section


def get_all_sells(session: Session) -> list[Sell]:
    return session.query(Sell).all()


def get_sell(session: Session, id: int) -> Sell:
    db_sell = session.get(Sell, id)
    if not db_sell:
        raise HTTPException(status_code=404, detail=f'Продажа #{id} не найдена')
    return db_sell


def create_sell(session: Session, sell: SellCreate) -> Sell:
    db_sell = Sell.model_validate(sell)
    db_product = get_product(session, db_sell.product_id)
    if db_product.amount < db_sell.amount:
        raise HTTPException(status_code=409, detail={'message': 'Недостаточно продукта', 'available': db_product.amount})
    db_sell.section_id = db_product.section_id
    db_sell.price = db_sell.amount * db_product.price
    session.add_all([db_sell, db_product])
    session.commit()
    session.refresh(db_sell)
    return db_sell
