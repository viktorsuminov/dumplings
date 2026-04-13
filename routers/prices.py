from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
import crud
import schemas

router = APIRouter(prefix="/prices", tags=["Цены"])


@router.get("/", response_model=list[schemas.PriceResponse])
async def get_prices(
    shop_id: int | None = None,
    dumpling_id: int | None = None,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Получить список цен (с фильтрацией)"""
    if shop_id:
        prices = await crud.get_prices_by_shop(db, shop_id)
    elif dumpling_id:
        prices = await crud.get_prices_by_dumpling(db, dumpling_id)
    else:
        prices = []
    return prices[:limit]


@router.get("/{price_id}", response_model=schemas.PriceResponse)
async def get_price(price_id: int, db: AsyncSession = Depends(get_db)):
    """Получить цену по ID"""
    price = await crud.get_price(db, price_id)
    if not price:
        raise HTTPException(status_code=404, detail="Цена не найдена")
    return price


@router.post("/", response_model=schemas.PriceResponse, status_code=201)
async def create_price(price: schemas.PriceCreate, db: AsyncSession = Depends(get_db)):
    """Добавить цену (автоматически вычисляет цену за кг)"""
    return await crud.create_price(db, price)


@router.put("/{price_id}", response_model=schemas.PriceResponse)
async def update_price(
    price_id: int,
    price_update: schemas.PriceUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Обновить цену"""
    price = await crud.update_price(db, price_id, price_update)
    if not price:
        raise HTTPException(status_code=404, detail="Цена не найдена")
    return price


@router.delete("/{price_id}", status_code=204)
async def delete_price(price_id: int, db: AsyncSession = Depends(get_db)):
    """Удалить цену"""
    deleted = await crud.delete_price(db, price_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Цена не найдена")
    return None