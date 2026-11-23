import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from sqlalchemy import insert
from app.models.associations import business_business_models, opportunity_categories
from app.models import Category, Business, Country, BusinessModel, Opportunity




@pytest.mark.asyncio
async def test_country_name_must_be_unique(db_session):

    country1 = Country(
        name="Nigeria",
        iso_code="NG"
    )

    country2 = Country(
        name="Nigeria",
        iso_code="NI"
    )

    db_session.add_all([country1, country2])

    with pytest.raises(IntegrityError):
        await db_session.commit()

@pytest.mark.asyncio
async def test_country_iso_code_must_be_unique(db_session):

    country1 = Country(
        name="Nigeria",
        iso_code="NG"
    )

    country2 = Country(
        name="Niger",
        iso_code="NG"
    )

    db_session.add_all([country1, country2])

    with pytest.raises(IntegrityError):
        await db_session.commit()

@pytest.mark.asyncio
async def test_category_name_must_be_unique(db_session):

    category1 = Category(
        name="Technology",
        slug="technology",
        description="Technology-related opportunities"
    )

    category2 = Category(
        name="Technology",
        slug="digital-technology",
        description="Other technology opportunities"
    )

    db_session.add_all([category1, category2])

    with pytest.raises(IntegrityError):
        await db_session.commit()


@pytest.mark.asyncio
async def test_business_name_must_be_unique(db_session):

    country = Country(
        name="Nigeria",
        iso_code="NG"
    )

    business1 = Business(
        name="Uber",
        slug="uber",
        description="Ride-hailing company",
        headquarters_country=country
    )

    business2 = Business(
        name="Uber",
        slug="uber-nigeria",
        description="Another business with the same name",
        headquarters_country=country
    )

    db_session.add_all([business1, business2])

    with pytest.raises(IntegrityError):
        await db_session.commit()

@pytest.mark.asyncio
async def test_business_model_name_must_be_unique(db_session):

    model1 = BusinessModel(
        name="Subscription Model",
        slug="subscription-model",
        summary="Recurring customer payments",
        description="Customers pay regularly for a service"
    )

    model2 = BusinessModel(
        name="Subscription Model",
        slug="recurring-model",
        summary="Another recurring payment model",
        description="A different description"
    )

    db_session.add_all([model1, model2])

    with pytest.raises(IntegrityError):
        await db_session.commit()

@pytest.mark.asyncio
async def test_opportunity_slug_must_be_unique(db_session):

    country = Country(
        name="Nigeria",
        iso_code="NG"
    )

    business_model = BusinessModel(
        name="Subscription Model",
        slug="subscription-model",
        summary="Recurring customer payments",
        description="Customers pay regularly for a service"
    )

    opportunity1 = Opportunity(
        title="Online Learning Platform",
        slug="online-learning-platform",
        summary="An online education platform",
        problem="Limited access to affordable education",
        proposed_solution="Provide affordable online courses",
        country=country,
        business_model=business_model
    )

    opportunity2 = Opportunity(
        title="Digital Education Service",
        slug="online-learning-platform",
        summary="Another online education opportunity",
        problem="Limited access to educational resources",
        proposed_solution="Provide digital learning resources",
        country=country,
        business_model=business_model
    )

    db_session.add_all([opportunity1, opportunity2])

    with pytest.raises(IntegrityError):
        await db_session.commit()


@pytest.mark.asyncio
async def test_business_slug_must_be_unique(db_session):

    country = Country(
        name="Nigeria",
        iso_code="NG"
    )

    business1 = Business(
        name="Uber",
        slug="uber",
        description="Ride-hailing company",
        headquarters_country=country
    )

    business2 = Business(
        name="Bolt",
        slug="uber",
        description="Another ride-hailing company",
        headquarters_country=country
    )

    db_session.add_all([business1, business2])

    with pytest.raises(IntegrityError):
        await db_session.commit()


