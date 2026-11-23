from sqlalchemy import String, Text, DateTime, ForeignKey, false
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from app.database.base import Base

if TYPE_CHECKING:
    from country import Country
    from businessmodel import BusinessModel
    from associations import opportunity_category
    from category import Category


class Opportunity(Base):

    __tablename__ = "opportunities"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    slug: Mapped[str] = mapped_column(
        String(220),
        unique=True,
        nullable=False
    )

    summary: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    problem: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    proposed_solution: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    target_market: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    revenue_model: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    operational_requirements: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    risks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    country_id: Mapped[int] = mapped_column(
        ForeignKey("countries.id"),
        nullable=False
    )

    business_model_id: Mapped[int] = mapped_column(
        ForeignKey("business_models.id"),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="draft",
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    country : Mapped['Country'] = relationship(back_populates='opportunities')

    business_model : Mapped['BusinessModel'] = relationship(back_populates='opportunities')

    categories : Mapped[list['Category']] = relationship(secondary='opportunity_categories', back_populates='opportunities')

    is_featured: Mapped[bool] = mapped_column(
    default=False,
    server_default=false()
)