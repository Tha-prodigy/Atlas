import pytest

from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.api.v1.opportunities import router
from app.database.connection import get_db
from app.models import Country, BusinessModel, Opportunity


def create_test_app(db_session):
    app = FastAPI()
    app.include_router(router)

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    return app


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

    app = create_test_app(db_session)

    # Act
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.get(
            "/opportunities/affordable-solar-energy-rural-households"
        )

    # Assert
    assert response.status_code == 200

    data = response.json()

    assert data["id"] == opportunity.id
    assert data["title"] == opportunity.title
    assert data["slug"] == opportunity.slug


@pytest.mark.asyncio
async def test_get_opportunity_by_slug_not_found(db_session):
    # Arrange
    app = create_test_app(db_session)

    # Act
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.get(
            "/opportunities/nonexistent-opportunity"
        )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Opportunity not found"}