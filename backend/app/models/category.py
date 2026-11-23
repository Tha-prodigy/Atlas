from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from associations import opportunity_category
    from opportunity import Opportunity

class Category(Base):

    __tablename__ = 'categories'

    id : Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False
    )

    name : Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    slug : Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False

    )

    description : Mapped[str] = mapped_column(
        String(255),
        nullable=False

    )

    parent_id : Mapped[int| None] = mapped_column( ForeignKey('categories.id'),
        nullable=True
    )

    parent : Mapped['Category'] = relationship(back_populates='children', remote_side='Category.id')
    children : Mapped[list['Category']] = relationship(back_populates='parent')

    opportunities : Mapped[list['Opportunity']] = relationship(secondary='opportunity_categories', back_populates='categories')

