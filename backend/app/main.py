from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.database.connection import get_db


app = FastAPI(title="Africa Opportunity Atlas")


@app.get("/health")
async def health_check():

    return {"status": "Application is running"}


@app.get("/health/db")
async def database_check(db: AsyncSession = Depends(get_db)):

    result = await db.execute(text("SELECT 1"))

    return {
        "database": "Connected",
        "result": result.scalar_one()
    }