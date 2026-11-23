import pytest

from app.models import Country, Business, BusinessModel, Opportunity, Category


@pytest.mark.asyncio
async def test_country_business_relationship(db_session):

    country = Country(
        name="Nigeria",
        iso_code="NG"
    )

    business = Business(
        name="Test Business",
        slug="test-business",
        description="A business created for testing",
        website=None,
        headquarters_country=country
    )

    db_session.add(business)
    await db_session.commit()

    assert business.headquarters_country.name == "Nigeria"
    assert len(country.businesses) == 1
    assert country.businesses[0].name == "Test Business"

# test business to businnesModel relationship

@pytest.mark.asyncio
async def test_business_business_model_relationship(db_session):

    country = Country(
        name="Nigeria",
        iso_code="NG"
    )

    business1 = Business(
        name="Business One",
        slug="business-one",
        description="First test business",
        headquarters_country=country
    )

    business2 = Business(
        name="Business Two",
        slug="business-two",
        description="Second test business",
        headquarters_country=country
    )

    model1 = BusinessModel(
        name="Subscription Model",
        slug="subscription-model",
        summary="Customers pay recurring fees",
        description="A recurring payment business model"
    )

    model2 = BusinessModel(
        name="Marketplace Model",
        slug="marketplace-model",
        summary="Connect buyers and sellers",
        description="A platform connecting buyers and sellers"
    )

    # Establish the relationships
    business1.business_models.append(model1)
    business1.business_models.append(model2)
    business2.business_models.append(model1)

    db_session.add_all([business1, business2])

    await db_session.commit()

    # Test the Business -> BusinessModel direction
    assert len(business1.business_models) == 2
    assert model1 in business1.business_models
    assert model2 in business1.business_models

    assert len(business2.business_models) == 1
    assert model1 in business2.business_models

    # Test the BusinessModel -> Business direction
    assert len(model1.businesses) == 2
    assert business1 in model1.businesses
    assert business2 in model1.businesses

    assert len(model2.businesses) == 1
    assert business1 in model2.businesses


# test businessModel to opportunity relationship

@pytest.mark.asyncio
async def test_business_model_opportunity_relationship(db_session):

    country = Country(
        name="Nigeria",
        iso_code="NG"
    )

    model = BusinessModel(
        name="Subscription Model",
        slug="subscription-model",
        summary="Customers pay recurring fees",
        description="A recurring payment business model"
    )

    opportunity1 = Opportunity(
        title="Online Learning Platform",
        slug="online-learning-platform",
        summary="An online learning opportunity",
        problem="Limited access to affordable education",
        proposed_solution="Provide affordable online courses",
        country=country,
        business_model=model
    )

    opportunity2 = Opportunity(
        title="Subscription Grocery Service",
        slug="subscription-grocery-service",
        summary="A recurring grocery delivery service",
        problem="Inconsistent access to grocery deliveries",
        proposed_solution="Deliver groceries through subscriptions",
        country=country,
        business_model=model
    )

    db_session.add_all([opportunity1, opportunity2])

    await db_session.commit()

    # BusinessModel -> Opportunities
    assert len(model.opportunities) == 2
    assert opportunity1 in model.opportunities
    assert opportunity2 in model.opportunities

    # Opportunity -> BusinessModel
    assert opportunity1.business_model is model
    assert opportunity2.business_model is model   

# Opportunity to Category relationship

@pytest.mark.asyncio
async def test_opportunity_category_relationship(db_session):

    country = Country(
        name="Nigeria",
        iso_code="NG"
    )

    business_model = BusinessModel(
        name="Subscription Model",
        slug="subscription-model",
        summary="Customers pay recurring fees",
        description="A recurring payment business model"
    )

    category1 = Category(
        name="Education",
        slug="education",
        description="Education-related opportunities"
    )

    category2 = Category(
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

    # Associate the opportunity with both categories
    opportunity.categories.extend([category1, category2])

    db_session.add(opportunity)

    await db_session.commit()

    # Opportunity -> Categories
    assert len(opportunity.categories) == 2
    assert category1 in opportunity.categories
    assert category2 in opportunity.categories

    # Categories -> Opportunities
    assert opportunity in category1.opportunities
    assert opportunity in category2.opportunities


# Category to sub categories

@pytest.mark.asyncio
async def test_category_parent_child_relationship(db_session):

    parent = Category(
        name="Technology",
        slug="technology",
        description="Technology-related opportunities"
    )

    child1 = Category(
        name="Software",
        slug="software",
        description="Software-related opportunities",
        parent=parent
    )

    child2 = Category(
        name="Hardware",
        slug="hardware",
        description="Hardware-related opportunities",
        parent=parent
    )

    db_session.add_all([parent, child1, child2])

    await db_session.commit()

    # Parent -> Children
    assert len(parent.children) == 2
    assert child1 in parent.children
    assert child2 in parent.children

    # Child -> Parent
    assert child1.parent is parent
    assert child2.parent is parent


# country to opportunity relationship

@pytest.mark.asyncio
async def test_country_opportunity_relationship(db_session):

    country = Country(
        name="Nigeria",
        iso_code="NG"
    )

    business_model = BusinessModel(
        name="Marketplace Model",
        slug="marketplace-model",
        summary="Connect buyers and sellers",
        description="A platform connecting buyers and sellers"
    )

    opportunity1 = Opportunity(
        title="Agricultural Marketplace",
        slug="agricultural-marketplace",
        summary="A marketplace for agricultural products",
        problem="Farmers struggle to reach buyers",
        proposed_solution="Connect farmers directly with buyers",
        country=country,
        business_model=business_model
    )

    opportunity2 = Opportunity(
        title="Local Artisan Marketplace",
        slug="local-artisan-marketplace",
        summary="A marketplace for local artisans",
        problem="Artisans struggle to find customers",
        proposed_solution="Connect artisans with potential customers",
        country=country,
        business_model=business_model
    )

    db_session.add_all([opportunity1, opportunity2])

    await db_session.commit()

    # Country -> Opportunities
    assert len(country.opportunities) == 2
    assert opportunity1 in country.opportunities
    assert opportunity2 in country.opportunities

    # Opportunity -> Country
    assert opportunity1.country is country
    assert opportunity2.country is country