from sqlalchemy import select
from app.models.opportunity import Opportunity
from sqlalchemy.ext.asyncio import AsyncSession


async def get_by_slug(slug:str, db : AsyncSession)-> Opportunity| None:
    result = await db.execute(select(Opportunity).where(Opportunity.slug == slug))

    return result.scalar_one_or_none()