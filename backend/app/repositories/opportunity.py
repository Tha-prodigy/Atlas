from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.opportunity import Opportunity
from app.models.category import Category

# retrieve data by slug
async def get_by_slug(
    db: AsyncSession,
    slug: str
) -> Opportunity | None:

    result = await db.execute(
        select(Opportunity).where(Opportunity.slug == slug)
    )

    return result.scalar_one_or_none()


# retrieve data by id
async def get_by_id(
    session: AsyncSession,
    opportunity_id: int
) -> Opportunity | None:

    result = await session.execute(
        select(Opportunity).where(Opportunity.id == opportunity_id)
    )

    return result.scalar_one_or_none()

# retrieve all opportunities

async def get_all(session: AsyncSession, page: int = 1, page_size: int= 20) -> list[Opportunity]:

    offset = (page-1)*page_size


    result = await session.execute(
        select(Opportunity).order_by(Opportunity.id).offset(offset).limit(page_size)
    )

    return result.scalars().all()


# retrieve data based on search and filter entry
async def search_opportunities(
        session : AsyncSession,
        search : str|None= None,
        country_id : int| None = None,
        business_model_id : int| None = None,
        category_id : int|None = None,
        page : int = 1,
        page_size : int = 20

)-> list[Opportunity]:
    statement = select(Opportunity)
    if search:
        statement = statement.where(
            or_(
                Opportunity.title.ilike(f'%{search}%'),
                Opportunity.summary.ilike(f"%{search}%")
            )
        )

    if country_id is not None:
        statement = statement.where(
            Opportunity.country_id == country_id
        )

    if business_model_id is not None:
        statement = statement.where(
            Opportunity.business_model_id == business_model_id
        )

    # .any() is used in this case because of the many to many relationship between opportunity and category
    # so the code below searches all the categories in an opportunity and returns only the opportunity which contains the category.id matching with the passed category_id
    if category_id is not None:
        statement = statement.where(
            Opportunity.categories.any(Category.id == category_id)
        )

    offset = (page -1) * page_size

    result = await session.execute(statement.order_by(Opportunity.id).offset(offset).limit(page_size))

    return result.scalars().all()

