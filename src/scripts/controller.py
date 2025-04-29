from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from enum import StrEnum

from src.dependencies import get_db
from src.scripts.seed import create_sample_data, bulk_update_products

router = APIRouter(prefix="/dev", tags=["Development"])


@router.post("/seed", summary="Seed sample data")
async def seed_sample_data(db: AsyncSession = Depends(get_db)):
    try:
        await create_sample_data(db)
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


@router.post("/product", summary="Add new product")
async def add_new_product(db: AsyncSession = Depends(get_db)):
    await bulk_update_products(db)
    return ""
