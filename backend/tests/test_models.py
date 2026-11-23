from app.database.base import Base
from sqlalchemy import inspect
from sqlalchemy.orm import configure_mappers
from app.models import Country, Category, Business, BusinessModel, Opportunity


def test_all_models_are_registered():
    expected_tables = {
        "countries",
        "categories",
        "businesses",
        "business_models",
        "opportunities",
        "business_business_models",
        "opportunity_categories",
    }

    assert expected_tables.issubset(Base.metadata.tables.keys())


def test_relationships_configure_successfully():
    configure_mappers()


def test_expected_relationships_exist():
    expected_relationships = {
        Country: {"businesses", "opportunities"},
        Business: {"headquarters_country", "business_models"},
        BusinessModel: {"businesses", "opportunities"},
        Opportunity: {"country", "business_model", "categories"},
        Category: {"parent", "children", "opportunities"},
    }

    for model, expected in expected_relationships.items():
        actual = set(inspect(model).relationships.keys())

        assert expected.issubset(actual)