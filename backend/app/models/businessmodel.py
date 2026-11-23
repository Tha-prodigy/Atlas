from sqlalchemy import String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from business import Business
    from associations import business_business_model
    from opportunity import Opportunity



class BusinessModel(Base):

    __tablename__ = 'business_models'

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

    summary : Mapped[str] = mapped_column(
        String(255),
        nullable=False
        
    )

    description : Mapped[str] = mapped_column(
        Text,
        nullable=False

    )

    revenue_model : Mapped[str | None] = mapped_column(
        Text,
        nullable= True

    )

    

    operational_requirements : Mapped[str| None] = mapped_column(
        Text,
        nullable=True
    )

    created_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)

    )

    updated_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc)

    )

    businesses : Mapped[list['Business']]= relationship(secondary='business_business_models', back_populates='business_models')
    
    opportunities : Mapped[list['Opportunity']] = relationship(back_populates='business_model')