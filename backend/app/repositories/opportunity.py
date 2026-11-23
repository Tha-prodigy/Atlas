from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.opportunity import Opportunity

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

    offset = (page -1) * page_size

    result = await session.execute(statement.order_by(Opportunity.id).offset(offset).limit(page_size))

    return result.scalars().all()

