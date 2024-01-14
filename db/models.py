from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class ProductBase(SQLModel):
    name: str = Field(index=True, unique=True, nullable=False)
    variety: str = Field(index=True, nullable=False)
    price: float = Field(nullable=False)
    amount: int = Field(default=0)


class ProductCreate(ProductBase):
    section_id: int


class ProductEdit(ProductCreate):
    pass


class Product(ProductBase, table=True):
    __tablename__ = 'products'

    id: Optional[int] = Field(primary_key=True, unique=True, default=None)

    section: 'Section' = Relationship(back_populates='products')
    section_id: int = Field(foreign_key='sections.id')

    sells: list['Sell'] = Relationship(back_populates='product')


class SectionBase(SQLModel):
    name: str = Field(index=True, unique=True, nullable=False)
    description: Optional[str] = Field(index=True, nullable=True)


class SectionCreate(SectionBase):
    pass


class SectionEdit(SectionBase):
    pass


class Section(SectionBase, table=True):
    __tablename__ = 'sections'

    id: Optional[int] = Field(primary_key=True, unique=True, default=None)
    products: list[Product] = Relationship(back_populates='section')
    sells: list['Sell'] = Relationship(back_populates='section')


class SellBase(SQLModel):
    product_id: int = Field(foreign_key='products.id', nullable=True, default=-1, index=True)
    amount: int = Field(nullable=False)


class SellCreate(SellBase):
    pass


class Sell(SellBase, table=True):
    __tablename__ = 'sells'

    id: Optional[int] = Field(primary_key=True, unique=True, default=None)
    price: Optional[float] = Field(default=None)
    date: datetime = Field(default_factory=datetime.now)

    section_id: int = Field(foreign_key='sections.id', nullable=True, default=-1, index=True)

    product: Product = Relationship(back_populates='sells')
    section: Section = Relationship(back_populates='sells')


class ProductRead(ProductBase):
    id: int
    section: Section


class SectionRead(SectionBase):
    id: int
    products: list[Product] = []
    sells: list[Sell] = []


class SellRead(SellBase):
    id: int
    product: Optional[Product] = None
    section: Optional[Section] = None
