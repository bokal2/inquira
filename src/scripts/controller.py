from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from enum import StrEnum

from src.dependencies import get_db
from src.scripts.seed import create_sample_data

router = APIRouter(prefix="/dev", tags=["Development"])


@router.post("/seed", summary="Seed sample data")
async def seed_sample_data(db: AsyncSession = Depends(get_db)):
    try:
        await create_sample_data(db)
        return {"message": "Database seeded!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class ProductCategory(StrEnum):
    saas = "SaaS"
    subscription = "Subscription"
    hardware = "Hardware"


class ProductIn(BaseModel):
    name: str
    category: ProductCategory
    price: float
