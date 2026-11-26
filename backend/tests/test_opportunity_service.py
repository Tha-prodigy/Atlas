import pytest

from app.models import Country, BusinessModel, Opportunity
from app.services.opportunity import get_opportunity_by_slug


@pytest.mark.asyncio
async def test_get_opportunity_by_slug(db_session):
    # Arrange
    country = Country(name="Kenya", iso_code="KE")

    business_model = BusinessModel(
        name="Pay-as-you-go Solar Energy",
        slug="pay-as-you-go-solar-energy",
        summary="Providing affordable solar energy through flexible payments.",
        description="A business model that allows households and businesses to access solar energy systems through instalment-based payments."
    )

    db_session.add_all([country, business_model])
    await db_session.flush()

    opportunity = Opportunity(
        title="Affordable Solar Energy for Rural Households",
        slug="affordable-solar-energy-rural-households",
        summary="Making solar electricity accessible to rural households.",
        problem="Many rural households lack reliable access to electricity.",
        proposed_solution="Provide solar home systems through a pay-as-you-go payment model.",
        country_id=country.id,
        business_model_id=business_model.id
    )

    db_session.add(opportunity)
    await db_session.flush()

    # Act
    result = await get_opportunity_by_slug(
        db_session,
        slug="affordable-solar-energy-rural-households"
    )

    # Assert
    assert result is not None
    assert result.id == opportunity.id
    assert result.slug == opportunity.slug
    assert result.title == opportunity.title


@pytest.mark.asyncio
async def test_get_opportunity_by_slug_not_found(db_session):
    # Act
    result = await get_opportunity_by_slug(
        db_session,
        slug="nonexistent-opportunity"
    )

    # Assert
    assert result is None