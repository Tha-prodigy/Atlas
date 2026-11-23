from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from app.database.base import Base

if TYPE_CHECKING:
    from business import Business
    from opportunity import Opportunity



class Country(Base):

    __tablename__ = 'countries'

    id : Mapped[int] = mapped_column(primary_key=True)

    name : Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
        
    )

    iso_code : Mapped[str] = mapped_column(
        String(2),
        unique=True,
        nullable=False
    )

    businesses : Mapped[list["Business"]]= relationship(back_populates='headquarters_country')
    
    opportunities: Mapped[list["Opportunity"]] = relationship(
    back_populates="country"
)
    