@pytest.mark.asyncio
async def test_business_model_slug_must_be_unique(db_session):

    model1 = BusinessModel(
        name="Subscription Model",
        slug="subscription-model",
        summary="Recurring customer payments",
        description="Customers pay recurring fees"
    )

    model2 = BusinessModel(
        name="Recurring Payment Model",
        slug="subscription-model",
        summary="Another recurring payment model",
        description="A different recurring payment structure"
    )

    db_session.add_all([model1, model2])

    with pytest.raises(IntegrityError):
        await db_session.commit()


# ======== FOREIGN KEY CONSTRAINT ===========

@pytest.mark.asyncio
async def test_opportunity_requires_existing_country(db_session):

    business_model = BusinessModel(
        name="Marketplace Model",
        slug="marketplace-model",
        summary="Connect buyers and sellers",
        description="A platform connecting buyers and sellers"
    )

    opportunity = Opportunity(
        title="Agricultural Marketplace",
        slug="agricultural-marketplace",
        summary="A marketplace for agricultural products",
        problem="Farmers struggle to reach buyers",
        proposed_solution="Connect farmers directly with buyers",
        country_id=999999,
        business_model=business_model
    )

    db_session.add_all([business_model, opportunity])

    # SQLite often disables foreign key enforcement by default.
    # PostgreSQL enforces it, but let's explicitly test the constraint.
    with pytest.raises(IntegrityError):
        await db_session.commit()


@pytest.mark.asyncio
async def test_opportunity_requires_existing_business_model(db_session):

    country = Country(
        name="Nigeria",
        iso_code="NG"
    )

    opportunity = Opportunity(
        title="Agricultural Marketplace",
        slug="agricultural-marketplace",
        summary="A marketplace for agricultural products",
        problem="Farmers struggle to reach buyers",
        proposed_solution="Connect farmers directly with buyers",
        country=country,
        business_model_id=999999
    )

    db_session.add(opportunity)

    with pytest.raises(IntegrityError):
        await db_session.commit()


# ============= ASSOCIATION CONSTRAINT ==================

@pytest.mark.asyncio
async def test_duplicate_business_model_association_is_rejected(db_session):

    country = Country(
        name="Nigeria",
        iso_code="NG"
    )

    business = Business(
        name="Test Business",
        slug="test-business",
        description="A business created for testing",
        headquarters_country=country
    )

    model = BusinessModel(
        name="Subscription Model",
        slug="subscription-model",
        summary="Recurring customer payments",
        description="Customers pay recurring fees"
    )

    db_session.add_all([business, model])
    await db_session.flush()

    association = {
        "business_id": business.id,
        "business_model_id": model.id
    }

    await db_session.execute(
        insert(business_business_models).values(**association)
    )

    with pytest.raises(IntegrityError):
        await db_session.execute(
            insert(business_business_models).values(**association)
        )

        await db_session.commit()


@pytest.mark.asyncio
async def test_duplicate_opportunity_category_association_is_rejected(db_session):

    country = Country(
        name="Nigeria",
        iso_code="NG"
    )

    business_model = BusinessModel(
        name="Subscription Model",
        slug="subscription-model",
        summary="Recurring customer payments",
        description="Customers pay recurring fees"
    )

    category = Category(
        name="Technology",
        slug="technology",
        description="Technology-related opportunities"
    )

    opportunity = Opportunity(
        title="Online Learning Platform",
        slug="online-learning-platform",
        summary="An online learning opportunity",
        problem="Limited access to affordable education",
        proposed_solution="Provide affordable online courses",
        country=country,
        business_model=business_model
    )

    db_session.add_all([opportunity, category])
    await db_session.flush()

    association = {
        "opportunity_id": opportunity.id,
        "category_id": category.id
    }

    await db_session.execute(
        insert(opportunity_categories).values(**association)
    )

    with pytest.raises(IntegrityError):
        await db_session.execute(
            insert(opportunity_categories).values(**association)
        )

        await db_session.commit()