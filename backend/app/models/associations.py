from sqlalchemy import Table, Column, ForeignKey
from app.database.base import Base


business_business_models = Table(
    "business_business_models",
    Base.metadata,
    Column('business_id', ForeignKey('businesses.id'), primary_key=True),
    Column('business_model_id', ForeignKey('business_models.id'), primary_key=True)
    
)


opportunity_categories = Table(
    'opportunity_categories',
    Base.metadata,
    Column('opportunity_id', ForeignKey('opportunities.id'), primary_key=True),
    Column('category_id', ForeignKey('categories.id'), primary_key=True)

)