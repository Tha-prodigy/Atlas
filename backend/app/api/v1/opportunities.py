from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_db
from app.schemas.opportunity import OpportunityResponse
from app.services.opportunity import (
    get_opportunity_by_slug,
    get_opportunities_by_search_and_filters
)


router = APIRouter(prefix="/opportunities", tags=["Opportunities"])


@router.get("/{slug}", response_model=OpportunityResponse)
async def get_opportunity(
    slug: str,
    session: AsyncSession = Depends(get_db)
):
    opportunity = await get_opportunity_by_slug(session, slug)

    if opportunity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opportunity not found"
        )

    return opportunity


@router.get("/", response_model=list[OpportunityResponse])
async def get_opportunities(
    search: str | None = None,
    country_id: int | None = Query(default=None, ge=1),
    business_model_id: int | None = Query(default=None, ge=1),
    category_id: int | None = Query(default=None, ge=1),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    session: AsyncSession = Depends(get_db)
):
    opportunities = await get_opportunities_by_search_and_filters(
        session=session,
        search=search,
        country_id=country_id,
        business_model_id=business_model_id,
        category_id=category_id,
        page=page,
        page_size=page_size
    )

    return opportunities