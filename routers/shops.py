from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
import crud
import schemas

router = APIRouter(prefix="/shops", tags=["Магазины"])


@router.get("/", response_model=list[schemas.ShopResponse])
async def get_shops(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
    db: AsyncSession = Depends(get_db)
):
    """Получить список магазинов"""
    shops = await crud.get_shops(db, skip=skip, limit=limit, active_only=active_only)
    return shops


@router.get("/{shop_id}", response_model=schemas.ShopResponse)
async def get_shop(shop_id: int, db: AsyncSession = Depends(get_db)):
    """Получить магазин по ID"""
    shop = await crud.get_shop(db, shop_id)
    if not shop:
        raise HTTPException(status_code=404, detail="Магазин не найден")
    return shop


@router.post("/", response_model=schemas.ShopResponse, status_code=201)
async def create_shop(shop: schemas.ShopCreate, db: AsyncSession = Depends(get_db)):
    """Создать новый магазин"""
    return await crud.create_shop(db, shop)


@router.patch("/{shop_id}", response_model=schemas.ShopResponse)
async def update_shop(
    shop_id: int,
    shop_update: schemas.ShopUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Обновить магазин"""
    shop = await crud.update_shop(db, shop_id, shop_update)
    if not shop:
        raise HTTPException(status_code=404, detail="Магазин не найден")
    return shop


@router.delete("/{shop_id}", status_code=204)
async def delete_shop(shop_id: int, db: AsyncSession = Depends(get_db)):
    """Удалить магазин"""
    deleted = await crud.delete_shop(db, shop_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Магазин не найден")
    return None