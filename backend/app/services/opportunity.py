from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.opportunity import (get_by_slug, search_opportunities)


async def get_opportunity_by_slug(session : AsyncSession, slug: str):
    result = await get_by_slug(session, slug)
    
    return result

async def get_opportunities_by_search_and_filters(session: AsyncSession, search: str, country_id: int, business_model_id: int, category_id: int, page: int, page_size: int):

    opportunities = await search_opportunities(session, search, country_id, business_model_id, category_id, page, page_size)
    return opportunities


