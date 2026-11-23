from sqlalchemy import String, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base
from datetime import datetime, timezone

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.country import Country
    from associations import business_business_model
    from businessmodel import BusinessModel
    

class Business(Base):

    __tablename__ = 'businesses'

    id : Mapped[int] = mapped_column(
        primary_key=True
    )

    name : Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False
    )

    slug : Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False

    )

    description : Mapped[str] = mapped_column(
        Text,
        nullable=False

    )

    website : Mapped[str | None] = mapped_column(
        String(255),
        nullable=True

    )

    headquarters_country_id : Mapped[int] = mapped_column(ForeignKey('countries.id'), nullable=False)

    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True),  default=lambda: datetime.now(timezone.utc))

    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True),  default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    headquarters_country : Mapped['Country']= relationship(
        back_populates='businesses'
    )


    business_models : Mapped[list['BusinessModel']]= relationship(secondary='business_business_models', back_populates='businesses')

