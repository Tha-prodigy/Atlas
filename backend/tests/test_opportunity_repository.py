import pytest

from app.models.country import Country
from app.models.businessmodel import BusinessModel
from app.models.opportunity import Opportunity
from app.repositories.opportunity import (get_by_slug, 
                                          get_by_id, 
                                          get_all, search_opportunities)


@pytest.mark.asyncio
async def test_get_by_slug_returns_opportunity(db_session):

    country = Country(
        name="Nigeria",
        iso_code="NG"
    )

    business_model = BusinessModel(
        name="Cold Storage as a Service",
        slug="cold-storage-as-a-service",
        summary="Providing cold storage facilities on demand.",
        description="A business model that provides businesses with access to refrigerated storage."
    )

    db_session.add_all([country, business_model])

    await db_session.flush()

    opportunity = Opportunity(
        title="Solar-powered Cold Storage",
        slug="solar-powered-cold-storage",
        summary="Solar-powered cold storage for farmers.",
        problem="Farmers lose produce due to inadequate storage.",
        proposed_solution="Provide solar-powered cold storage facilities.",
        country_id=country.id,
        business_model_id=business_model.id
    )

    db_session.add(opportunity)

    await db_session.flush()

    result = await get_by_slug(
        db_session,
        "solar-powered-cold-storage"
    )

    assert result is not None
    assert result.id == opportunity.id
    assert result.title == "Solar-powered Cold Storage"
    assert result.slug == "solar-powered-cold-storage"

@pytest.mark.asyncio
async def test_get_by_slug_returns_none_when_not_found(db_session):

    result = await get_by_slug(
        db_session,
        "non-existent-opportunity"
    )

    assert result is None


@pytest.mark.asyncio
async def test_get_by_id_returns_opportunity(db_session):
    business_model = BusinessModel(
            name="Cold Storage as a Service",
            slug="cold-storage-as-a-service",
            summary="Providing cold storage facilities on demand.",
            description="A business model that provides businesses with access to refrigerated storage."
        )


    country = Country(
        name="Nigeria",
        iso_code="NG"
    )

    db_session.add_all([country, business_model])

    await db_session.flush()

    opportunity = Opportunity(
        title="Solar-powered Cold Storage",
        slug="solar-powered-cold-storage",
        summary="Solar-powered cold storage for farmers.",
        problem="Farmers lose produce due to inadequate storage.",
        proposed_solution="Provide solar-powered cold storage facilities.",
        country_id=country.id,
        business_model_id=business_model.id
    )

    db_session.add(opportunity)

    await db_session.flush()

    result = await get_by_id(db_session, opportunity.id)

    assert result is not None
    assert result.id == opportunity.id
    assert result.title == "Solar-powered Cold Storage"
    assert result.slug == "solar-powered-cold-storage"



@pytest.mark.asyncio
async def test_get_all_opportunities(db_session):
    business_model = BusinessModel(
            name="Cold Storage as a Service",
            slug="cold-storage-as-a-service",
            summary="Providing cold storage facilities on demand.",
            description="A business model that provides businesses with access to refrigerated storage."
        )


    country = Country(
        name="Nigeria",
        iso_code="NG"
    )

    db_session.add_all([country, business_model])

    await db_session.flush()

    opportunity = Opportunity(
        title="Solar-powered Cold Storage",
        slug="solar-powered-cold-storage",
        summary="Solar-powered cold storage for farmers.",
        problem="Farmers lose produce due to inadequate storage.",
        proposed_solution="Provide solar-powered cold storage facilities.",
        country_id=country.id,
        business_model_id=business_model.id
    )

    db_session.add(opportunity)

    await db_session.flush()

    business_model1 = BusinessModel(
        name="Laundry delivery Service",
        slug="laundry-delivery-service",
        summary="Providing laundry services to people in urban settlements",
        description="A business model that provides laundry services to busy people residing in urban settlements"
    )

    country1 = Country(
        name="South Africa",
        iso_code="SA"
    )

    db_session.add_all([country1, business_model1])
    await db_session.flush()

    opportunity1 = Opportunity(
        title="Laundry delivery service",
        slug="laundry-delivery-service",
        summary="Seamless laundry delivery service for busy urban workers",
        problem="Urban workers usually have a tight and busy schedule and as a result find it difficult to do their laundry",
        proposed_solution="Provide complete laundry service channels",
        country_id=country1.id,
        business_model_id=business_model1.id
    )

    db_session.add(opportunity1)
    await db_session.flush()

    business_model2 = BusinessModel(
    name="Pay-as-you-go Solar Energy",
    slug="pay-as-you-go-solar-energy",
    summary="Providing affordable solar energy through flexible payments.",
    description="A business model that allows households and businesses to access solar energy systems through instalment-based payments."
)

    country2 = Country(
        name="Kenya",
        iso_code="KE"
    )

    db_session.add_all([country2, business_model2])
    await db_session.flush()

    opportunity2 = Opportunity(
        title="Affordable Solar Energy for Rural Households",
        slug="affordable-solar-energy-rural-households",
        summary="Making solar electricity accessible to rural households.",
        problem="Many rural households lack reliable access to electricity.",
        proposed_solution="Provide solar home systems through a pay-as-you-go payment model.",
        country_id=country2.id,
        business_model_id=business_model2.id
    )

    db_session.add(opportunity2)
    await db_session.flush()



    result = await get_all(db_session, 1, 2)
    result1 = await get_all(db_session, 2, 2)


    assert len(result) == 2
    assert len(result1) == 1


    result_ids = {item.id for item in result}

    assert result_ids == {opportunity.id, opportunity1.id}
    assert result1[0].id not in result_ids


@pytest.mark.asyncio
async def test_search_opportunities_by_title(db_session):
    business_model = BusinessModel(
            name="Cold Storage as a Service",
            slug="cold-storage-as-a-service",
            summary="Providing cold storage facilities on demand.",
            description="A business model that provides businesses with access to refrigerated storage."
        )


    country = Country(
        name="Nigeria",
        iso_code="NG"
    )

    db_session.add_all([country, business_model])

    await db_session.flush()

    opportunity = Opportunity(
        title="Solar-powered Cold Storage",
        slug="solar-powered-cold-storage",
        summary="Solar-powered cold storage for farmers.",
        problem="Farmers lose produce due to inadequate storage.",
        proposed_solution="Provide solar-powered cold storage facilities.",
        country_id=country.id,
        business_model_id=business_model.id
    )

    db_session.add(opportunity)

    await db_session.flush()
    result = await search_opportunities(
        db_session,
        search="Solar-powered"
    )

    result1 = await search_opportunities(
    db_session,
    search="SOLAR-POWERED COLD STORAGE"
    )

    # Assert
    assert len(result) == 1
    assert result[0].id == opportunity.id

    assert len(result1) == 1
    assert result1[0].id == opportunity.id


@pytest.mark.asyncio
async def test_search_opportunities_by_summary(db_session):

    business_model2 = BusinessModel(
        name="Pay-as-you-go Solar Energy",
        slug="pay-as-you-go-solar-energy",
        summary="Providing affordable solar energy through flexible payments.",
        description="A business model that allows households and businesses to access solar energy systems through instalment-based payments."
    )

    country2 = Country(
        name="Kenya",
        iso_code="KE"
    )

    db_session.add_all([country2, business_model2])
    await db_session.flush()

    opportunity2 = Opportunity(
        title="Affordable Solar Energy for Rural Households",
        slug="affordable-solar-energy-rural-households",
        summary="Making solar electricity accessible to rural households.",
        problem="Many rural households lack reliable access to electricity.",
        proposed_solution="Provide solar home systems through a pay-as-you-go payment model.",
        country_id=country2.id,
        business_model_id=business_model2.id
    )

    db_session.add(opportunity2)
    await db_session.flush()

    
    result = await search_opportunities(
        db_session,
        search="solar energy"
    )

    assert len(result) == 1
    assert result[0].id == opportunity2.id
   



    

    